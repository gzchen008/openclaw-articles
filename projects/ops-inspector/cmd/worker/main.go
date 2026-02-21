package main

import (
	"context"
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/opsinspector/opsinspector/pkg/config"
	"github.com/opsinspector/opsinspector/pkg/inspector"
	"github.com/opsinspector/opsinspector/pkg/models"
	"github.com/opsinspector/opsinspector/pkg/observability"
	"github.com/opsinspector/opsinspector/pkg/queue"
	"github.com/opsinspector/opsinspector/pkg/store"
	"github.com/opsinspector/opsinspector/plugins/inspectors"
	"go.uber.org/zap"
)

func main() {
	var configPath string
	flag.StringVar(&configPath, "config", "configs/config.yaml", "Path to config file")
	flag.Parse()

	// 加载配置
	cfg, err := config.Load(configPath)
	if err != nil {
		log.Fatalf("Failed to load config: %v", err)
	}

	// 创建日志
	logger, err := zap.NewProduction()
	if cfg.Server.Mode == "debug" {
		logger, err = zap.NewDevelopment()
	}
	if err != nil {
		log.Fatalf("Failed to create logger: %v", err)
	}
	defer logger.Sync()

	logger.Info("Starting OpsInspector Worker",
		zap.String("version", "1.0.0"),
		zap.Int("concurrency", cfg.Worker.Concurrency),
	)

	// 连接数据库
	db, err := store.NewStore(cfg.Database.DSN, cfg.Server.Mode == "debug")
	if err != nil {
		logger.Fatal("Failed to connect database", zap.Error(err))
	}
	defer db.Close()

	// 测试数据库连接
	if err := db.Ping(); err != nil {
		logger.Fatal("Failed to ping database", zap.Error(err))
	}
	logger.Info("Database connected")

	// 创建队列（内存队列）
	q := queue.NewMemoryQueue(1000)

	// 创建巡检器注册表
	registry := inspector.NewRegistry()

	// 注册巡检器
	registry.Register(inspectors.NewHTTPInspector())
	registry.Register(inspectors.NewK8sPodInspector())
	registry.Register(inspectors.NewDiskInspector())
	registry.Register(inspectors.NewMemoryInspector())

	logger.Info("Registered inspectors",
		zap.Int("count", len(registry.List())),
	)

	// 设置 Worker 池大小指标
	observability.SetWorkerPoolSize(float64(cfg.Worker.Concurrency))

	// 创建 Worker
	worker := NewWorker(q, db, registry, logger, cfg.Worker.Concurrency)

	// 启动 Worker
	ctx, cancel := context.WithCancel(context.Background())
	go worker.Start(ctx)

	// 启动指标收集（定期更新数据库连接数）
	go func() {
		ticker := time.NewTicker(30 * time.Second)
		defer ticker.Stop()
		for {
			select {
			case <-ticker.C:
				observability.UpdateDBMetrics(db.DB())
			case <-ctx.Done():
				return
			}
		}
	}()

	// 优雅关闭
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

	<-quit
	logger.Info("Shutting down worker...")

	cancel()
	time.Sleep(time.Second)

	logger.Info("Worker stopped")
}

// Worker 任务执行器
type Worker struct {
	queue       queue.Queue
	store       store.Store
	registry    *inspector.Registry
	logger      *zap.Logger
	concurrency int
	activeTasks int64
	workerID    string
}

// NewWorker 创建 Worker
func NewWorker(q queue.Queue, s store.Store, r *inspector.Registry, l *zap.Logger, c int) *Worker {
	return &Worker{
		queue:       q,
		store:       s,
		registry:    r,
		logger:      l,
		concurrency: c,
		workerID:    "worker-1", // 实际应该生成唯一ID
	}
}

// Start 启动 Worker
func (w *Worker) Start(ctx context.Context) {
	w.logger.Info("Worker started")

	for i := 0; i < w.concurrency; i++ {
		go w.process(ctx, i)
	}

	<-ctx.Done()
}

// process 处理任务
func (w *Worker) process(ctx context.Context, workerNum int) {
	workerID := fmt.Sprintf("%s-%d", w.workerID, workerNum)

	for {
		select {
		case <-ctx.Done():
			return
		default:
		}

		task, err := w.queue.Pop(ctx, time.Second*5)
		if err != nil {
			w.logger.Error("Failed to pop task", zap.Error(err))
			continue
		}
		if task == nil {
			continue
		}

		// 更新活跃任务数
		w.activeTasks++
		observability.SetWorkerActiveTasks(float64(w.activeTasks))

		w.handleTask(ctx, task, workerID)

		// 更新活跃任务数
		w.activeTasks--
		observability.SetWorkerActiveTasks(float64(w.activeTasks))

		// 更新队列大小指标
		size, _ := w.queue.Size(ctx)
		observability.SetQueueSize(float64(size))
	}
}

