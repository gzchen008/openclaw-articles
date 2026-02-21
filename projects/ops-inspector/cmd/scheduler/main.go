package main

import (
	"context"
	"flag"
	"log"
	"net/http"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/opsinspector/opsinspector/pkg/config"
	"github.com/opsinspector/opsinspector/pkg/models"
	"github.com/opsinspector/opsinspector/pkg/queue"
	"github.com/opsinspector/opsinspector/pkg/scheduler"
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

	// 创建日志
	logger, err := zap.NewProduction()
	if cfg.Server.Mode == "debug" {
		logger, err = zap.NewDevelopment()
	}
	if err != nil {
		log.Fatalf("Failed to create logger: %v", err)
	}
	defer logger.Sync()

	logger.Info("Starting OpsInspector Scheduler",
		zap.String("version", "1.0.0"),
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

	// 创建调度器
	sch := scheduler.NewScheduler(q, db, logger)

	// 启动调度器
	ctx := context.Background()
	if err := sch.Start(ctx); err != nil {
		logger.Fatal("Failed to start scheduler", zap.Error(err))
	}

	// 创建 Gin 路由（用于健康检查和 API）
	r := gin.Default()

	// 健康检查
	r.GET("/health", func(c *gin.Context) {
		c.JSON(http.StatusOK, gin.H{
			"status": "ok",
			"time":   time.Now().Format(time.RFC3339),
		})
	})

	// 手动触发巡检
	r.POST("/api/v1/inspections/:id/trigger", func(c *gin.Context) {
		id := c.Param("id")
		if err := sch.TriggerInspection(c.Request.Context(), id, "manual"); err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
			return
		}
		c.JSON(http.StatusOK, gin.H{"message": "Inspection triggered"})
	})

	// 优雅关闭
	quit := make(chan os.Signal, 1)
	signal.Notify(quit, syscall.SIGINT, syscall.SIGTERM)

	go func() {
		port := cfg.Server.Port
		logger.Info("HTTP server starting", zap.Int("port", port))
		if err := r.Run(":" + string(rune(port))); err != nil {
			logger.Error("HTTP server error", zap.Error(err))
		}
	}()

	<-quit
	logger.Info("Shutting down scheduler...")

	// 停止调度器
	sch.Stop()

	logger.Info("Scheduler stopped")
}
