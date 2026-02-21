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
	"github.com/google/uuid"
	"github.com/opsinspector/opsinspector/pkg/config"
	"github.com/opsinspector/opsinspector/pkg/models"
	"github.com/opsinspector/opsinspector/pkg/observability"
	"github.com/opsinspector/opsinspector/pkg/scheduler"
	"github.com/opsinspector/opsinspector/pkg/sop"
	"github.com/opsinspector/opsinspector/pkg/store"
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

	// 设置 Gin 模式
	if cfg.Server.Mode == "release" {
		gin.SetMode(gin.ReleaseMode)
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

	logger.Info("Starting OpsInspector API",
		zap.String("version", "1.0.0"),
		zap.Int("port", cfg.Server.Port),
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

	// 创建调度器（用于手动触发）
	sch := scheduler.NewScheduler(nil, db, logger)
	if err := sch.Start(context.Background()); err != nil {
		logger.Fatal("Failed to start scheduler", zap.Error(err))
	}

	// 创建 SOP 引擎
	sopEngine := sop.NewEngine(db, logger)
	sopEngine.InitDefaultActions()

	// 创建 Gin 路由
	r := gin.Default()

	// 添加 Prometheus 中间件
	r.Use(observability.PrometheusMiddleware())

	// 健康检查
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status":    "ok",
			"version":   "1.0.0",
			"timestamp": time.Now().Format(time.RFC3339),
		})
	})

	r.GET("/ready", func(c *gin.Context) {
		if err := db.Ping(); err != nil {
			c.JSON(http.StatusServiceUnavailable, gin.H{"status": "unavailable"})
			return
		}
		c.JSON(http.StatusOK, gin.H{"status": "ready"})
	})

	// Prometheus 指标端点
	r.GET("/metrics", observability.MetricsHandler())

	// API v1 路由组
	v1 := r.Group("/api/v1")
	{
		// 巡检任务管理
		v1.GET("/inspections", listInspections(db))
		v1.POST("/inspections", createInspection(db, sch))
		v1.GET("/inspections/:id", getInspection(db))
		v1.PUT("/inspections/:id", updateInspection(db, sch))
		v1.DELETE("/inspections/:id", deleteInspection(db, sch))
		v1.POST("/inspections/:id/trigger", triggerInspection(db, sch))

		// 执行记录
		v1.GET("/inspections/:id/runs", listInspectionRuns(db))
		v1.GET("/runs/:id", getInspectionRun(db))

		// 通知渠道
		v1.GET("/channels", listChannels(db))
		v1.POST("/channels", createChannel(db))

		// SOP
		v1.GET("/sops", listSOPs(db))
		v1.POST("/sops", createSOP(db))
		v1.GET("/sops/:id", getSOP(db))
		v1.POST("/sops/:id/execute", executeSOP(db, sopEngine))
	}

	// 优雅关闭
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

	srv := &http.Server{
		Addr:    ":" + string(rune(cfg.Server.Port)),
		Handler: r,
	}

	go func() {
		if err := srv.ListenAndServe(); err != nil && err != http.ErrServerClosed {
			logger.Fatal("Failed to start server", zap.Error(err))
		}
	}()

	logger.Info("API server started", zap.Int("port", cfg.Server.Port))

	<-quit
	logger.Info("Shutting down API server...")

	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	if err := srv.Shutdown(ctx); err != nil {
		logger.Error("Server forced to shutdown", zap.Error(err))
	}

	sch.Stop()

	logger.Info("API server stopped")
}

// listInspections 列出巡检任务
func listInspections(db store.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		inspections, err := db.ListInspections(c.Request.Context(), store.ListInspectionsFilter{})
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, inspections)
	}
}

// createInspection 创建巡检任务
func createInspection(db store.Store, sch *scheduler.Scheduler) gin.HandlerFunc {
	return func(c *gin.Context) {
		var inspection models.Inspection
		if err := c.ShouldBindJSON(&inspection); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		// 验证必填字段
		if inspection.Name == "" || inspection.Type == "" {
			c.JSON(http.StatusBadRequest, gin.H{"error": "name and type are required"})
			return
		}

		inspection.ID = uuid.New()
		inspection.Enabled = true

		if err := db.CreateInspection(c.Request.Context(), &inspection); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		// 添加到调度器
		if err := sch.AddInspection(&inspection); err != nil {
			// 记录错误但不返回失败
			log.Printf("Failed to add inspection to scheduler: %v", err)
		}

		c.JSON(http.StatusCreated, inspection)
	}
}

