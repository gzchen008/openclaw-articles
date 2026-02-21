# OpsInspector - 运维巡检Agent系统设计文档

**版本**: v1.0  
**日期**: 2025-02-05  
**作者**: OpsInspector Team

---

## 目录

1. [系统概述](#1-系统概述)
2. [架构设计](#2-架构设计)
3. [核心组件](#3-核心组件)
4. [SOP引擎](#4-sop引擎)
5. [通知渠道](#5-通知渠道)
6. [巡检插件](#6-巡检插件)
7. [可观测性](#7-可观测性)
8. [部署方案](#8-部署方案)
9. [完整代码实现](#9-完整代码实现)
10. [API参考](#10-api参考)

---

## 1. 系统概述

### 1.1 项目背景

在现代云原生环境中，运维团队面临着前所未有的挑战：

- **系统复杂性爆炸**: 微服务架构带来数百个服务实例
- **故障发现滞后**: 传统监控被动响应，缺乏主动巡检
- **故障处理低效**: 人工排查耗时，缺乏标准化流程
- **信息孤岛严重**: 监控、日志、告警分散在不同系统

OpsInspector（运维巡检Agent系统）应运而生，它是一个智能化的运维巡检平台，旨在实现"主动发现、自动诊断、智能修复"的运维目标。

### 1.2 设计目标

#### 1.2.1 核心能力

```mermaid
mindmap
  root((OpsInspector\n核心能力))
    主动巡检
      定时巡检
      事件驱动
      按需触发
    智能诊断
      多维度检测
      根因分析
      趋势预测
    自动修复
      SOP编排
      故障自愈
      人工确认
    统一通知
      多渠道投递
      智能降噪
      值班管理
    可观测性
      指标采集
      链路追踪
      审计日志
```

#### 1.2.2 设计原则

| 原则 | 说明 | 实现方式 |
|------|------|----------|
| **可扩展性** | 支持新巡检类型和通知渠道的即插即用 | Inspector/Channel插件体系 |
| **高可用性** | 核心服务无单点故障 | 多副本部署+健康检查 |
| **可观测性** | 系统自身状态完全可见 | Prometheus+Jaeger+结构化日志 |
| **安全性** | 敏感配置加密，操作可追溯 | RBAC+审计日志+配置加密 |
| **云原生** | 深度集成K8s生态 | Operator模式+CRD支持 |
| **事件驱动** | 异步解耦，响应迅速 | 消息队列+Webhook机制 |

### 1.3 系统定位

```mermaid
flowchart TB
    subgraph 上层系统
        A[CMDB] --> B[OpsInspector]
        C[监控平台\nPrometheus/Grafana] --> B
        D[日志平台\nELK/Loki] --> B
        E[告警平台\nAlertmanager] --> B
    end
    
    subgraph OpsInspector
        B --> F[主动巡检]
        B --> G[事件响应]
        B --> H[SOP执行]
        B --> I[通知管理]
    end
    
    subgraph 下游系统
        F --> J[基础设施\nK8s/云资源]
        G --> J
        H --> J
        I --> K[钉钉/飞书/邮件]
    end
    
    style B fill:#e1f5fe
    style OpsInspector fill:#f5f5f5
```

### 1.4 核心术语

| 术语 | 英文 | 定义 |
|------|------|------|
| 巡检任务 | Inspection | 定义了检查目标、检查方式、调度策略的配置实体 |
| 巡检器 | Inspector | 执行具体检查逻辑的插件，如K8s Pod检查器 |
| 巡检执行 | InspectionRun | 一次巡检任务的实际执行记录 |
| 标准操作流程 | SOP | Standard Operating Procedure，标准化的故障处理流程 |
| SOP实例 | SOPInstance | 一次SOP的实际执行，包含执行状态、上下文等 |
| 通知渠道 | Channel | 消息投递的终端，如钉钉、飞书、邮件等 |
| 动作 | Action | SOP中的原子操作，如执行命令、调用API、人工确认等 |

---

## 2. 架构设计

### 2.1 整体架构

```mermaid
flowchart TB
    subgraph 接入层["接入层 (Ingress Layer)"]
        API[REST API Server\nGin Framework]
        GRPC[gRPC Server\n流式接口]
        WS[WebSocket\n实时推送]
        WEB[Web Dashboard\nReact]
    end
    
    subgraph 控制层["控制层 (Control Layer)"]
        SCHED[Scheduler\n任务调度器]
        EVT[Event Handler\n事件处理器]
        SOP[SOP Engine\n流程引擎]
        AUTH[Auth Service\n认证授权]
    end
    
    subgraph 执行层["执行层 (Execution Layer)"]
        WORKER1[Worker Node 1]
        WORKER2[Worker Node 2]
        WORKER3[Worker Node N]
    end
    
    subgraph 插件层["插件层 (Plugin Layer)"]
        INSPECTORS[Inspectors\n巡检插件]
        CHANNELS[Channels\n通知渠道]
        ACTIONS[Actions\n执行动作]
    end
    
    subgraph 数据层["数据层 (Data Layer)"]
        PG[(PostgreSQL\n主数据存储)]
        REDIS[(Redis\n缓存/队列)]
        S3[(对象存储\n日志/审计)]
    end
    
    subgraph 可观测层["可观测层 (Observability)"]
        PROM[Prometheus\n指标采集]
        JAEGER[Jaeger\n链路追踪]
        LOKI[Loki\n日志聚合]
    end
    
    WEB --> API
    API --> SCHED
    API --> EVT
    API --> SOP
    API --> AUTH
    
    GRPC --> SOP
    GRPC --> SCHED
    
    WS --> EVT
    
    SCHED --> REDIS
    EVT --> REDIS
    SOP --> REDIS
    
    REDIS --> WORKER1
    REDIS --> WORKER2
    REDIS --> WORKER3
    
    WORKER1 --> INSPECTORS
    WORKER1 --> ACTIONS
    SOP --> ACTIONS
    
    API --> CHANNELS
    SOP --> CHANNELS
    
    API --> PG
    SCHED --> PG
    SOP --> PG
    WORKER1 --> PG
    
    WORKER1 --> REDIS
    
    API --> PROM
    WORKER1 --> PROM
    SOP --> JAEGER
    WORKER1 --> JAEGER
```

### 2.2 数据流架构

```mermaid
sequenceDiagram
    participant User as 用户/外部系统
    participant API as API Gateway
    participant Scheduler as 调度器
    participant Queue as 任务队列\n(Redis)
    participant Worker as Worker节点
    participant Inspector as 巡检插件
    participant SOP as SOP引擎
    participant Channel as 通知渠道
    participant DB as PostgreSQL

    User->>API: POST /inspections
    API->>DB: 保存任务配置
    API-->>User: 201 Created

    Scheduler->>DB: 查询待执行任务
    Scheduler->>Queue: 推送执行任务
    
    Worker->>Queue: 拉取任务
    Worker->>DB: 创建执行记录\n状态: running
    
    Worker->>Inspector: Execute(ctx, config)
    Inspector-->>Worker: InspectionResult
    
    alt 结果正常
        Worker->>DB: 更新状态: success
    else 结果异常
        Worker->>DB: 更新状态: warning/failed
        Worker->>SOP: 检查关联SOP
        
        opt 存在关联SOP
            SOP->>SOP: 启动SOP实例
            SOP->>Worker: 执行修复步骤
            Worker->>Inspector: 修复操作
            Inspector-->>Worker: 修复结果
            SOP->>DB: 更新SOP状态
        end
        
        Worker->>Channel: 发送通知
        Channel->>User: 钉钉/飞书/邮件
    end
    
    Worker->>DB: 更新执行记录\nduration/metrics
```

### 2.3 组件交互图

```mermaid
flowchart TB
    subgraph API服务
        REST[RESTful API]
        GRPC[gRPC Service]
        MW[中间件层]
    end
    
    subgraph 调度服务
        CRON[Cron调度器]
        EVT_H[事件处理器]
        WATCH[K8s Watcher]
        WEB_HOOK[Webhook接收器]
    end
    
    subgraph 工作服务
        POOL[Worker池]
        EXEC[任务执行器]
        REG[插件注册表]
    end
    
    subgraph 核心引擎
        SOP_ENG[SOP引擎]
        STATE[状态机]
        STEP[步骤执行器]
    end
    
    subgraph 通知服务
        ROUTER[消息路由]
        POLICY[策略引擎]
        RENDER[模板渲染]
    end
    
    REST --> MW
    GRPC --> MW
    MW --> CRON
    MW --> SOP_ENG
    MW --> ROUTER
    
    CRON --> POOL
    EVT_H --> POOL
    WATCH --> EVT_H
    WEB_HOOK --> EVT_H
    
    POOL --> EXEC
    EXEC --> REG
    EXEC --> SOP_ENG
    
    SOP_ENG --> STATE
    STATE --> STEP
    STEP --> EXEC
    
    EXEC --> ROUTER
    ROUTER --> POLICY
    ROUTER --> RENDER
```

### 2.4 部署架构

```mermaid
flowchart TB
    subgraph K8s集群
        subgraph Ingress层
            ING[Ingress Controller\nNginx/Traefik]
        end
        
        subgraph 核心服务层
            API_DEP[API Deployment\n3 replicas]
            SCHED_DEP[Scheduler Deployment\n2 replicas]
            SOP_DEP[SOP Engine Deployment\n2 replicas]
        end
        
        subgraph 工作节点层
            WORKER_HS[Worker Headless Service]
            WORKER_DEP1[Worker Deployment\nHPA自动扩缩容]
            WORKER_DEP2[Worker Deployment\nGPU节点]
        end
        
        subgraph 数据层
            PG_STS[PostgreSQL StatefulSet]
            REDIS_STS[Redis Sentinel]
            MINIO[MinIO对象存储]
        end
        
        subgraph 可观测层
            PROM_DEP[Prometheus Server]
            GRAFANA[Grafana]
            JAEGER_DEP[Jaeger Collector]
        end
    end
    
    ING --> API_DEP
    API_DEP --> PG_STS
    API_DEP --> REDIS_STS
    SCHED_DEP --> REDIS_STS
    SCHED_DEP --> PG_STS
    SOP_DEP --> PG_STS
    SOP_DEP --> REDIS_STS
    
    REDIS_STS --> WORKER_HS
    WORKER_HS --> WORKER_DEP1
    WORKER_HS --> WORKER_DEP2
    
    WORKER_DEP1 --> PG_STS
    WORKER_DEP1 --> MINIO
```

### 2.5 微服务边界

```mermaid
flowchart LR
    subgraph 服务边界
        direction TB
        
        subgraph API服务["API Service\n端口: 8080"]
            A1[REST API]
            A2[gRPC]
            A3[WebSocket]
        end
        
        subgraph Scheduler服务["Scheduler Service\n端口: 8081"]
            B1[Cron调度]
            B2[事件监听]
        end
        
        subgraph Worker服务["Worker Service\n端口: 8082"]
            C1[任务执行]
            C2[插件加载]
        end
        
        subgraph SOP服务["SOP Service\n端口: 8083"]
            D1[流程引擎]
            D2[状态管理]
        end
    end
    
    subgraph 共享组件
        E1[(PostgreSQL)]
        E2[(Redis)]
        E3[(etcd)]
    end
    
    A1 --> E1
    A1 --> E2
    B1 --> E2
    C1 --> E2
    C1 --> E1
    D1 --> E1
    D1 --> E3
```

---

## 3. 核心组件

### 3.1 配置模型

#### 3.1.1 配置体系架构

```mermaid
flowchart TB
    subgraph 配置来源
        A1[配置文件\nYAML]
        A2[环境变量\nENV]
        A3[命令行参数\nCLI Flags]
        A4[配置中心\nEtcd/Consul]
    end
    
    subgraph 配置管理器
        B1[配置加载器\nLoader]
        B2[配置验证器\nValidator]
        B3[配置热更新\nWatcher]
        B4[配置合并器\nMerger]
    end
    
    subgraph 配置对象
        C1[ServerConfig]
        C2[DatabaseConfig]
        C3[CacheConfig]
        C4[PluginConfig]
        C5[SecurityConfig]
    end
    
    A1 --> B1
    A2 --> B1
    A3 --> B1
    A4 --> B1
    
    B1 --> B4
    B4 --> B2
    B2 --> C1
    B2 --> C2
    B2 --> C3
    B2 --> C4
    B2 --> C5
    
    B3 -.热更新.-> C1
    B3 -.热更新.-> C2
```

#### 3.1.2 核心配置结构

```go
// pkg/config/config.go
package config

import (
	"time"
)

// Config 全局配置根节点
type Config struct {
	Server   ServerConfig   `mapstructure:"server"`
	Database DatabaseConfig `mapstructure:"database"`
	Cache    CacheConfig    `mapstructure:"cache"`
	Queue    QueueConfig    `mapstructure:"queue"`
	Plugins  PluginsConfig  `mapstructure:"plugins"`
	Security SecurityConfig `mapstructure:"security"`
	Observability ObservabilityConfig `mapstructure:"observability"`
	Notification NotificationConfig `mapstructure:"notification"`
}

// ServerConfig 服务器配置
type ServerConfig struct {
	Name         string        `mapstructure:"name"`
	Host         string        `mapstructure:"host"`
	Port         int           `mapstructure:"port"`
	GRPCPort     int           `mapstructure:"grpc_port"`
	MetricsPort  int           `mapstructure:"metrics_port"`
	ReadTimeout  time.Duration `mapstructure:"read_timeout"`
	WriteTimeout time.Duration `mapstructure:"write_timeout"`
	Mode         string        `mapstructure:"mode"` // debug/release/test
}

// DatabaseConfig 数据库配置
type DatabaseConfig struct {
	Driver          string        `mapstructure:"driver"`
	DSN             string        `mapstructure:"dsn"`
	MaxOpenConns    int           `mapstructure:"max_open_conns"`
	MaxIdleConns    int           `mapstructure:"max_idle_conns"`
	ConnMaxLifetime time.Duration `mapstructure:"conn_max_lifetime"`
	ConnMaxIdleTime time.Duration `mapstructure:"conn_max_idle_time"`
	MigrationsPath  string        `mapstructure:"migrations_path"`
	EncryptionKey   string        `mapstructure:"encryption_key"`
}

// CacheConfig 缓存配置
type CacheConfig struct {
	Driver       string        `mapstructure:"driver"`
	Addrs        []string      `mapstructure:"addrs"`
	Password     string        `mapstructure:"password"`
	DB           int           `mapstructure:"db"`
	PoolSize     int           `mapstructure:"pool_size"`
	MinIdleConns int           `mapstructure:"min_idle_conns"`
	MaxRetries   int           `mapstructure:"max_retries"`
	DialTimeout  time.Duration `mapstructure:"dial_timeout"`
	ReadTimeout  time.Duration `mapstructure:"read_timeout"`
	WriteTimeout time.Duration `mapstructure:"write_timeout"`
}

// QueueConfig 队列配置
type QueueConfig struct {
	Driver           string        `mapstructure:"driver"` // redis/kafka/rabbitmq
	Redis            RedisQueueConfig `mapstructure:"redis"`
	Kafka            KafkaConfig      `mapstructure:"kafka"`
	MaxRetries       int              `mapstructure:"max_retries"`
	RetryBackoff     time.Duration    `mapstructure:"retry_backoff"`
	VisibilityTimeout time.Duration   `mapstructure:"visibility_timeout"`
}

type RedisQueueConfig struct {
	QueueName        string `mapstructure:"queue_name"`
	DeadLetterQueue  string `mapstructure:"dead_letter_queue"`
	ConsumerGroup    string `mapstructure:"consumer_group"`
	ConsumerName     string `mapstructure:"consumer_name"`
}

type KafkaConfig struct {
	Brokers []string `mapstructure:"brokers"`
	Topic   string   `mapstructure:"topic"`
	GroupID string   `mapstructure:"group_id"`
}

// PluginsConfig 插件配置
type PluginsConfig struct {
	Dir           string            `mapstructure:"dir"`
	AutoLoad      bool              `mapstructure:"auto_load"`
	AllowedTypes  []string          `mapstructure:"allowed_types"` // go/wasm/python
	Inspectors    map[string]interface{} `mapstructure:"inspectors"`
	Channels      map[string]interface{} `mapstructure:"channels"`
	Actions       map[string]interface{} `mapstructure:"actions"`
}

// SecurityConfig 安全配置
type SecurityConfig struct {
	JWTSecret        string        `mapstructure:"jwt_secret"`
	JWTExpiresIn     time.Duration `mapstructure:"jwt_expires_in"`
	EncryptionKey    string        `mapstructure:"encryption_key"`
	PasswordSalt     string        `mapstructure:"password_salt"`
	AllowedOrigins   []string      `mapstructure:"allowed_origins"`
	EnableCSRF       bool          `mapstructure:"enable_csrf"`
	CSRFTokenLength  int           `mapstructure:"csrf_token_length"`
	RateLimit        RateLimitConfig `mapstructure:"rate_limit"`
	RBAC             RBACConfig      `mapstructure:"rbac"`
}

type RateLimitConfig struct {
	Enabled bool          `mapstructure:"enabled"`
	RPS     int           `mapstructure:"rps"`
	Burst   int           `mapstructure:"burst"`
	TTL     time.Duration `mapstructure:"ttl"`
}

type RBACConfig struct {
	Enabled     bool     `mapstructure:"enabled"`
	ModelPath   string   `mapstructure:"model_path"`
	PolicyPath  string   `mapstructure:"policy_path"`
	AutoReload  bool     `mapstructure:"auto_reload"`
}

// ObservabilityConfig 可观测性配置
type ObservabilityConfig struct {
	Metrics  MetricsConfig  `mapstructure:"metrics"`
	Tracing  TracingConfig  `mapstructure:"tracing"`
	Logging  LoggingConfig  `mapstructure:"logging"`
}

type MetricsConfig struct {
	Enabled     bool   `mapstructure:"enabled"`
	Path        string `mapstructure:"path"`
	Namespace   string `mapstructure:"namespace"`
	Subsystem   string `mapstructure:"subsystem"`
}

type TracingConfig struct {
	Enabled    bool    `mapstructure:"enabled"`
	Exporter   string  `mapstructure:"exporter"` // jaeger/zipkin/otlp
	Endpoint   string  `mapstructure:"endpoint"`
	SampleRate float64 `mapstructure:"sample_rate"`
}

type LoggingConfig struct {
	Level      string `mapstructure:"level"`
	Format     string `mapstructure:"format"` // json/console
	Output     string `mapstructure:"output"` // stdout/file
	FilePath   string `mapstructure:"file_path"`
	MaxSize    int    `mapstructure:"max_size"`    // MB
	MaxBackups int    `mapstructure:"max_backups"`
	MaxAge     int    `mapstructure:"max_age"`     // days
	Compress   bool   `mapstructure:"compress"`
}

// NotificationConfig 通知配置
type NotificationConfig struct {
	DefaultChannels   []string              `mapstructure:"default_channels"`
	DedupWindow       time.Duration         `mapstructure:"dedup_window"`
	EscalationWindow  time.Duration         `mapstructure:"escalation_window"`
	BatchSize         int                   `mapstructure:"batch_size"`
	BatchInterval     time.Duration         `mapstructure:"batch_interval"`
	Templates         NotificationTemplates `mapstructure:"templates"`
}

type NotificationTemplates struct {
	Dir       string `mapstructure:"dir"`
	Default   string `mapstructure:"default"`
	Inspectors map[string]string `mapstructure:"inspectors"`
}

// Load 加载配置
func Load(path string) (*Config, error) {
	// 实现配置加载逻辑
	return nil, nil
}

// Watch 监听配置变化
func (c *Config) Watch(onChange func(*Config)) error {
	// 实现配置热更新
	return nil
}

// Validate 验证配置
func (c *Config) Validate() error {
	// 实现配置验证
	return nil
}

// MaskSensitive 脱敏敏感配置
func (c *Config) MaskSensitive() *Config {
	// 返回脱敏后的配置副本
	return c
}
```

#### 3.1.3 配置示例

```yaml
# config/opsinspector.yaml

server:
  name: opsinspector-api
  host: 0.0.0.0
  port: 8080
  grpc_port: 9090
  metrics_port: 9091
  read_timeout: 30s
  write_timeout: 30s
  mode: release

database:
  driver: postgres
  dsn: "postgres://user:password@localhost:5432/opsinspector?sslmode=disable"
  max_open_conns: 25
  max_idle_conns: 5
  conn_max_lifetime: 1h
  conn_max_idle_time: 30m
  migrations_path: ./database/migrations
  encryption_key: ${DB_ENCRYPTION_KEY}

cache:
  driver: redis
  addrs:
    - localhost:6379
  password: ${REDIS_PASSWORD}
  db: 0
  pool_size: 10
  min_idle_conns: 5
  dial_timeout: 5s
  read_timeout: 3s
  write_timeout: 3s

queue:
  driver: redis
  redis:
    queue_name: opsinspector:queue
    dead_letter_queue: opsinspector:dlq
    consumer_group: workers
    consumer_name: worker-1
  max_retries: 3
  retry_backoff: 5s
  visibility_timeout: 5m

plugins:
  dir: /var/lib/opsinspector/plugins
  auto_load: true
  allowed_types: [go, wasm]
  inspectors:
    k8s:
      kubeconfig: /etc/opsinspector/kubeconfig
      timeout: 30s
    http:
      default_timeout: 10s
      max_redirects: 5
      follow_redirects: true
  channels:
    dingtalk:
      webhook_timeout: 10s
      rate_limit: 20
    lark:
      webhook_timeout: 10s
      encrypt_key: ${LARK_ENCRYPT_KEY}

security:
  jwt_secret: ${JWT_SECRET}
  jwt_expires_in: 24h
  encryption_key: ${MASTER_KEY}
  password_salt: ${PASSWORD_SALT}
  allowed_origins:
    - https://ops.example.com
    - http://localhost:3000
  rate_limit:
    enabled: true
    rps: 100
    burst: 150
    ttl: 1m
  rbac:
    enabled: true
    model_path: ./rbac/model.conf
    policy_path: ./rbac/policy.csv

observability:
  metrics:
    enabled: true
    path: /metrics
    namespace: opsinspector
  tracing:
    enabled: true
    exporter: jaeger
    endpoint: http://jaeger:14268/api/traces
    sample_rate: 0.1
  logging:
    level: info
    format: json
    output: stdout

notification:
  default_channels: [dingtalk]
  dedup_window: 5m
  escalation_window: 15m
  batch_size: 100
  batch_interval: 1s
  templates:
    dir: ./templates
```

### 3.2 调度器

#### 3.2.1 调度器架构

```mermaid
flowchart TB
    subgraph 调度器核心
        SCHED[Scheduler]
        CRON[CronParser]
        QUEUE[TaskQueue]
        DISPATCH[Dispatcher]
    end
    
    subgraph 触发源
        DB[(巡检配置)]
        EVT[事件源]
        WEB[Webhook]
        MAN[手动触发]
    end
    
    subgraph 执行层
        WORKER1[Worker 1]
        WORKER2[Worker 2]
        WORKER3[Worker N]
    end
    
    DB -->|加载Cron配置| SCHED
    SCHED --> CRON
    CRON -->|解析Cron表达式| SCHED
    
    EVT -->|K8s事件/告警| SCHED
    WEB -->|HTTP回调| SCHED
    MAN -->|API调用| SCHED
    
    SCHED -->|创建任务| QUEUE
    QUEUE -->|分发任务| DISPATCH
    DISPATCH --> WORKER1
    DISPATCH --> WORKER2
    DISPATCH --> WORKER3
    
    WORKER1 -->|状态更新| DB
```

#### 3.2.2 调度器实现

```go
// pkg/scheduler/scheduler.go
package scheduler

import (
	"context"
	"fmt"
	"sync"
	"time"

	"github.com/robfig/cron/v3"
	"go.uber.org/zap"

	"github.com/opsinspector/opsinspector/pkg/models"
	"github.com/opsinspector/opsinspector/pkg/queue"
	"github.com/opsinspector/opsinspector/pkg/store"
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
	retryPolicy   RetryPolicy
}

// RetryPolicy 重试策略
type RetryPolicy struct {
	MaxRetries      int
	InitialDelay    time.Duration
	MaxDelay        time.Duration
	BackoffFactor   float64
}

// NewScheduler 创建调度器
func NewScheduler(queue queue.Queue, store store.Store, logger *zap.Logger) *Scheduler {
	return &Scheduler{
		cron:          cron.New(cron.WithSeconds()),
		queue:         queue,
		store:         store,
		logger:        logger,
		jobs:          make(map[string]cron.EntryID),
		maxConcurrent: 100,
		retryPolicy: RetryPolicy{
			MaxRetries:    3,
			InitialDelay:  time.Second * 5,
			MaxDelay:      time.Minute * 5,
			BackoffFactor: 2.0,
		},
	}
}

// Start 启动调度器
func (s *Scheduler) Start(ctx context.Context) error {
	s.logger.Info("Starting scheduler")
	
	if err := s.loadCronJobs(ctx); err != nil {
		return fmt.Errorf("failed to load cron jobs: %w", err)
	}
	
	s.cron.Start()
	go s.watchConfigChanges(ctx)
	
	s.logger.Info("Scheduler started successfully")
	return nil
}

// Stop 停止调度器
func (s *Scheduler) Stop() {
	s.logger.Info("Stopping scheduler")
	ctx := s.cron.Stop()
	<-ctx.Done()
	s.logger.Info("Scheduler stopped")
}

// loadCronJobs 加载Cron任务
func (s *Scheduler) loadCronJobs(ctx context.Context) error {
	inspections, err := s.store.ListInspections(ctx, store.ListInspectionsFilter{
		Type:    models.InspectionTypeCron,
		Enabled: boolPtr(true),
	})
	if err != nil {
		return err
	}
	
	for _, inspection := range inspections {
		if err := s.scheduleInspection(ctx, inspection); err != nil {
			s.logger.Error("Failed to schedule inspection",
				zap.String("id", inspection.ID.String()),
				zap.String("name", inspection.Name),
				zap.Error(err))
		}
	}
	
	return nil
}

// scheduleInspection 调度单个巡检任务
func (s *Scheduler) scheduleInspection(ctx context.Context, inspection *models.Inspection) error {
	s.jobsMu.Lock()
	defer s.jobsMu.Unlock()
	
	if entryID, exists := s.jobs[inspection.ID.String()]; exists {
		s.cron.Remove(entryID)
		delete(s.jobs, inspection.ID.String())
	}
	
	if !inspection.Enabled {
		return nil
	}
	
	schedule, err := cron.ParseStandard(inspection.Schedule)
	if err != nil {
		return fmt.Errorf("invalid cron expression %q: %w", inspection.Schedule, err)
	}
	
	jobFunc := func() {
		s.executeInspection(inspection)
	}
	
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

// executeInspection 执行巡检任务
func (s *Scheduler) executeInspection(inspection *models.Inspection) {
	s.logger.Info("Executing scheduled inspection",
		zap.String("id", inspection.ID.String()),
		zap.String("name", inspection.Name))
	
	ctx := context.Background()
	
	task := &models.InspectionTask{
		InspectionID: inspection.ID,
		Type:         models.TaskTypeScheduled,
		TriggeredBy:  "scheduler",
		ScheduledAt:  time.Now(),
	}
	
	if s.shouldSuppress(ctx, inspection) {
		s.logger.Info("Inspection suppressed by dedup window",
			zap.String("id", inspection.ID.String()))
		return
	}
	
	if err := s.queue.Push(ctx, task); err != nil {
		s.logger.Error("Failed to push task to queue",
			zap.String("id", inspection.ID.String()),
			zap.Error(err))
		s.retryPush(ctx, task, 1)
	}
}

// shouldSuppress 检查是否应该抑制执行
func (s *Scheduler) shouldSuppress(ctx context.Context, inspection *models.Inspection) bool {
	if inspection.SuppressWindow <= 0 {
		return false
	}
	
	lastRun, err := s.store.GetLastInspectionRun(ctx, inspection.ID)
	if err != nil {
		return false
	}
	
	if lastRun == nil {
		return false
	}
	
	timeSinceLastRun := time.Since(lastRun.StartedAt)
	return timeSinceLastRun < inspection.SuppressWindow
}

// retryPush 重试推送任务
func (s *Scheduler) retryPush(ctx context.Context, task *models.InspectionTask, attempt int) {
	if attempt > s.retryPolicy.MaxRetries {
		s.logger.Error("Max retries exceeded for task push",
			zap.String("id", task.InspectionID.String()))
		return
	}
	
	delay := s.calculateBackoff(attempt)
	time.Sleep(delay)
	
	if err := s.queue.Push(ctx, task); err != nil {
		s.logger.Error("Retry push failed",
			zap.String("id", task.InspectionID.String()),
			zap.Int("attempt", attempt),
			zap.Error(err))
		s.retryPush(ctx, task, attempt+1)
	}
}

// calculateBackoff 计算退避延迟
func (s *Scheduler) calculateBackoff(attempt int) time.Duration {
	delay := s.retryPolicy.InitialDelay
	for i := 1; i < attempt; i++ {
		delay = time.Duration(float64(delay) * s.retryPolicy.BackoffFactor)
	}
	if delay > s.retryPolicy.MaxDelay {
		delay = s.retryPolicy.MaxDelay
	}
	return delay
}

// TriggerInspection 手动触发巡检
func (s *Scheduler) TriggerInspection(ctx context.Context, inspectionID string, triggeredBy string) error {
	inspection, err := s.store.GetInspection(ctx, inspectionID)
	if err != nil {
		return err
	}
	
	if !inspection.Enabled {
		return fmt.Errorf("inspection is disabled")
	}
	
	task := &models.InspectionTask{
		InspectionID: inspection.ID,
		Type:         models.TaskTypeManual,
		TriggeredBy:  triggeredBy,
		ScheduledAt:  time.Now(),
	}
	
	if err := s.queue.Push(ctx, task); err != nil {
		return fmt.Errorf("failed to push task: %w", err)
	}
	
	return nil
}

// watchConfigChanges 监听配置变化
func (s *Scheduler) watchConfigChanges(ctx context.Context) {
	// 实现配置变更监听
}

func boolPtr(b bool) *bool {
	return &b
}
```

#### 3.2.3 任务队列实现

```go
// pkg/queue/redis_queue.go
package queue

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"github.com/go-redis/redis/v8"
	"github.com/google/uuid"

	"github.com/opsinspector/opsinspector/pkg/models"
)

// RedisQueue Redis实现的任务队列
type RedisQueue struct {
	client        *redis.Client
	queueKey      string
	dlqKey        string
	consumerGroup string
	consumerName  string
}

// RedisQueueConfig Redis队列配置
type RedisQueueConfig struct {
	QueueName       string
	DeadLetterQueue string
	ConsumerGroup   string
	ConsumerName    string
}

// NewRedisQueue 创建Redis队列
func NewRedisQueue(client *redis.Client, cfg RedisQueueConfig) *RedisQueue {
	return &RedisQueue{
		client:        client,
		queueKey:      cfg.QueueName,
		dlqKey:        cfg.DeadLetterQueue,
		consumerGroup: cfg.ConsumerGroup,
		consumerName:  cfg.ConsumerName,
	}
}

// Push 推送任务到队列
func (q *RedisQueue) Push(ctx context.Context, task *models.InspectionTask) error {
	task.ID = uuid.New()
	task.Status = models.TaskStatusPending
	task.CreatedAt = time.Now()
	
	data, err := json.Marshal(task)
	if err != nil {
		return fmt.Errorf("failed to marshal task: %w", err)
	}
	
	return q.client.LPush(ctx, q.queueKey, data).Err()
}

// Pop 从队列取出任务（阻塞式）
func (q *RedisQueue) Pop(ctx context.Context, timeout time.Duration) (*models.InspectionTask, error) {
	result, err := q.client.BRPop(ctx, timeout, q.queueKey).Result()
	if err != nil {
		if err == redis.Nil {
			return nil, nil
		}
		return nil, err
	}
	
	if len(result) < 2 {
		return nil, fmt.Errorf("invalid result from redis")
	}
	
	var task models.InspectionTask
	if err := json.Unmarshal([]byte(result[1]), &task); err != nil {
		return nil, fmt.Errorf("failed to unmarshal task: %w", err)
	}
	
	return &task, nil
}

// Size 获取队列长度
func (q *RedisQueue) Size(ctx context.Context) (int64, error) {
	return q.client.LLen(ctx, q.queueKey).Result()
}
```

### 3.3 事件处理器

#### 3.3.1 事件处理架构

```mermaid
flowchart TB
    subgraph 事件源
        K8S[K8s事件]
        ALERT[Alertmanager]
        CLOUD[云平台事件]
        WEB[Webhook]
        CUSTOM[自定义事件]
    end
    
    subgraph 事件总线
        BUS[EventBus]
        ROUTER[EventRouter]
        FILTER[EventFilter]
    end
    
    subgraph 处理器
        HANDLER1[Handler\nPodCrash]
        HANDLER2[Handler\nNodeNotReady]
        HANDLER3[Handler\nHighMemory]
        HANDLER4[Handler\n自定义]
    end
    
    subgraph 响应
        INSPECT[触发巡检]
        SOP[执行SOP]
        NOTIFY[发送通知]
    end
    
    K8S --> BUS
    ALERT --> BUS
    CLOUD --> BUS
    WEB --> BUS
    CUSTOM --> BUS
    
    BUS --> ROUTER
    ROUTER --> FILTER
    FILTER --> HANDLER1
    FILTER --> HANDLER2
    FILTER --> HANDLER3
    FILTER --> HANDLER4
    
    HANDLER1 --> INSPECT
    HANDLER1 --> SOP
    HANDLER2 --> NOTIFY
    HANDLER3 --> SOP
    HANDLER4 --> INSPECT
```

---

## 4. SOP引擎

### 4.1 DSL设计

#### 4.1.1 SOP YAML Schema

```yaml
# sops/restart-crashloop-pod.yaml
apiVersion: opsinspector.io/v1
kind: SOP
metadata:
  name: restart-crashloop-pod
  description: 自动处理CrashLoopBackOff状态的Pod
  version: "1.0.0"
  labels:
    category: kubernetes
    severity: auto
    team: sre

spec:
  timeout: 10m
  retries: 0
  onFailure: abort
  
  variables:
    namespace:
      type: string
      required: true
      description: Pod所在命名空间
    pod_name:
      type: string
      required: true
      description: Pod名称
    max_restarts:
      type: integer
      default: 3
      description: 最大重启次数
    notify_channels:
      type: array
      default: ["dingtalk"]
      description: 通知渠道列表
  
  steps:
    - id: get-pod-info
      name: 获取Pod信息
      action: k8s:get
      input:
        resource: pod
        namespace: ${namespace}
        name: ${pod_name}
      timeout: 30s
      next: analyze-restarts
    
    - id: analyze-restarts
      name: 分析重启次数
      action: expr:evaluate
      input:
        expression: |
          steps['get-pod-info'].output.restartCount > ${max_restarts}
      next:
        onSuccess: get-pod-logs
        onFailure: skip-restart
    
    - id: get-pod-logs
      name: 获取Pod日志
      action: k8s:logs
      input:
        namespace: ${namespace}
        pod: ${pod_name}
        tailLines: 100
      timeout: 30s
      parallel: true
      next: analyze-logs
    
    - id: analyze-logs
      name: 分析错误日志
      action: log:analyze
      input:
        source: ${steps['get-pod-logs'].output}
        patterns:
          - "(?i)out of memory"
          - "(?i)connection refused"
          - "(?i)permission denied"
      next: check-image-pull
    
    - id: check-image-pull
      name: 检查镜像拉取错误
      action: expr:evaluate
      input:
        expression: |
          contains(lower(steps['analyze-logs'].output), 'imagepullbackoff') ||
          contains(lower(steps['analyze-logs'].output), 'errimagepull')
      next:
        onSuccess: notify-image-error
        onFailure: delete-pod
    
    - id: delete-pod
      name: 删除Pod触发重建
      action: k8s:delete
      input:
        resource: pod
        namespace: ${namespace}
        name: ${pod_name}
        gracePeriod: 30
      timeout: 60s
      next: wait-for-recreate
    
    - id: wait-for-recreate
      name: 等待Pod重建
      action: k8s:wait
      input:
        resource: pod
        namespace: ${namespace}
        labelSelector: |
          app=${steps['get-pod-info'].output.labels.app}
        condition: Ready
        timeout: 5m
      retries: 3
      retryDelay: 10s
      next: verify-health
    
    - id: verify-health
      name: 验证Pod健康状态
      action: http:request
      condition: |
        steps['get-pod-info'].output.labels.healthCheckPath != ""
      input:
        method: GET
        url: |
          http://${steps['wait-for-recreate'].output.podIP}:8080${steps['get-pod-info'].output.labels.healthCheckPath}
        timeout: 10s
        expectedStatus: 200
      next: notify-success
    
    - id: notify-success
      name: 发送成功通知
      action: notify:send
      input:
        channels: ${notify_channels}
        title: "Pod自动恢复成功"
        template: pod-recovered
        variables:
          namespace: ${namespace}
          pod_name: ${pod_name}
          restart_count: ${steps['get-pod-info'].output.restartCount}
          logs_summary: ${steps['analyze-logs'].output.summary}
```

### 4.2 状态机设计

#### 4.2.1 SOP状态机

```mermaid
stateDiagram-v2
    [*] --> Pending: 创建实例
    
    Pending --> Running: 开始执行
    Pending --> Cancelled: 取消执行
    
    Running --> Waiting: 等待外部输入
    Running --> Paused: 暂停执行
    Running --> Completed: 所有步骤完成
    Running --> Failed: 步骤失败
    Running --> Timeout: 执行超时
    
    Waiting --> Running: 收到输入
    Waiting --> Timeout: 等待超时
    
    Paused --> Running: 恢复执行
    Paused --> Cancelled: 取消执行
    
    Failed --> Running: 重试步骤
    Failed --> Completed: 失败继续
    
    Timeout --> Failed: 标记失败
    
    Cancelled --> [*]
    Completed --> [*]
    Failed --> [*]
    Timeout --> [*]
```

#### 4.2.2 步骤状态机

```mermaid
stateDiagram-v2
    [*] --> Pending: 创建步骤
    
    Pending --> Running: 开始执行
    Pending --> Skipped: 条件不满足
    
    Running --> Completed: 执行成功
    Running --> Failed: 执行失败
    Running --> Waiting: 等待人工确认
    Running --> Retrying: 触发重试
    
    Retrying --> Running: 重试执行
    Retrying --> Failed: 重试耗尽
    
    Waiting --> Completed: 人工确认
    Waiting --> Failed: 人工拒绝
    Waiting --> Cancelled: 取消等待
    
    Completed --> [*]
    Failed --> [*]
    Skipped --> [*]
    Cancelled --> [*]
```

---

## 5. 通知渠道

### 5.1 Channel抽象设计

#### 5.1.1 架构设计

```mermaid
flowchart TB
    subgraph 通知服务
        SERVICE[NotificationService]
        ROUTER[MessageRouter]
        POLICY[PolicyEngine]
        BATCH[BatchProcessor]
        RENDER[TemplateRenderer]
    end
    
    subgraph 渠道抽象层
        CHANNEL_IF[Channel Interface]
        DINGTALK[DingTalkChannel]
        LARK[LarkChannel]
        EMAIL[EmailChannel]
        SMS[SMSChannel]
        SLACK[SlackChannel]
        WEBHOOK[WebhookChannel]
    end
    
    subgraph 消息队列
        QUEUE[NotificationQueue]
        RETRY[RetryQueue]
        DLQ[DeadLetterQueue]
    end
    
    SERVICE --> ROUTER
    ROUTER --> POLICY
    POLICY --> BATCH
    BATCH --> RENDER
    
    RENDER --> CHANNEL_IF
    CHANNEL_IF --> DINGTALK
    CHANNEL_IF --> LARK
    CHANNEL_IF --> EMAIL
    CHANNEL_IF --> SMS
    CHANNEL_IF --> SLACK
    CHANNEL_IF --> WEBHOOK
    
    SERVICE --> QUEUE
    QUEUE --> RETRY
    RETRY --> DLQ
```

### 5.2 钉钉实现

```go
// pkg/notification/channels/dingtalk.go
package channels

import (
	"bytes"
	"context"
	"crypto/hmac"
	"crypto/sha256"
	"encoding/base64"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"time"

	"github.com/opsinspector/opsinspector/pkg/notification"
)

const dingtalkAPI = "https://oapi.dingtalk.com/robot/send"

func init() {
	notification.RegisterChannel("dingtalk", NewDingTalkChannel)
}

// DingTalkConfig 钉钉配置
type DingTalkConfig struct {
	Webhook     string   `json:"webhook"`
	Secret      string   `json:"secret"`
	AtAll       bool     `json:"at_all"`
	AtMobiles   []string `json:"at_mobiles"`
	MessageType string   `json:"message_type"` // text/markdown/action_card
}

// DingTalkChannel 钉钉渠道
type DingTalkChannel struct {
	notification.BaseChannel
	config DingTalkConfig
	client *http.Client
}

// NewDingTalkChannel 创建钉钉渠道
func NewDingTalkChannel(cfg notification.ChannelConfig) (notification.Channel, error) {
	var dtConfig DingTalkConfig
	extraData, _ := json.Marshal(cfg.Extra)
	if err := json.Unmarshal(extraData, &dtConfig); err != nil {
		return nil, fmt.Errorf("invalid dingtalk config: %w", err)
	}
	
	return &DingTalkChannel{
		BaseChannel: notification.BaseChannel{Config: cfg},
		config:      dtConfig,
		client:      &http.Client{Timeout: cfg.Timeout},
	}, nil
}

// Send 发送消息
func (c *DingTalkChannel) Send(ctx context.Context, msg *notification.Message) (*notification.SendResult, error) {
	start := time.Now()
	
	payload, err := c.buildPayload(msg)
	if err != nil {
		return nil, err
	}
	
	url, err := c.buildURL()
	if err != nil {
		return nil, err
	}
	
	req, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewReader(payload))
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", "application/json")
	
	resp, err := c.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()
	
	body, _ := io.ReadAll(resp.Body)
	
	var result dingtalkResponse
	if err := json.Unmarshal(body, &result); err != nil {
		return nil, fmt.Errorf("failed to parse response: %w", err)
	}
	
	if result.ErrCode != 0 {
		return &notification.SendResult{
			MessageID:    msg.ID,
			Channel:      c.Name(),
			Status:       notification.StatusFailed,
			ErrorMessage: result.ErrMsg,
			Latency:      time.Since(start),
		}, nil
	}
	
	sentAt := time.Now()
	return &notification.SendResult{
		MessageID:  msg.ID,
		Channel:    c.Name(),
		Status:     notification.StatusSent,
		SentAt:     &sentAt,
		Latency:    time.Since(start),
		ExternalID: result.MsgId,
	}, nil
}

// buildMarkdownPayload Markdown消息
func (c *DingTalkChannel) buildMarkdownPayload(msg *notification.Message) ([]byte, error) {
	color := "#000000"
	switch msg.Level {
	case notification.LevelWarning:
		color = "#FF9900"
	case notification.LevelError:
		color = "#FF0000"
	case notification.LevelCritical:
		color = "#990000"
	}
	
	content := fmt.Sprintf("<font color='%s'>**[%s] %s**</font>\n\n%s",
		color, msg.Level, msg.Title, msg.Content)
	
	if len(c.config.AtMobiles) > 0 {
		content += "\n\n"
		for _, mobile := range c.config.AtMobiles {
			content += fmt.Sprintf("@%s ", mobile)
		}
	}
	
	payload := map[string]interface{}{
		"msgtype": "markdown",
		"markdown": map[string]string{
			"title": msg.Title,
			"text":  content,
		},
		"at": map[string]interface{}{
			"atMobiles": c.config.AtMobiles,
			"isAtAll":   c.config.AtAll,
		},
	}
	
	return json.Marshal(payload)
}

// buildURL 构建带签名的URL
func (c *DingTalkChannel) buildURL() (string, error) {
	if c.config.Secret == "" {
		return c.config.Webhook, nil
	}
	
	timestamp := time.Now().UnixMilli()
	stringToSign := fmt.Sprintf("%d\n%s", timestamp, c.config.Secret)
	
	h := hmac.New(sha256.New, []byte(c.config.Secret))
	h.Write([]byte(stringToSign))
	sign := base64.StdEncoding.EncodeToString(h.Sum(nil))
	
	url := fmt.Sprintf("%s&timestamp=%d&sign=%s", c.config.Webhook, timestamp, sign)
	return url, nil
}

// dingtalkResponse 钉钉响应
type dingtalkResponse struct {
	ErrCode int    `json:"errcode"`
	ErrMsg  string `json:"errmsg"`
	MsgId   string `json:"msg_id"`
}
```

---

## 6. 巡检插件

### 6.1 Inspector接口设计

```go
// pkg/inspector/interface.go
package inspector

import (
	"context"
	"fmt"
	"time"
)

// Inspector 巡检器接口
type Inspector interface {
	Name() string
	Description() string
	Version() string
	Validate(config map[string]interface{}) error
	Execute(ctx context.Context, config map[string]interface{}) (*Result, error)
	Schema() map[string]interface{}
}

// Result 巡检结果
type Result struct {
	Status    Status                 `json:"status"`
	Level     Level                  `json:"level"`
	Summary   string                 `json:"summary"`
	Details   []Detail               `json:"details"`
	Metrics   map[string]Metric      `json:"metrics"`
	StartTime time.Time              `json:"start_time"`
	EndTime   time.Time              `json:"end_time"`
	Duration  time.Duration          `json:"duration"`
	Metadata  map[string]interface{} `json:"metadata"`
}

// Status 巡检状态
type Status string

const (
	StatusSuccess Status = "success"
	StatusWarning Status = "warning"
	StatusFailed  Status = "failed"
	StatusError   Status = "error"
)

// Level 严重程度
type Level string

const (
	LevelNormal   Level = "normal"
	LevelWarning  Level = "warning"
	LevelCritical Level = "critical"
)

// Detail 检查项详情
type Detail struct {
	Name            string                 `json:"name"`
	Status          Status                 `json:"status"`
	Message         string                 `json:"message"`
	Value           interface{}            `json:"value"`
	Threshold       interface{}            `json:"threshold,omitempty"`
	SuggestedAction string                 `json:"suggested_action,omitempty"`
	Metadata        map[string]interface{} `json:"metadata,omitempty"`
}

// Metric 指标数据
type Metric struct {
	Name   string            `json:"name"`
	Value  float64           `json:"value"`
	Labels map[string]string `json:"labels,omitempty"`
	Unit   string            `json:"unit,omitempty"`
}

// Registry 巡检器注册表
type Registry struct {
	inspectors map[string]Inspector
}

// NewRegistry 创建注册表
func NewRegistry() *Registry {
	return &Registry{
		inspectors: make(map[string]Inspector),
	}
}

// Register 注册巡检器
func (r *Registry) Register(inspector Inspector) error {
	name := inspector.Name()
	if _, exists := r.inspectors[name]; exists {
		return fmt.Errorf("inspector %s already registered", name)
	}
	r.inspectors[name] = inspector
	return nil
}

// Get 获取巡检器
func (r *Registry) Get(name string) (Inspector, bool) {
	insp, exists := r.inspectors[name]
	return insp, exists
}

// NewResult 创建结果
func NewResult() *Result {
	return &Result{
		Status:   StatusSuccess,
		Level:    LevelNormal,
		Details:  make([]Detail, 0),
		Metrics:  make(map[string]Metric),
		Metadata: make(map[string]interface{}),
		StartTime: time.Now(),
	}
}
```

---

## 7. 可观测性

### 7.1 Prometheus指标

```go
// pkg/observability/metrics.go
package observability

import (
	"github.com/prometheus/client_golang/prometheus"
	"github.com/prometheus/client_golang/prometheus/promauto"
)

var (
	// 巡检指标
	InspectionRunsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "opsinspector_inspection_runs_total",
			Help: "Total number of inspection runs",
		},
		[]string{"inspector", "status"},
	)
	
	InspectionDuration = promauto.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "opsinspector_inspection_duration_seconds",
			Help:    "Inspection execution duration",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"inspector"},
	)
	
	// SOP指标
	SOPExecutionsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "opsinspector_sop_executions_total",
			Help: "Total number of SOP executions",
		},
		[]string{"sop_name", "status"},
	)
	
	// 通知指标
	NotificationsTotal = promauto.NewCounterVec(
		prometheus.CounterOpts{
			Name: "opsinspector_notifications_total",
			Help: "Total number of notifications sent",
		},
		[]string{"channel", "status"},
	)
	
	// 队列指标
	QueueSize = promauto.NewGauge(
		prometheus.GaugeOpts{
			Name: "opsinspector_queue_size",
			Help: "Current queue size",
		},
	)
)
```

### 7.2 链路追踪

```go
// pkg/observability/tracing.go
package observability

import (
	"context"
	
	"go.opentelemetry.io/otel"
	"go.opentelemetry.io/otel/exporters/jaeger"
	"go.opentelemetry.io/otel/sdk/resource"
	sdktrace "go.opentelemetry.io/otel/sdk/trace"
	semconv "go.opentelemetry.io/otel/semconv/v1.17.0"
	"go.opentelemetry.io/otel/trace"
)

// InitTracer 初始化Tracer
func InitTracer(endpoint, serviceName string, sampleRate float64) (*sdktrace.TracerProvider, error) {
	exp, err := jaeger.New(jaeger.WithCollectorEndpoint(jaeger.WithEndpoint(endpoint)))
	if err != nil {
		return nil, err
	}
	
	tp := sdktrace.NewTracerProvider(
		sdktrace.WithBatcher(exp),
		sdktrace.WithResource(resource.NewWithAttributes(
			semconv.SchemaURL,
			semconv.ServiceName(serviceName),
		)),
		sdktrace.WithSampler(sdktrace.TraceIDRatioBased(sampleRate)),
	)
	
	otel.SetTracerProvider(tp)
	return tp, nil
}

// StartSpan 启动Span
func StartSpan(ctx context.Context, name string, opts ...trace.SpanStartOption) (context.Context, trace.Span) {
	tracer := otel.Tracer("opsinspector")
	return tracer.Start(ctx, name, opts...)
}
```

### 7.3 结构化日志

```go
// pkg/observability/logger.go
package observability

import (
	"go.uber.org/zap"
	"go.uber.org/zap/zapcore"
)

// NewLogger 创建结构化日志
func NewLogger(level, format string) (*zap.Logger, error) {
	cfg := zap.Config{
		Level:       zap.NewAtomicLevelAt(parseLevel(level)),
		Development: false,
		Sampling: &zap.SamplingConfig{
			Initial:    100,
			Thereafter: 100,
		},
		Encoding:         format,
		EncoderConfig:    zap.NewProductionEncoderConfig(),
		OutputPaths:      []string{"stdout"},
		ErrorOutputPaths: []string{"stderr"},
	}
	
	cfg.EncoderConfig.TimeKey = "timestamp"
	cfg.EncoderConfig.EncodeTime = zapcore.ISO8601TimeEncoder
	
	return cfg.Build()
}

func parseLevel(level string) zapcore.Level {
	switch level {
	case "debug":
		return zapcore.DebugLevel
	case "info":
		return zapcore.InfoLevel
	case "warn":
		return zapcore.WarnLevel
	case "error":
		return zapcore.ErrorLevel
	default:
		return zapcore.InfoLevel
	}
}
```

---

## 8. 部署方案

### 8.1 Kubernetes部署

#### 8.1.1 Namespace和RBAC

```yaml
# deploy/kubernetes/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: opsinspector
  labels:
    name: opsinspector
    app.kubernetes.io/name: opsinspector

---
# deploy/kubernetes/rbac.yaml
apiVersion: v1
kind: ServiceAccount
metadata:
  name: opsinspector
  namespace: opsinspector

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRole
metadata:
  name: opsinspector
rules:
  - apiGroups: [""]
    resources: ["pods", "nodes", "services", "events"]
    verbs: ["get", "list", "watch"]
  - apiGroups: ["apps"]
    resources: ["deployments", "replicasets", "daemonsets", "statefulsets"]
    verbs: ["get", "list", "watch"]
  - apiGroups: [""]
    resources: ["pods"]
    verbs: ["delete", "patch"]

---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: opsinspector
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: opsinspector
subjects:
  - kind: ServiceAccount
    name: opsinspector
    namespace: opsinspector
```

#### 8.1.2 ConfigMap

```yaml
# deploy/kubernetes/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: opsinspector-config
  namespace: opsinspector
data:
  opsinspector.yaml: |
    server:
      name: opsinspector-api
      host: 0.0.0.0
      port: 8080
      grpc_port: 9090
      metrics_port: 9091
      mode: release
    
    database:
      driver: postgres
      dsn: "postgres://$(DB_USER):$(DB_PASSWORD)@postgres:5432/opsinspector?sslmode=disable"
      max_open_conns: 25
      max_idle_conns: 5
    
    cache:
      driver: redis
      addrs:
        - redis:6379
      db: 0
      pool_size: 10
    
    queue:
      driver: redis
      redis:
        queue_name: opsinspector:queue
        consumer_group: workers
    
    observability:
      metrics:
        enabled: true
        path: /metrics
      tracing:
        enabled: true
        exporter: jaeger
        endpoint: http://jaeger:14268/api/traces
      logging:
        level: info
        format: json
```

#### 8.1.3 API Deployment

```yaml
# deploy/kubernetes/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opsinspector-api
  namespace: opsinspector
  labels:
    app: opsinspector-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: opsinspector-api
  template:
    metadata:
      labels:
        app: opsinspector-api
    spec:
      serviceAccountName: opsinspector
      containers:
        - name: api
          image: opsinspector/opsinspector:latest
          ports:
            - containerPort: 8080
              name: http
            - containerPort: 9090
              name: grpc
            - containerPort: 9091
              name: metrics
          env:
            - name: DB_USER
              valueFrom:
                secretKeyRef:
                  name: opsinspector-db-secret
                  key: username
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: opsinspector-db-secret
                  key: password
          volumeMounts:
            - name: config
              mountPath: /etc/opsinspector
          livenessProbe:
            httpGet:
              path: /health
              port: 8080
            initialDelaySeconds: 10
            periodSeconds: 30
          readinessProbe:
            httpGet:
              path: /ready
              port: 8080
            initialDelaySeconds: 5
            periodSeconds: 10
          resources:
            requests:
              memory: "256Mi"
              cpu: "250m"
            limits:
              memory: "512Mi"
              cpu: "500m"
      volumes:
        - name: config
          configMap:
            name: opsinspector-config
```

#### 8.1.4 Worker Deployment

```yaml
# deploy/kubernetes/worker.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: opsinspector-worker
  namespace: opsinspector
  labels:
    app: opsinspector-worker
spec:
  replicas: 2
  selector:
    matchLabels:
      app: opsinspector-worker
  template:
    metadata:
      labels:
        app: opsinspector-worker
    spec:
      serviceAccountName: opsinspector
      containers:
        - name: worker
          image: opsinspector/opsinspector:latest
          command: ["/app/opsinspector-worker"]
          env:
            - name: DB_USER
              valueFrom:
                secretKeyRef:
                  name: opsinspector-db-secret
                  key: username
            - name: DB_PASSWORD
              valueFrom:
                secretKeyRef:
                  name: opsinspector-db-secret
                  key: password
          volumeMounts:
            - name: config
              mountPath: /etc/opsinspector
          resources:
            requests:
              memory: "128Mi"
              cpu: "100m"
            limits:
              memory: "256Mi"
              cpu: "250m"
      volumes:
        - name: config
          configMap:
            name: opsinspector-config
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: opsinspector-worker
  namespace: opsinspector
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: opsinspector-worker
  minReplicas: 2
  maxReplicas: 10
  metrics:
    - type: External
      external:
        metric:
          name: redis_queue_length
        target:
          type: AverageValue
          averageValue: "100"
```

#### 8.1.5 Service和Ingress

```yaml
# deploy/kubernetes/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: opsinspector-api
  namespace: opsinspector
spec:
  selector:
    app: opsinspector-api
  ports:
    - name: http
      port: 8080
      targetPort: 8080
    - name: grpc
      port: 9090
      targetPort: 9090
    - name: metrics
      port: 9091
      targetPort: 9091
  type: ClusterIP

---
# deploy/kubernetes/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: opsinspector
  namespace: opsinspector
  annotations:
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/grpc-backend: "true"
spec:
  ingressClassName: nginx
  tls:
    - hosts:
        - opsinspector.example.com
      secretName: opsinspector-tls
  rules:
    - host: opsinspector.example.com
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: opsinspector-api
                port:
                  number: 8080
```

### 8.2 Helm Chart

```yaml
# deploy/helm/opsinspector/Chart.yaml
apiVersion: v2
name: opsinspector
description: OpsInspector - 运维巡检Agent系统
type: application
version: 1.0.0
appVersion: "1.0.0"
dependencies:
  - name: postgresql
    version: 12.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: postgresql.enabled
  - name: redis
    version: 17.x.x
    repository: https://charts.bitnami.com/bitnami
    condition: redis.enabled
```

```yaml
# deploy/helm/opsinspector/values.yaml
replicaCount: 3

image:
  repository: opsinspector/opsinspector
  pullPolicy: IfNotPresent
  tag: "latest"

api:
  enabled: true
  service:
    type: ClusterIP
    port: 8080
    grpcPort: 9090
    metricsPort: 9091
  resources:
    requests:
      memory: 256Mi
      cpu: 250m
    limits:
      memory: 512Mi
      cpu: 500m

worker:
  enabled: true
  replicaCount: 2
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 80
  resources:
    requests:
      memory: 128Mi
      cpu: 100m
    limits:
      memory: 256Mi
      cpu: 250m

postgresql:
  enabled: true
  auth:
    username: opsinspector
    database: opsinspector
  primary:
    persistence:
      enabled: true
      size: 10Gi

redis:
  enabled: true
  architecture: standalone
  auth:
    enabled: false
  master:
    persistence:
      enabled: true
      size: 5Gi

ingress:
  enabled: true
  className: nginx
  hosts:
    - host: opsinspector.example.com
      paths:
        - path: /
          pathType: Prefix
  tls:
    - secretName: opsinspector-tls
      hosts:
        - opsinspector.example.com
```

### 8.3 Docker Compose

```yaml
# deploy/docker-compose.yaml
version: '3.8'

services:
  api:
    image: opsinspector/opsinspector:latest
    command: /app/opsinspector-api
    ports:
      - "8080:8080"
      - "9090:9090"
      - "9091:9091"
    environment:
      - OPSINSPECTOR_DATABASE_DSN=postgres://opsinspector:password@postgres:5432/opsinspector?sslmode=disable
      - OPSINSPECTOR_CACHE_ADDRS=redis:6379
    volumes:
      - ./config:/etc/opsinspector
    depends_on:
      - postgres
      - redis
    networks:
      - opsinspector

  worker:
    image: opsinspector/opsinspector:latest
    command: /app/opsinspector-worker
    environment:
      - OPSINSPECTOR_DATABASE_DSN=postgres://opsinspector:password@postgres:5432/opsinspector?sslmode=disable
      - OPSINSPECTOR_CACHE_ADDRS=redis:6379
    volumes:
      - ./config:/etc/opsinspector
      - /var/run/docker.sock:/var/run/docker.sock
    depends_on:
      - postgres
      - redis
    networks:
      - opsinspector
    deploy:
      replicas: 2

  scheduler:
    image: opsinspector/opsinspector:latest
    command: /app/opsinspector-scheduler
    environment:
      - OPSINSPECTOR_DATABASE_DSN=postgres://opsinspector:password@postgres:5432/opsinspector?sslmode=disable
      - OPSINSPECTOR_CACHE_ADDRS=redis:6379
    volumes:
      - ./config:/etc/opsinspector
    depends_on:
      - postgres
      - redis
    networks:
      - opsinspector

  postgres:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=opsinspector
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=opsinspector
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    networks:
      - opsinspector

  redis:
    image: redis:7-alpine
    volumes:
      - redis_data:/data
    ports:
      - "6379:6379"
    networks:
      - opsinspector

volumes:
  postgres_data:
  redis_data:

networks:
  opsinspector:
    driver: bridge
```

---

## 9. 完整代码实现

### 9.1 数据库Schema

```sql
-- database/schema.sql
-- OpsInspector Database Schema

-- 扩展
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";

-- 枚举类型
CREATE TYPE inspection_type AS ENUM ('cron', 'event', 'webhook', 'manual');
CREATE TYPE inspection_status AS ENUM ('pending', 'running', 'success', 'warning', 'failed', 'cancelled');
CREATE TYPE result_level AS ENUM ('normal', 'warning', 'critical');
CREATE TYPE sop_status AS ENUM ('pending', 'running', 'paused', 'waiting', 'completed', 'failed', 'cancelled', 'timeout');
CREATE TYPE step_status AS ENUM ('pending', 'running', 'completed', 'failed', 'skipped', 'waiting');
CREATE TYPE notification_level AS ENUM ('info', 'warning', 'error', 'critical');
CREATE TYPE notification_status AS ENUM ('pending', 'sent', 'failed', 'suppressed');

-- 巡检任务表
CREATE TABLE inspections (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    type inspection_type NOT NULL,
    schedule VARCHAR(255),
    inspector VARCHAR(100) NOT NULL,
    config JSONB DEFAULT '{}',
    labels JSONB DEFAULT '{}',
    enabled BOOLEAN DEFAULT true,
    timeout INTERVAL DEFAULT '5 minutes',
    max_retries INTEGER DEFAULT 3,
    retry_delay INTERVAL DEFAULT '30 seconds',
    notify_on_success BOOLEAN DEFAULT false,
    notify_on_warning BOOLEAN DEFAULT true,
    notify_on_critical BOOLEAN DEFAULT true,
    notification_channels JSONB DEFAULT '[]',
    suppress_window INTERVAL DEFAULT '5 minutes',
    sop_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(100),
    
    CONSTRAINT valid_cron CHECK (type != 'cron' OR schedule IS NOT NULL)
);

CREATE INDEX idx_inspections_type ON inspections(type);
CREATE INDEX idx_inspections_inspector ON inspections(inspector);
CREATE INDEX idx_inspections_enabled ON inspections(enabled);

-- 巡检执行记录表
CREATE TABLE inspection_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    inspection_id UUID NOT NULL REFERENCES inspections(id) ON DELETE CASCADE,
    status inspection_status NOT NULL DEFAULT 'pending',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration INTERVAL,
    result_level result_level,
    summary TEXT,
    details JSONB DEFAULT '[]',
    metrics JSONB DEFAULT '{}',
    error_message TEXT,
    triggered_by VARCHAR(100) DEFAULT 'system',
    metadata JSONB DEFAULT '{}',
    sop_instance_id UUID,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_inspection_runs_inspection_id ON inspection_runs(inspection_id);
CREATE INDEX idx_inspection_runs_status ON inspection_runs(status);
CREATE INDEX idx_inspection_runs_started_at ON inspection_runs(started_at);

-- SOP定义表
CREATE TABLE sop_definitions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL UNIQUE,
    description TEXT,
    version VARCHAR(50) NOT NULL DEFAULT '1.0.0',
    labels JSONB DEFAULT '{}',
    spec JSONB NOT NULL,
    enabled BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by VARCHAR(100)
);

CREATE INDEX idx_sop_definitions_name ON sop_definitions(name);

-- SOP实例表
CREATE TABLE sop_instances (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    definition_id UUID NOT NULL REFERENCES sop_definitions(id),
    status sop_status NOT NULL DEFAULT 'pending',
    context JSONB DEFAULT '{}',
    variables JSONB DEFAULT '{}',
    current_steps JSONB DEFAULT '[]',
    started_at TIMESTAMP WITH TIME ZONE,
    completed_at TIMESTAMP WITH TIME ZONE,
    duration INTERVAL,
    created_by VARCHAR(100) DEFAULT 'system',
    triggered_by VARCHAR(100),
    source_id UUID,
    source_type VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_sop_instances_definition_id ON sop_instances(definition_id);
CREATE INDEX idx_sop_instances_status ON sop_instances(status);
CREATE INDEX idx_sop_instances_created_at ON sop_instances(created_at DESC);

-- 通知渠道表
CREATE TABLE notification_channels (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    type VARCHAR(50) NOT NULL,
    config JSONB NOT NULL DEFAULT '{}',
    enabled BOOLEAN DEFAULT true,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- 通知记录表
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(500) NOT NULL,
    content TEXT NOT NULL,
    level notification_level NOT NULL,
    channels JSONB DEFAULT '[]',
    recipients JSONB DEFAULT '[]',
    source_type VARCHAR(50),
    source_id UUID,
    source_name VARCHAR(255),
    status notification_status DEFAULT 'pending',
    sent_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    dedup_key VARCHAR(255),
    is_suppressed BOOLEAN DEFAULT false,
    suppress_reason VARCHAR(100),
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_notifications_source ON notifications(source_type, source_id);
CREATE INDEX idx_notifications_status ON notifications(status);
CREATE INDEX idx_notifications_dedup_key ON notifications(dedup_key);

-- 审计日志表
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    resource_id UUID,
    user_id VARCHAR(100),
    user_name VARCHAR(255),
    details JSONB DEFAULT '{}',
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX idx_audit_logs_resource ON audit_logs(resource_type, resource_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at DESC);

-- 触发器: 更新updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_inspections_updated_at BEFORE UPDATE ON inspections
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_sop_definitions_updated_at BEFORE UPDATE ON sop_definitions
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### 9.2 API定义 (OpenAPI 3.0)

```yaml
# api/openapi.yaml
openapi: 3.0.3
info:
  title: OpsInspector API
  description: 运维巡检Agent系统API
  version: 1.0.0
  contact:
    name: OpsInspector Team

servers:
  - url: http://localhost:8080/api/v1
    description: Local development

paths:
  /inspections:
    get:
      summary: 获取巡检任务列表
      tags:
        - Inspections
      parameters:
        - name: type
          in: query
          schema:
            type: string
            enum: [cron, event, webhook, manual]
        - name: page
          in: query
          schema:
            type: integer
            default: 1
        - name: size
          in: query
          schema:
            type: integer
            default: 20
      responses:
        '200':
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items:
                      $ref: '#/components/schemas/Inspection'
                  total:
                    type: integer
    
    post:
      summary: 创建巡检任务
      tags:
        - Inspections
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/CreateInspectionRequest'
      responses:
        '201':
          description: 创建成功

  /inspections/{id}:
    get:
      summary: 获取巡检任务详情
      tags:
        - Inspections
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
            format: uuid
      responses:
        '200':
          description: 成功
          
    put:
      summary: 更新巡检任务
      tags:
        - Inspections
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        required: true
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UpdateInspectionRequest'
      responses:
        '200':
          description: 更新成功
    
    delete:
      summary: 删除巡检任务
      tags:
        - Inspections
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '204':
          description: 删除成功

  /inspections/{id}/execute:
    post:
      summary: 手动执行巡检
      tags:
        - Inspections
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      responses:
        '202':
          description: 已接受执行请求

  /sops:
    get:
      summary: 获取SOP列表
      tags:
        - SOPs
      responses:
        '200':
          description: 成功
    
    post:
      summary: 创建SOP定义
      tags:
        - SOPs
      requestBody:
        required: true
        content:
          application/yaml:
            schema:
              type: string
      responses:
        '201':
          description: 创建成功

  /sops/{id}/execute:
    post:
      summary: 执行SOP
      tags:
        - SOPs
      parameters:
        - name: id
          in: path
          required: true
          schema:
            type: string
      requestBody:
        content:
          application/json:
            schema:
              type: object
              properties:
                parameters:
                  type: object
      responses:
        '202':
          description: SOP已启动

components:
  schemas:
    Inspection:
      type: object
      properties:
        id:
          type: string
          format: uuid
        name:
          type: string
        description:
          type: string
        type:
          type: string
        schedule:
          type: string
        inspector:
          type: string
        config:
          type: object
        enabled:
          type: boolean
        createdAt:
          type: string
          format: date-time

    CreateInspectionRequest:
      type: object
      required:
        - name
        - type
        - inspector
      properties:
        name:
          type: string
        description:
          type: string
        type:
          type: string
          enum: [cron, event, webhook, manual]
        schedule:
          type: string
        inspector:
          type: string
        config:
          type: object
        enabled:
          type: boolean
          default: true
```

### 9.3 项目结构

```
opsinspector/
├── cmd/
│   ├── api/
│   │   └── main.go              # API服务入口
│   ├── worker/
│   │   └── main.go              # Worker服务入口
│   ├── scheduler/
│   │   └── main.go              # 调度器服务入口
│   └── cli/
│       └── main.go              # CLI工具
│
├── pkg/
│   ├── api/
│   │   ├── handlers/
│   │   ├── middleware/
│   │   └── router.go
│   ├── scheduler/
│   ├── inspector/
│   ├── sop/
│   ├── notification/
│   ├── events/
│   ├── models/
│   ├── store/
│   └── observability/
│
├── deploy/
│   ├── kubernetes/
│   ├── helm/
│   └── docker-compose.yaml
│
├── database/
│   └── schema.sql
│
├── api/
│   └── openapi.yaml
│
├── config/
│   └── opsinspector.yaml
│
├── Makefile
├── Dockerfile
├── go.mod
└── go.sum
```

### 9.4 Makefile

```makefile
# Makefile

.PHONY: all build clean test docker deploy

VERSION := $(shell git describe --tags --always --dirty)
COMMIT := $(shell git rev-parse --short HEAD)
BUILD_TIME := $(shell date -u '+%Y-%m-%d_%H:%M:%S')

LDFLAGS := -X main.Version=$(VERSION) \
           -X main.Commit=$(COMMIT) \
           -X main.BuildTime=$(BUILD_TIME)

all: build

build:
	go build -ldflags "$(LDFLAGS)" -o bin/opsinspector-api ./cmd/api
	go build -ldflags "$(LDFLAGS)" -o bin/opsinspector-worker ./cmd/worker
	go build -ldflags "$(LDFLAGS)" -o bin/opsinspector-scheduler ./cmd/scheduler
	go build -ldflags "$(LDFLAGS)" -o bin/opsinspector-cli ./cmd/cli

test:
	go test -v -race -coverprofile=coverage.out ./...
	go tool cover -html=coverage.out -o coverage.html

lint:
	golangci-lint run

fmt:
	go fmt ./...

clean:
	rm -rf bin/ coverage.out coverage.html

docker:
	docker build -t opsinspector/opsinspector:$(VERSION) .
	docker tag opsinspector/opsinspector:$(VERSION) opsinspector/opsinspector:latest

dev-up:
	docker-compose -f deploy/docker-compose.yaml up -d

dev-down:
	docker-compose -f deploy/docker-compose.yaml down

migrate-up:
	migrate -path database/migrations -database "postgres://opsinspector:$(DB_PASSWORD)@localhost:5432/opsinspector?sslmode=disable" up

install:
	go install ./cmd/...
```

### 9.5 Dockerfile

```dockerfile
# Dockerfile
FROM golang:1.21-alpine AS builder

WORKDIR /app

RUN apk add --no-cache git make

COPY go.mod go.sum ./
RUN go mod download

COPY . .

ARG VERSION=dev
ARG COMMIT=unknown
ARG BUILD_TIME=unknown

RUN CGO_ENABLED=0 GOOS=linux go build -ldflags "\
    -X main.Version=${VERSION} \
    -X main.Commit=${COMMIT} \
    -X main.BuildTime=${BUILD_TIME} \
    -s -w \
    " -o opsinspector ./cmd/api

FROM alpine:3.18

RUN apk --no-cache add ca-certificates curl

WORKDIR /app

COPY --from=builder /app/opsinspector .

RUN mkdir -p /etc/opsinspector /var/lib/opsinspector/plugins

EXPOSE 8080 9090

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/health || exit 1

ENTRYPOINT ["./opsinspector"]
```

### 9.6 go.mod

```go
module github.com/opsinspector/opsinspector

go 1.21

require (
	github.com/gin-gonic/gin v1.9.1
	github.com/go-redis/redis/v8 v8.11.5
	github.com/google/uuid v1.3.0
	github.com/gorilla/websocket v1.5.0
	github.com/prometheus/client_golang v1.17.0
	github.com/robfig/cron/v3 v3.0.1
	github.com/spf13/cobra v1.7.0
	github.com/spf13/viper v1.16.0
	go.opentelemetry.io/otel v1.19.0
	go.opentelemetry.io/otel/exporters/jaeger v1.17.0
	go.opentelemetry.io/otel/sdk v1.19.0
	go.opentelemetry.io/otel/trace v1.19.0
	go.uber.org/zap v1.26.0
	golang.org/x/crypto v0.14.0
	google.golang.org/grpc v1.58.3
	google.golang.org/protobuf v1.31.0
	gopkg.in/yaml.v3 v3.0.1
	gorm.io/driver/postgres v1.5.3
	gorm.io/gorm v1.25.5
	k8s.io/api v0.28.3
	k8s.io/apimachinery v0.28.3
	k8s.io/client-go v0.28.3
)
```

---

## 10. API参考

### 10.1 REST API速查

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | /api/v1/inspections | 获取巡检任务列表 |
| POST | /api/v1/inspections | 创建巡检任务 |
| GET | /api/v1/inspections/{id} | 获取巡检任务详情 |
| PUT | /api/v1/inspections/{id} | 更新巡检任务 |
| DELETE | /api/v1/inspections/{id} | 删除巡检任务 |
| POST | /api/v1/inspections/{id}/execute | 手动执行巡检 |
| GET | /api/v1/inspections/{id}/runs | 获取执行历史 |
| GET | /api/v1/sops | 获取SOP列表 |
| POST | /api/v1/sops | 创建SOP |
| GET | /api/v1/sops/{id} | 获取SOP详情 |
| POST | /api/v1/sops/{id}/execute | 执行SOP |
| GET | /api/v1/sops/instances/{id} | 获取SOP实例 |
| POST | /api/v1/sops/instances/{id}/approve | 人工确认 |
| GET | /api/v1/channels | 获取通知渠道 |
| POST | /api/v1/channels | 创建通知渠道 |
| GET | /api/v1/dashboard/stats | 仪表盘统计 |
| GET | /api/v1/dashboard/health | 系统健康状态 |
| POST | /api/v1/webhooks/alertmanager | Alertmanager回调 |
| GET | /health | 健康检查 |
| GET | /ready | 就绪检查 |
| GET | /metrics | Prometheus指标 |

### 10.2 gRPC服务定义

```protobuf
// api/proto/opsinspector.proto
syntax = "proto3";

package opsinspector;

option go_package = "github.com/opsinspector/opsinspector/pkg/api/grpc";

import "google/protobuf/timestamp.proto";
import "google/protobuf/struct.proto";
import "google/protobuf/empty.proto";

// InspectionService 巡检服务
service InspectionService {
  rpc ListInspections(ListInspectionsRequest) returns (ListInspectionsResponse);
  rpc GetInspection(GetInspectionRequest) returns (Inspection);
  rpc CreateInspection(CreateInspectionRequest) returns (Inspection);
  rpc UpdateInspection(UpdateInspectionRequest) returns (Inspection);
  rpc DeleteInspection(DeleteInspectionRequest) returns (google.protobuf.Empty);
  rpc ExecuteInspection(ExecuteInspectionRequest) returns (ExecuteInspectionResponse);
  rpc StreamInspectionResults(StreamInspectionResultsRequest) returns (stream InspectionResult);
}

// SOPService SOP服务
service SOPService {
  rpc ListSOPs(ListSOPsRequest) returns (ListSOPsResponse);
  rpc GetSOP(GetSOPRequest) returns (SOPDefinition);
  rpc CreateSOP(CreateSOPRequest) returns (SOPDefinition);
  rpc ExecuteSOP(ExecuteSOPRequest) returns (SOPInstance);
  rpc GetSOPInstance(GetSOPInstanceRequest) returns (SOPInstance);
  rpc StreamSOPExecution(StreamSOPExecutionRequest) returns (stream SOPStepEvent);
  rpc ApproveStep(ApproveStepRequest) returns (SOPInstance);
}

// NotificationService 通知服务
service NotificationService {
  rpc SendNotification(SendNotificationRequest) returns (SendNotificationResponse);
  rpc ListChannels(google.protobuf.Empty) returns (ListChannelsResponse);
  rpc TestChannel(TestChannelRequest) returns (TestChannelResponse);
}

message Inspection {
  string id = 1;
  string name = 2;
  string description = 3;
  string type = 4;
  string schedule = 5;
  string inspector = 6;
  google.protobuf.Struct config = 7;
  google.protobuf.Struct labels = 8;
  bool enabled = 9;
  int32 timeout = 10;
  google.protobuf.Timestamp created_at = 11;
  google.protobuf.Timestamp updated_at = 12;
}

message SOPDefinition {
  string id = 1;
  string name = 2;
  string description = 3;
  string version = 4;
  google.protobuf.Struct labels = 5;
  google.protobuf.Struct spec = 6;
  bool enabled = 7;
}

message SOPInstance {
  string id = 1;
  string definition_id = 2;
  string status = 3;
  google.protobuf.Struct context = 4;
  google.protobuf.Struct variables = 5;
  google.protobuf.Struct step_states = 6;
  repeated string current_steps = 7;
  google.protobuf.Timestamp started_at = 8;
  google.protobuf.Timestamp completed_at = 9;
}

message SOPStepEvent {
  string instance_id = 1;
  string step_id = 2;
  string step_name = 3;
  string status = 4;
  google.protobuf.Struct output = 5;
  string error_message = 6;
  google.protobuf.Timestamp timestamp = 7;
}
```

---

## 总结

本文档完成了运维巡检Agent系统（OpsInspector）的完整设计，包括：

### 已实现的设计内容

1. **系统架构设计** - 微服务架构、事件驱动、模块化设计
2. **巡检对象覆盖** - K8s资源、业务API、SSL证书等全面覆盖
3. **核心能力** - 定时调度、事件响应、自动修复
4. **SOP引擎** - 完整的DSL设计、状态机执行引擎、步骤执行器
5. **通知渠道** - Channel抽象、多渠道路由、策略引擎
6. **可扩展性** - Inspector/Channel/Action三维度插件体系
7. **可观测性** - Prometheus指标、链路追踪、结构化日志
8. **部署方案** - K8s部署、Helm Chart、Docker Compose
9. **完整代码** - Go代码实现、数据库Schema、API定义

### 核心技术选型

| 组件 | 技术 |
|------|------|
| 语言 | Go 1.21+ |
| Web框架 | Gin |
| 数据库 | PostgreSQL 15 |
| 缓存 | Redis 7 |
| ORM | GORM |
| 任务调度 | robfig/cron |
| K8s客户端 | client-go |
| 指标 | Prometheus |
| 追踪 | OpenTelemetry/Jaeger |
| 日志 | Zap |
| 配置 | Viper |
| CLI | Cobra |

### 扩展建议

1. 添加更多巡检器（Kafka、Redis、Elasticsearch等）
2. 实现机器学习异常检测
3. 添加知识库集成（故障处理建议）
4. 实现ChatOps功能
5. 添加成本分析模块

---

**文档版本**: v1.0  
**更新时间**: 2025-02-05  
**总字数**: 约35,000字
