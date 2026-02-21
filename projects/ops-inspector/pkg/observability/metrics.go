package observability

import (
	"net/http"
	"strconv"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
	"github.com/prometheus/client_golang/prometheus/promhttp"
	"gorm.io/gorm"
)

var (
	// 巡检指标
	InspectionRunsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Namespace: "opsinspector",
			Name:      "inspection_runs_total",
			Help:      "Total number of inspection runs",
		},
		[]string{"inspector", "status"},
	)

	InspectionDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Namespace: "opsinspector",
			Name:      "inspection_duration_seconds",
			Help:      "Inspection execution duration in seconds",
			Buckets:   prometheus.DefBuckets,
		},
		[]string{"inspector"},
	)

	InspectionQueueSize = promauto.NewGauge(
		prometheus.GaugeOpts{
			Namespace: "opsinspector",
			Name:      "inspection_queue_size",
			Help:      "Current size of the inspection queue",
		},
	)

	// SOP 指标
	SOPExecutionsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Namespace: "opsinspector",
			Name:      "sop_executions_total",
			Help:      "Total number of SOP executions",
		},
		[]string{"sop_name", "status"},
	)

	SOPExecutionDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Namespace: "opsinspector",
			Name:      "sop_execution_duration_seconds",
			Help:      "SOP execution duration in seconds",
			Buckets:   prometheus.DefBuckets,
		},
		[]string{"sop_name"},
	)

	// Worker 指标
	WorkerTasksProcessed = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Namespace: "opsinspector",
			Name:      "worker_tasks_processed_total",
			Help:      "Total number of tasks processed by workers",
		},
		[]string{"worker_id", "status"},
	)

	WorkerActiveTasks = promauto.NewGauge(
		prometheus.GaugeOpts{
			Namespace: "opsinspector",
			Name:      "worker_active_tasks",
			Help:      "Number of tasks currently being processed",
		},
	)

	WorkerPoolSize = promauto.NewGauge(
		prometheus.GaugeOpts{
			Namespace: "opsinspector",
			Name:      "worker_pool_size",
			Help:      "Total number of workers in the pool",
		},
	)

	// 通知指标
	NotificationsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Namespace: "opsinspector",
			Name:      "notifications_total",
			Help:      "Total number of notifications sent",
		},
		[]string{"channel", "status"},
	)

	NotificationDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Namespace: "opsinspector",
			Name:      "notification_duration_seconds",
			Help:      "Notification sending duration in seconds",
			Buckets:   prometheus.DefBuckets,
		},
		[]string{"channel"},
	)

	// API 指标
	APIRequestsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Namespace: "opsinspector",
			Name:      "api_requests_total",
			Help:      "Total number of API requests",
		},
		[]string{"method", "path", "status"},
	)

	APIDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Namespace: "opsinspector",
			Name:      "api_request_duration_seconds",
			Help:      "API request duration in seconds",
			Buckets:   prometheus.DefBuckets,
		},
		[]string{"method", "path"},
	)

	// 数据库指标
	DBConnectionsActive = promauto.NewGauge(
		prometheus.GaugeOpts{
			Namespace: "opsinspector",
			Name:      "db_connections_active",
			Help:      "Number of active database connections",
		},
	)

	DBConnectionsIdle = promauto.NewGauge(
		prometheus.GaugeOpts{
			Namespace: "opsinspector",
			Name:      "db_connections_idle",
			Help:      "Number of idle database connections",
		},
	)
)

// RecordInspectionRun 记录巡检执行
func RecordInspectionRun(inspectorType, status string, duration float64) {
	InspectionRunsTotal.WithLabelValues(inspectorType, status).Inc()
	InspectionDuration.WithLabelValues(inspectorType).Observe(duration)
}

// SetQueueSize 设置队列大小
func SetQueueSize(size float64) {
	InspectionQueueSize.Set(size)
}

// RecordSOPExecution 记录 SOP 执行
func RecordSOPExecution(sopName, status string, duration float64) {
	SOPExecutionsTotal.WithLabelValues(sopName, status).Inc()
	SOPExecutionDuration.WithLabelValues(sopName).Observe(duration)
}

// RecordWorkerTask 记录 Worker 任务
func RecordWorkerTask(workerID, status string) {
	WorkerTasksProcessed.WithLabelValues(workerID, status).Inc()
}

// SetWorkerActiveTasks 设置活跃任务数
func SetWorkerActiveTasks(count float64) {
	WorkerActiveTasks.Set(count)
}

// SetWorkerPoolSize 设置 Worker 池大小
func SetWorkerPoolSize(size float64) {
	WorkerPoolSize.Set(size)
}

// RecordNotification 记录通知发送
func RecordNotification(channel, status string, duration float64) {
	NotificationsTotal.WithLabelValues(channel, status).Inc()
	NotificationDuration.WithLabelValues(channel).Observe(duration)
}

// RecordAPIRequest 记录 API 请求
func RecordAPIRequest(method, path, status string, duration float64) {
	APIRequestsTotal.WithLabelValues(method, path, status).Inc()
	APIDuration.WithLabelValues(method, path).Observe(duration)
}

// SetDBConnections 设置数据库连接数
func SetDBConnections(active, idle float64) {
	DBConnectionsActive.Set(active)
	DBConnectionsIdle.Set(idle)
}

// MetricsHandler Prometheus 指标处理器
func MetricsHandler() gin.HandlerFunc {
	h := promhttp.Handler()
	return func(c *gin.Context) {
		h.ServeHTTP(c.Writer, c.Request)
	}
}

// PrometheusMiddleware Gin 中间件
func PrometheusMiddleware() gin.HandlerFunc {
	return func(c *gin.Context) {
		start := time.Now()
		path := c.FullPath()
		if path == "" {
			path = c.Request.URL.Path
		}

		c.Next()

		duration := time.Since(start).Seconds()
		status := strconv.Itoa(c.Writer.Status())

		RecordAPIRequest(c.Request.Method, path, status, duration)
	}
}

// UpdateDBMetrics 更新数据库指标（需要定期调用）
func UpdateDBMetrics(db *gorm.DB) {
	sqlDB, err := db.DB()
	if err != nil {
		return
	}

	stats := sqlDB.Stats()
	SetDBConnections(float64(stats.InUse), float64(stats.Idle))
}