// getInspection 获取巡检任务
func getInspection(db store.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		inspection, err := db.GetInspection(c.Request.Context(), id)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		if inspection == nil {
			c.JSON(http.StatusNotFound, gin.H{"error": "inspection not found"})
			return
		}
		c.JSON(http.StatusOK, inspection)
	}
}

// updateInspection 更新巡检任务
func updateInspection(db store.Store, sch *scheduler.Scheduler) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		var inspection models.Inspection
		if err := c.ShouldBindJSON(&inspection); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		inspection.ID = uuid.MustParse(id)
		if err := db.UpdateInspection(c.Request.Context(), &inspection); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		// 重新添加到调度器
		sch.RemoveInspection(id)
		if err := sch.AddInspection(&inspection); err != nil {
			log.Printf("Failed to update inspection in scheduler: %v", err)
		}

		c.JSON(http.StatusOK, inspection)
	}
}

// deleteInspection 删除巡检任务
func deleteInspection(db store.Store, sch *scheduler.Scheduler) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		
		// 从调度器移除
		sch.RemoveInspection(id)
		
		if err := db.DeleteInspection(c.Request.Context(), id); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"message": "deleted"})
	}
}

// triggerInspection 手动触发巡检
func triggerInspection(db store.Store, sch *scheduler.Scheduler) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		if err := sch.TriggerInspection(c.Request.Context(), id, "api"); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"message": "Inspection triggered"})
	}
}

// listInspectionRuns 列出执行记录
func listInspectionRuns(db store.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		runs, err := db.ListInspectionRuns(c.Request.Context(), id, 50)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, runs)
	}
}

// getInspectionRun 获取执行记录
func getInspectionRun(db store.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		run, err := db.GetInspectionRun(c.Request.Context(), id)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		if run == nil {
			c.JSON(http.StatusNotFound, gin.H{"error": "run not found"})
			return
		}
		c.JSON(http.StatusOK, run)
	}
}

// listChannels 列出通知渠道
func listChannels(db store.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		channels, err := db.ListNotificationChannels(c.Request.Context())
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, channels)
	}
}

// createChannel 创建通知渠道
func createChannel(db store.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		var channel models.NotificationChannel
		if err := c.ShouldBindJSON(&channel); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		channel.ID = uuid.New()
		if err := db.CreateNotificationChannel(c.Request.Context(), &channel); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusCreated, channel)
	}
}

// listSOPs 列出SOP
func listSOPs(db store.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		sops, err := db.ListSOPs(c.Request.Context())
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, sops)
	}
}

// getSOP 获取SOP
func getSOP(db store.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		sop, err := db.GetSOP(c.Request.Context(), id)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		if sop == nil {
			c.JSON(http.StatusNotFound, gin.H{"error": "sop not found"})
			return
		}
		c.JSON(http.StatusOK, sop)
	}
}

// createSOP 创建SOP
func createSOP(db store.Store) gin.HandlerFunc {
	return func(c *gin.Context) {
		var sop models.SOP
		if err := c.ShouldBindJSON(&sop); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}

		sop.ID = uuid.New()
		if err := db.CreateSOP(c.Request.Context(), &sop); err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusCreated, sop)
	}
}

// executeSOP 执行SOP
func executeSOP(db store.Store, engine *sop.Engine) gin.HandlerFunc {
	return func(c *gin.Context) {
		id := c.Param("id")
		
		sop, err := db.GetSOP(c.Request.Context(), id)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}
		if sop == nil {
			c.JSON(http.StatusNotFound, gin.H{"error": "sop not found"})
			return
		}

		// 获取变量
		var vars map[string]interface{}
		if err := c.ShouldBindJSON(&vars); err != nil {
			// 允许空请求体
			vars = make(map[string]interface{})
		}

		// 启动 SOP 执行
		instance, err := engine.StartSOP(c.Request.Context(), sop.ID, uuid.New(), vars)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
			return
		}

		c.JSON(http.StatusAccepted, gin.H{
			"instance_id": instance.ID,
			"sop_id":      sop.ID,
			"status":      instance.Status,
		})
	}
}