// handleTask 处理单个任务
func (w *Worker) handleTask(ctx context.Context, task *queue.InspectionTask, workerID string) {
	startTime := time.Now()
	logger := w.logger.With(
		zap.String("task_id", task.ID.String()),
		zap.String("inspection_id", task.InspectionID.String()),
		zap.String("worker_id", workerID),
	)

	logger.Info("Processing task")

	// 获取巡检配置
	inspection, err := w.store.GetInspection(ctx, task.InspectionID.String())
	if err != nil {
		logger.Error("Failed to get inspection", zap.Error(err))
		w.queue.Fail(ctx, task.ID, err.Error())
		observability.RecordWorkerTask(workerID, "error")
		return
	}
	if inspection == nil {
		logger.Error("Inspection not found")
		w.queue.Fail(ctx, task.ID, "inspection not found")
		observability.RecordWorkerTask(workerID, "error")
		return
	}

	// 创建执行记录
	run := &models.InspectionRun{
		ID:           task.ID,
		InspectionID: task.InspectionID,
		Status:       models.RunStatusRunning,
		TriggeredBy:  task.TriggeredBy,
		StartedAt:    time.Now(),
	}
	if err := w.store.CreateInspectionRun(ctx, run); err != nil {
		logger.Error("Failed to create run record", zap.Error(err))
	}

	// 获取巡检器
	insp, ok := w.registry.Get(inspection.Type)
	if !ok {
		logger.Error("Inspector not found", zap.String("type", string(inspection.Type)))
		run.Status = models.RunStatusFailed
		run.ErrorMessage = "inspector not found: " + string(inspection.Type)
		run.CompletedAt = &[]time.Time{time.Now()}[0]
		run.Duration = int(time.Since(run.StartedAt).Milliseconds())
		w.store.UpdateInspectionRun(ctx, run)
		w.queue.Fail(ctx, task.ID, run.ErrorMessage)
		observability.RecordWorkerTask(workerID, "failed")
		
		// 记录指标
		duration := time.Since(startTime).Seconds()
		observability.RecordInspectionRun(string(inspection.Type), "failed", duration)
		return
	}

	// 执行巡检
	taskCtx, cancel := context.WithTimeout(ctx, time.Duration(inspection.Timeout)*time.Second)
	defer cancel()

	result, err := insp.Execute(taskCtx, inspection.Config)
	if err != nil {
		logger.Error("Inspection execution error", zap.Error(err))
		run.Status = models.RunStatusFailed
		run.ErrorMessage = err.Error()
	} else {
		// 根据结果设置状态
		switch result.Status {
		case inspector.StatusSuccess:
			run.Status = models.RunStatusSuccess
		case inspector.StatusWarning:
			run.Status = models.RunStatusWarning
		case inspector.StatusFailed:
			run.Status = models.RunStatusFailed
		case inspector.StatusError:
			run.Status = models.RunStatusFailed
		}
		run.Result = &models.InspectionResult{
			Status:   models.ResultStatus(result.Status),
			Level:    models.ResultLevel(result.Level),
			Summary:  result.Summary,
			Details:  convertDetails(result.Details),
			Metrics:  result.Metrics,
		}
	}

	completedAt := time.Now()
	run.CompletedAt = &completedAt
	run.Duration = int(time.Since(run.StartedAt).Milliseconds())

	// 更新执行记录
	if err := w.store.UpdateInspectionRun(ctx, run); err != nil {
		logger.Error("Failed to update run record", zap.Error(err))
	}

	// 完成任务
	w.queue.Complete(ctx, task.ID)

	duration := time.Since(startTime).Seconds()
	logger.Info("Task completed",
		zap.String("status", string(run.Status)),
		zap.Int("duration_ms", run.Duration),
	)

	// 记录指标
	observability.RecordInspectionRun(string(inspection.Type), string(run.Status), duration)
	observability.RecordWorkerTask(workerID, string(run.Status))
}

// convertDetails 转换详情
func convertDetails(details []inspector.Detail) []models.InspectionDetail {
	result := make([]models.InspectionDetail, len(details))
	for i, d := range details {
		result[i] = models.InspectionDetail{
			Name:            d.Name,
			Status:          models.ResultStatus(d.Status),
			Message:         d.Message,
			Value:           d.Value,
			Threshold:       d.Threshold,
			SuggestedAction: d.SuggestedAction,
		}
	}
	return result
}
