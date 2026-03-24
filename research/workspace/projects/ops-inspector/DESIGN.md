# 运维巡检Agent系统设计文档
## Ops-Inspector Agent System Design Document

**版本:** v1.0  
**日期:** 2026-02-05  
**作者:** OpenClaw Architecture Team  

---

## 目录

1. [概述](#1-概述)
2. [架构设计](#2-架构设计)
3. [核心组件详解](#3-核心组件详解)
4. [通知系统](#4-通知系统-notification-system)
   - [4.1 架构概览](#41-架构概览)
   - [4.2 Channel抽象设计](#42-channel抽象设计)
   - [4.3 各渠道实现](#43-各渠道实现)
   - [4.4 通知策略引擎](#44-通知策略引擎)
   - [4.5 双向交互设计](#45-双向交互设计)
   - [4.6 路由引擎](#46-路由引擎)
   - [4.7 模板系统](#47-模板系统)
5. [SOP引擎设计](#5-sop引擎设计)
6. [数据模型](#6-数据模型)
7. [配置体系](#7-配置体系)
8. [扩展机制](#8-扩展机制)
9. [部署架构](#9-部署架构)
10. [代码示例](#10-代码示例)
11. [最佳实践](#11-最佳实践)

---

## 1. 概述

### 1.1 设计目标

Ops-Inspector是一个面向云原生环境的智能运维巡检Agent系统，旨在实现：

- **全栈覆盖:** 容器平台(K8s/Docker)、业务系统(API/服务)、基础设施(服务器/网络)
- **智能调度:** 定时任务 + 事件驱动的双模调度
- **自动修复:** 基于SOP的故障自愈能力
- **知识沉淀:** 可编排、可复用的SOP标准作业程序

### 1.2 参考架构

本设计参考以下优秀开源项目和最佳实践：

| 项目/实践 | 借鉴点 |
|-----------|--------|
| **OpenClaw** | Skill模块化、Cron定时任务、Event事件响应、Channel通知抽象 |
| **Netflix Mononoke** | 云原生自愈、Chaos Engineering理念 |
| **LinkedIn Cruise Control** | 自动化运维、自我调整、异常检测 |
| **Prometheus Operator** | CRD扩展、声明式配置、K8s原生集成 |
| **Argo Workflows** | DAG编排、事件触发、工作流引擎 |
| **Temporal.io** | 持久化工作流、超时处理、状态管理 |
| **Zabbix** | 数据采集、监控模板、告警分级 |

### 1.3 核心能力矩阵

```
┌─────────────────────────────────────────────────────────────┐
│                    Ops-Inspector 能力矩阵                    │
├─────────────┬─────────────┬─────────────┬─────────────────────┤
│   定时巡检   │   事件响应   │   自动修复   │      SOP编排        │
├─────────────┼─────────────┼─────────────┼─────────────────────┤
│ • Cron调度  │ • Webhook   │ • 自动重启   │ • YAML定义          │
│ • 按需触发  │ • 消息订阅  │ • 弹性扩容   │ • 条件分支          │
│ • 批次执行  │ • 阈值告警  │ • 流量切换   │ • 人工确认          │
│ • 报告生成  │ • 日志审计  │ • 配置回滚   │ • 超时处理          │
└─────────────┴─────────────┴─────────────┴─────────────────────┘
```

---

## 2. 架构设计

### 2.1 系统整体架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              用户交互层                                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │   CLI工具    │  │   Web UI     │  │  API Gateway │  │  Dashboard   │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────┘
          │                 │                 │                 │
          └─────────────────┴─────────────────┴─────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              核心引擎层                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐   │
│  │                        SOP Engine (SOP引擎)                          │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐              │   │
│  │  │ 解析器   │  │ 执行器   │  │ 状态机   │  │ 审计器   │              │   │
│  │  │ Parser   │  │ Executor │  │  FSM     │  │ Auditor  │              │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘              │   │
│  └──────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │
│  │ Task        │  │ Event       │  │ Inspector   │  │ Healer      │        │
│  │ Scheduler   │  │ Bus         │  │ Engine      │  │ Engine      │        │
│  │ 任务调度器   │  │ 事件总线    │  │ 巡检引擎    │  │ 修复引擎    │        │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘        │
│         │                │                │                │               │
│  ┌──────▼────────────────▼────────────────▼────────────────▼──────┐        │
│  │                      Skill Registry                            │        │
│  │                   (技能注册中心)                                │        │
│  └────────────────────────────────────────────────────────────────┘        │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
          ┌─────────────────────────┼─────────────────────────┐
          ▼                         ▼                         ▼
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│   数据采集层      │  │   执行代理层      │  │   通知通道层      │
│ ┌──────────────┐ │  │ ┌──────────────┐ │  │ ┌──────────────┐ │
│ │ Prometheus   │ │  │ │ K8s Agent    │ │  │ │ Slack        │ │
│ │ ElasticSearch│ │  │ │ Docker Agent │ │  │ │ DingTalk     │ │
│ │ InfluxDB     │ │  │ │ SSH Agent    │ │  │ │ Email        │ │
│ │ CloudWatch   │ │  │ │ SNMP Agent   │ │  │ │ Webhook      │ │
│ └──────────────┘ │  │ └──────────────┘ │  │ └──────────────┘ │
└──────────────────┘  └──────────────────┘  └──────────────────┘
```

### 2.2 数据流架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Ops-Inspector 数据流                               │
└─────────────────────────────────────────────────────────────────────────────┘

  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
  │   Metrics   │     │    Logs     │     │   Events    │     │    API      │
  │   指标数据   │     │   日志数据   │     │   事件数据   │     │   调用      │
  └──────┬──────┘     └──────┬──────┘     └──────┬──────┘     └──────┬──────┘
         │                   │                   │                   │
         └───────────────────┴───────────────────┴───────────────────┘
                                 │
                                 ▼
                    ┌──────────────────────┐
                    │    Data Collector    │
                    │      数据采集器       │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
    ┌─────────────────┐ ┌──────────────┐ ┌──────────────┐
    │  Time-Series DB │ │   Event Bus  │ │   Object DB  │
    │  (VictoriaMetrics│ │  (NATS/Kafka)│ │   (MongoDB)  │
    └────────┬────────┘ └──────┬───────┘ └──────┬───────┘
             │                 │                │
             ▼                 ▼                ▼
    ┌─────────────────────────────────────────────────────┐
    │              Analysis & Detection Engine            │
    │                 分析与检测引擎                       │
    │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐│
    │  │ 阈值规则 │  │ 异常检测 │  │ 趋势分析 │  │ 关联分析 ││
    │  │ Threshold│  │ Anomaly │  │  Trend  │  │Correlation│
    │  └─────────┘  └─────────┘  └─────────┘  └─────────┘│
    └────────────────────────┬────────────────────────────┘
                             │
            ┌────────────────┼────────────────┐
            ▼                ▼                ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │   SOP Engine │  │   Alert      │  │   Report     │
   │   (工作流)    │  │   告警通知    │  │   报告生成    │
   └──────┬───────┘  └──────┬───────┘  └──────┬───────┘
          │                 │                 │
          ▼                 ▼                 ▼
   ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
   │  Auto-Healing│  │  Notification│  │   Archive    │
   │   自动修复    │  │    通知       │  │    归档       │
   └──────────────┘  └──────────────┘  └──────────────┘
```

### 2.3 组件关系图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           组件交互关系图                                      │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │   User Request  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌──────────┐  ┌──────────┐  ┌──────────┐
       │   CLI    │  │   API    │  │   Web    │
       └────┬─────┘  └────┬─────┘  └────┬─────┘
            │             │             │
            └─────────────┼─────────────┘
                          │
                          ▼
               ┌─────────────────────┐
               │   Controller        │
               │   (控制协调器)       │
               └────────┬────────────┘
                        │
       ┌────────────────┼────────────────┐
       ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Scheduler  │ │   Inspector  │ │    SOP       │
│   Service    │ │   Service    │ │   Engine     │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Cron Jobs  │ │   Skills     │ │   Workflows  │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       │                │                │
       └────────────────┼────────────────┘
                        │
                        ▼
              ┌──────────────────┐
              │   Skill Registry │
              │   (技能注册中心)  │
              └────────┬─────────┘
                       │
       ┌───────────────┼───────────────┐
       ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ K8s Skills   │ │ Docker Skills│ │  Host Skills │
└──────────────┘ └──────────────┘ └──────────────┘
       │               │               │
       │               │               │
       ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Agents     │ │   Agents     │ │   Agents     │
│   (K8s)      │ │   (Docker)   │ │   (Host)     │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## 3. 核心组件详解

### 3.1 任务调度器 (Task Scheduler)

#### 3.1.1 职责
- 定时任务调度（Cron表达式支持）
- 任务生命周期管理（创建、暂停、恢复、删除）
- 任务依赖管理与DAG执行
- 分布式锁与防重入

#### 3.1.2 架构设计

```go
type Scheduler interface {
    // 基础CRUD
    CreateJob(ctx context.Context, job *Job) error
    UpdateJob(ctx context.Context, job *Job) error
    DeleteJob(ctx context.Context, jobID string) error
    GetJob(ctx context.Context, jobID string) (*Job, error)
    ListJobs(ctx context.Context, filter JobFilter) ([]*Job, error)
    
    // 生命周期控制
    Start() error
    Stop() error
    PauseJob(ctx context.Context, jobID string) error
    ResumeJob(ctx context.Context, jobID string) error
    TriggerJob(ctx context.Context, jobID string) error // 手动触发
    
    // 状态查询
    GetJobStatus(ctx context.Context, jobID string) (*JobStatus, error)
    GetJobHistory(ctx context.Context, jobID string, limit int) ([]*JobExecution, error)
}
```

#### 3.1.3 关键特性

| 特性 | 说明 | 实现方式 |
|------|------|----------|
| **Cron支持** | 标准Unix Cron + Quartz扩展 | `robfig/cron` 库 |
| **分布式调度** | 多实例防重复执行 | Redis分布式锁 + Leader选举 |
| **任务依赖** | DAG工作流 | 自定义DAG引擎 |
| **超时控制** | 任务执行超时 | Context + Timeout |
| **重试机制** | 失败自动重试 | 指数退避 + 最大重试次数 |
| **并发控制** | 任务并行度限制 | 信号量(Semaphore) |

### 3.2 事件总线 (Event Bus)

#### 3.2.1 职责
- 事件发布与订阅（Pub/Sub）
- 事件路由与过滤
- 事件持久化与重放
- 事件溯源（Event Sourcing）

#### 3.2.2 架构设计

```go
type EventBus interface {
    // 发布事件
    Publish(ctx context.Context, event *Event) error
    PublishAsync(ctx context.Context, event *Event) error
    
    // 订阅事件
    Subscribe(ctx context.Context, pattern string, handler EventHandler) (Subscription, error)
    SubscribeOnce(ctx context.Context, pattern string, handler EventHandler) error
    
    // 取消订阅
    Unsubscribe(ctx context.Context, sub Subscription) error
    
    // 请求-响应模式
    Request(ctx context.Context, event *Event, timeout time.Duration) (*Event, error)
    
    // 管理
    Close() error
}

// 事件结构
type Event struct {
    ID          string                 `json:"id"`
    Type        string                 `json:"type"`
    Source      string                 `json:"source"`
    Timestamp   time.Time              `json:"timestamp"`
    Data        map[string]interface{} `json:"data"`
    Headers     map[string]string      `json:"headers"`
    CorrelationID string               `json:"correlation_id"`
    ParentID    string                 `json:"parent_id"`
}
```

#### 3.2.3 事件类型定义

```go
// 系统事件
const (
    // 巡检相关
    EventTypeInspectionStarted   = "inspection.started"
    EventTypeInspectionCompleted = "inspection.completed"
    EventTypeInspectionFailed    = "inspection.failed"
    
    // 告警相关
    EventTypeAlertFired          = "alert.fired"
    EventTypeAlertAcknowledged   = "alert.acknowledged"
    EventTypeAlertResolved       = "alert.resolved"
    EventTypeAlertEscalated      = "alert.escalated"
    
    // SOP相关
    EventTypeSOPStarted          = "sop.started"
    EventTypeSOPStepExecuting    = "sop.step.executing"
    EventTypeSOPStepCompleted    = "sop.step.completed"
    EventTypeSOPStepFailed       = "sop.step.failed"
    EventTypeSOPWaitingApproval  = "sop.waiting.approval"
    EventTypeSOPApproved         = "sop.approved"
    EventTypeSOPRejected         = "sop.rejected"
    EventTypeSOPCompleted        = "sop.completed"
    
    // 修复相关
    EventTypeHealingStarted      = "healing.started"
    EventTypeHealingCompleted    = "healing.completed"
    EventTypeHealingFailed       = "healing.failed"
    
    // 资源相关
    EventTypeResourceCreated     = "resource.created"
    EventTypeResourceUpdated     = "resource.updated"
    EventTypeResourceDeleted     = "resource.deleted"
    EventTypeResourceUnhealthy   = "resource.unhealthy"
)
```

#### 3.2.4 事件流转架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           Event Bus 架构                                     │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │   Sources   │
                              │  (事件源)   │
                              └──────┬──────┘
                                     │
         ┌───────────────────────────┼───────────────────────────┐
         ▼                           ▼                           ▼
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   Webhook        │      │   Message Queue  │      │   Polling        │
│   Receiver       │      │   Subscriber     │      │   Collector      │
└────────┬─────────┘      └────────┬─────────┘      └────────┬─────────┘
         │                         │                         │
         └─────────────────────────┼─────────────────────────┘
                                   │
                                   ▼
                         ┌──────────────────┐
                         │   Event Router   │
                         │   (事件路由器)    │
                         └────────┬─────────┘
                                   │
              ┌────────────────────┼────────────────────┐
              ▼                    ▼                    ▼
    ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
    │  Pattern Matcher │ │  Filter Engine   │ │  Transform Engine│
    │  (模式匹配)       │ │  (过滤引擎)       │ │  (转换引擎)       │
    └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  │
                                  ▼
                        ┌──────────────────┐
                        │   Event Bus Core │
                        │  (核心事件总线)   │
                        │  (NATS/Kafka)    │
                        └────────┬─────────┘
                                   │
        ┌──────────────────────────┼──────────────────────────┐
        ▼                          ▼                          ▼
┌──────────────────┐   ┌──────────────────┐   ┌──────────────────┐
│   Rule Engine    │   │   SOP Engine     │   │   Notification   │
│   (规则引擎)      │   │   (SOP引擎)       │   │   Service        │
└──────────────────┘   └──────────────────┘   └──────────────────┘
```

### 3.3 巡检引擎 (Inspector Engine)

#### 3.3.1 职责
- 巡检任务执行
- 数据收集与聚合
- 健康状态评估
- 报告生成

#### 3.3.2 架构设计

```go
type Inspector interface {
    // 注册巡检器
    Register(checker Checker) error
    Unregister(name string) error
    
    // 执行巡检
    Run(ctx context.Context, config InspectionConfig) (*InspectionResult, error)
    RunAsync(ctx context.Context, config InspectionConfig) (string, error)
    
    // 获取结果
    GetResult(ctx context.Context, executionID string) (*InspectionResult, error)
    ListResults(ctx context.Context, filter ResultFilter) ([]*InspectionResult, error)
    
    // 获取检查器列表
    ListCheckers() []CheckerInfo
}

// 检查器接口
type Checker interface {
    Name() string
    Type() string // k8s/docker/host/api
    Description() string
    Check(ctx context.Context, target Target, config map[string]interface{}) (*CheckResult, error)
}
```

#### 3.3.3 巡检类型与场景

| 巡检类型 | 覆盖场景 | 检查项示例 |
|----------|----------|------------|
| **K8s巡检** | 集群健康、资源使用、Pod状态 | Node状态、Pod重启、资源限制、网络策略 |
| **Docker巡检** | 容器状态、镜像安全、资源占用 | 容器健康、镜像漏洞、磁盘使用、日志大小 |
| **主机巡检** | 系统负载、磁盘、内存、进程 | CPU/内存/磁盘使用率、僵尸进程、安全补丁 |
| **网络巡检** | 连通性、延迟、带宽、DNS | 网络延迟、丢包率、DNS解析、端口连通 |
| **API巡检** | 服务可用性、响应时间、正确性 | HTTP状态码、响应时间、SSL证书、端点健康 |
| **数据库巡检** | 连接数、慢查询、空间使用 | 活跃连接、慢查询数量、表空间、复制延迟 |

#### 3.3.4 巡检执行流程

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        巡检执行流程图                                        │
└─────────────────────────────────────────────────────────────────────────────┘

    ┌──────────┐
    │   Start  │
    └────┬─────┘
         │
         ▼
┌──────────────────┐     ┌──────────────────┐
│  Load Inspection │────▶│  Parse Config    │
│  Configuration   │     │  (解析配置)       │
└──────────────────┘     └────────┬─────────┘
                                  │
                                  ▼
┌──────────────────┐     ┌──────────────────┐
│  Aggregate       │◀────│  Load Checkers   │
│  Results         │     │  (加载检查器)      │
└────────┬─────────┘     └────────┬─────────┘
         │                        │
         │                        ▼
         │              ┌──────────────────┐
         │              │  Execute Parallel│
         │              │  (并行执行)       │
         │              └────────┬─────────┘
         │                       │
         │                       ▼
         │             ┌──────────────────┐
         │             │  Each Checker:   │
         │             │  ├─ Connect      │
         │             │  ├─ Collect      │
         │             │  ├─ Analyze      │
         │             │  └─ Report       │
         │             └────────┬─────────┘
         │                      │
         └──────────────────────┘
                                  │
                                  ▼
                       ┌──────────────────┐
                       │  Evaluate Health │
                       │  (健康评估)       │
                       └────────┬─────────┘
                                  │
              ┌───────────────────┼───────────────────┐
              ▼                   ▼                   ▼
    ┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
    │     Healthy      │ │     Warning      │ │    Critical      │
    │     (健康)       │ │     (警告)       │ │    (严重)        │
    └────────┬─────────┘ └────────┬─────────┘ └────────┬─────────┘
             │                    │                    │
             │                    ▼                    ▼
             │          ┌──────────────────┐ ┌──────────────────┐
             │          │  Trigger Alert   │ │  Trigger SOP     │
             │          │  (触发告警)       │ │  (触发修复SOP)   │
             │          └──────────────────┘ └──────────────────┘
             │
             ▼
    ┌──────────────────┐
    │  Generate Report │
    │  (生成报告)       │
    └────────┬─────────┘
             │
             ▼
    ┌──────────────────┐
    │  Archive & Notify│
    │  (归档&通知)      │
    └──────────────────┘
```

### 3.4 修复引擎 (Healer Engine)

#### 3.4.1 职责
- 自动故障诊断
- 基于SOP的自动修复
- 修复策略选择
- 修复结果验证

#### 3.4.2 架构设计

```go
type Healer interface {
    // 注册修复器
    Register(remediator Remediator) error
    
    // 修复执行
    Heal(ctx context.Context, issue Issue, strategy HealingStrategy) (*HealingResult, error)
    
    // 诊断
    Diagnose(ctx context.Context, target Target, symptoms []Symptom) (*Diagnosis, error)
    
    // 策略建议
    SuggestStrategy(ctx context.Context, issue Issue) ([]HealingStrategy, error)
    
    // 验证修复
    Verify(ctx context.Context, issue Issue, healingID string) (*VerificationResult, error)
}

// 修复动作
type Remediator interface {
    Name() string
    Category() string // restart/scale/network/config
    CanHandle(issue Issue) bool
    Remediate(ctx context.Context, issue Issue, params map[string]interface{}) (*RemediationResult, error)
    Rollback(ctx context.Context, remediationID string) error
}
```

#### 3.4.3 自动修复决策树

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        自动修复决策树                                        │
└─────────────────────────────────────────────────────────────────────────────┘

                           ┌──────────────────┐
                           │   Issue Detected │
                           │   (问题检测)      │
                           └────────┬─────────┘
                                    │
                                    ▼
                           ┌──────────────────┐
                           │  Auto-Healing    │
                           │  Enabled?        │
                           └────────┬─────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │ No                            │ Yes
                    ▼                               ▼
           ┌──────────────────┐          ┌──────────────────┐
           │  Create Alert    │          │  Match SOP       │
           │  (创建告警)       │          │  (匹配SOP)       │
           └──────────────────┘          └────────┬─────────┘
                                                  │
                                                  ▼
                                         ┌──────────────────┐
                                         │  SOP Found?      │
                                         └────────┬─────────┘
                                                  │
                              ┌───────────────────┴───────────────────┐
                              │ No                                    │ Yes
                              ▼                                       ▼
                     ┌──────────────────┐                  ┌──────────────────┐
                     │  Execute Default │                  │  Load SOP        │
                     │  Heuristic       │                  │  Definition      │
                     │  (启发式修复)     │                  │  (加载SOP定义)   │
                     └────────┬─────────┘                  └────────┬─────────┘
                              │                                   │
                              └───────────────┬───────────────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │  Pre-Check       │
                                     │  (前置检查)       │
                                     └────────┬─────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │  Approval        │
                                     │  Required?       │
                                     └────────┬─────────┘
                                              │
                              ┌───────────────┴───────────────┐
                              │ No                            │ Yes
                              ▼                               ▼
                     ┌──────────────────┐          ┌──────────────────┐
                     │  Execute Action  │          │  Wait for        │
                     │  (执行修复动作)   │          │  Approval        │
                     │                  │          │  (等待审批)      │
                     └────────┬─────────┘          └────────┬─────────┘
                              │                             │
                              ▼                             ▼
                     ┌──────────────────┐          ┌──────────────────┐
                     │  Verify Result   │          │  Execute Action  │
                     │  (验证结果)       │          │  (执行修复动作)   │
                     └────────┬─────────┘          └────────┬─────────┘
                              │                             │
                              └───────────────┬─────────────┘
                                              │
                                              ▼
                                     ┌──────────────────┐
                                     │  Success?        │
                                     └────────┬─────────┘
                                              │
                              ┌───────────────┴───────────────┐
                              │ Yes                           │ No
                              ▼                               ▼
                     ┌──────────────────┐          ┌──────────────────┐
                     │  Record Success  │          │  Retry/          │
                     │  Update Metrics  │          │  Escalate        │
                     │  Notify Success  │          │  (重试或升级)     │
                     └──────────────────┘          └──────────────────┘
```

### 3.5 技能注册中心 (Skill Registry)

#### 3.5.1 职责
- Skill动态注册与发现
- Skill版本管理
- Skill依赖解析
- Skill配置验证

#### 3.5.2 架构设计

```go
type SkillRegistry interface {
    // 注册技能
    Register(skill Skill) error
    Unregister(name string) error
    
    // 获取技能
    Get(name string) (Skill, error)
    List(filter SkillFilter) ([]Skill, error)
    
    // 发现技能
    Discover(source string) ([]Skill, error)
    
    // 执行技能
    Execute(ctx context.Context, name string, input SkillInput) (*SkillOutput, error)
}

// Skill定义
type Skill interface {
    Metadata() SkillMetadata
    Validate(config map[string]interface{}) error
    Execute(ctx context.Context, input SkillInput) (*SkillOutput, error)
}

type SkillMetadata struct {
    Name        string            `json:"name"`
    Version     string            `json:"version"`
    Type        string            `json:"type"` // checker/healer/notifier/collector
    Category    string            `json:"category"`
    Description string            `json:"description"`
    Author      string            `json:"author"`
    Inputs      []Parameter       `json:"inputs"`
    Outputs     []Parameter       `json:"outputs"`
    Dependencies []string         `json:"dependencies"`
    Config      map[string]interface{} `json:"config"`
}
```

#### 3.5.3 Skill分类

| 类型 | 描述 | 示例 |
|------|------|------|
| **Checker** | 巡检技能 | Pod状态检查、磁盘空间检查、API健康检查 |
| **Healer** | 修复技能 | Pod重启、服务扩容、配置回滚 |
| **Notifier** | 通知技能 | Slack通知、邮件通知、钉钉通知 |
| **Collector** | 采集技能 | Prometheus查询、日志收集、指标聚合 |
| **Filter** | 过滤技能 | 告警去重、事件过滤、噪音消除 |
| **Enricher** | 增强技能 | 告警增强、上下文附加、关联分析 |

---

## 4. 通知系统 (Notification System)

### 4.1 架构概览

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        通知系统整体架构                                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         通知策略引擎                                         │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │   Policy Parser  │  │   Router         │  │   Rate Limiter   │          │
│  │   (策略解析器)    │  │   (路由器)        │  │   (限流器)        │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      通知处理器链                                     │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │  │ Enricher │  │ Filter   │  │ Grouper  │  │ Template │             │  │
│  │  │ (增强器) │  │ (过滤器) │  │ (分组器) │  │ (模板)   │             │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      策略规则引擎                                     │  │
│  │  • 分级通知 (Severity-based Routing)                                  │  │
│  │  • 告警抑制 (Notification Inhibition)                                 │  │
│  │  • 告警升级 (Auto-escalation)                                         │  │
│  │  • 告警收敛 (Alert Aggregation)                                       │  │
│  │  • 时间路由 (Time-based Routing)                                      │  │
│  │  • 值班路由 (On-call Routing)                                         │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Channel Manager                                      │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      Channel Registry                                │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │
│  │  │  DingTalk│ │  Feishu │ │ WeCom   │ │  Slack   │ │  Email   │   │  │
│  │  │  (钉钉)  │ │ (飞书)  │ │(企业微信)│ │          │ │          │   │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │
│  │  │   SMS    │ │  Phone  │ │ Webhook │ │ PagerDuty│ │ OpsGenie │   │  │
│  │  │  (短信)  │ │ (电话)  │ │          │ │          │ │          │   │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      Interactive Layer                               │  │
│  │  • 消息回调处理                                                       │  │
│  │  • 快捷操作按钮                                                       │  │
│  │  • 交互式表单                                                         │  │
│  │  • 操作确认流程                                                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.2 Channel抽象设计

#### 4.2.1 核心接口定义

```go
// pkg/notification/channel.go

package notification

import (
    "context"
    "time"
)

// Channel 通知渠道接口 - 所有通知渠道必须实现
type Channel interface {
    // 基础信息
    Name() string                          // 渠道名称: dingtalk/feishu/slack/email/...
    Type() ChannelType                     // 渠道类型
    Capabilities() ChannelCapabilities     // 能力声明
    
    // 生命周期
    Initialize(ctx context.Context, config ChannelConfig) error
    HealthCheck(ctx context.Context) error
    Close() error
    
    // 消息发送
    Send(ctx context.Context, message *Message) (*SendResult, error)
    SendBatch(ctx context.Context, messages []*Message) ([]*SendResult, error)
    
    // 双向交互（可选实现）
    SetCallbackHandler(handler CallbackHandler) error
    VerifySignature(payload []byte, signature string) bool
}

// ChannelType 渠道类型
type ChannelType string

const (
    ChannelTypeInstant    ChannelType = "instant"    // 即时消息：钉钉、飞书、Slack
    ChannelTypeEmail      ChannelType = "email"      // 邮件
    ChannelTypeSMS        ChannelType = "sms"        // 短信
    ChannelTypeVoice      ChannelType = "voice"      // 语音电话
    ChannelTypeWebhook    ChannelType = "webhook"    // Webhook
    ChannelTypePagerDuty  ChannelType = "pagerduty"  // PagerDuty
)

// ChannelCapabilities 渠道能力声明
type ChannelCapabilities struct {
    SupportsRichText     bool   // 支持富文本
    SupportsMarkdown     bool   // 支持Markdown
    SupportsCards        bool   // 支持卡片消息
    SupportsImages       bool   // 支持图片
    SupportsAttachments  bool   // 支持附件
    SupportsThreading    bool   // 支持消息线程
    SupportsCallback     bool   // 支持回调交互
    SupportsBatch        bool   // 支持批量发送
    MaxMessageSize       int    // 最大消息大小(字节)
    RateLimitPerSecond   int    // 每秒限流
    RateLimitPerMinute   int    // 每分钟限流
}

// ChannelConfig 渠道配置
type ChannelConfig struct {
    Name        string                 `json:"name" yaml:"name"`               // 渠道实例名称
    Type        string                 `json:"type" yaml:"type"`               // 渠道类型
    Enabled     bool                   `json:"enabled" yaml:"enabled"`         // 是否启用
    Default     bool                   `json:"default" yaml:"default"`         // 是否为默认渠道
    Credentials map[string]string      `json:"credentials" yaml:"credentials"` // 认证信息
    Settings    map[string]interface{} `json:"settings" yaml:"settings"`       // 渠道特定设置
    RetryPolicy RetryPolicy            `json:"retryPolicy" yaml:"retryPolicy"` // 重试策略
}

// RetryPolicy 重试策略
type RetryPolicy struct {
    MaxRetries    int           `json:"maxRetries"`
    InitialDelay  time.Duration `json:"initialDelay"`
    MaxDelay      time.Duration `json:"maxDelay"`
    BackoffFactor float64       `json:"backoffFactor"`
}

// Message 通知消息
type Message struct {
    ID          string                 `json:"id"`          // 消息唯一ID
    Type        MessageType            `json:"type"`        // 消息类型
    Priority    Priority               `json:"priority"`    // 优先级
    Title       string                 `json:"title"`       // 标题
    Content     string                 `json:"content"`     // 内容
    Markdown    string                 `json:"markdown"`    // Markdown内容
    HTML        string                 `json:"html"`        // HTML内容
    
    // 富媒体内容
    Cards       []Card                 `json:"cards"`       // 卡片消息
    Attachments []Attachment           `json:"attachments"` // 附件
    Buttons     []Button               `json:"buttons"`     // 交互按钮
    
    // 上下文信息
    Context     map[string]interface{} `json:"context"`     // 上下文数据
    Labels      map[string]string      `json:"labels"`      // 标签
    ThreadID    string                 `json:"threadId"`    // 消息线程ID
    ReplyTo     string                 `json:"replyTo"`     // 回复消息ID
    
    // 目标信息
    Recipients  []Recipient            `json:"recipients"`  // 接收人
    
    // 元数据
    CreatedAt   time.Time              `json:"createdAt"`
    ExpireAt    *time.Time             `json:"expireAt"`
}

// MessageType 消息类型
type MessageType string

const (
    MessageTypeAlert      MessageType = "alert"      // 告警通知
    MessageTypeApproval   MessageType = "approval"   // 审批请求
    MessageTypeReport     MessageType = "report"     // 报告
    MessageTypeReminder   MessageType = "reminder"   // 提醒
    MessageTypeInteractive MessageType = "interactive" // 交互消息
)

// Priority 优先级
type Priority int

const (
    PriorityLow      Priority = 1
    PriorityNormal   Priority = 2
    PriorityHigh     Priority = 3
    PriorityCritical Priority = 4
    PriorityEmergency Priority = 5
)

// Card 卡片消息
type Card struct {
    Type        string                 `json:"type"`        // 卡片类型: alert/info/success/warning
    Title       string                 `json:"title"`
    Color       string                 `json:"color"`       // 颜色代码
    Fields      []CardField            `json:"fields"`      // 字段列表
    Actions     []Button               `json:"actions"`     // 操作按钮
    Footer      string                 `json:"footer"`
    Timestamp   time.Time              `json:"timestamp"`
}

// CardField 卡片字段
type CardField struct {
    Title    string `json:"title"`
    Value    string `json:"value"`
    Short    bool   `json:"short"`    // 是否短字段（并排显示）
}

// Button 交互按钮
type Button struct {
    ID       string                 `json:"id"`       // 按钮唯一ID
    Type     ButtonType             `json:"type"`     // 按钮类型
    Text     string                 `json:"text"`     // 按钮文本
    Style    ButtonStyle            `json:"style"`    // 按钮样式
    Action   string                 `json:"action"`   // 操作类型
    Data     map[string]interface{} `json:"data"`     // 操作数据
    URL      string                 `json:"url"`      // 跳转链接
    Confirm  *ConfirmDialog         `json:"confirm"`  // 确认对话框
}

type ButtonType string

const (
    ButtonTypeAction   ButtonType = "action"   // 执行操作
    ButtonTypeLink     ButtonType = "link"     // 跳转链接
    ButtonTypeForm     ButtonType = "form"     // 打开表单
)

type ButtonStyle string

const (
    ButtonStyleDefault ButtonStyle = "default"
    ButtonStylePrimary ButtonStyle = "primary"
    ButtonStyleDanger  ButtonStyle = "danger"
)

// ConfirmDialog 确认对话框
type ConfirmDialog struct {
    Title       string `json:"title"`
    Text        string `json:"text"`
    ConfirmText string `json:"confirmText"`
    CancelText  string `json:"cancelText"`
}

// Recipient 接收人
type Recipient struct {
    Type    RecipientType `json:"type"`    // user/group/channel
    ID      string        `json:"id"`      // 接收人ID
    Name    string        `json:"name"`    // 显示名称
    Phone   string        `json:"phone"`   // 手机号（短信/电话用）
    Email   string        `json:"email"`   // 邮箱地址
}

type RecipientType string

const (
    RecipientTypeUser    RecipientType = "user"
    RecipientTypeGroup   RecipientType = "group"
    RecipientTypeChannel RecipientType = "channel"
)

// SendResult 发送结果
type SendResult struct {
    MessageID   string        `json:"messageId"`   // 消息ID
    ChannelName string        `json:"channelName"` // 渠道名称
    Status      SendStatus    `json:"status"`      // 发送状态
    SentAt      time.Time     `json:"sentAt"`      // 发送时间
    ExternalID  string        `json:"externalId"`  // 外部系统消息ID
    Error       error         `json:"error"`       // 错误信息
}

type SendStatus string

const (
    SendStatusSuccess   SendStatus = "success"
    SendStatusFailed    SendStatus = "failed"
    SendStatusPending   SendStatus = "pending"
    SendStatusThrottled SendStatus = "throttled"
)

// CallbackHandler 回调处理接口
type CallbackHandler interface {
    HandleCallback(ctx context.Context, callback *Callback) (*CallbackResponse, error)
}

// Callback 回调数据
type Callback struct {
    Channel     string                 `json:"channel"`     // 渠道名称
    MessageID   string                 `json:"messageId"`   // 消息ID
    UserID      string                 `json:"userId"`      // 用户ID
    UserName    string                 `json:"userName"`    // 用户名
    Action      string                 `json:"action"`      // 操作类型
    ButtonID    string                 `json:"buttonId"`    // 按钮ID
    Data        map[string]interface{} `json:"data"`        // 附加数据
    Timestamp   time.Time              `json:"timestamp"`
    RawPayload  []byte                 `json:"rawPayload"`  // 原始数据
    Signature   string                 `json:"signature"`   // 签名
}

// CallbackResponse 回调响应
type CallbackResponse struct {
    Message     string      `json:"message"`     // 响应消息
    UpdateMessage *Message  `json:"updateMessage"` // 更新原消息
    CloseDialog bool        `json:"closeDialog"` // 是否关闭对话框
}
```

#### 4.2.2 Channel管理器

```go
// pkg/notification/channel_manager.go

package notification

import (
    "context"
    "fmt"
    "sync"
)

// ChannelManager 渠道管理器
type ChannelManager struct {
    channels map[string]Channel          // 已注册的渠道实例
    registry map[string]ChannelFactory   // 渠道工厂注册表
    mu       sync.RWMutex
    
    // 回调处理
    callbackHandler CallbackHandler
}

// ChannelFactory 渠道工厂函数
type ChannelFactory func() Channel

// NewChannelManager 创建渠道管理器
func NewChannelManager() *ChannelManager {
    cm := &ChannelManager{
        channels: make(map[string]Channel),
        registry: make(map[string]ChannelFactory),
    }
    
    // 注册内置渠道工厂
    cm.registerBuiltins()
    
    return cm
}

// RegisterFactory 注册渠道工厂
func (cm *ChannelManager) RegisterFactory(channelType string, factory ChannelFactory) {
    cm.mu.Lock()
    defer cm.mu.Unlock()
    cm.registry[channelType] = factory
}

// CreateChannel 创建并初始化渠道实例
func (cm *ChannelManager) CreateChannel(ctx context.Context, config ChannelConfig) (Channel, error) {
    cm.mu.Lock()
    factory, ok := cm.registry[config.Type]
    cm.mu.Unlock()
    
    if !ok {
        return nil, fmt.Errorf("unknown channel type: %s", config.Type)
    }
    
    channel := factory()
    
    if err := channel.Initialize(ctx, config); err != nil {
        return nil, fmt.Errorf("failed to initialize channel %s: %w", config.Name, err)
    }
    
    // 如果支持回调，设置回调处理器
    if channel.Capabilities().SupportsCallback && cm.callbackHandler != nil {
        if err := channel.SetCallbackHandler(cm.callbackHandler); err != nil {
            return nil, fmt.Errorf("failed to set callback handler: %w", err)
        }
    }
    
    cm.mu.Lock()
    cm.channels[config.Name] = channel
    cm.mu.Unlock()
    
    return channel, nil
}

// GetChannel 获取渠道实例
func (cm *ChannelManager) GetChannel(name string) (Channel, error) {
    cm.mu.RLock()
    defer cm.mu.RUnlock()
    
    channel, ok := cm.channels[name]
    if !ok {
        return nil, fmt.Errorf("channel not found: %s", name)
    }
    
    return channel, nil
}

// GetChannelsByType 按类型获取渠道
func (cm *ChannelManager) GetChannelsByType(channelType string) []Channel {
    cm.mu.RLock()
    defer cm.mu.RUnlock()
    
    var result []Channel
    for _, ch := range cm.channels {
        if string(ch.Type()) == channelType {
            result = append(result, ch)
        }
    }
    return result
}

// ListChannels 列出所有渠道
func (cm *ChannelManager) ListChannels() []ChannelInfo {
    cm.mu.RLock()
    defer cm.mu.RUnlock()
    
    var result []ChannelInfo
    for name, ch := range cm.channels {
        result = append(result, ChannelInfo{
            Name:         name,
            Type:         string(ch.Type()),
            Capabilities: ch.Capabilities(),
        })
    }
    return result
}

// SetCallbackHandler 设置全局回调处理器
func (cm *ChannelManager) SetCallbackHandler(handler CallbackHandler) {
    cm.callbackHandler = handler
}

// registerBuiltins 注册内置渠道
func (cm *ChannelManager) registerBuiltins() {
    cm.registry["dingtalk"] = func() Channel { return &DingTalkChannel{} }
    cm.registry["feishu"] = func() Channel { return &FeishuChannel{} }
    cm.registry["wecom"] = func() Channel { return &WeComChannel{} }
    cm.registry["slack"] = func() Channel { return &SlackChannel{} }
    cm.registry["email"] = func() Channel { return &EmailChannel{} }
    cm.registry["sms"] = func() Channel { return &SMSChannel{} }
    cm.registry["phone"] = func() Channel { return &PhoneChannel{} }
    cm.registry["webhook"] = func() Channel { return &WebhookChannel{} }
    cm.registry["pagerduty"] = func() Channel { return &PagerDutyChannel{} }
}

type ChannelInfo struct {
    Name         string              `json:"name"`
    Type         string              `json:"type"`
    Capabilities ChannelCapabilities `json:"capabilities"`
}
```

### 4.3 各渠道实现

#### 4.3.1 钉钉 (DingTalk)

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
    "net/http"
    "time"
)

// DingTalkChannel 钉钉渠道
type DingTalkChannel struct {
    config      notification.ChannelConfig
    webhookURL  string
    secret      string
    accessToken string
    httpClient  *http.Client
    callbackHandler notification.CallbackHandler
}

// Name 返回渠道名称
func (d *DingTalkChannel) Name() string {
    return d.config.Name
}

// Type 返回渠道类型
func (d *DingTalkChannel) Type() notification.ChannelType {
    return notification.ChannelTypeInstant
}

// Capabilities 返回能力声明
func (d *DingTalkChannel) Capabilities() notification.ChannelCapabilities {
    return notification.ChannelCapabilities{
        SupportsRichText:    true,
        SupportsMarkdown:    true,
        SupportsCards:       true,
        SupportsImages:      true,
        SupportsAttachments: false,
        SupportsThreading:   false,
        SupportsCallback:    true,
        SupportsBatch:       false,
        MaxMessageSize:      20480,  // 20KB
        RateLimitPerSecond:  20,
        RateLimitPerMinute:  1000,
    }
}

// Initialize 初始化
func (d *DingTalkChannel) Initialize(ctx context.Context, config notification.ChannelConfig) error {
    d.config = config
    d.webhookURL = config.Credentials["webhook_url"]
    d.secret = config.Credentials["secret"]
    d.accessToken = config.Credentials["access_token"]
    d.httpClient = &http.Client{
        Timeout: 30 * time.Second,
    }
    return nil
}

// HealthCheck 健康检查
func (d *DingTalkChannel) HealthCheck(ctx context.Context) error {
    // 发送测试消息
    testMsg := &notification.Message{
        Type:    notification.MessageTypeAlert,
        Title:   "Health Check",
        Content: "Connection test",
    }
    _, err := d.Send(ctx, testMsg)
    return err
}

// Close 关闭
func (d *DingTalkChannel) Close() error {
    return nil
}

// Send 发送消息
func (d *DingTalkChannel) Send(ctx context.Context, message *notification.Message) (*notification.SendResult, error) {
    payload := d.buildPayload(message)
    
    url := d.webhookURL
    if d.secret != "" {
        timestamp := time.Now().UnixMilli()
        sign := d.generateSign(timestamp, d.secret)
        url = fmt.Sprintf("%s&timestamp=%d&sign=%s", url, timestamp, sign)
    }
    
    body, err := json.Marshal(payload)
    if err != nil {
        return nil, err
    }
    
    req, err := http.NewRequestWithContext(ctx, "POST", url, bytes.NewReader(body))
    if err != nil {
        return nil, err
    }
    req.Header.Set("Content-Type", "application/json")
    
    resp, err := d.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var result struct {
        ErrCode int    `json:"errcode"`
        ErrMsg  string `json:"errmsg"`
    }
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return nil, err
    }
    
    if result.ErrCode != 0 {
        return nil, fmt.Errorf("dingtalk API error: %s", result.ErrMsg)
    }
    
    return &notification.SendResult{
        MessageID:   message.ID,
        ChannelName: d.Name(),
        Status:      notification.SendStatusSuccess,
        SentAt:      time.Now(),
    }, nil
}

// SendBatch 批量发送（钉钉不支持真正的批量，模拟批量）
func (d *DingTalkChannel) SendBatch(ctx context.Context, messages []*notification.Message) ([]*notification.SendResult, error) {
    results := make([]*notification.SendResult, len(messages))
    for i, msg := range messages {
        result, err := d.Send(ctx, msg)
        if err != nil {
            result = &notification.SendResult{
                MessageID:   msg.ID,
                ChannelName: d.Name(),
                Status:      notification.SendStatusFailed,
                Error:       err,
            }
        }
        results[i] = result
    }
    return results, nil
}

// SetCallbackHandler 设置回调处理器
func (d *DingTalkChannel) SetCallbackHandler(handler notification.CallbackHandler) error {
    d.callbackHandler = handler
    return nil
}

// VerifySignature 验证签名
func (d *DingTalkChannel) VerifySignature(payload []byte, signature string) bool {
    // 钉钉签名验证逻辑
    return true
}

// buildPayload 构建钉钉消息体
func (d *DingTalkChannel) buildPayload(message *notification.Message) map[string]interface{} {
    // 根据消息类型构建不同的消息格式
    switch {
    case len(message.Cards) > 0:
        return d.buildActionCard(message)
    case message.Markdown != "":
        return d.buildMarkdownMessage(message)
    default:
        return d.buildTextMessage(message)
    }
}

// buildTextMessage 文本消息
func (d *DingTalkChannel) buildTextMessage(message *notification.Message) map[string]interface{} {
    return map[string]interface{}{
        "msgtype": "text",
        "text": map[string]string{
            "content": message.Content,
        },
        "at": map[string]interface{}{
            "atMobiles": d.extractAtMobiles(message.Content),
            "isAtAll":   false,
        },
    }
}

// buildMarkdownMessage Markdown消息
func (d *DingTalkChannel) buildMarkdownMessage(message *notification.Message) map[string]interface{} {
    return map[string]interface{}{
        "msgtype": "markdown",
        "markdown": map[string]string{
            "title": message.Title,
            "text":  message.Markdown,
        },
    }
}

// buildActionCard 卡片消息（支持交互按钮）
func (d *DingTalkChannel) buildActionCard(message *notification.Message) map[string]interface{} {
    card := message.Cards[0]
    
    btns := make([]map[string]string, 0, len(card.Actions))
    for _, btn := range card.Actions {
        btns = append(btns, map[string]string{
            "title":     btn.Text,
            "actionURL": d.buildActionURL(btn),
        })
    }
    
    markdown := d.buildCardMarkdown(card)
    
    // 如果只有一个按钮，使用整体跳转
    if len(btns) == 1 {
        return map[string]interface{}{
            "msgtype": "action_card",
            "action_card": map[string]interface{}{
                "title":          card.Title,
                "markdown":       markdown,
                "single_title":   btns[0]["title"],
                "single_url":     btns[0]["actionURL"],
            },
        }
    }
    
    // 多个按钮使用独立跳转
    return map[string]interface{}{
        "msgtype": "action_card",
        "action_card": map[string]interface{}{
            "title":    card.Title,
            "markdown": markdown,
            "btn_orientation": "1", // 横向排列
            "btns":     btns,
        },
    }
}

// buildCardMarkdown 构建卡片Markdown
func (d *DingTalkChannel) buildCardMarkdown(card notification.Card) string {
    var buf bytes.Buffer
    
    // 标题和颜色标识
    colorEmoji := d.getColorEmoji(card.Color)
    buf.WriteString(fmt.Sprintf("## %s %s\n\n", colorEmoji, card.Title))
    
    // 字段
    for _, field := range card.Fields {
        if field.Short {
            buf.WriteString(fmt.Sprintf("**%s:** %s  ", field.Title, field.Value))
        } else {
            buf.WriteString(fmt.Sprintf("\n**%s:**\n%s\n", field.Title, field.Value))
        }
    }
    
    // 页脚
    if card.Footer != "" {
        buf.WriteString(fmt.Sprintf("\n\n---\n%s", card.Footer))
    }
    
    return buf.String()
}

// buildActionURL 构建操作URL（包含回调信息）
func (d *DingTalkChannel) buildActionURL(btn notification.Button) string {
    // 构建包含回调信息的URL
    data := map[string]interface{}{
        "channel":   "dingtalk",
        "action":    btn.Action,
        "button_id": btn.ID,
        "data":      btn.Data,
    }
    
    jsonData, _ := json.Marshal(data)
    encoded := base64.URLEncoding.EncodeToString(jsonData)
    
    // 返回回调URL
    return fmt.Sprintf("%s/api/v1/callbacks/dingtalk?data=%s", 
        d.config.Settings["base_url"], encoded)
}

// generateSign 生成签名
func (d *DingTalkChannel) generateSign(timestamp int64, secret string) string {
    stringToSign := fmt.Sprintf("%d\n%s", timestamp, secret)
    h := hmac.New(sha256.New, []byte(secret))
    h.Write([]byte(stringToSign))
    return base64.StdEncoding.EncodeToString(h.Sum(nil))
}

// extractAtMobiles 提取@的手机号
func (d *DingTalkChannel) extractAtMobiles(content string) []string {
    // 实现从内容中提取@手机号逻辑
    return nil
}

// getColorEmoji 获取颜色emoji
func (d *DingTalkChannel) getColorEmoji(color string) string {
    switch color {
    case "red", "critical":
        return "🔴"
    case "orange", "warning":
        return "🟠"
    case "yellow":
        return "🟡"
    case "green", "resolved":
        return "🟢"
    case "blue", "info":
        return "🔵"
    default:
        return "⚪"
    }
}
```

#### 4.3.2 飞书 (Feishu/Lark)

```go
// pkg/notification/channels/feishu.go

package channels

import (
    "bytes"
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "time"
)

// FeishuChannel 飞书渠道
type FeishuChannel struct {
    config      notification.ChannelConfig
    webhookURL  string
    appID       string
    appSecret   string
    accessToken string
    tokenExpiry time.Time
    httpClient  *http.Client
    callbackHandler notification.CallbackHandler
}

func (f *FeishuChannel) Name() string {
    return f.config.Name
}

func (f *FeishuChannel) Type() notification.ChannelType {
    return notification.ChannelTypeInstant
}

func (f *FeishuChannel) Capabilities() notification.ChannelCapabilities {
    return notification.ChannelCapabilities{
        SupportsRichText:    true,
        SupportsMarkdown:    true,
        SupportsCards:       true,
        SupportsImages:      true,
        SupportsAttachments: true,
        SupportsThreading:   true,
        SupportsCallback:    true,
        SupportsBatch:       true,
        MaxMessageSize:      65535,
        RateLimitPerSecond:  50,
        RateLimitPerMinute:  3000,
    }
}

func (f *FeishuChannel) Initialize(ctx context.Context, config notification.ChannelConfig) error {
    f.config = config
    f.webhookURL = config.Credentials["webhook_url"]
    f.appID = config.Credentials["app_id"]
    f.appSecret = config.Credentials["app_secret"]
    f.httpClient = &http.Client{Timeout: 30 * time.Second}
    return f.refreshAccessToken(ctx)
}

// 获取access token
func (f *FeishuChannel) refreshAccessToken(ctx context.Context) error {
    if time.Now().Before(f.tokenExpiry) {
        return nil
    }
    
    url := "https://open.feishu.cn/open-apis/auth/v3/app_access_token/internal"
    body, _ := json.Marshal(map[string]string{
        "app_id":     f.appID,
        "app_secret": f.appSecret,
    })
    
    req, _ := http.NewRequestWithContext(ctx, "POST", url, bytes.NewReader(body))
    req.Header.Set("Content-Type", "application/json")
    
    resp, err := f.httpClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    var result struct {
        Code              int    `json:"code"`
        Msg               string `json:"msg"`
        AppAccessToken    string `json:"app_access_token"`
        Expire            int    `json:"expire"`
    }
    
    if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
        return err
    }
    
    if result.Code != 0 {
        return fmt.Errorf("feishu auth error: %s", result.Msg)
    }
    
    f.accessToken = result.AppAccessToken
    f.tokenExpiry = time.Now().Add(time.Duration(result.Expire-300) * time.Second)
    
    return nil
}

func (f *FeishuChannel) Send(ctx context.Context, message *notification.Message) (*notification.SendResult, error) {
    if err := f.refreshAccessToken(ctx); err != nil {
        return nil, err
    }
    
    var payload map[string]interface{}
    
    // 根据消息内容选择消息类型
    switch {
    case len(message.Cards) > 0:
        payload = f.buildInteractiveCard(message)
    case message.Markdown != "":
        payload = f.buildMarkdownMessage(message)
    default:
        payload = f.buildTextMessage(message)
    }
    
    body, _ := json.Marshal(payload)
    
    req, _ := http.NewRequestWithContext(ctx, "POST", f.webhookURL, bytes.NewReader(body))
    req.Header.Set("Content-Type", "application/json")
    req.Header.Set("Authorization", "Bearer "+f.accessToken)
    
    resp, err := f.httpClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var result struct {
        Code int    `json:"code"`
        Msg  string `json:"msg"`
        Data struct {
            MessageID string `json:"message_id"`
        } `json:"data"`
    }
    
    json.NewDecoder(resp.Body).Decode(&result)
    
    if result.Code != 0 {
        return nil, fmt.Errorf("feishu send error: %s", result.Msg)
    }
    
    return &notification.SendResult{
        MessageID:   message.ID,
        ChannelName: f.Name(),
        Status:      notification.SendStatusSuccess,
        SentAt:      time.Now(),
        ExternalID:  result.Data.MessageID,
    }, nil
}

// buildInteractiveCard 构建飞书交互式卡片
func (f *FeishuChannel) buildInteractiveCard(message *notification.Message) map[string]interface{} {
    card := message.Cards[0]
    
    // 构建卡片元素
    elements := []map[string]interface{}{
        {
            "tag": "div",
            "text": map[string]interface{}{
                "tag":     "lark_md",
                "content": f.buildCardContent(card),
            },
        },
    }
    
    // 添加操作按钮
    if len(card.Actions) > 0 {
        actions := make([]map[string]interface{}, 0, len(card.Actions))
        for _, btn := range card.Actions {
            action := map[string]interface{}{
                "tag": "button",
                "text": map[string]string{
                    "tag":     "plain_text",
                    "content": btn.Text,
                },
                "type":  f.mapButtonStyle(btn.Style),
                "value": btn.Data,
            }
            
            // 如果有确认对话框
            if btn.Confirm != nil {
                action["confirm"] = map[string]interface{}{
                    "title": map[string]string{
                        "tag":     "plain_text",
                        "content": btn.Confirm.Title,
                    },
                    "text": map[string]string{
                        "tag":     "plain_text",
                        "content": btn.Confirm.Text,
                    },
                }
            }
            
            actions = append(actions, action)
        }
        
        elements = append(elements, map[string]interface{}{
            "tag":     "action",
            "actions": actions,
        })
    }
    
    return map[string]interface{}{
        "msg_type": "interactive",
        "card": map[string]interface{}{
            "config": map[string]interface{}{
                "wide_screen_mode": true,
            },
            "header": map[string]interface{}{
                "title": map[string]string{
                    "tag":     "plain_text",
                    "content": card.Title,
                },
                "template": f.mapColor(card.Color),
            },
            "elements": elements,
        },
    }
}

func (f *FeishuChannel) buildCardContent(card notification.Card) string {
    var content string
    for _, field := range card.Fields {
        content += fmt.Sprintf("**%s:** %s\n", field.Title, field.Value)
    }
    return content
}

func (f *FeishuChannel) mapColor(color string) string {
    switch color {
    case "red", "critical":
        return "red"
    case "orange", "warning":
        return "orange"
    case "yellow":
        return "yellow"
    case "green", "resolved":
        return "green"
    case "blue", "info":
        return "blue"
    default:
        return "grey"
    }
}

func (f *FeishuChannel) mapButtonStyle(style notification.ButtonStyle) string {
    switch style {
    case notification.ButtonStylePrimary:
        return "primary"
    case notification.ButtonStyleDanger:
        return "danger"
    default:
        return "default"
    }
}

// 其他方法实现...
func (f *FeishuChannel) HealthCheck(ctx context.Context) error { return nil }
func (f *FeishuChannel) Close() error { return nil }
func (f *FeishuChannel) SendBatch(ctx context.Context, messages []*notification.Message) ([]*notification.SendResult, error) {
    // 飞书支持批量发送
    results := make([]*notification.SendResult, len(messages))
    for i, msg := range messages {
        result, _ := f.Send(ctx, msg)
        results[i] = result
    }
    return results, nil
}
func (f *FeishuChannel) SetCallbackHandler(handler notification.CallbackHandler) error {
    f.callbackHandler = handler
    return nil
}
func (f *FeishuChannel) VerifySignature(payload []byte, signature string) bool { return true }
func (f *FeishuChannel) buildTextMessage(msg *notification.Message) map[string]interface{} {
    return map[string]interface{}{
        "msg_type": "text",
        "content": map[string]string{
            "text": msg.Content,
        },
    }
}
func (f *FeishuChannel) buildMarkdownMessage(msg *notification.Message) map[string]interface{} {
    return map[string]interface{}{
        "msg_type": "interactive",
        "card": map[string]interface{}{
            "elements": []map[string]interface{}{
                {
                    "tag": "div",
                    "text": map[string]interface{}{
                        "tag":     "lark_md",
                        "content": msg.Markdown,
                    },
                },
            },
        },
    }
}
```

#### 4.3.3 企业微信 (WeCom/WeChat Work)

```go
// pkg/notification/channels/wecom.go

package channels

import (
    "context"
    "encoding/json"
    "fmt"
    "net/http"
    "net/url"
    "time"
)

// WeComChannel 企业微信渠道
type WeComChannel struct {
    config      notification.ChannelConfig
    corpID      string
    agentID     string
    secret      string
    accessToken string
    tokenExpiry time.Time
    httpClient  *http.Client
}

func (w *WeComChannel) Name() string {
    return w.config.Name
}

func (w *WeComChannel) Type() notification.ChannelType {
    return notification.ChannelTypeInstant
}

func (w *WeComChannel) Capabilities() notification.ChannelCapabilities {
    return notification.ChannelCapabilities{
        SupportsRichText:    true,
        SupportsMarkdown:    true,
        SupportsCards:       true,
        SupportsImages:      true,
        SupportsAttachments: true,
        SupportsThreading:   false,
        SupportsCallback:    true,
        SupportsBatch:       true,
        MaxMessageSize:      2048,
        RateLimitPerSecond:  30,
        RateLimitPerMinute:  2000,
    }
}

func (w *WeComChannel) Initialize(ctx context.Context, config notification.ChannelConfig) error {
    w.config = config
    w.corpID = config.Credentials["corp_id"]
    w.agentID = config.Credentials["agent_id"]
    w.secret = config.Credentials["secret"]
    w.httpClient = &http.Client{Timeout: 30 * time.Second}
    return w.refreshAccessToken(ctx)
}

func (w *WeComChannel) refreshAccessToken(ctx context.Context) error {
    if time.Now().Before(w.tokenExpiry) {
        return nil
    }
    
    u := fmt.Sprintf("https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid=%s&corpsecret=%s",
        w.corpID, w.secret)
    
    resp, err := w.httpClient.Get(u)
    if err != nil {
        return err
    }
    defer resp.Body.Close()
    
    var result struct {
        ErrCode     int    `json:"errcode"`
        ErrMsg      string `json:"errmsg"`
        AccessToken string `json:"access_token"`
        ExpiresIn   int    `json:"expires_in"`
    }
    
    json.NewDecoder(resp.Body).Decode(&result)
    
    if result.ErrCode != 0 {
        return fmt.Errorf("wecom auth error: %s", result.ErrMsg)
    }
    
    w.accessToken = result.AccessToken
    w.tokenExpiry = time.Now().Add(time.Duration(result.ExpiresIn-300) * time.Second)
    return nil
}

func (w *WeComChannel) Send(ctx context.Context, message *notification.Message) (*notification.SendResult, error) {
    if err := w.refreshAccessToken(ctx); err != nil {
        return nil, err
    }
    
    var msgType string
    var content interface{}
    
    switch {
    case len(message.Cards) > 0:
        msgType = "template_card"
        content = w.buildTemplateCard(message.Cards[0])
    case message.Markdown != "":
        msgType = "markdown"
        content = map[string]string{"content": message.Markdown}
    default:
        msgType = "text"
        content = map[string]interface{}{
            "content":             message.Content,
            "mentioned_mobile_list": w.extractMentions(message.Content),
        }
    }
    
    payload := map[string]interface{}{
        "touser":  "@all",
        "msgtype": msgType,
        "agentid": w.agentID,
        msgType:   content,
    }
    
    body, _ := json.Marshal(payload)
    u := fmt.Sprintf("https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token=%s", w.accessToken)
    
    resp, err := w.httpClient.Post(u, "application/json", bytes.NewReader(body))
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var result struct {
        ErrCode int    `json:"errcode"`
        ErrMsg  string `json:"errmsg"`
        MsgID   string `json:"msgid"`
    }
    json.NewDecoder(resp.Body).Decode(&result)
    
    if result.ErrCode != 0 {
        return nil, fmt.Errorf("wecom send error: %s", result.ErrMsg)
    }
    
    return &notification.SendResult{
        MessageID:   message.ID,
        ChannelName: w.Name(),
        Status:      notification.SendStatusSuccess,
        SentAt:      time.Now(),
        ExternalID:  result.MsgID,
    }, nil
}

// buildTemplateCard 构建企业微信模板卡片
func (w *WeComChannel) buildTemplateCard(card notification.Card) map[string]interface{} {
    // 构建来源信息
    source := map[string]interface{}{
        "desc": "Ops Inspector",
    }
    
    // 构建主标题
    mainTitle := map[string]string{
        "title": card.Title,
    }
    
    // 构建跳转列表（操作按钮）
    var jumpList []map[string]string
    for _, btn := range card.Actions {
        jumpList = append(jumpList, map[string]string{
            "type":  "1", // URL跳转
            "url":   w.buildActionURL(btn),
            "title": btn.Text,
        })
    }
    
    // 构建关键数据（字段）
    var emphasisContent map[string]string
    var subTitleText string
    
    if len(card.Fields) > 0 {
        emphasisContent = map[string]string{
            "title": card.Fields[0].Title,
            "desc":  card.Fields[0].Value,
        }
    }
    
    if len(card.Fields) > 1 {
        for _, f := range card.Fields[1:] {
            subTitleText += fmt.Sprintf("%s: %s\n", f.Title, f.Value)
        }
    }
    
    // 构建卡片
    templateCard := map[string]interface{}{
        "card_type": "text_notice",
        "source":    source,
        "main_title": mainTitle,
    }
    
    if emphasisContent != nil {
        templateCard["emphasis_content"] = emphasisContent
    }
    
    if subTitleText != "" {
        templateCard["sub_title_text"] = subTitleText
    }
    
    if len(jumpList) > 0 {
        templateCard["jump_list"] = jumpList
        templateCard["card_action"] = map[string]string{
            "type": "1",
            "url":  jumpList[0]["url"],
        }
    }
    
    return templateCard
}

func (w *WeComChannel) buildActionURL(btn notification.Button) string {
    data := map[string]interface{}{
        "channel":   "wecom",
        "action":    btn.Action,
        "button_id": btn.ID,
        "data":      btn.Data,
    }
    
    jsonData, _ := json.Marshal(data)
    encoded := base64.URLEncoding.EncodeToString(jsonData)
    
    return fmt.Sprintf("%s/api/v1/callbacks/wecom?data=%s", 
        w.config.Settings["base_url"], encoded)
}

func (w *WeComChannel) extractMentions(content string) []string {
    // 提取@手机号
    return nil
}

// 其他方法实现...
func (w *WeComChannel) HealthCheck(ctx context.Context) error { return nil }
func (w *WeComChannel) Close() error { return nil }
func (w *WeComChannel) SendBatch(ctx context.Context, messages []*notification.Message) ([]*notification.SendResult, error) {
    // 企业微信支持批量发送
    results := make([]*notification.SendResult, len(messages))
    for i, msg := range messages {
        result, _ := w.Send(ctx, msg)
        results[i] = result
    }
    return results, nil
}
func (w *WeComChannel) SetCallbackHandler(handler notification.CallbackHandler) error { return nil }
func (w *WeComChannel) VerifySignature(payload []byte, signature string) bool { return true }
```

#### 4.3.4 其他渠道简要实现

```go
// pkg/notification/channels/slack.go
package channels

// SlackChannel Slack渠道
type SlackChannel struct {
    webhookURL string
    botToken   string
}

func (s *SlackChannel) Name() string { return "slack" }
func (s *SlackChannel) Type() notification.ChannelType { return notification.ChannelTypeInstant }
func (s *SlackChannel) Capabilities() notification.ChannelCapabilities {
    return notification.ChannelCapabilities{
        SupportsRichText:    true,
        SupportsMarkdown:    true,
        SupportsCards:       true, // Block Kit
        SupportsImages:      true,
        SupportsAttachments: true,
        SupportsThreading:   true,
        SupportsCallback:    true,
        SupportsBatch:       false,
        MaxMessageSize:      40000,
        RateLimitPerSecond:  50,
    }
}

// pkg/notification/channels/email.go
package channels

// EmailChannel 邮件渠道
type EmailChannel struct {
    smtpHost string
    smtpPort int
    username string
    password string
    from     string
}

func (e *EmailChannel) Name() string { return "email" }
func (e *EmailChannel) Type() notification.ChannelType { return notification.ChannelTypeEmail }
func (e *EmailChannel) Capabilities() notification.ChannelCapabilities {
    return notification.ChannelCapabilities{
        SupportsRichText:    true,
        SupportsMarkdown:    false,
        SupportsCards:       false,
        SupportsImages:      true,
        SupportsAttachments: true,
        SupportsThreading:   false,
        SupportsCallback:    false,
        SupportsBatch:       true,
        MaxMessageSize:      10485760, // 10MB
        RateLimitPerSecond:  10,
    }
}

// pkg/notification/channels/sms.go
package channels

// SMSChannel 短信渠道（支持多运营商）
type SMSChannel struct {
    provider string // aliyun/tencent/aws
    accessKey string
    secretKey string
    signName  string
    templateCode string
}

func (s *SMSChannel) Name() string { return "sms" }
func (s *SMSChannel) Type() notification.ChannelType { return notification.ChannelTypeSMS }
func (s *SMSChannel) Capabilities() notification.ChannelCapabilities {
    return notification.ChannelCapabilities{
        SupportsRichText:    false,
        SupportsMarkdown:    false,
        SupportsCards:       false,
        SupportsImages:      false,
        SupportsAttachments: false,
        SupportsThreading:   false,
        SupportsCallback:    false,
        SupportsBatch:       true,
        MaxMessageSize:      500, // 短信限制
        RateLimitPerSecond:  100,
    }
}

// pkg/notification/channels/phone.go
package channels

// PhoneChannel 电话渠道（语音通知）
type PhoneChannel struct {
    provider string // twilio/aliyun/yunpian
}

func (p *PhoneChannel) Name() string { return "phone" }
func (p *PhoneChannel) Type() notification.ChannelType { return notification.ChannelTypeVoice }
func (p *PhoneChannel) Capabilities() notification.ChannelCapabilities {
    return notification.ChannelCapabilities{
        SupportsRichText:    false,
        SupportsMarkdown:    false,
        SupportsCards:       false,
        SupportsImages:      false,
        SupportsAttachments: false,
        SupportsThreading:   false,
        SupportsCallback:    true, // 支持按键确认
        SupportsBatch:       false,
        MaxMessageSize:      0,
        RateLimitPerSecond:  5, // 电话限速更严格
    }
}

// pkg/notification/channels/webhook.go
package channels

// WebhookChannel 通用Webhook渠道
type WebhookChannel struct {
    url     string
    method  string
    headers map[string]string
    timeout time.Duration
}

func (w *WebhookChannel) Name() string { return "webhook" }
func (w *WebhookChannel) Type() notification.ChannelType { return notification.ChannelTypeWebhook }
func (w *WebhookChannel) Capabilities() notification.ChannelCapabilities {
    return notification.ChannelCapabilities{
        SupportsRichText:    true,
        SupportsMarkdown:    true,
        SupportsCards:       false,
        SupportsImages:      false,
        SupportsAttachments: false,
        SupportsThreading:   false,
        SupportsCallback:    true,
        SupportsBatch:       false,
        MaxMessageSize:      1048576,
        RateLimitPerSecond:  100,
    }
}
```

### 4.4 通知策略引擎

#### 4.4.1 策略配置模型

```yaml
# 通知策略配置示例
apiVersion: ops-inspector.io/v1
kind: NotificationPolicy
metadata:
  name: default-policy
  description: "默认通知策略"

spec:
  # 1. 分级通知策略
  severity_routing:
    - name: info
      match:
        severity: info
      channels:
        - channel: feishu
          target: "#ops-info"
          template: simple
          
    - name: warning
      match:
        severity: warning
      channels:
        - channel: dingtalk
          target: "#ops-alerts"
          template: standard
        - channel: email
          target: "ops-team@company.com"
          template: detailed
          
    - name: critical
      match:
        severity: critical
      channels:
        - channel: dingtalk
          target: "#ops-critical"
          template: detailed
          at: ["oncall-sre"]
        - channel: phone
          target: "${oncall.phone}"
          template: voice
          # 重要：立即电话通知
          
    - name: emergency
      match:
        severity: emergency
      channels:
        - channel: phone
          target: "${oncall.phone},${manager.phone}"
          template: emergency-voice
        - channel: sms
          target: "${oncall.phone}"
          template: emergency-sms
        - channel: dingtalk
          target: "#ops-emergency"
          template: emergency
          at: ["all"]

  # 2. 告警抑制策略
  inhibition:
    # 相同问题的抑制
    - name: duplicate-suppression
      condition: |
        alert.group == previous_alert.group &&
        alert.fingerprint == previous_alert.fingerprint
      duration: 5m
      action: suppress
      
    # 高频告警抑制
    - name: high-frequency-suppression
      condition: |
        count(alerts where fingerprint == alert.fingerprint and 
              timestamp > now() - 5m) >= 5
      duration: 30m
      action: throttle
      notify: summary  # 只发送汇总
      
    # 级联抑制（上游故障抑制下游告警）
    - name: cascade-inhibition
      rules:
        - source:
            alertname: "NodeDown"
          target:
            - alertname: "PodUnhealthy"
              node: "${source.node}"
            - alertname: "DiskFull"
              node: "${source.node}"

  # 3. 告警升级策略
  escalation:
    - name: auto-escalation
      trigger:
        condition: alert.status == "fired"
        duration: 15m
      steps:
        - after: 0m
          channels:
            - channel: dingtalk
              target: "#ops-alerts"
              
        - after: 15m
          if: alert.status == "fired"
          channels:
            - channel: phone
              target: "${oncall.phone}"
              
        - after: 30m
          if: alert.status == "fired"
          channels:
            - channel: phone
              target: "${manager.phone}"
            - channel: dingtalk
              target: "#ops-management"
              at: ["director"]
              
        - after: 60m
          if: alert.status == "fired"
          action: create_incident
          channels:
            - channel: phone
              target: "${director.phone}"

  # 4. 告警收敛策略
  aggregation:
    # 按标签分组
    - name: group-by-service
      group_by:
        - namespace
        - service
      wait: 30s
      max_wait: 2m
      notification:
        template: group-summary
        channels:
          - channel: dingtalk
            target: "#ops-alerts"
            
    # 时间窗口收敛
    - name: time-window-aggregation
      window: 5m
      max_alerts: 10
      notification:
        template: window-summary
        
  # 5. 时间路由策略
  time_based_routing:
    - name: work-hours
      time_range:
        - days: [mon,tue,wed,thu,fri]
          hours: "09:00-18:00"
      channels:
        - channel: dingtalk
          target: "#ops-workhours"
          
    - name: off-hours
      time_range:
        - days: [mon,tue,wed,thu,fri]
          hours: "18:00-09:00"
        - days: [sat,sun]
          hours: "00:00-23:59"
      channels:
        - channel: phone
          target: "${oncall.phone}"
        - channel: dingtalk
          target: "#ops-oncall"
          
  # 6. 值班表路由
  oncall_routing:
    - name: primary-oncall
      schedule: "ops-oncall-primary"
      channels:
        - channel: phone
          target: "${schedule.user.phone}"
        - channel: dingtalk
          target: "${schedule.user.dingtalk}"
          
    - name: secondary-oncall
      schedule: "ops-oncall-secondary"
      delay: 5m  # 5分钟后通知二线
      condition: alert.status == "fired"
```

#### 4.4.2 策略引擎实现

```go
// pkg/notification/policy/engine.go

package policy

import (
    "context"
    "fmt"
    "sync"
    "time"
)

// Engine 通知策略引擎
type Engine struct {
    policies      []NotificationPolicy
    inhibitions   []InhibitionRule
    escalations   []EscalationPolicy
    aggregations  []AggregationRule
    
    // 状态管理
    alertHistory  *AlertHistory
    activeAlerts  map[string]*ActiveAlert
    mu            sync.RWMutex
    
    // 依赖
    channelManager *notification.ChannelManager
    router         *Router
    
    // 控制
    ctx    context.Context
    cancel context.CancelFunc
}

// ActiveAlert 活跃告警状态
type ActiveAlert struct {
    Alert        *Alert
    FirstFired   time.Time
    LastFired    time.Time
    Status       AlertStatus
    EscalationLevel int
    NotifiedChannels map[string]time.Time
    Suppressed   bool
}

// NewEngine 创建策略引擎
func NewEngine(cm *notification.ChannelManager) *Engine {
    ctx, cancel := context.WithCancel(context.Background())
    
    return &Engine{
        activeAlerts:   make(map[string]*ActiveAlert),
        alertHistory:   NewAlertHistory(24 * time.Hour),
        channelManager: cm,
        router:         NewRouter(cm),
        ctx:            ctx,
        cancel:         cancel,
    }
}

// LoadPolicy 加载通知策略
func (e *Engine) LoadPolicy(policy NotificationPolicy) error {
    e.mu.Lock()
    defer e.mu.Unlock()
    
    e.policies = append(e.policies, policy)
    e.inhibitions = append(e.inhibitions, policy.InhibitionRules...)
    e.escalations = append(e.escalations, policy.EscalationPolicies...)
    e.aggregations = append(e.aggregations, policy.AggregationRules...)
    
    return nil
}

// ProcessAlert 处理告警
func (e *Engine) ProcessAlert(ctx context.Context, alert *Alert) error {
    // 1. 检查抑制规则
    if e.isInhibited(alert) {
        return nil
    }
    
    // 2. 检查高频抑制
    if e.isHighFrequency(alert) {
        return e.sendThrottledNotification(ctx, alert)
    }
    
    // 3. 更新活跃告警
    active := e.updateActiveAlert(alert)
    
    // 4. 应用聚合规则
    if aggregated := e.checkAggregation(alert); aggregated != nil {
        return e.sendAggregatedNotification(ctx, aggregated)
    }
    
    // 5. 路由到渠道
    routes := e.router.CalculateRoutes(alert, e.policies)
    
    // 6. 发送通知
    for _, route := range routes {
        if err := e.sendNotification(ctx, alert, route); err != nil {
            // 记录错误但继续
            continue
        }
        active.NotifiedChannels[route.Channel] = time.Now()
    }
    
    // 7. 启动升级监控
    e.startEscalationMonitor(active)
    
    return nil
}

// isInhibited 检查是否被抑制
func (e *Engine) isInhibited(alert *Alert) bool {
    e.mu.RLock()
    defer e.mu.RUnlock()
    
    for _, rule := range e.inhibitions {
        if rule.Matches(alert, e.activeAlerts) {
            return true
        }
    }
    return false
}

// isHighFrequency 检查是否高频告警
func (e *Engine) isHighFrequency(alert *Alert) bool {
    count := e.alertHistory.Count(alert.Fingerprint, 5*time.Minute)
    return count >= 5
}

// checkAggregation 检查聚合
func (e *Engine) checkAggregation(alert *Alert) *AggregatedAlert {
    e.mu.RLock()
    defer e.mu.RUnlock()
    
    for _, rule := range e.aggregations {
        if group := rule.TryAdd(alert); group != nil {
            return group
        }
    }
    return nil
}

// sendNotification 发送通知
func (e *Engine) sendNotification(ctx context.Context, alert *Alert, route Route) error {
    // 构建消息
    message := e.buildMessage(alert, route)
    
    // 获取渠道
    channel, err := e.channelManager.GetChannel(route.Channel)
    if err != nil {
        return err
    }
    
    // 发送
    result, err := channel.Send(ctx, message)
    if err != nil {
        return err
    }
    
    // 记录发送历史
    e.recordNotification(alert, route, result)
    
    return nil
}

// buildMessage 构建通知消息
func (e *Engine) buildMessage(alert *Alert, route Route) *notification.Message {
    msg := &notification.Message{
        ID:       generateID(),
        Type:     notification.MessageTypeAlert,
        Priority: mapSeverityToPriority(alert.Severity),
        Title:    alert.Title,
        Content:  alert.Summary,
        Context: map[string]interface{}{
            "alert_id":    alert.ID,
            "fingerprint": alert.Fingerprint,
            "severity":    alert.Severity,
            "source":      alert.Source,
        },
        Labels: alert.Labels,
    }
    
    // 根据模板构建富媒体内容
    switch route.Template {
    case "simple":
        msg.Content = fmt.Sprintf("[%s] %s", alert.Severity, alert.Title)
        
    case "standard":
        msg.Markdown = e.buildStandardMarkdown(alert)
        
    case "detailed":
        msg.Markdown = e.buildDetailedMarkdown(alert)
        msg.Cards = []notification.Card{e.buildAlertCard(alert)}
        
    case "group-summary":
        msg = e.buildGroupSummaryMessage(alert)
    }
    
    return msg
}

// buildAlertCard 构建告警卡片
func (e *Engine) buildAlertCard(alert *Alert) notification.Card {
    color := mapSeverityToColor(alert.Severity)
    
    fields := []notification.CardField{
        {Title: "告警级别", Value: alert.Severity, Short: true},
        {Title: "告警来源", Value: alert.Source, Short: true},
        {Title: "触发时间", Value: alert.FiredAt.Format("2006-01-02 15:04:05"), Short: true},
        {Title: "持续时间", Value: formatDuration(time.Since(alert.FiredAt)), Short: true},
    }
    
    if alert.Node != "" {
        fields = append(fields, notification.CardField{
            Title: "节点", Value: alert.Node, Short: true,
        })
    }
    
    if alert.Service != "" {
        fields = append(fields, notification.CardField{
            Title: "服务", Value: alert.Service, Short: true,
        })
    }
    
    // 添加详情
    fields = append(fields, notification.CardField{
        Title: "详情", Value: alert.Description, Short: false,
    })
    
    // 操作按钮
    buttons := []notification.Button{
        {
            ID:     "acknowledge",
            Type:   notification.ButtonTypeAction,
            Text:   "确认告警",
            Style:  notification.ButtonStylePrimary,
            Action: "acknowledge_alert",
            Data: map[string]interface{}{
                "alert_id": alert.ID,
            },
        },
        {
            ID:     "view_dashboard",
            Type:   notification.ButtonTypeLink,
            Text:   "查看监控",
            Style:  notification.ButtonStyleDefault,
            URL:    alert.DashboardURL,
        },
    }
    
    // 如果有自动修复SOP，添加执行按钮
    if alert.AutoHealSOP != "" {
        buttons = append(buttons, notification.Button{
            ID:     "auto_heal",
            Type:   notification.ButtonTypeAction,
            Text:   "执行修复",
            Style:  notification.ButtonStyleDanger,
            Action: "execute_sop",
            Data: map[string]interface{}{
                "sop_id": alert.AutoHealSOP,
                "alert_id": alert.ID,
            },
            Confirm: &notification.ConfirmDialog{
                Title:       "确认执行自动修复",
                Text:        "将执行自动修复SOP，是否确认？",
                ConfirmText: "确认执行",
                CancelText:  "取消",
            },
        })
    }
    
    return notification.Card{
        Type:      string(alert.Severity),
        Title:     alert.Title,
        Color:     color,
        Fields:    fields,
        Actions:   buttons,
        Footer:    fmt.Sprintf("Ops Inspector • %s", time.Now().Format("15:04:05")),
        Timestamp: time.Now(),
    }
}

// startEscalationMonitor 启动升级监控
func (e *Engine) startEscalationMonitor(active *ActiveAlert) {
    go func() {
        ticker := time.NewTicker(1 * time.Minute)
        defer ticker.Stop()
        
        for {
            select {
            case <-e.ctx.Done():
                return
            case <-ticker.C:
                if active.Status == AlertStatusResolved {
                    return
                }
                
                e.checkEscalation(active)
            }
        }
    }()
}

// checkEscalation 检查是否需要升级
func (e *Engine) checkEscalation(active *ActiveAlert) {
    duration := time.Since(active.FirstFired)
    
    for _, policy := range e.escalations {
        for _, step := range policy.Steps {
            if duration >= step.After && active.EscalationLevel < step.Level {
                // 执行升级
                e.executeEscalation(active, step)
                active.EscalationLevel = step.Level
            }
        }
    }
}

// executeEscalation 执行升级
func (e *Engine) executeEscalation(active *ActiveAlert, step EscalationStep) {
    ctx := context.Background()
    
    for _, channelSpec := range step.Channels {
        route := Route{
            Channel:  channelSpec.Channel,
            Target:   channelSpec.Target,
            Template: channelSpec.Template,
        }
        
        e.sendNotification(ctx, active.Alert, route)
    }
}

// HandleCallback 处理回调
func (e *Engine) HandleCallback(ctx context.Context, callback *notification.Callback) (*notification.CallbackResponse, error) {
    switch callback.Action {
    case "acknowledge_alert":
        return e.handleAcknowledge(ctx, callback)
        
    case "execute_sop":
        return e.handleExecuteSOP(ctx, callback)
        
    case "silence_alert":
        return e.handleSilence(ctx, callback)
        
    default:
        return nil, fmt.Errorf("unknown action: %s", callback.Action)
    }
}

// handleAcknowledge 处理确认告警
func (e *Engine) handleAcknowledge(ctx context.Context, callback *notification.Callback) (*notification.CallbackResponse, error) {
    alertID := callback.Data["alert_id"].(string)
    
    // 更新告警状态
    if err := e.acknowledgeAlert(alertID, callback.UserName); err != nil {
        return nil, err
    }
    
    // 更新原消息
    return &notification.CallbackResponse{
        Message: "✅ 告警已确认",
        UpdateMessage: &notification.Message{
            Type: notification.MessageTypeInteractive,
            Content: fmt.Sprintf("告警已由 %s 于 %s 确认", 
                callback.UserName, 
                time.Now().Format("15:04:05")),
        },
    }, nil
}

// handleExecuteSOP 处理执行SOP
func (e *Engine) handleExecuteSOP(ctx context.Context, callback *notification.Callback) (*notification.CallbackResponse, error) {
    sopID := callback.Data["sop_id"].(string)
    alertID := callback.Data["alert_id"].(string)
    
    // 执行SOP
    executionID, err := e.sopEngine.Execute(ctx, sopID, map[string]interface{}{
        "alert_id": alertID,
        "triggered_by": callback.UserName,
    })
    if err != nil {
        return nil, err
    }
    
    return &notification.CallbackResponse{
        Message: fmt.Sprintf("🚀 修复SOP已启动，执行ID: %s", executionID),
    }, nil
}
```

### 4.5 双向交互设计

```go
// pkg/notification/interactive/handler.go

package interactive

import (
    "context"
    "encoding/json"
    "net/http"
)

// CallbackServer 回调服务器
type CallbackServer struct {
    engine     *policy.Engine
    handlers   map[string]ChannelCallbackHandler
    httpServer *http.Server
}

// ChannelCallbackHandler 渠道回调处理器
type ChannelCallbackHandler interface {
    ParseCallback(r *http.Request) (*notification.Callback, error)
    SendResponse(w http.ResponseWriter, response *notification.CallbackResponse)
}

// NewCallbackServer 创建回调服务器
func NewCallbackServer(engine *policy.Engine) *CallbackServer {
    cs := &CallbackServer{
        engine:   engine,
        handlers: make(map[string]ChannelCallbackHandler),
    }
    
    // 注册各渠道处理器
    cs.handlers["dingtalk"] = &DingTalkCallbackHandler{}
    cs.handlers["feishu"] = &FeishuCallbackHandler{}
    cs.handlers["wecom"] = &WeComCallbackHandler{}
    cs.handlers["slack"] = &SlackCallbackHandler{}
    
    return cs
}

// Start 启动回调服务器
func (cs *CallbackServer) Start(addr string) error {
    mux := http.NewServeMux()
    mux.HandleFunc("/api/v1/callbacks/", cs.handleCallback)
    
    cs.httpServer = &http.Server{
        Addr:    addr,
        Handler: mux,
    }
    
    return cs.httpServer.ListenAndServe()
}

// handleCallback 处理回调请求
func (cs *CallbackServer) handleCallback(w http.ResponseWriter, r *http.Request) {
    // 从URL提取渠道名称
    channel := extractChannelFromPath(r.URL.Path)
    
    handler, ok := cs.handlers[channel]
    if !ok {
        http.Error(w, "Unknown channel", http.StatusBadRequest)
        return
    }
    
    // 解析回调
    callback, err := handler.ParseCallback(r)
    if err != nil {
        http.Error(w, err.Error(), http.StatusBadRequest)
        return
    }
    
    // 处理回调
    response, err := cs.engine.HandleCallback(r.Context(), callback)
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }
    
    // 返回响应
    handler.SendResponse(w, response)
}

// DingTalkCallbackHandler 钉钉回调处理器
type DingTalkCallbackHandler struct{}

func (h *DingTalkCallbackHandler) ParseCallback(r *http.Request) (*notification.Callback, error) {
    // 解析钉钉回调数据
    var payload struct {
        ChatbotCorpId string `json:"chatbotCorpId"`
        ChatbotUserId string `json:"chatbotUserId"`
        Msg           struct {
            Content string `json:"content"`
        } `json:"msg"`
        SenderStaffId string `json:"senderStaffId"`
        SenderNick    string `json:"senderNick"`
    }
    
    if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
        return nil, err
    }
    
    // 从content解析操作
    // 钉钉通过URL参数传递操作信息
    actionData := r.URL.Query().Get("data")
    
    return &notification.Callback{
        Channel:   "dingtalk",
        UserID:    payload.SenderStaffId,
        UserName:  payload.SenderNick,
        RawPayload: mustMarshal(payload),
    }, nil
}

func (h *DingTalkCallbackHandler) SendResponse(w http.ResponseWriter, response *notification.CallbackResponse) {
    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(map[string]interface{}{
        "msgtype": "text",
        "text": map[string]string{
            "content": response.Message,
        },
    })
}

// FeishuCallbackHandler 飞书回调处理器
type FeishuCallbackHandler struct{}

func (h *FeishuCallbackHandler) ParseCallback(r *http.Request) (*notification.Callback, error) {
    // 飞书使用事件推送机制
    var payload struct {
        Challenge string `json:"challenge"` // 验证URL时使用
        Token     string `json:"token"`
        Type      string `json:"type"`      // url_verification/event_callback
        Event     struct {
            Type       string `json:"type"`
            OpenID     string `json:"open_id"`
            UserName   string `json:"user_name"`
            MessageID  string `json:"message_id"`
            Action     struct {
                Value map[string]interface{} `json:"value"`
                Tag   string                 `json:"tag"`
            } `json:"action"`
        } `json:"event"`
    }
    
    if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
        return nil, err
    }
    
    // URL验证
    if payload.Type == "url_verification" {
        return nil, nil
    }
    
    return &notification.Callback{
        Channel:   "feishu",
        MessageID: payload.Event.MessageID,
        UserID:    payload.Event.OpenID,
        UserName:  payload.Event.UserName,
        Action:    payload.Event.Action.Value["action"].(string),
        Data:      payload.Event.Action.Value,
        RawPayload: mustMarshal(payload),
    }, nil
}

func (h *FeishuCallbackHandler) SendResponse(w http.ResponseWriter, response *notification.CallbackResponse) {
    w.Header().Set("Content-Type", "application/json")
    
    if response.UpdateMessage != nil {
        // 飞书支持更新原消息
        json.NewEncoder(w).Encode(map[string]interface{}{
            "code": 0,
            "data": map[string]interface{}{
                "toast": map[string]string{
                    "type":    "success",
                    "content": response.Message,
                },
            },
        })
    } else {
        json.NewEncoder(w).Encode(map[string]interface{}{
            "code": 0,
        })
    }
}
```

### 4.6 路由引擎

```go
// pkg/notification/router.go

package notification

import (
    "context"
    "fmt"
    "time"
)

// Router 通知路由器
type Router struct {
    channelManager *ChannelManager
    oncallService  *OncallService
    templateEngine *TemplateEngine
}

// Route 路由结果
type Route struct {
    Channel      string
    Target       string
    Template     string
    At           []string
    Transformers []MessageTransformer
}

// CalculateRoutes 计算告警的路由
func (r *Router) CalculateRoutes(alert *Alert, policies []NotificationPolicy) []Route {
    var routes []Route
    
    for _, policy := range policies {
        // 检查策略匹配
        if !r.matchesPolicy(alert, policy) {
            continue
        }
        
        // 获取时间路由
        timeRoutes := r.calculateTimeRoutes(alert, policy.TimeBasedRouting)
        routes = append(routes, timeRoutes...)
        
        // 获取值班路由
        oncallRoutes := r.calculateOncallRoutes(alert, policy.OncallRouting)
        routes = append(routes, oncallRoutes...)
        
        // 获取严重级别路由
        severityRoutes := r.calculateSeverityRoutes(alert, policy.SeverityRouting)
        routes = append(routes, severityRoutes...)
    }
    
    // 去重
    return r.deduplicateRoutes(routes)
}

// calculateSeverityRoutes 计算严重级别路由
func (r *Router) calculateSeverityRoutes(alert *Alert, rules []SeverityRoute) []Route {
    var routes []Route
    
    for _, rule := range rules {
        if rule.Match.Severity != string(alert.Severity) {
            continue
        }
        
        for _, channel := range rule.Channels {
            target := r.resolveTarget(channel.Target, alert)
            
            route := Route{
                Channel:  channel.Channel,
                Target:   target,
                Template: channel.Template,
                At:       channel.At,
            }
            
            // 添加转换器
            route.Transformers = r.getTransformers(channel.Channel)
            
            routes = append(routes, route)
        }
    }
    
    return routes
}

// calculateTimeRoutes 计算时间路由
func (r *Router) calculateTimeRoutes(alert *Alert, rules []TimeBasedRoute) []Route {
    var routes []Route
    now := time.Now()
    
    for _, rule := range rules {
        if !r.isInTimeRange(now, rule.TimeRange) {
            continue
        }
        
        for _, channel := range rule.Channels {
            routes = append(routes, Route{
                Channel:  channel.Channel,
                Target:   r.resolveTarget(channel.Target, alert),
                Template: channel.Template,
            })
        }
    }
    
    return routes
}

// calculateOncallRoutes 计算值班路由
func (r *Router) calculateOncallRoutes(alert *Alert, rules []OncallRoute) []Route {
    var routes []Route
    
    for _, rule := range rules {
        // 获取当前值班人
        oncall, err := r.oncallService.GetCurrentOncall(rule.Schedule)
        if err != nil {
            continue
        }
        
        // 检查是否需要延迟通知
        if rule.Delay > 0 {
            go r.scheduleDelayedNotification(alert, rule, oncall, rule.Delay)
            continue
        }
        
        for _, channel := range rule.Channels {
            target := r.resolveTargetWithOncall(channel.Target, oncall)
            
            routes = append(routes, Route{
                Channel:  channel.Channel,
                Target:   target,
                Template: channel.Template,
            })
        }
    }
    
    return routes
}

// resolveTarget 解析目标地址（支持变量替换）
func (r *Router) resolveTarget(template string, alert *Alert) string {
    // 简单的变量替换
    // 支持 ${alert.labels.xxx}, ${alert.annotations.xxx}
    return r.templateEngine.Render(template, map[string]interface{}{
        "alert": alert,
    })
}

// resolveTargetWithOncall 解析值班人目标
func (r *Router) resolveTargetWithOncall(template string, oncall *OncallUser) string {
    return r.templateEngine.Render(template, map[string]interface{}{
        "oncall": oncall,
        "schedule": map[string]string{
            "user.phone":    oncall.Phone,
            "user.email":    oncall.Email,
            "user.dingtalk": oncall.DingTalkID,
            "user.feishu":   oncall.FeishuID,
        },
    })
}

// getTransformers 获取消息转换器
func (r *Router) getTransformers(channelName string) []MessageTransformer {
    channel, err := r.channelManager.GetChannel(channelName)
    if err != nil {
        return nil
    }
    
    caps := channel.Capabilities()
    var transformers []MessageTransformer
    
    // 根据渠道能力添加转换器
    if !caps.SupportsMarkdown {
        transformers = append(transformers, MarkdownToTextTransformer{})
    }
    
    if caps.MaxMessageSize > 0 {
        transformers = append(transformers, TruncateTransformer{MaxSize: caps.MaxMessageSize})
    }
    
    return transformers
}

// deduplicateRoutes 路由去重
func (r *Router) deduplicateRoutes(routes []Route) []Route {
    seen := make(map[string]bool)
    var unique []Route
    
    for _, route := range routes {
        key := fmt.Sprintf("%s:%s", route.Channel, route.Target)
        if !seen[key] {
            seen[key] = true
            unique = append(unique, route)
        }
    }
    
    return unique
}

// isInTimeRange 检查是否在时间范围内
func (r *Router) isInTimeRange(t time.Time, ranges []TimeRange) bool {
    weekday := t.Weekday().String()[:3]
    currentTime := t.Format("15:04")
    
    for _, tr := range ranges {
        // 检查星期
        dayMatch := false
        for _, day := range tr.Days {
            if day == weekday {
                dayMatch = true
                break
            }
        }
        if !dayMatch {
            continue
        }
        
        // 检查时间
        if currentTime >= tr.StartTime && currentTime <= tr.EndTime {
            return true
        }
    }
    
    return false
}
```

### 4.7 模板系统

```yaml
# 通知模板配置
apiVersion: ops-inspector.io/v1
kind: NotificationTemplate
metadata:
  name: alert-templates

spec:
  templates:
    # 简单文本模板
    - name: simple
      format: text
      content: |
        [{{.Severity}}] {{.Title}}
        
    # 标准Markdown模板
    - name: standard
      format: markdown
      content: |
        ## 🚨 {{.Title}}
        
        **告警级别:** {{.Severity}}
        **告警来源:** {{.Source}}
        **触发时间:** {{.FiredAt.Format "2006-01-02 15:04:05"}}
        
        ### 详情
        {{.Description}}
        
        [查看监控]({{.DashboardURL}})
        
    # 详细模板
    - name: detailed
      format: markdown
      content: |
        ## {{getEmoji .Severity}} {{.Title}}
        
        | 属性 | 值 |
        |------|-----|
        | 告警级别 | {{.Severity}} |
        | 告警来源 | {{.Source}} |
        | 命名空间 | {{.Labels.namespace}} |
        | 服务 | {{.Labels.service}} |
        | Pod | {{.Labels.pod}} |
        | 节点 | {{.Labels.node}} |
        | 触发时间 | {{.FiredAt.Format "2006-01-02 15:04:05"}} |
        | 持续时间 | {{duration .FiredAt}} |
        
        ### 详情
        {{.Description}}
        
        ### 标签
        {{range $k, $v := .Labels}}
        - {{$k}}: {{$v}}
        {{end}}
        
        ---
        [查看监控]({{.DashboardURL}}) | [查看日志]({{.LogsURL}}) | [执行SOP]({{.SOPURL}})
        
    # 分组汇总模板
    - name: group-summary
      format: markdown
      content: |
        ## 📊 告警汇总 ({{.AlertCount}}条)
        
        | 级别 | 数量 |
        |------|------|
        {{range .SeverityCount}}| {{.Severity}} | {{.Count}} |
        {{end}}
        
        ### 最新告警
        {{range .LatestAlerts}}
        - [{{.Severity}}] {{.Title}}
        {{end}}
        
    # 语音电话模板（短文本）
    - name: voice
      format: text
      max_length: 200
      content: |
        Ops Inspector告警。{{.Title}}。严重程度{{.Severity}}。请尽快处理。
        
    # 短信模板
    - name: sms
      format: text
      max_length: 140
      content: |
        【Ops】{{.Severity}}告警:{{.Title}}。{{.FiredAt.Format "15:04"}}
```

---

## 5. SOP引擎设计

### 4.1 设计原则

SOP（Standard Operating Procedure，标准作业程序）引擎是本系统的核心差异化能力，设计遵循以下原则：

1. **声明式定义:** 使用YAML声明式定义SOP流程
2. **可视化编排:** 支持Web UI可视化编排
3. **状态持久化:** 执行状态持久化，支持断点续传
4. **人工介入:** 支持人工确认节点，实现人机协同
5. **审计追踪:** 完整记录执行轨迹，支持回溯和复盘

### 4.2 SOP定义语言 (SOP DSL)

#### 4.2.1 YAML Schema

```yaml
# SOP定义文件示例
apiVersion: ops-inspector.io/v1
kind: SOP
metadata:
  name: pod-restart-sop
  version: "1.0.0"
  category: kubernetes
  description: "Pod异常自动重启SOP"
  labels:
    severity: critical
    team: platform

# 触发条件
triggers:
  - type: event
    source: kubernetes
    event: PodCrashLooping
    filters:
      - field: namespace
        operator: notIn
        value: ["kube-system", "monitoring"]
  - type: schedule
    cron: "0 */4 * * *"  # 每4小时检查一次

# 输入参数
inputs:
  - name: namespace
    type: string
    required: true
    description: "Pod所在命名空间"
  - name: pod_name
    type: string
    required: true
    description: "Pod名称"
  - name: max_retries
    type: integer
    default: 3
    description: "最大重试次数"

# 变量定义
variables:
  - name: restart_count
    default: 0
  - name: original_replicas
    default: 0

# 执行流程
workflow:
  # 步骤1: 前置检查
  - id: pre-check
    name: "前置检查"
    type: check
    action:
      skill: k8s-pod-describe
      inputs:
        namespace: "${inputs.namespace}"
        pod_name: "${inputs.pod_name}"
    outputs:
      - name: pod_status
        from: status
      - name: restart_count
        from: restart_count
    
  # 步骤2: 决策分支
  - id: decision
    name: "决策分支"
    type: switch
    condition: "${steps.pre-check.outputs.restart_count}"
    cases:
      - when: "> 5"
        then: escalate
      - when: "> 3"
        then: approval-check
      - default: direct-restart
  
  # 步骤3: 人工确认（条件分支）
  - id: approval-check
    name: "人工确认"
    type: approval
    timeout: "10m"
    approvers:
      - group: oncall-platform
      - user: admin@company.com
    message: |
      Pod ${inputs.pod_name} 重启次数过多(${steps.pre-check.outputs.restart_count})，
      是否确认执行重启操作？
    on_timeout: escalate
    on_reject: abort
    
  # 步骤4: 直接重启
  - id: direct-restart
    name: "执行Pod重启"
    type: action
    action:
      skill: k8s-pod-delete
      inputs:
        namespace: "${inputs.namespace}"
        pod_name: "${inputs.pod_name}"
        grace_period: 30
    retry:
      max_attempts: 3
      backoff: exponential
      initial_delay: 5s
    
  # 步骤5: 等待恢复
  - id: wait-recovery
    name: "等待Pod恢复"
    type: wait
    condition:
      skill: k8s-pod-status
      inputs:
        namespace: "${inputs.namespace}"
        pod_name: "${inputs.pod_name}"
      expected: "Running"
    timeout: "5m"
    on_timeout: escalate
    
  # 步骤6: 健康检查
  - id: health-check
    name: "健康检查"
    type: check
    depends_on: [direct-restart, wait-recovery]
    action:
      skill: http-health-check
      inputs:
        endpoint: "http://${inputs.pod_name}.${inputs.namespace}.svc/health"
        timeout: 30s
    
  # 步骤7: 失败升级
  - id: escalate
    name: "升级处理"
    type: notification
    action:
      skill: notify-pagerduty
      inputs:
        severity: critical
        summary: "Pod ${inputs.pod_name} 自动修复失败，需要人工介入"
        details:
          namespace: "${inputs.namespace}"
          restart_count: "${steps.pre-check.outputs.restart_count}"
    final: true
    
  # 步骤8: 成功通知
  - id: notify-success
    name: "通知成功"
    type: notification
    action:
      skill: notify-slack
      inputs:
        channel: "#alerts"
        message: "✅ Pod ${inputs.pod_name} 自动重启成功"
    final: true

# 异常处理
error_handling:
  - on: any_error
    action: notify
    target: oncall-platform
  - on: timeout
    action: escalate
    target: senior-sre

# 审计配置
audit:
  level: detailed  # summary/normal/detailed
  retention: 90d
```

#### 4.2.2 Step类型定义

```yaml
# 1. 动作步骤 (action) - 执行具体的Skill
step:
  id: step-id
  name: "步骤名称"
  type: action
  action:
    skill: skill-name
    inputs: {}
  retry: {}
  timeout: "5m"
  on_error: continue|retry|abort|escalate

# 2. 检查步骤 (check) - 执行检查并捕获输出
step:
  id: step-id
  name: "检查步骤"
  type: check
  action:
    skill: checker-skill
  outputs: []

# 3. 条件步骤 (condition) - 基于条件执行不同分支
step:
  id: step-id
  name: "条件判断"
  type: condition
  condition: "${var} > 10"
  then: next-step-id
  else: another-step-id

# 4. 分支步骤 (switch) - 多分支选择
step:
  id: step-id
  name: "多分支选择"
  type: switch
  condition: "${var}"
  cases:
    - when: "value1"
      then: step-1
    - when: "value2"
      then: step-2
    - default: step-3

# 5. 并行步骤 (parallel) - 并行执行多个子步骤
step:
  id: step-id
  name: "并行执行"
  type: parallel
  steps:
    - id: sub-1
      action: {}
    - id: sub-2
      action: {}
  aggregation: all|any  # 全部完成|任一完成

# 6. 循环步骤 (loop) - 迭代执行
step:
  id: step-id
  name: "循环执行"
  type: loop
  items: "${array_var}"
  item_name: item
  step:
    action: {}

# 7. 等待步骤 (wait) - 等待条件满足或时间
step:
  id: step-id
  name: "等待"
  type: wait
  duration: "5m"  # 或
  condition:
    skill: check-condition
    expected: true
  timeout: "10m"

# 8. 人工确认步骤 (approval) - 等待人工审批
step:
  id: step-id
  name: "人工确认"
  type: approval
  approvers:
    - group: team-platform
    - user: admin@example.com
  timeout: "30m"
  on_timeout: escalate
  on_reject: abort

# 9. 通知步骤 (notification) - 发送通知
step:
  id: step-id
  name: "发送通知"
  type: notification
  action:
    skill: notify-slack
    inputs: {}

# 10. 子流程步骤 (subflow) - 调用其他SOP
step:
  id: step-id
  name: "调用子流程"
  type: subflow
  sop: another-sop-name
  inputs: {}
  outputs:
    - name: result
      from: output.result
```

### 4.3 SOP执行引擎架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SOP Engine 架构                                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                           API Layer                                          │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Create SOP   │  │ Update SOP   │  │ Delete SOP   │  │ Execute SOP  │     │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘     │
└─────────┼─────────────────┼─────────────────┼─────────────────┼─────────────┘
          │                 │                 │                 │
          └─────────────────┴─────────────────┴─────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Parser & Validator                                      │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │  YAML Parser     │  │  Schema Validate │  │  Dependency Check│          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Workflow Builder                                        │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │  AST Builder     │  │  DAG Builder     │  │  Step Linker     │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Execution Engine                                        │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      State Machine                                   │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐       │  │
│  │  │ Pending  │───▶│ Running  │───▶│ Waiting  │───▶│Completed │       │  │
│  │  └──────────┘    └────┬─────┘    └────┬─────┘    └──────────┘       │  │
│  │       │               │               │                             │  │
│  │       ▼               ▼               ▼                             │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                       │  │
│  │  │ Failed   │    │ Retry    │    │ Approved │                       │  │
│  │  └──────────┘    └──────────┘    └──────────┘                       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      Step Executor                                   │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐             │  │
│  │  │ Action   │  │ Check    │  │ Wait     │  │ Approval │             │  │
│  │  │ Executor │  │ Executor │  │ Executor │  │ Executor │             │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘             │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      Concurrency Control                             │  │
│  │  • Semaphore for parallel steps                                      │  │
│  │  • Worker pool for step execution                                    │  │
│  │  • Rate limiter for external calls                                   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                      Persistence Layer                                       │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │  State Store     │  │  Event Store     │  │  Audit Log       │          │
│  │  (PostgreSQL)    │  │  (Event Sourcing)│  │  (S3/MinIO)      │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 4.4 SOP状态机

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        SOP Execution State Machine                          │
└─────────────────────────────────────────────────────────────────────────────┘

                              ┌─────────────┐
                              │   Created   │
                              │   (已创建)   │
                              └──────┬──────┘
                                     │
                                     │ validate
                                     ▼
                              ┌─────────────┐
                              │   Valid     │
                              │   (已验证)   │
                              └──────┬──────┘
                                     │
                                     │ start
                                     ▼
┌─────────────┐              ┌─────────────┐              ┌─────────────┐
│   Failed    │◀─────────────│   Running   │─────────────▶│  Paused     │
│   (失败)    │   on error   │   (执行中)   │  on pause    │  (已暂停)   │
└──────┬──────┘              └──────┬──────┘              └──────┬──────┘
       │                            │ resume                     │
       │ retry                      │                            │
       ▼                            ▼                            │
┌─────────────┐              ┌─────────────┐                     │
│  Retrying   │              │   Waiting   │─────────────────────┘
│  (重试中)   │              │   (等待中)   │
└─────────────┘              └──────┬──────┘
       ▲                            │
       │                            │ condition met / approved
       │                            ▼
       │                     ┌─────────────┐
       │                     │  Approved   │
       │                     │  (已批准)   │
       │                     └──────┬──────┘
       │                            │
       │                            │ execute next
       │                            │
       └────────────────────────────┘
                                    │
                                    │ all steps completed
                                    ▼
                              ┌─────────────┐
                              │  Completed  │
                              │   (已完成)   │
                              └──────┬──────┘
                                     │
                                     ▼
                              ┌─────────────┐
                              │   Archived  │
                              │   (已归档)   │
                              └─────────────┘

================================================================================
                              Step Level State
================================================================================

Pending ──▶ Running ──▶ Succeeded
              │
              ├──▶ Failed ──▶ Retrying ──▶ Running
              │
              ├──▶ Waiting ──▶ Approved ──▶ Running
              │      │
              │      └──▶ Rejected ──▶ Failed
              │
              └──▶ Timedout ──▶ Failed
```

### 4.5 SOP内置模板

#### 4.5.1 Pod重启SOP模板

```yaml
# 模板: pod-restart
apiVersion: ops-inspector.io/v1
kind: SOPTemplate
metadata:
  name: pod-restart
  description: "Pod异常自动重启标准流程"
  
spec:
  parameters:
    - name: namespace
      type: string
      required: true
    - name: pod_name
      type: string
      required: true
    - name: approval_threshold
      type: integer
      default: 3
      description: "超过此次数需要人工确认"
      
  workflow: |
    1. 获取Pod状态信息
    2. 检查重启次数
    3. 如果重启次数 > ${approval_threshold}:
       - 发起人工确认
    4. 删除Pod触发重建
    5. 等待Pod Running
    6. 健康检查
    7. 发送通知
```

#### 4.5.2 服务扩容SOP模板

```yaml
# 模板: service-scale
apiVersion: ops-inspector.io/v1
kind: SOPTemplate
metadata:
  name: service-scale
  description: "服务自动扩容标准流程"
  
spec:
  parameters:
    - name: deployment
      type: string
      required: true
    - name: namespace
      type: string
      required: true
    - name: target_replicas
      type: integer
      required: true
    - name: cpu_threshold
      type: integer
      default: 80
    - name: max_replicas
      type: integer
      default: 10
      
  workflow: |
    1. 检查当前副本数
    2. 验证目标副本数 <= max_replicas
    3. 检查资源配额
    4. 执行扩容
    5. 等待Pod Ready
    6. 验证负载均衡
    7. 发送通知
```

#### 4.5.3 故障切换SOP模板

```yaml
# 模板: failover
apiVersion: ops-inspector.io/v1
kind: SOPTemplate
metadata:
  name: database-failover
  description: "数据库故障切换标准流程"
  
spec:
  parameters:
    - name: cluster_name
      type: string
      required: true
    - name: failed_node
      type: string
      required: true
    - name: force
      type: boolean
      default: false
      
  workflow: |
    1. 检查集群健康状态
    2. 确认备节点同步状态
    3. 人工确认（critical级别）
    4. 执行切换
    5. 验证新主节点
    6. 更新DNS/配置
    7. 通知相关业务方
    8. 记录切换事件
```

### 4.6 SOP审计与复盘

```yaml
# 审计配置
audit:
  # 审计级别
  level: detailed  # summary | normal | detailed
  
  # 审计内容
  content:
    - trigger_info      # 触发信息
    - input_params      # 输入参数
    - step_executions   # 步骤执行详情
    - output_results    # 输出结果
    - state_transitions # 状态转换
    - approvals         # 审批记录
    - errors            # 错误信息
    - timing            # 时间记录
    
  # 保留策略
  retention:
    detailed: 90d
    normal: 180d
    summary: 1y
    
  # 存储配置
  storage:
    type: s3
    bucket: ops-inspector-audit
    path: "sop-executions/{{date}}/{{execution_id}}"
    
# 复盘报告
review:
  # 自动生成复盘报告
  auto_generate: true
  
  # 报告模板
  template: |
    ## SOP执行复盘: {{sop_name}}
    
    ### 基本信息
    - 执行ID: {{execution_id}}
    - 执行时间: {{start_time}} - {{end_time}}
    - 总耗时: {{duration}}
    - 最终状态: {{final_status}}
    
    ### 执行统计
    - 总步骤数: {{total_steps}}
    - 成功步骤: {{succeeded_steps}}
    - 失败步骤: {{failed_steps}}
    - 跳过的步骤: {{skipped_steps}}
    
    ### 人工介入
    - 审批次数: {{approval_count}}
    - 平均审批时间: {{avg_approval_time}}
    
    ### 建议优化
    {{recommendations}}

### 4.7 详细SOP数据模型与CRD

#### 4.7.1 SOP CRD完整定义

```yaml
# CRD: StandardOperatingProcedure.ops-inspector.io
apiVersion: apiextensions.k8s.io/v1
kind: CustomResourceDefinition
metadata:
  name: standardoperatingprocedures.ops-inspector.io
spec:
  group: ops-inspector.io
  names:
    kind: StandardOperatingProcedure
    listKind: StandardOperatingProcedureList
    plural: standardoperatingprocedures
    singular: standardoperatingprocedure
    shortNames:
      - sop
  scope: Namespaced
  versions:
    - name: v1
      served: true
      storage: true
      schema:
        openAPIV3Schema:
          type: object
          required:
            - spec
          properties:
            spec:
              type: object
              required:
                - steps
              properties:
                # 基本信息
                version:
                  type: string
                  default: "1.0.0"
                description:
                  type: string
                  maxLength: 1000
                category:
                  type: string
                  enum: 
                    - incident-response
                    - change-management
                    - routine-maintenance
                    - emergency-recovery
                    - compliance-check
                severity:
                  type: string
                  enum: [critical, high, medium, low]
                  default: medium
                # 触发条件、输入参数、步骤定义等详见完整文档
            status:
              type: object
              properties:
                phase:
                  type: string
                  enum: [Draft, Active, Deprecated, Archived]
                executionCount:
                  type: integer
                  default: 0
                successRate:
                  type: string
```

#### 4.7.2 SOPInstance CRD

```yaml
# SOPInstance CRD
apiVersion: ops-inspector.io/v1
kind: SOPInstance
metadata:
  name: pod-recovery-instance-xyz
spec:
  sopRef: template-pod-auto-recovery
  inputs:
    namespace: production
    pod_name: api-gateway-abc
    max_restart_threshold: 5
  trigger:
    type: alert
    source: prometheus-alerts
    alertRef: PodCrashLooping
  priority: 8
status:
  phase: Running
  currentStep: analyze
  steps:
    - id: collect-info
      name: 收集Pod信息
      status: Succeeded
      startTime: "2026-02-05T10:00:00Z"
      endTime: "2026-02-05T10:00:05Z"
    - id: analyze
      name: 分析问题
      status: Running
      startTime: "2026-02-05T10:00:05Z"
  startTime: "2026-02-05T10:00:00Z"
  duration: "5m30s"
```

### 4.8 完整SOP模板库

#### 4.8.1 系统内置模板清单

| 模板名称 | 分类 | 描述 | 适用场景 |
|---------|------|------|---------|
| `template-pod-auto-recovery` | kubernetes | Pod自动恢复 | CrashLoopBackOff、Evicted等 |
| `template-db-failover` | database | 数据库故障切换 | 主库宕机 |
| `template-service-scale-up` | capacity | 服务自动扩容 | CPU/内存高负载 |
| `template-disk-cleanup` | maintenance | 磁盘清理 | 节点磁盘空间不足 |
| `template-cert-renewal` | security | 证书续期 | TLS证书即将过期 |
| `template-node-cordon` | kubernetes | 节点隔离 | 节点故障或不健康 |
| `template-ingress-failover` | network | Ingress故障转移 | 负载均衡异常 |
| `template-cache-warmup` | performance | 缓存预热 | 服务重启后 |
| `template-log-rotation` | maintenance | 日志轮转 | 日志文件过大 |
| `template-security-patch` | security | 安全补丁 | CVE漏洞修复 |

#### 4.8.2 模板使用示例

```yaml
# 使用模板创建SOP
apiVersion: ops-inspector.io/v1
kind: StandardOperatingProcedure
metadata:
  name: my-pod-recovery
  annotations:
    ops-inspector.io/template-ref: template-pod-auto-recovery
    ops-inspector.io/template-version: "1.0.0"
spec:
  # 继承模板配置，可覆盖特定参数
  inputs:
    - name: max_restart_threshold
      default: 3  # 覆盖模板的默认值
  
  # 添加额外的通知配置
  steps:
    - id: notify
      name: 发送通知
      type: notification
      notification:
        channels: [slack-ops, email-team]
```

### 4.9 完整的SOP执行引擎实现

```go
// 核心执行引擎伪代码
package engine

type Engine struct {
    executors      map[string]StepExecutor
    approvalMgr    *ApprovalManager
    eventBus       EventBus
    auditLogger    *AuditLogger
    variableStore  *VariableStore
    celEnv         *cel.Env
}

func (e *Engine) Execute(ctx context.Context, sop *SOP, inputs map[string]interface{}) (string, error) {
    // 1. 创建执行实例
    execution := e.createExecution(sop, inputs)
    
    // 2. 发布开始事件
    e.eventBus.Publish(ctx, Event{Type: "sop.execution.started"})
    
    // 3. 异步执行工作流
    go e.runExecution(ctx, execution)
    
    return execution.ID, nil
}

func (e *Engine) runExecution(ctx context.Context, exec *Execution) {
    for currentStep := range exec.SOP.Steps {
        // 检查条件
        if !e.evaluateCondition(currentStep.Condition, exec) {
            continue
        }
        
        // 执行步骤
        result := e.executeStep(ctx, exec, currentStep)
        
        // 记录审计日志
        e.auditLogger.Log(ctx, AuditRecord{
            Type:          "step.completed",
            SOPInstanceID: exec.ID,
            StepID:        currentStep.ID,
            Status:        result.Status,
        })
        
        // 处理结果
        if result.Error != nil {
            e.handleStepError(exec, currentStep, result.Error)
            return
        }
        
        // 状态转移
        exec.CurrentStep = result.NextStep
    }
    
    // 执行完成
    exec.Status = Succeeded
    e.eventBus.Publish(ctx, Event{Type: "sop.execution.succeeded"})
}
```

### 4.10 SOP与自动修复深度集成

```yaml
# 自动修复策略集成SOP
apiVersion: ops-inspector.io/v1
kind: RemediationPolicy
metadata:
  name: integrated-remediation
spec:
  # 简单场景：直接修复
  autoRemediation:
    - condition: "alert.labels.severity == 'low'"
      action:
        type: direct
        ref: restart-pod
  
  # 复杂场景：调用SOP
  sopRemediation:
    - name: pod-failure-recovery
      condition: |
        alert.labels.alertname == 'PodNotReady'
      sopRef: template-pod-auto-recovery
      parameterMapping:
        namespace: "${alert.labels.namespace}"
        pod_name: "${alert.labels.pod}"
    
    - name: database-failover
      condition: |
        alert.labels.alertname == 'DatabasePrimaryDown'
      sopRef: template-db-failover
      forceApproval: true  # 关键操作强制审批
```

### 4.11 完整的SOP审计系统

```go
// 审计系统核心实现
type AuditLogger struct {
    storage AuditStorage
}

type ExecutionReport struct {
    ExecutionID       string
    SOPName           string
    Status            string
    TriggerSource     string
    StartTime         time.Time
    EndTime           *time.Time
    Duration          time.Duration
    TotalSteps        int
    SucceededSteps    int
    FailedSteps       int
    Efficiency        EfficiencyMetrics
    AuditTrail        []AuditRecord
    Recommendations   []Recommendation
}

func (l *AuditLogger) GenerateExecutionReport(ctx context.Context, executionID string) (*ExecutionReport, error) {
    // 查询审计记录
    records := l.storage.Query(ctx, AuditQuery{SOPInstanceID: executionID})
    
    // 构建报告
    report := &ExecutionReport{
        ExecutionID: executionID,
        AuditTrail:  records,
    }
    
    // 计算效率指标
    report.Efficiency = calculateEfficiency(report)
    
    // 生成改进建议
    report.Recommendations = generateRecommendations(report)
    
    return report, nil
}
```

#### 4.11.1 复盘API

```yaml
# SOP复盘相关API
paths:
  /sops/{name}/reports:
    get:
      summary: 获取SOP执行报告列表
      parameters:
        - name: name
          in: path
          required: true
        - name: startTime
          in: query
          schema:
            type: string
            format: date-time
        - name: status
          in: query
          schema:
            type: string
            enum: [Succeeded, Failed, Timeout]
      responses:
        200:
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  items:
                    type: array
                    items:
                      $ref: '#/components/schemas/ExecutionReport'
                  summary:
                    type: object
                    properties:
                      totalExecutions:
                        type: integer
                      successRate:
                        type: number
                      avgDuration:
                        type: string
                      mttr:  # 平均修复时间
                        type: string
  
  /sops/{name}/analytics:
    get:
      summary: 获取SOP执行分析
      responses:
        200:
          description: 成功
          content:
            application/json:
              schema:
                type: object
                properties:
                  executionTrend:
                    type: array
                    items:
                      type: object
                      properties:
                        date:
                          type: string
                        count:
                          type: integer
                        successRate:
                          type: number
                  bottleneckSteps:
                    type: array
                    description: "瓶颈步骤分析"
                  improvementOpportunities:
                    type: array
```

---

## 6. 数据模型

### 5.1 核心实体关系图

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          数据模型ER图                                        │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│      SOP        │       │  SOPExecution   │       │   SOPStep       │
│   (SOP定义)      │1    * │   (SOP执行)      │1    * │  (SOP步骤)       │
├─────────────────┤◀──────├─────────────────┤◀──────├─────────────────┤
│ id              │       │ id              │       │ id              │
│ name            │       │ sop_id          │       │ execution_id    │
│ version         │       │ status          │       │ step_id         │
│ category        │       │ trigger_type    │       │ type            │
│ triggers        │       │ trigger_source  │       │ status          │
│ workflow        │       │ inputs          │       │ inputs          │
│ variables       │       │ outputs         │       │ outputs         │
│ error_handling  │       │ started_at      │       │ started_at      │
│ audit_config    │       │ completed_at    │       │ completed_at    │
└─────────────────┘       │ error_info      │       │ error_info      │
                          └─────────────────┘       └─────────────────┘
                                  │
                                  │
                                  ▼
                          ┌─────────────────┐
                          │  SOPApproval    │
                          │  (SOP审批)       │
                          ├─────────────────┤
                          │ id              │
                          │ execution_id    │
                          │ step_id         │
                          │ approvers       │
                          │ approved_by     │
                          │ status          │
                          │ requested_at    │
                          │ responded_at    │
                          └─────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│  Inspection     │       │ InspectionResult│       │   CheckResult   │
│   (巡检定义)     │1    * │   (巡检结果)     │1    * │   (检查结果)    │
├─────────────────┤◀──────├─────────────────┤◀──────├─────────────────┤
│ id              │       │ id              │       │ id              │
│ name            │       │ inspection_id   │       │ result_id       │
│ schedule        │       │ status          │       │ checker_name    │
│ checkers        │       │ started_at      │       │ target          │
│ targets         │       │ completed_at    │       │ status          │
│ timeout         │       │ summary         │       │ output          │
│ notification    │       │ details         │       │ duration_ms     │
└─────────────────┘       └─────────────────┘       └─────────────────┘

┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│     Skill       │       │  SkillExecution │       │   Alert         │
│   (技能定义)     │1    * │  (技能执行)      │*    1 │   (告警)        │
├─────────────────┤◀──────├─────────────────┤──────▶├─────────────────┤
│ id              │       │ id              │       │ id              │
│ name            │       │ skill_id        │       │ source          │
│ type            │       │ inputs          │       │ severity        │
│ category        │       │ outputs         │       │ status          │
│ description     │       │ status          │       │ message         │
│ inputs          │       │ error           │       │ context         │
│ outputs         │       │ started_at      │       │ triggered_at    │
│ code            │       │ completed_at    │       │ resolved_at     │
│ dependencies    │       └─────────────────┘       │ sop_execution_id│
└─────────────────┘                                 └─────────────────┘
```

### 5.2 数据库Schema

```sql
-- SOP定义表
CREATE TABLE sops (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    version         VARCHAR(50) NOT NULL,
    category        VARCHAR(100),
    description     TEXT,
    triggers        JSONB NOT NULL,
    inputs          JSONB,
    variables       JSONB,
    workflow        JSONB NOT NULL,
    error_handling  JSONB,
    audit_config    JSONB,
    status          VARCHAR(50) DEFAULT 'active',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(name, version)
);

-- SOP执行实例表
CREATE TABLE sop_executions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    sop_id          UUID NOT NULL REFERENCES sops(id),
    status          VARCHAR(50) NOT NULL, -- pending/running/waiting/completed/failed
    trigger_type    VARCHAR(50), -- manual/scheduled/event/webhook
    trigger_source  VARCHAR(255),
    inputs          JSONB,
    outputs         JSONB,
    context         JSONB, -- 执行上下文，包括变量值
    current_step_id VARCHAR(100),
    started_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at    TIMESTAMP,
    error_info      JSONB,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SOP步骤执行记录表
CREATE TABLE sop_step_executions (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id    UUID NOT NULL REFERENCES sop_executions(id),
    step_id         VARCHAR(100) NOT NULL,
    type            VARCHAR(50) NOT NULL,
    status          VARCHAR(50) NOT NULL,
    inputs          JSONB,
    outputs         JSONB,
    error_info      JSONB,
    retry_count     INTEGER DEFAULT 0,
    started_at      TIMESTAMP,
    completed_at    TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SOP审批记录表
CREATE TABLE sop_approvals (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    execution_id    UUID NOT NULL REFERENCES sop_executions(id),
    step_id         VARCHAR(100) NOT NULL,
    approvers       JSONB NOT NULL, -- [{"type": "group/user", "id": "xxx"}]
    approved_by     VARCHAR(255),
    status          VARCHAR(50) NOT NULL, -- pending/approved/rejected/expired
    message         TEXT,
    requested_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    responded_at    TIMESTAMP,
    timeout_at      TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 技能表
CREATE TABLE skills (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL UNIQUE,
    version         VARCHAR(50) NOT NULL DEFAULT '1.0.0',
    type            VARCHAR(50) NOT NULL, -- checker/healer/notifier/collector
    category        VARCHAR(100),
    description     TEXT,
    inputs          JSONB, -- 参数定义
    outputs         JSONB, -- 输出定义
    dependencies    JSONB, -- 依赖的其他skill
    code            TEXT, -- 执行代码或脚本路径
    config_schema   JSONB, -- 配置schema
    status          VARCHAR(50) DEFAULT 'active',
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 巡检定义表
CREATE TABLE inspections (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name            VARCHAR(255) NOT NULL,
    description     TEXT,
    schedule        VARCHAR(100), -- Cron表达式
    checkers        JSONB NOT NULL, -- [{"name": "xxx", "config": {}}]
    targets         JSONB NOT NULL, -- 巡检目标
    timeout         INTEGER DEFAULT 300, -- 秒
    notification    JSONB, -- 通知配置
    sop_bindings    JSONB, -- 关联的SOP
    enabled         BOOLEAN DEFAULT true,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 巡检结果表
CREATE TABLE inspection_results (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    inspection_id   UUID NOT NULL REFERENCES inspections(id),
    status          VARCHAR(50) NOT NULL, -- success/warning/critical
    summary         JSONB, -- 汇总信息
    details         JSONB, -- 详细结果
    started_at      TIMESTAMP,
    completed_at    TIMESTAMP,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 告警表
CREATE TABLE alerts (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source          VARCHAR(255) NOT NULL, -- 告警来源
    severity        VARCHAR(50) NOT NULL, -- info/warning/critical/emergency
    status          VARCHAR(50) NOT NULL DEFAULT 'fired', -- fired/acknowledged/resolved
    title           VARCHAR(500),
    message         TEXT,
    context         JSONB, -- 告警上下文
    labels          JSONB, -- 标签用于路由和分组
    annotations     JSONB, -- 附加信息
    triggered_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    acknowledged_by VARCHAR(255),
    acknowledged_at TIMESTAMP,
    resolved_at     TIMESTAMP,
    sop_execution_id UUID REFERENCES sop_executions(id),
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 事件表
CREATE TABLE events (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    type            VARCHAR(255) NOT NULL,
    source          VARCHAR(255) NOT NULL,
    data            JSONB,
    headers         JSONB,
    correlation_id  VARCHAR(255),
    parent_id       VARCHAR(255),
    timestamp       TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 审计日志表
CREATE TABLE audit_logs (
    id              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    entity_type     VARCHAR(100) NOT NULL, -- sop/inspection/alert/skill
    entity_id       UUID NOT NULL,
    action          VARCHAR(100) NOT NULL, -- create/update/delete/execute
    actor           VARCHAR(255), -- 执行者
    details         JSONB,
    ip_address      VARCHAR(100),
    user_agent      TEXT,
    created_at      TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 索引优化
CREATE INDEX idx_sop_exec_status ON sop_executions(status);
CREATE INDEX idx_sop_exec_sop_id ON sop_executions(sop_id);
CREATE INDEX idx_step_exec_execution ON sop_step_executions(execution_id);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_severity ON alerts(severity);
CREATE INDEX idx_alerts_triggered ON alerts(triggered_at);
CREATE INDEX idx_events_type ON events(type);
CREATE INDEX idx_events_timestamp ON events(timestamp);
CREATE INDEX idx_inspection_results_inspection ON inspection_results(inspection_id);
```

### 5.3 配置模型

```yaml
# 系统配置模型
system:
  # 调度器配置
  scheduler:
    workers: 10
    queue_size: 1000
    retry_policy:
      max_attempts: 3
      backoff: exponential
      initial_delay: 1s
      max_delay: 1m
      
  # 事件总线配置
  event_bus:
    type: nats  # nats/kafka/redis
    nats:
      url: nats://localhost:4222
      max_reconnects: 10
      reconnect_wait: 1s
      
  # 存储配置
  storage:
    database:
      type: postgresql
      host: localhost
      port: 5432
      database: ops_inspector
      pool_size: 20
    cache:
      type: redis
      host: localhost
      port: 6379
      db: 0
    object:
      type: s3
      endpoint: s3.amazonaws.com
      bucket: ops-inspector
      
  # 技能注册表配置
  skill_registry:
    paths:
      - /etc/ops-inspector/skills
      - /var/lib/ops-inspector/skills
    auto_reload: true
    verify_signature: true
    
  # 通知配置
  notification:
    channels:
      - name: default
        type: slack
        webhook: ${SLACK_WEBHOOK_URL}
      - name: pagerduty
        type: pagerduty
        integration_key: ${PAGERDUTY_KEY}
    
  # 安全配置
  security:
    jwt_secret: ${JWT_SECRET}
    token_ttl: 24h
    rbac:
      enabled: true
      policy_file: /etc/ops-inspector/rbac.yaml
```

---

## 7. 配置体系

### 6.1 配置层次结构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        配置层次结构                                          │
└─────────────────────────────────────────────────────────────────────────────┘

Priority ▲
    10  │  ┌─────────────────────────────────────────┐
        │  │      Environment Variables              │
        │  │      (环境变量，最高优先级)              │
        │  └─────────────────────────────────────────┘
     9  │  ┌─────────────────────────────────────────┐
        │  │      Command Line Flags                 │
        │  │      (命令行参数)                        │
        │  └─────────────────────────────────────────┘
     8  │  ┌─────────────────────────────────────────┐
        │  │      Runtime Configuration (etcd/consul)│
        │  │      (运行时配置，支持动态更新)          │
        │  └─────────────────────────────────────────┘
     7  │  ┌─────────────────────────────────────────┐
        │  │      Secret Configuration (Vault/AWS SM)│
        │  │      (密钥配置)                          │
        │  └─────────────────────────────────────────┘
     6  │  ┌─────────────────────────────────────────┐
        │  │      Instance Configuration             │
        │  │      (实例级配置，/etc/ops-inspector/)   │
        │  └─────────────────────────────────────────┘
     5  │  ┌─────────────────────────────────────────┐
        │  │      Application Configuration          │
        │  │      (应用配置，/opt/ops-inspector/)     │
        │  └─────────────────────────────────────────┘
     4  │  ┌─────────────────────────────────────────┐
        │  │      User Configuration                 │
        │  │      (用户配置，~/.ops-inspector/)       │
        │  └─────────────────────────────────────────┘
     3  │  ┌─────────────────────────────────────────┐
        │  │      Default Configuration (Embedded)   │
        │  │      (默认配置，内嵌)                    │
        │  └─────────────────────────────────────────┘
        │
        └─────────────────────────────────────────────────────────────────────
```

### 6.2 配置热更新机制

```go
// ConfigManager 配置管理器接口
type ConfigManager interface {
    // 获取配置
    Get(key string) (Value, error)
    GetString(key string) (string, error)
    GetInt(key string) (int, error)
    GetBool(key string) (bool, error)
    GetDuration(key string) (time.Duration, error)
    GetObject(key string, target interface{}) error
    
    // 设置配置
    Set(key string, value interface{}) error
    
    // 监听配置变化
    Watch(key string, callback ConfigChangeCallback) (Watcher, error)
    
    // 重新加载配置
    Reload() error
    
    // 获取完整配置
    AllSettings() map[string]interface{}
}

// 配置热更新示例
func setupHotReload(cm ConfigManager) {
    // 监听调度器配置变化
    watcher, _ := cm.Watch("scheduler.workers", func(oldVal, newVal Value) {
        log.Infof("调度器workers配置变更: %v -> %v", oldVal, newVal)
        // 动态调整worker数量
        scheduler.AdjustWorkers(newVal.ToInt())
    })
    defer watcher.Stop()
    
    // 监听通知通道配置变化
    cm.Watch("notification.channels", func(oldVal, newVal Value) {
        log.Info("通知通道配置变更，重新初始化")
        notifier.ReloadChannels()
    })
}
```

### 6.3 配置验证

```yaml
# 配置Schema定义
apiVersion: ops-inspector.io/v1
kind: ConfigSchema
spec:
  validations:
    - path: scheduler.workers
      rules:
        - type: required
        - type: range
          min: 1
          max: 100
          
    - path: storage.database.host
      rules:
        - type: required
        - type: hostname
        
    - path: event_bus.nats.url
      rules:
        - type: required
        - type: url
        
    - path: notification.channels
      rules:
        - type: required
        - type: array
          min_items: 1
      children:
        - path: "[*].name"
          rules:
            - type: required
            - type: pattern
              regex: "^[a-z0-9-]+$"
              
    - path: security.jwt_secret
      rules:
        - type: required
        - type: min_length
          value: 32
```

---

## 8. 扩展机制

### 7.1 Skill扩展机制

#### 7.1.1 内置Skill类型

```go
// 1. Go插件式Skill（动态加载）
type GoSkill struct {
    metadata SkillMetadata
    plugin   plugin.Plugin
}

func (s *GoSkill) Execute(ctx context.Context, input SkillInput) (*SkillOutput, error) {
    // 通过plugin机制调用
}

// 2. WASM Skill（沙箱执行）
type WASMSkill struct {
    metadata SkillMetadata
    runtime  wazero.Runtime
    module   api.Module
}

func (s *WASMSkill) Execute(ctx context.Context, input SkillInput) (*SkillOutput, error) {
    // 通过WASM运行时执行
}

// 3. 脚本Skill（Python/Bash/JS）
type ScriptSkill struct {
    metadata SkillMetadata
    interpreter string
    scriptPath  string
}

func (s *ScriptSkill) Execute(ctx context.Context, input SkillInput) (*SkillOutput, error) {
    // 调用解释器执行脚本
}

// 4. HTTP Skill（外部服务调用）
type HTTPSkill struct {
    metadata SkillMetadata
    endpoint string
    method   string
    headers  map[string]string
}

func (s *HTTPSkill) Execute(ctx context.Context, input SkillInput) (*SkillOutput, error) {
    // HTTP调用外部服务
}

// 5. gRPC Skill
// 6. 容器化Skill（Kubernetes Job/Docker Container）
```

#### 7.1.2 Skill开发SDK

```go
// Skill开发SDK示例
package sdk

// BaseSkill 基础Skill结构
type BaseSkill struct {
    metadata SkillMetadata
}

func (s *BaseSkill) Metadata() SkillMetadata {
    return s.metadata
}

func (s *BaseSkill) Validate(config map[string]interface{}) error {
    // 使用JSON Schema验证
    return validateSchema(s.metadata.Config, config)
}

// CheckerSkill 巡检Skill基类
type CheckerSkill struct {
    BaseSkill
}

func (s *CheckerSkill) Check(ctx context.Context, target Target, config map[string]interface{}) (*CheckResult, error) {
    // 子类实现具体检查逻辑
    return nil, nil
}

// 开发自定义Skill示例
func main() {
    skill := &MyCustomChecker{
        CheckerSkill: CheckerSkill{
            BaseSkill: BaseSkill{
                metadata: SkillMetadata{
                    Name:        "k8s-pod-health",
                    Version:     "1.0.0",
                    Type:        "checker",
                    Category:    "kubernetes",
                    Description: "检查Kubernetes Pod健康状态",
                    Inputs: []Parameter{
                        {Name: "namespace", Type: "string", Required: true},
                        {Name: "pod_name", Type: "string", Required: true},
                    },
                    Outputs: []Parameter{
                        {Name: "status", Type: "string"},
                        {Name: "restart_count", Type: "integer"},
                    },
                },
            },
        },
    }
    
    // 注册到Registry
    registry.Register(skill)
}

type MyCustomChecker struct {
    CheckerSkill
}

func (c *MyCustomChecker) Check(ctx context.Context, target Target, config map[string]interface{}) (*CheckResult, error) {
    namespace := config["namespace"].(string)
    podName := config["pod_name"].(string)
    
    // 实现具体的检查逻辑
    // ...
    
    return &CheckResult{
        Status:  StatusHealthy,
        Outputs: map[string]interface{}{
            "status":        "Running",
            "restart_count": 0,
        },
    }, nil
}
```

### 7.2 插件系统架构

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        插件系统架构                                          │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         Core System                                          │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      Plugin Manager                                  │  │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌────────────┐     │  │
│  │  │ Discovery  │  │  Loader    │  │ Lifecycle  │  │  Registry  │     │  │
│  │  └────────────┘  └────────────┘  └────────────┘  └────────────┘     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
│                                                                             │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                      Extension Points                                │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐   │  │
│  │  │ Checker  │ │ Healer   │ │ Notifier │ │ Collector│ │ Filter   │   │  │
│  │  │ Extension│ │ Extension│ │ Extension│ │ Extension│ │ Extension│   │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘ └──────────┘   │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    │ Plugin API
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                         Plugins                                              │
│                                                                             │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │   Go Plugins     │  │   WASM Plugins   │  │ Script Plugins   │          │
│  │   (.so)          │  │   (.wasm)        │  │ (.py/.sh/.js)    │          │
│  │                  │  │                  │  │                  │          │
│  │  ┌────────────┐  │  │  ┌────────────┐  │  │  ┌────────────┐  │          │
│  │  │ k8s-skills │  │  │  │ wasm-check │  │  │  │ custom-    │  │          │
│  │  └────────────┘  │  │  └────────────┘  │  │  │ notifier   │  │          │
│  │  ┌────────────┐  │  │  ┌────────────┐  │  │  └────────────┘  │          │
│  │  │ aws-skills │  │  │  │ wasm-heal  │  │  │  ┌────────────┐  │          │
│  │  └────────────┘  │  │  └────────────┘  │  │  │ analyzer   │  │          │
│  └──────────────────┘  └──────────────────┘  │  └────────────┘  │          │
│                                              └──────────────────┘          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### 7.3 Webhook扩展点

```yaml
# Webhook配置
webhooks:
  - name: pre-inspection
    url: https://example.com/webhooks/pre-inspection
    events:
      - inspection.started
    timeout: 5s
    
  - name: post-check
    url: https://example.com/webhooks/post-check
    events:
      - check.completed
    filter: |
      event.status == "failed"
    
  - name: alert-webhook
    url: https://example.com/webhooks/alert
    events:
      - alert.fired
      - alert.resolved
    headers:
      X-Custom-Header: value
    secret: ${WEBHOOK_SECRET}  # 用于签名验证
```

---

## 9. 部署架构

### 8.1 Kubernetes部署架构

```yaml
# 部署架构说明
#
# ┌─────────────────────────────────────────────────────────────────────────────┐
# │                         Kubernetes Namespace: ops-inspector                  │
# │                                                                              │
# │  ┌──────────────────────────────────────────────────────────────────────┐   │
# │  │                     Ingress / Gateway                                │   │
# │  │                     (API入口)                                        │   │
# │  └──────────────────────────────────────────────────────────────────────┘   │
# │                                    │                                        │
# │                                    ▼                                        │
# │  ┌──────────────────────────────────────────────────────────────────────┐   │
# │  │                     API Service                                      │   │
# │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
# │  │  │ API Pod 1   │  │ API Pod 2   │  │ API Pod 3   │  │ ...         │ │   │
# │  │  │ (3 replicas)│  │             │  │             │  │             │ │   │
# │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
# │  └──────────────────────────────────────────────────────────────────────┘   │
# │                                    │                                        │
# │                                    ▼                                        │
# │  ┌──────────────────────────────────────────────────────────────────────┐   │
# │  │                     Worker Service                                   │   │
# │  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │   │
# │  │  │ Worker Pod 1│  │ Worker Pod 2│  │ Worker Pod 3│  │ ...         │ │   │
# │  │  │ (5 replicas)│  │             │  │             │  │             │ │   │
# │  │  │ - Scheduler │  │             │  │             │  │             │ │   │
# │  │  │ - SOP Engine│  │             │  │             │  │             │ │   │
# │  │  │ - Inspector │  │             │  │             │  │             │ │   │
# │  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘ │   │
# │  └──────────────────────────────────────────────────────────────────────┘   │
# │                                    │                                        │
# │                                    ▼                                        │
# │  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
# │  │   PostgreSQL     │  │   Redis          │  │   MinIO / S3     │          │
# │  │   (StatefulSet)  │  │   (StatefulSet)  │  │   (Object Store) │          │
# │  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
# │                                                                              │
# │  ┌──────────────────┐  ┌──────────────────┐                                │
# │  │   NATS / Kafka   │  │   VictoriaMetrics│                                │
# │  │   (Event Bus)    │  │   (TSDB)         │                                │
# │  └──────────────────┘  └──────────────────┘                                │
# │                                                                              │
# └─────────────────────────────────────────────────────────────────────────────┘
```

### 8.2 Helm Chart结构

```yaml
# values.yaml 示例
# Chart: ops-inspector

global:
  imageRegistry: ""
  imagePullSecrets: []
  storageClass: ""

# API服务配置
api:
  enabled: true
  replicaCount: 3
  image:
    repository: ops-inspector/api
    tag: v1.0.0
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8080
  ingress:
    enabled: true
    className: nginx
    hosts:
      - host: ops-inspector.example.com
        paths:
          - path: /
            pathType: Prefix
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi

# Worker服务配置
worker:
  enabled: true
  replicaCount: 5
  image:
    repository: ops-inspector/worker
    tag: v1.0.0
  resources:
    limits:
      cpu: 2000m
      memory: 4Gi
    requests:
      cpu: 1000m
      memory: 2Gi

# 数据库配置
database:
  type: postgresql
  postgresql:
    enabled: true
    auth:
      username: ops_inspector
      password: changeme
      database: ops_inspector
    persistence:
      enabled: true
      size: 50Gi

# Redis配置
redis:
  enabled: true
  architecture: standalone
  auth:
    enabled: true
    password: changeme

# NATS配置
nats:
  enabled: true
  cluster:
    enabled: true
    replicas: 3

# 监控配置
monitoring:
  enabled: true
  prometheus:
    enabled: true
  grafana:
    enabled: true
```

### 8.3 高可用设计

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        高可用架构设计                                        │
└─────────────────────────────────────────────────────────────────────────────┘

================================================================================
                              单集群高可用
================================================================================

┌─────────────────────────────────────────────────────────────────────────────┐
│                          Load Balancer                                       │
│                        (Nginx/HAProxy/AWS ALB)                               │
└─────────────────────────────────────────────────────────────────────────────┘
          │                           │                           │
          ▼                           ▼                           ▼
┌──────────────────┐        ┌──────────────────┐        ┌──────────────────┐
│   API Instance   │        │   API Instance   │        │   API Instance   │
│       #1         │◀──────▶│       #2         │◀──────▶│       #3         │
│  (Leader)        │  Raft  │                  │  Raft  │                  │
└────────┬─────────┘        └────────┬─────────┘        └────────┬─────────┘
         │                           │                           │
         └───────────────────────────┼───────────────────────────┘
                                     │
                                     ▼
                         ┌──────────────────────┐
                         │   Database Cluster   │
                         │  (PostgreSQL Patroni)│
                         │  Primary ◀──▶ Standby│
                         └──────────────────────┘
                                     │
                                     ▼
                         ┌──────────────────────┐
                         │   Redis Sentinel     │
                         │  Master ◀──▶ Replica │
                         └──────────────────────┘

================================================================================
                              多集群灾备
================================================================================

┌─────────────────────────────┐              ┌─────────────────────────────┐
│      Region: Beijing        │              │      Region: Shanghai       │
│                             │              │                             │
│  ┌───────────────────────┐  │   Replicate  │  ┌───────────────────────┐  │
│  │  Primary Cluster      │  │◀────────────▶│  │  Standby Cluster      │  │
│  │  - Active Mode        │  │   Async      │  │  - Standby Mode       │  │
│  │  - Handle all traffic │  │              │  │  - Ready for failover │  │
│  └───────────────────────┘  │              │  └───────────────────────┘  │
│                             │              │                             │
│  ┌───────────────────────┐  │              │  ┌───────────────────────┐  │
│  │  SOP State Sync       │  │◀────────────▶│  │  SOP State Sync       │  │
│  │  - Execution states   │  │   Sync       │  │  - Execution states   │  │
│  │  - Pending approvals  │  │              │  │  - Pending approvals  │  │
│  └───────────────────────┘  │              │  └───────────────────────┘  │
│                             │              │                             │
│  ┌───────────────────────┐  │              │  ┌───────────────────────┐  │
│  │  Global Event Bus     │  │◀────────────▶│  │  Global Event Bus     │  │
│  │  (NATS JetStream)     │  │   Mirror     │  │  (NATS JetStream)     │  │
│  └───────────────────────┘  │              │  └───────────────────────┘  │
└─────────────────────────────┘              └─────────────────────────────┘

================================================================================
                              故障转移流程
================================================================================

Normal State:
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Primary   │◀───────▶│   Standby   │◀───────▶│   Witness   │
│   (Active)  │  Sync   │   (Sync)    │  Vote   │   (Vote)    │
└─────────────┘         └─────────────┘         └─────────────┘

Failure Detected:
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Primary   │╳╳╳╳╳╳╳╳╳│   Standby   │◀───────▶│   Witness   │
│   (Failed)  │  ╳╳╳╳╳╳  │   (Active)  │  Vote   │   (Vote)    │
└─────────────┘         └─────────────┘         └─────────────┘

Failover Complete:
┌─────────────┐         ┌─────────────┐         ┌─────────────┐
│   Primary   │         │   Standby   │         │   Witness   │
│   (Recover) │         │   (Active)  │         │   (Vote)    │
└─────────────┘         └─────────────┘         └─────────────┘
       │
       ▼ Rejoin as Standby
┌─────────────┐
│   Standby   │
│   (Sync)    │
└─────────────┘
```

---

## 10. 代码示例

### 9.1 核心服务实现

```go
// main.go - 服务入口
package main

import (
    "context"
    "log"
    "os"
    "os/signal"
    "syscall"
    
    "ops-inspector/internal/api"
    "ops-inspector/internal/config"
    "ops-inspector/internal/scheduler"
    "ops-inspector/internal/sop"
    "ops-inspector/internal/skill"
    "ops-inspector/pkg/eventbus"
)

func main() {
    // 加载配置
    cfg, err := config.Load()
    if err != nil {
        log.Fatalf("Failed to load config: %v", err)
    }
    
    // 初始化上下文
    ctx, cancel := context.WithCancel(context.Background())
    defer cancel()
    
    // 初始化事件总线
    eventBus, err := eventbus.New(cfg.EventBus)
    if err != nil {
        log.Fatalf("Failed to initialize event bus: %v", err)
    }
    defer eventBus.Close()
    
    // 初始化技能注册表
    skillRegistry := skill.NewRegistry(cfg.SkillRegistry)
    if err := skillRegistry.LoadSkills(ctx); err != nil {
        log.Fatalf("Failed to load skills: %v", err)
    }
    
    // 初始化SOP引擎
    sopEngine, err := sop.NewEngine(cfg.SOP, skillRegistry, eventBus)
    if err != nil {
        log.Fatalf("Failed to initialize SOP engine: %v", err)
    }
    
    // 初始化调度器
    taskScheduler := scheduler.New(cfg.Scheduler, sopEngine)
    if err := taskScheduler.Start(ctx); err != nil {
        log.Fatalf("Failed to start scheduler: %v", err)
    }
    
    // 初始化API服务
    apiServer := api.NewServer(cfg.API, taskScheduler, sopEngine, skillRegistry)
    
    // 启动API服务
    go func() {
        if err := apiServer.Start(); err != nil {
            log.Printf("API server error: %v", err)
            cancel()
        }
    }()
    
    // 等待中断信号
    sigChan := make(chan os.Signal, 1)
    signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
    
    <-sigChan
    log.Println("Shutting down...")
    
    // 优雅关闭
    shutdownCtx, shutdownCancel := context.WithTimeout(context.Background(), cfg.ShutdownTimeout)
    defer shutdownCancel()
    
    apiServer.Shutdown(shutdownCtx)
    taskScheduler.Stop(shutdownCtx)
    sopEngine.Shutdown(shutdownCtx)
}
```

### 9.2 SOP引擎实现

```go
// internal/sop/engine.go
package sop

import (
    "context"
    "fmt"
    "sync"
    "time"
    
    "ops-inspector/pkg/eventbus"
    "ops-inspector/pkg/skill"
)

// Engine SOP执行引擎
type Engine struct {
    store        Store
    skillRegistry skill.Registry
    eventBus     eventbus.EventBus
    executors    map[string]StepExecutor
    
    // 执行中的SOP
    executions   map[string]*Execution
    mu           sync.RWMutex
    
    // Worker池
    workerPool   chan struct{}
    wg           sync.WaitGroup
}

// NewEngine 创建SOP引擎
func NewEngine(cfg Config, registry skill.Registry, bus eventbus.EventBus) (*Engine, error) {
    engine := &Engine{
        store:         NewPostgresStore(cfg.Database),
        skillRegistry: registry,
        eventBus:      bus,
        executors:     make(map[string]StepExecutor),
        executions:    make(map[string]*Execution),
        workerPool:    make(chan struct{}, cfg.MaxConcurrency),
    }
    
    // 注册步骤执行器
    engine.registerExecutors()
    
    // 恢复未完成的执行
    if err := engine.resumeExecutions(context.Background()); err != nil {
        return nil, fmt.Errorf("failed to resume executions: %w", err)
    }
    
    return engine, nil
}

// 注册步骤执行器
func (e *Engine) registerExecutors() {
    e.executors["action"] = NewActionExecutor(e.skillRegistry)
    e.executors["check"] = NewCheckExecutor(e.skillRegistry)
    e.executors["condition"] = NewConditionExecutor()
    e.executors["switch"] = NewSwitchExecutor()
    e.executors["parallel"] = NewParallelExecutor(e)
    e.executors["loop"] = NewLoopExecutor(e)
    e.executors["wait"] = NewWaitExecutor()
    e.executors["approval"] = NewApprovalExecutor(e.eventBus)
    e.executors["notification"] = NewNotificationExecutor(e.skillRegistry)
    e.executors["subflow"] = NewSubflowExecutor(e)
}

// Execute 执行SOP
func (e *Engine) Execute(ctx context.Context, sop *SOP, inputs map[string]interface{}) (string, error) {
    // 创建执行实例
    execution := NewExecution(sop, inputs)
    
    // 保存到存储
    if err := e.store.CreateExecution(ctx, execution); err != nil {
        return "", fmt.Errorf("failed to create execution: %w", err)
    }
    
    // 添加到活跃执行列表
    e.mu.Lock()
    e.executions[execution.ID] = execution
    e.mu.Unlock()
    
    // 发布事件
    e.eventBus.Publish(ctx, &eventbus.Event{
        Type:      "sop.started",
        Source:    "sop-engine",
        Data: map[string]interface{}{
            "execution_id": execution.ID,
            "sop_name":     sop.Name,
            "sop_version":  sop.Version,
        },
    })
    
    // 异步执行
    e.wg.Add(1)
    go func() {
        defer e.wg.Done()
        e.runExecution(context.Background(), execution)
    }()
    
    return execution.ID, nil
}

// runExecution 执行SOP工作流
func (e *Engine) runExecution(ctx context.Context, execution *Execution) {
    // 获取Worker槽位
    e.workerPool <- struct{}{}
    defer func() { <-e.workerPool }()
    
    sop := execution.SOP
    currentStep := execution.CurrentStep
    
    for currentStep != nil {
        select {
        case <-ctx.Done():
            execution.SetStatus(StatusCancelled)
            e.saveExecution(ctx, execution)
            return
        default:
        }
        
        // 获取步骤执行器
        executor, ok := e.executors[currentStep.Type]
        if !ok {
            execution.SetError(fmt.Errorf("unknown step type: %s", currentStep.Type))
            break
        }
        
        // 执行步骤
        stepExecution := execution.StartStep(currentStep)
        result, err := executor.Execute(ctx, stepExecution)
        
        if err != nil {
            // 处理错误
            if !e.handleStepError(ctx, execution, currentStep, err) {
                break
            }
        } else {
            // 保存步骤结果
            stepExecution.Complete(result)
            
            // 确定下一步
            currentStep = e.determineNextStep(sop, currentStep, result)
        }
        
        // 保存执行状态
        if err := e.saveExecution(ctx, execution); err != nil {
            log.Printf("Failed to save execution: %v", err)
        }
    }
    
    // 完成执行
    execution.Complete()
    e.saveExecution(ctx, execution)
    
    // 发布完成事件
    e.eventBus.Publish(ctx, &eventbus.Event{
        Type:   fmt.Sprintf("sop.%s", execution.Status),
        Source: "sop-engine",
        Data: map[string]interface{}{
            "execution_id": execution.ID,
            "sop_name":     sop.Name,
            "status":       execution.Status,
        },
    })
    
    // 从活跃列表移除
    e.mu.Lock()
    delete(e.executions, execution.ID)
    e.mu.Unlock()
}

// handleStepError 处理步骤错误
func (e *Engine) handleStepError(ctx context.Context, execution *Execution, step *Step, err error) bool {
    // 检查是否有重试配置
    if step.Retry != nil && execution.GetStepRetryCount(step.ID) < step.Retry.MaxAttempts {
        execution.IncrementRetry(step.ID)
        time.Sleep(step.Retry.CalculateBackoff(execution.GetStepRetryCount(step.ID)))
        return true // 重试当前步骤
    }
    
    // 检查错误处理策略
    if step.OnError == "continue" {
        return true // 继续下一步
    }
    
    // 记录错误并终止
    execution.SetError(err)
    return false
}

// determineNextStep 确定下一步
func (e *Engine) determineNextStep(sop *SOP, currentStep *Step, result *StepResult) *Step {
    // 根据步骤类型和结果确定下一步
    switch currentStep.Type {
    case "condition":
        if result.Outputs["condition"] == true {
            return sop.GetStep(currentStep.Then)
        }
        return sop.GetStep(currentStep.Else)
        
    case "switch":
        value := result.Outputs["value"]
        for _, c := range currentStep.Cases {
            if c.Matches(value) {
                return sop.GetStep(c.Then)
            }
        }
        return sop.GetStep(currentStep.Default)
        
    default:
        // 默认使用步骤定义的下一个步骤
        if currentStep.Next != "" {
            return sop.GetStep(currentStep.Next)
        }
        return nil
    }
}

// Approve 审批SOP执行
func (e *Engine) Approve(ctx context.Context, executionID string, approver string, approved bool, comment string) error {
    e.mu.RLock()
    execution, ok := e.executions[executionID]
    e.mu.RUnlock()
    
    if !ok {
        // 从存储加载
        var err error
        execution, err = e.store.GetExecution(ctx, executionID)
        if err != nil {
            return fmt.Errorf("execution not found: %w", err)
        }
    }
    
    if execution.Status != StatusWaiting {
        return fmt.Errorf("execution is not waiting for approval")
    }
    
    approvalStep := execution.CurrentStep
    if approvalStep.Type != "approval" {
        return fmt.Errorf("current step is not an approval step")
    }
    
    // 验证审批人权限
    if !approvalStep.CanApprove(approver) {
        return fmt.Errorf("user %s is not authorized to approve", approver)
    }
    
    // 处理审批结果
    if approved {
        execution.Approve(approver, comment)
        // 触发继续执行
        // ...
    } else {
        execution.Reject(approver, comment)
    }
    
    return e.saveExecution(ctx, execution)
}
```

### 9.3 技能实现示例

```go
// skills/k8s/pod_checker.go
package k8s

import (
    "context"
    "fmt"
    
    metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
    "k8s.io/client-go/kubernetes"
    "k8s.io/client-go/rest"
    
    "ops-inspector/pkg/checker"
)

// PodChecker Pod健康检查器
type PodChecker struct {
    clientset *kubernetes.Clientset
}

// NewPodChecker 创建Pod检查器
func NewPodChecker() (*PodChecker, error) {
    config, err := rest.InClusterConfig()
    if err != nil {
        return nil, err
    }
    
    clientset, err := kubernetes.NewForConfig(config)
    if err != nil {
        return nil, err
    }
    
    return &PodChecker{clientset: clientset}, nil
}

// Name 返回检查器名称
func (c *PodChecker) Name() string {
    return "k8s-pod-health"
}

// Type 返回检查器类型
func (c *PodChecker) Type() string {
    return "kubernetes"
}

// Description 返回描述
func (c *PodChecker) Description() string {
    return "检查Kubernetes Pod的健康状态"
}

// Check 执行检查
func (c *PodChecker) Check(ctx context.Context, target checker.Target, config map[string]interface{}) (*checker.Result, error) {
    namespace := config["namespace"].(string)
    podName := config["pod_name"].(string)
    
    // 获取Pod
    pod, err := c.clientset.CoreV1().Pods(namespace).Get(ctx, podName, metav1.GetOptions{})
    if err != nil {
        return &checker.Result{
            Status:  checker.StatusCritical,
            Message: fmt.Sprintf("Failed to get pod: %v", err),
        }, nil
    }
    
    // 分析Pod状态
    var status checker.Status
    var message string
    restartCount := 0
    
    // 计算重启次数
    for _, containerStatus := range pod.Status.ContainerStatuses {
        restartCount += int(containerStatus.RestartCount)
    }
    
    switch pod.Status.Phase {
    case "Running":
        // 检查容器状态
        allReady := true
        for _, condition := range pod.Status.Conditions {
            if condition.Type == "Ready" && condition.Status != "True" {
                allReady = false
                break
            }
        }
        
        if allReady && restartCount == 0 {
            status = checker.StatusHealthy
            message = "Pod is running and healthy"
        } else if restartCount > 0 {
            status = checker.StatusWarning
            message = fmt.Sprintf("Pod is running but has %d restarts", restartCount)
        } else {
            status = checker.StatusWarning
            message = "Pod is running but not ready"
        }
        
    case "Pending":
        status = checker.StatusWarning
        message = "Pod is pending"
        
    case "Failed":
        status = checker.StatusCritical
        message = fmt.Sprintf("Pod has failed: %s", pod.Status.Reason)
        
    case "Succeeded":
        status = checker.StatusHealthy
        message = "Pod has completed successfully"
        
    default:
        status = checker.StatusUnknown
        message = fmt.Sprintf("Unknown pod phase: %s", pod.Status.Phase)
    }
    
    // 构建输出
    outputs := map[string]interface{}{
        "status":         string(pod.Status.Phase),
        "restart_count":  restartCount,
        "pod_ip":         pod.Status.PodIP,
        "node_name":      pod.Spec.NodeName,
        "created_at":     pod.CreationTimestamp.Time,
    }
    
    // 添加事件信息
    if status != checker.StatusHealthy {
        events, _ := c.getPodEvents(ctx, namespace, podName)
        outputs["recent_events"] = events
    }
    
    return &checker.Result{
        Status:  status,
        Message: message,
        Outputs: outputs,
    }, nil
}

func (c *PodChecker) getPodEvents(ctx context.Context, namespace, podName string) ([]string, error) {
    fieldSelector := fmt.Sprintf("involvedObject.name=%s", podName)
    events, err := c.clientset.CoreV1().Events(namespace).List(ctx, metav1.ListOptions{
        FieldSelector: fieldSelector,
    })
    if err != nil {
        return nil, err
    }
    
    var eventMessages []string
    for _, event := range events.Items {
        eventMessages = append(eventMessages, fmt.Sprintf("[%s] %s: %s", 
            event.LastTimestamp.Time.Format("2006-01-02 15:04:05"),
            event.Reason,
            event.Message))
    }
    
    return eventMessages, nil
}
```

### 9.4 API实现

```go
// internal/api/handlers.go
package api

import (
    "net/http"
    
    "github.com/gin-gonic/gin"
    
    "ops-inspector/internal/sop"
    "ops-inspector/pkg/inspector"
)

// Handler API处理器
type Handler struct {
    scheduler  inspector.Scheduler
    sopEngine  *sop.Engine
    inspector  inspector.Engine
}

// NewHandler 创建处理器
func NewHandler(scheduler inspector.Scheduler, sopEngine *sop.Engine, insp inspector.Engine) *Handler {
    return &Handler{
        scheduler: scheduler,
        sopEngine: sopEngine,
        inspector: insp,
    }
}

// ==================== SOP API ====================

// CreateSOP 创建SOP
func (h *Handler) CreateSOP(c *gin.Context) {
    var req CreateSOPRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
        return
    }
    
    sop, err := sop.ParseYAML([]byte(req.Definition))
    if err != nil {
        c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
        return
    }
    
    // 验证SOP
    if err := sop.Validate(); err != nil {
        c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
        return
    }
    
    // 保存SOP
    if err := h.sopEngine.Store().CreateSOP(c.Request.Context(), sop); err != nil {
        c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
        return
    }
    
    c.JSON(http.StatusCreated, SOPResponse{SOP: sop})
}

// ExecuteSOP 执行SOP
func (h *Handler) ExecuteSOP(c *gin.Context) {
    sopID := c.Param("id")
    
    var req ExecuteSOPRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
        return
    }
    
    // 获取SOP
    sop, err := h.sopEngine.Store().GetSOP(c.Request.Context(), sopID)
    if err != nil {
        c.JSON(http.StatusNotFound, ErrorResponse{Error: "SOP not found"})
        return
    }
    
    // 执行SOP
    executionID, err := h.sopEngine.Execute(c.Request.Context(), sop, req.Inputs)
    if err != nil {
        c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
        return
    }
    
    c.JSON(http.StatusAccepted, ExecuteSOPResponse{
        ExecutionID: executionID,
        Status:      "started",
    })
}

// GetSOPExecution 获取SOP执行状态
func (h *Handler) GetSOPExecution(c *gin.Context) {
    executionID := c.Param("executionId")
    
    execution, err := h.sopEngine.Store().GetExecution(c.Request.Context(), executionID)
    if err != nil {
        c.JSON(http.StatusNotFound, ErrorResponse{Error: "Execution not found"})
        return
    }
    
    c.JSON(http.StatusOK, ExecutionResponse{Execution: execution})
}

// ApproveSOP 审批SOP
func (h *Handler) ApproveSOP(c *gin.Context) {
    executionID := c.Param("executionId")
    
    var req ApproveRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
        return
    }
    
    // 获取当前用户
    user := c.GetString("user")
    
    if err := h.sopEngine.Approve(c.Request.Context(), executionID, user, req.Approved, req.Comment); err != nil {
        c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
        return
    }
    
    c.JSON(http.StatusOK, gin.H{"status": "success"})
}

// ==================== Inspection API ====================

// CreateInspection 创建巡检任务
func (h *Handler) CreateInspection(c *gin.Context) {
    var req CreateInspectionRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
        return
    }
    
    inspection := &inspector.Inspection{
        Name:        req.Name,
        Schedule:    req.Schedule,
        Checkers:    req.Checkers,
        Targets:     req.Targets,
        Notification: req.Notification,
    }
    
    if err := h.scheduler.CreateJob(c.Request.Context(), inspection.ToJob()); err != nil {
        c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
        return
    }
    
    c.JSON(http.StatusCreated, InspectionResponse{Inspection: inspection})
}

// RunInspection 立即执行巡检
func (h *Handler) RunInspection(c *gin.Context) {
    inspectionID := c.Param("id")
    
    if err := h.scheduler.TriggerJob(c.Request.Context(), inspectionID); err != nil {
        c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
        return
    }
    
    c.JSON(http.StatusAccepted, gin.H{"status": "triggered"})
}

// GetInspectionResult 获取巡检结果
func (h *Handler) GetInspectionResult(c *gin.Context) {
    resultID := c.Param("resultId")
    
    result, err := h.inspector.GetResult(c.Request.Context(), resultID)
    if err != nil {
        c.JSON(http.StatusNotFound, ErrorResponse{Error: "Result not found"})
        return
    }
    
    c.JSON(http.StatusOK, InspectionResultResponse{Result: result})
}

// ==================== Skill API ====================

// ListSkills 列出所有技能
func (h *Handler) ListSkills(c *gin.Context) {
    skills := h.sopEngine.SkillRegistry().List()
    c.JSON(http.StatusOK, SkillsResponse{Skills: skills})
}

// ExecuteSkill 执行技能
func (h *Handler) ExecuteSkill(c *gin.Context) {
    skillName := c.Param("name")
    
    var req ExecuteSkillRequest
    if err := c.ShouldBindJSON(&req); err != nil {
        c.JSON(http.StatusBadRequest, ErrorResponse{Error: err.Error()})
        return
    }
    
    output, err := h.sopEngine.SkillRegistry().Execute(c.Request.Context(), skillName, req.Inputs)
    if err != nil {
        c.JSON(http.StatusInternalServerError, ErrorResponse{Error: err.Error()})
        return
    }
    
    c.JSON(http.StatusOK, SkillOutputResponse{Output: output})
}
```

### 9.5 客户端SDK示例

```python
# Python SDK示例
# ops_inspector/client.py

from typing import Dict, Any, Optional
import requests
import json
from dataclasses import dataclass
from enum import Enum

class SOPStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    WAITING = "waiting"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class SOPExecution:
    id: str
    sop_name: str
    status: SOPStatus
    current_step: Optional[str]
    started_at: str
    completed_at: Optional[str]

class OpsInspectorClient:
    """Ops Inspector API客户端"""
    
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })
    
    def create_sop(self, definition: str) -> Dict[str, Any]:
        """创建SOP"""
        response = self.session.post(
            f'{self.base_url}/api/v1/sops',
            json={'definition': definition}
        )
        response.raise_for_status()
        return response.json()
    
    def execute_sop(self, sop_id: str, inputs: Dict[str, Any]) -> str:
        """执行SOP，返回执行ID"""
        response = self.session.post(
            f'{self.base_url}/api/v1/sops/{sop_id}/execute',
            json={'inputs': inputs}
        )
        response.raise_for_status()
        return response.json()['execution_id']
    
    def get_execution(self, execution_id: str) -> SOPExecution:
        """获取执行状态"""
        response = self.session.get(
            f'{self.base_url}/api/v1/sop-executions/{execution_id}'
        )
        response.raise_for_status()
        data = response.json()
        return SOPExecution(
            id=data['id'],
            sop_name=data['sop_name'],
            status=SOPStatus(data['status']),
            current_step=data.get('current_step'),
            started_at=data['started_at'],
            completed_at=data.get('completed_at')
        )
    
    def approve_execution(self, execution_id: str, approved: bool, comment: str = '') -> None:
        """审批执行"""
        response = self.session.post(
            f'{self.base_url}/api/v1/sop-executions/{execution_id}/approve',
            json={'approved': approved, 'comment': comment}
        )
        response.raise_for_status()
    
    def wait_for_completion(self, execution_id: str, timeout: int = 300) -> SOPExecution:
        """等待SOP执行完成"""
        import time
        start = time.time()
        while time.time() - start < timeout:
            execution = self.get_execution(execution_id)
            if execution.status in [SOPStatus.COMPLETED, SOPStatus.FAILED]:
                return execution
            if execution.status == SOPStatus.WAITING:
                raise Exception(f"Execution {execution_id} is waiting for approval")
            time.sleep(2)
        raise TimeoutError(f"Execution {execution_id} did not complete within {timeout}s")

# 使用示例
if __name__ == '__main__':
    client = OpsInspectorClient(
        base_url='https://ops-inspector.example.com',
        api_key='your-api-key'
    )
    
    # 创建SOP
    sop_yaml = '''
apiVersion: ops-inspector.io/v1
kind: SOP
metadata:
  name: restart-pod
spec:
  inputs:
    - name: namespace
    - name: pod_name
  workflow:
    - id: delete
      type: action
      action:
        skill: k8s-pod-delete
        inputs:
          namespace: ${inputs.namespace}
          pod_name: ${inputs.pod_name}
'''
    
    sop = client.create_sop(sop_yaml)
    print(f"Created SOP: {sop['id']}")
    
    # 执行SOP
    execution_id = client.execute_sop(sop['id'], {
        'namespace': 'default',
        'pod_name': 'my-app-123'
    })
    print(f"Started execution: {execution_id}")
    
    # 等待完成
    result = client.wait_for_completion(execution_id)
    print(f"Execution completed with status: {result.status}")
```

---

## 11. 最佳实践

### 10.1 SOP设计原则

```yaml
# 1. 单一职责原则
# 每个SOP专注于解决一个具体问题

# ❌ 不好的设计：一个SOP处理所有Pod问题
apiVersion: ops-inspector.io/v1
kind: SOP
metadata:
  name: pod-all-in-one  # 避免这样的命名

# ✅ 好的设计：拆分为多个专注的SOP
---
apiVersion: ops-inspector.io/v1
kind: SOP
metadata:
  name: pod-restart-on-crash  # 专注处理CrashLoopBackOff
  
---
apiVersion: ops-inspector.io/v1
kind: SOP
metadata:
  name: pod-scale-on-high-cpu  # 专注处理CPU过载

---
apiVersion: ops-inspector.io/v1
kind: SOP
metadata:
  name: pod-migrate-on-node-failure  # 专注处理节点故障


# 2. 幂等性设计
# SOP应该可以安全地重复执行

workflow:
  - id: check-already-restarted
    name: "检查是否已经重启过"
    type: check
    action:
      skill: k8s-pod-info
    outputs:
      - name: age_seconds
    
  - id: skip-if-recent
    type: condition
    condition: "${steps.check-already-restarted.outputs.age_seconds} < 60"
    then: already-restarted  # 已经重启过，跳过
    else: perform-restart
    
  - id: already-restarted
    type: notification
    action:
      skill: notify-slack
      inputs:
        message: "Pod recently restarted, skipping..."
    final: true


# 3. 合理的超时设置
# 每个步骤都应该有合理的超时时间

workflow:
  - id: wait-pod-ready
    type: wait
    condition:
      skill: k8s-pod-status
      expected: "Running"
    timeout: "5m"  # 不要太短也不要太长
    on_timeout: escalate  # 超时后升级处理
    
  - id: long-running-check
    type: check
    action:
      skill: database-consistency-check
    timeout: "30m"  # 长时间运行的检查需要更长的超时
    

# 4. 完善的错误处理
# 每个步骤都应该考虑失败情况

workflow:
  - id: critical-step
    type: action
    action:
      skill: database-failover
    retry:
      max_attempts: 3
      backoff: exponential
      initial_delay: 5s
    timeout: "10m"
    on_error: escalate  # 失败后升级
    
error_handling:
  - on: timeout
    action: notify
    target: senior-dba
  - on: max_retry_exceeded
    action: create_incident
    severity: critical


# 5. 审计和可观测性
# 记录足够的信息用于复盘

audit:
  level: detailed
  capture:
    - all_inputs
    - all_outputs
    - execution_timeline
    - decision_points
    - approval_records
```

### 10.2 巡检策略建议

```yaml
# 巡检策略配置示例
inspection_policies:
  # 1. 分层巡检
  layers:
    - name: infrastructure  # 基础设施层
      frequency: "*/5 * * * *"  # 每5分钟
      checkers:
        - node-health
        - disk-usage
        - network-connectivity
        
    - name: platform  # 平台层
      frequency: "*/10 * * * *"  # 每10分钟
      checkers:
        - k8s-component-status
        - etcd-health
        - cni-status
        
    - name: application  # 应用层
      frequency: "*/2 * * * *"  # 每2分钟
      checkers:
        - pod-health
        - service-endpoint
        - ingress-health
        
    - name: business  # 业务层
      frequency: "*/1 * * * *"  # 每分钟
      checkers:
        - api-latency
        - error-rate
        - business-metric

  # 2. 分级告警
  alert_levels:
    - name: info
      condition: "status == 'info'"
      action: log_only
      
    - name: warning
      condition: "status == 'warning'"
      action: notify_team
      channels: ["slack"]
      
    - name: critical
      condition: "status == 'critical'"
      action: trigger_sop
      sop: auto-healing
      notify: ["slack", "pagerduty"]
      
    - name: emergency
      condition: "status == 'emergency'"
      action: escalate
      notify: ["slack", "pagerduty", "sms"]
      auto_call: true

  # 3. 智能降噪
  noise_reduction:
    # 告警分组
    grouping:
      - by: ["alertname", "namespace"]
        wait: 30s
        
    # 告警抑制
    inhibition:
      - source: "node-down"
        target: "pod-unreachable"
        
    # 重复告警间隔
    repeat_interval: 4h
    
    # 静默规则
    silences:
      - matchers:
          namespace: "test"
        duration: "1h"
```

### 10.3 安全最佳实践

```yaml
# 安全配置
security:
  # 1. 最小权限原则
  rbac:
    roles:
      - name: sop-executor
        permissions:
          - resource: sops
            actions: [read, execute]
          - resource: inspections
            actions: [read]
            
      - name: sop-admin
        permissions:
          - resource: sops
            actions: [create, read, update, delete, execute]
          - resource: inspections
            actions: [create, read, update, delete]
          - resource: skills
            actions: [create, read, update, delete]
            
      - name: readonly
        permissions:
          - resource: '*'
            actions: [read]
  
  # 2. 敏感信息处理
  secrets:
    # 使用Vault等密钥管理系统
    provider: vault
    vault:
      address: https://vault.example.com
      role: ops-inspector
      
    # 运行时注入，不在配置中硬编码
    injection:
      - name: database_password
        path: secret/data/ops-inspector/database
        key: password
        
  # 3. 审计日志
  audit:
    enabled: true
    log_all_requests: true
    sensitive_fields: ["password", "token", "secret", "key"]
    
  # 4. 网络隔离
  network:
    # 仅允许特定的出站连接
    egress:
      - to: kubernetes-api
        port: 6443
      - to: prometheus
        port: 9090
      - to: nats
        port: 4222
```

### 10.4 性能优化建议

```yaml
# 性能优化配置
performance:
  # 1. 并发控制
  concurrency:
    # SOP最大并行执行数
    max_parallel_sops: 50
    
    # 单个SOP的最大并行步骤数
    max_parallel_steps_per_sop: 5
    
    # 检查器并发数
    max_concurrent_checks: 100
    
  # 2. 缓存策略
  caching:
    # Skill结果缓存
    skill_results:
      enabled: true
      ttl: 30s
      max_size: 10000
      
    # K8s资源缓存
    k8s_resources:
      enabled: true
      ttl: 10s
      
  # 3. 数据库优化
  database:
    # 连接池
    pool_size: 20
    max_overflow: 10
    pool_timeout: 30s
    
    # 读写分离
    replicas:
      - host: read-replica-1
      - host: read-replica-2
      
  # 4. 批处理
  batching:
    # 事件批量处理
    events:
      size: 100
      timeout: 1s
      
    # 告警批量发送
    alerts:
      size: 50
      timeout: 5s
```

---

## 附录

### A. 术语表

| 术语 | 英文 | 说明 |
|------|------|------|
| SOP | Standard Operating Procedure | 标准作业程序，定义运维操作的标准流程 |
| Skill | Skill | 技能，系统中最小的可执行单元 |
| Inspector | Inspector | 巡检器，负责执行各类检查任务 |
| Healer | Healer | 修复器，负责执行故障修复操作 |
| Checker | Checker | 检查器，具体执行某项检查的技能 |
| Remediator | Remediator | 修复技能，具体执行某项修复操作 |
| Event Bus | Event Bus | 事件总线，负责事件的发布和订阅 |
| Execution | Execution | SOP的执行实例 |
| Step | Step | SOP中的执行步骤 |

### B. API参考

详见 [API文档](./API.md)

### C. 路线图

- **v1.0** - 基础功能：SOP引擎、巡检、基础技能
- **v1.1** - 可视化：Web UI、流程图编排
- **v1.2** - AI增强：智能诊断、异常预测
- **v1.3** - 生态扩展：更多开箱即用技能、第三方集成
- **v2.0** - 自治运维：全自动故障处理、容量管理

### D. 贡献指南

欢迎贡献代码和想法！请参考 [CONTRIBUTING.md](./CONTRIBUTING.md)

---

**文档结束**
