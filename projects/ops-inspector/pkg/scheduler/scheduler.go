package scheduler

import (
	"context"
	"fmt"
	"sync"
	"time"

	"github.com/google/uuid"
	"github.com/opsinspector/opsinspector/pkg/models"
	"github.com/opsinspector/opsinspector/pkg/queue"
	"github.com/opsinspector/opsinspector/pkg/store"
	"github.com/robfig/cron/v3"
	"go.uber.org/zap"
)

// Scheduler 任务调度器
type Scheduler struct {
	cron        *cron.Cron
	queue       queue.Queue
	store       store.Store
	logger      *zap.Logger

	jobs        map[string]cron.EntryID
	jobsMu      sync.RWMutex

	maxConcurrent int
	checkInterval time.Duration
	ctx           context.Context
	cancel        context.CancelFunc
}

// NewScheduler 创建调度器
func NewScheduler(queue queue.Queue, store store.Store, logger *zap.Logger) *Scheduler {
	ctx, cancel := context.WithCancel(context.Background())
	return &Scheduler{
		cron:          cron.New(cron.WithSeconds()),
		queue:         queue,
		store:         store,
		logger:        logger,
		jobs:          make(map[string]cron.EntryID),
		maxConcurrent: 100,
		checkInterval: time.Second * 10,
		ctx:           ctx,
		cancel:        cancel,
	}
}

// Start 启动调度器
func (s *Scheduler) Start(ctx context.Context) error {
	s.logger.Info("Starting scheduler")

	// 加载已有的 Cron 任务
	if err := s.loadCronJobs(ctx); err != nil {
		return fmt.Errorf("failed to load cron jobs: %w", err)
	}

	s.cron.Start()

	// 启动配置变更监听
	go s.watchConfigChanges()

	s.logger.Info("Scheduler started successfully")
	return nil
}

// Stop 停止调度器
func (s *Scheduler) Stop() {
	s.logger.Info("Stopping scheduler")
	s.cancel()
	ctx := s.cron.Stop()
	<-ctx.Done()
	s.logger.Info("Scheduler stopped")
}

// loadCronJobs 加载 Cron 任务
func (s *Scheduler) loadCronJobs(ctx context.Context) error {
	typeStr := models.InspectionTypeCron
	enabled := true
	inspections, err := s.store.ListInspections(ctx, store.ListInspectionsFilter{
		Type:    &typeStr,
		Enabled: &enabled,
	})
	if err != nil {
		return err
	}

	for _, inspection := range inspections {
		if err := s.scheduleInspection(inspection); err != nil {
			s.logger.Error("Failed to schedule inspection",
				zap.String("id", inspection.ID.String()),
				zap.String("name", inspection.Name),
				zap.Error(err))
		}
	}

	return nil
}

// scheduleInspection 调度单个巡检任务
func (s *Scheduler) scheduleInspection(inspection *models.Inspection) error {
	s.jobsMu.Lock()
	defer s.jobsMu.Unlock()

	// 如果已存在，先移除
	if entryID, exists := s.jobs[inspection.ID.String()]; exists {
		s.cron.Remove(entryID)
		delete(s.jobs, inspection.ID.String())
	}

	if !inspection.Enabled {
		return nil
	}

	// 解析 Cron 表达式
	_, err := cron.ParseStandard(inspection.Schedule)
	if err != nil {
		return fmt.Errorf("invalid cron expression %q: %w", inspection.Schedule, err)
	}

	// 创建任务函数
	jobFunc := func() {
		s.executeInspection(inspection)
	}

	// 添加到 Cron
	entryID, err := s.cron.AddFunc(inspection.Schedule, jobFunc)
	if err != nil {
		return fmt.Errorf("failed to add cron job: %w", err)
	}

	s.jobs[inspection.ID.String()] = entryID
	nextRun := s.cron.Entry(entryID).Next

	s.logger.Info("Inspection scheduled",
		zap.String("id", inspection.ID.String()),
		zap.String("name", inspection.Name),
		zap.String("schedule", inspection.Schedule),
		zap.Time("next_run", nextRun))

	return nil
}

// unscheduleInspection 取消调度
func (s *Scheduler) unscheduleInspection(inspectionID string) {
	s.jobsMu.Lock()
	defer s.jobsMu.Unlock()

	if entryID, exists := s.jobs[inspectionID]; exists {
		s.cron.Remove(entryID)
		delete(s.jobs, inspectionID)
		s.logger.Info("Inspection unscheduled", zap.String("id", inspectionID))
	}
}

// executeInspection 执行巡检任务
func (s *Scheduler) executeInspection(inspection *models.Inspection) {
	s.logger.Info("Executing scheduled inspection",
		zap.String("id", inspection.ID.String()),
		zap.String("name", inspection.Name))

	ctx := context.Background()

	// 检查抑制窗口
	if s.shouldSuppress(ctx, inspection) {
		s.logger.Info("Inspection suppressed by dedup window",
			zap.String("id", inspection.ID.String()))
		return
	}

	// 创建任务
	task := &models.InspectionTask{
		ID:           uuid.New(),
		InspectionID: inspection.ID,
		Type:         queue.TaskTypeScheduled,
		TriggeredBy:  "scheduler",
		ScheduledAt:  time.Now(),
		MaxAttempts:  inspection.Retries + 1,
		Status:       queue.TaskStatusPending,
	}

	// 推送到队列
	if err := s.queue.Push(ctx, task); err != nil {
		s.logger.Error("Failed to push task to queue",
			zap.String("id", inspection.ID.String()),
			zap.Error(err))
	}
}

// shouldSuppress 检查是否应该抑制执行
func (s *Scheduler) shouldSuppress(ctx context.Context, inspection *models.Inspection) bool {
	if inspection.SuppressWindow <= 0 {
		return false
	}

	lastRun, err := s.store.GetLastInspectionRun(ctx, inspection.ID)
	if err != nil || lastRun == nil {
		return false
	}

	timeSinceLastRun := time.Since(lastRun.StartedAt)
	return timeSinceLastRun < time.Duration(inspection.SuppressWindow)*time.Second
}

// TriggerInspection 手动触发巡检
func (s *Scheduler) TriggerInspection(ctx context.Context, inspectionID string, triggeredBy string) error {
	inspection, err := s.store.GetInspection(ctx, inspectionID)
	if err != nil {
		return err
	}
	if inspection == nil {
		return fmt.Errorf("inspection not found: %s", inspectionID)
	}

	if !inspection.Enabled {
		return fmt.Errorf("inspection is disabled: %s", inspectionID)
	}

	task := &models.InspectionTask{
		ID:           uuid.New(),
		InspectionID: inspection.ID,
		Type:         queue.TaskTypeManual,
		TriggeredBy:  triggeredBy,
		ScheduledAt:  time.Now(),
		MaxAttempts:  inspection.Retries + 1,
		Status:       queue.TaskStatusPending,
	}

	if err := s.queue.Push(ctx, task); err != nil {
		return fmt.Errorf("failed to push task: %w", err)
	}

	return nil
}

// AddInspection 添加新的巡检任务到调度器
func (s *Scheduler) AddInspection(inspection *models.Inspection) error {
	if inspection.Type == models.InspectionTypeCron && inspection.Schedule != "" {
		return s.scheduleInspection(inspection)
	}
	return nil
}

// RemoveInspection 从调度器移除巡检任务
func (s *Scheduler) RemoveInspection(inspectionID string) {
	s.unscheduleInspection(inspectionID)
}

// watchConfigChanges 监听配置变化（简化版）
func (s *Scheduler) watchConfigChanges() {
	ticker := time.NewTicker(s.checkInterval)
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			// 重新加载配置
			if err := s.loadCronJobs(s.ctx); err != nil {
				s.logger.Error("Failed to reload cron jobs", zap.Error(err))
			}
		case <-s.ctx.Done():
			return
		}
	}
}

// GetNextRunTime 获取下次执行时间
func (s *Scheduler) GetNextRunTime(inspectionID string) (time.Time, bool) {
	s.jobsMu.RLock()
	defer s.jobsMu.RUnlock()

	if entryID, exists := s.jobs[inspectionID]; exists {
		entry := s.cron.Entry(entryID)
		return entry.Next, true
	}
	return time.Time{}, false
}
