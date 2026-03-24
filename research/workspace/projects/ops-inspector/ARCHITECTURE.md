# OpsInspector 架构图

## 1. 整体架构图

```mermaid
flowchart TB
    subgraph UserLayer["用户交互层"]
        WebUI["Web UI"]
        CLI["CLI"]
        APIGW["API Gateway"]
        GitOps["GitOps (Flux)"]
    end

    subgraph ControlPlane["控制平面层 (Control Plane)"]
        subgraph InspectorOperator["Inspector Operator"]
            IC["Inspector\nController"]
            TS["Task\nScheduler"]
            EB["Event\nBus"]
            RC["Remediation\nController"]
        end
        
        subgraph ConfigMgmt["配置管理"]
            CRD["CRD (Spec)"]
            CM["ConfigMap"]
            Secret["Secret"]
            PolicyDB["Policy DB"]
        end
    end

    subgraph ExecutionLayer["巡检执行层"]
        subgraph SkillRuntime["Skill Runtime"]
            K8sSkill["Kubernetes\nSkill"]
            DockerSkill["Docker\nSkill"]
            SSHSkill["SSH\nSkill"]
            APISkill["API\nSkill"]
            NetworkSkill["Network\nSkill"]
            DBSkill["Database\nSkill"]
        end
        
        subgraph Adapters["执行适配器"]
            K8sClient["K8s Client"]
            DockerSDK["Docker SDK"]
            SSHClient["SSH/SCP"]
            HTTPClient["HTTP Client"]
        end
    end

    subgraph DataLayer["数据与通知层"]
        subgraph Storage["存储"]
            VM["VictoriaMetrics"]
            PG["PostgreSQL"]
        end
        
        subgraph EventBus["事件总线"]
            NATS["NATS\nJetStream"]
            CE["CloudEvents"]
        end
        
        subgraph Notification["通知通道"]
            Email["Email"]
            Slack["Slack"]
            Discord["Discord"]
            PagerDuty["PagerDuty"]
            Webhook["Webhook"]
        end
    end

    subgraph TargetLayer["监控目标层"]
        subgraph Container["容器平台"]
            K8s["Kubernetes"]
            Docker["Docker"]
        end
        
        subgraph Business["业务系统"]
            API["API Services"]
            MS["Microservices"]
        end
        
        subgraph Infra["基础设施"]
            Server["Servers"]
            Network["Network"]
            DB["Databases"]
        end
    end

    UserLayer --> ControlPlane
    ControlPlane --> ExecutionLayer
    ExecutionLayer --> Adapters
    Adapters --> TargetLayer
    ControlPlane <--> DataLayer
    ExecutionLayer --> Storage
    EventBus --> Notification
```

## 2. 控制循环流程

```mermaid
flowchart LR
    Watch["Watch CR"] --> Diff["Diff State"]
    Diff --> Reconcile["Reconcile"]
    Reconcile --> Update["Update Status"]
    Update --> Watch
    
    style Watch fill:#e1f5fe
    style Diff fill:#fff3e0
    style Reconcile fill:#e8f5e9
    style Update fill:#fce4ec
```

## 3. 事件驱动流程

```mermaid
sequenceDiagram
    participant Target as 监控目标
    participant Adapter as 执行适配器
    participant Skill as Skill
    participant EventBus as Event Bus
    participant Controller as Controller
    participant Notifier as 通知通道

    Target->>Adapter: 产生事件/指标
    Adapter->>Skill: 执行巡检
    Skill->>EventBus: 发布巡检事件
    EventBus->>Controller: 订阅事件
    
    alt 发现异常
        Controller->>Controller: 决策自动修复
        Controller->>Target: 执行修复动作
        Controller->>EventBus: 发布修复事件
    end
    
    EventBus->>Notifier: 路由通知
    Notifier->>Notifier: Slack/Email/...
```

## 4. Skill执行流程

```mermaid
flowchart TB
    subgraph Task["巡检任务"]
        Start["开始"] --> Validate["参数验证"]
        Validate --> CheckDeps["依赖检查"]
        CheckDeps --> Execute["执行Skill"]
        Execute --> Collect["收集结果"]
        Collect --> Analyze["分析结果"]
        Analyze --> Alert["触发告警?"]
        Alert -->|是| Notify["发送通知"]
        Alert -->|否| End["结束"]
        Notify --> End
    end
    
    subgraph Remediation["自动修复"]
        Detect["检测异常"] --> Policy["匹配策略"]
        Policy --> Approve["需要审批?"]
        Approve -->|是| Wait["等待审批"]
        Approve -->|否| AutoExec["自动执行"]
        Wait -->|批准| AutoExec
        Wait -->|拒绝| Cancel["取消修复"]
        AutoExec --> Record["记录变更"]
        Cancel --> End2["结束"]
        Record --> End2
    end
    
    Alert -.->|触发| Detect
```

## 5. 部署架构

```mermaid
flowchart TB
    subgraph K8sCluster["Kubernetes Cluster"]
        subgraph Ingress["Ingress Layer"]
            ING["Ingress Controller"]
        end
        
        subgraph APILayer["API Layer"]
            API1["API Pod 1"]
            API2["API Pod 2"]
        end
        
        subgraph ControllerLayer["Controller Layer"]
            C1["Controller 1\n(Leader)"]
            C2["Controller 2\n(Standby)"]
            C3["Controller 3\n(Standby)"]
        end
        
        subgraph RunnerLayer["Skill Runner Layer"]
            R1["Runner 1"]
            R2["Runner 2"]
            R3["Runner 3"]
        end
    end
    
    subgraph DataLayer["Data Layer"]
        NATS["NATS Cluster"]
        PG[("PostgreSQL\nHA")]
        VM[("VictoriaMetrics")]
    end

    ING --> API1
    ING --> API2
    API1 --> C1
    API2 --> C1
    C1 --> R1
    C1 --> R2
    C1 --> R3
    C1 <--> DataLayer
    
    style C1 fill:#e8f5e9
    style C2 fill:#fff3e0
    style C3 fill:#fff3e0
```

## 6. 数据流图

```mermaid
flowchart LR
    subgraph Sources["数据源"]
        Metrics["Metrics"]
        Logs["Logs"]
        Events["Events"]
        Traces["Traces"]
    end
    
    subgraph Collection["采集层"]
        OTel["OpenTelemetry"]
        Exporters["Exporters"]
    end
    
    subgraph Processing["处理层"]
        Skills["Skills"]
        Rules["Rule Engine"]
        ML["ML Analysis"]
    end
    
    subgraph Storage["存储层"]
        TSDB["Time Series DB"]
        RelDB["Relational DB"]
        ObjStore["Object Store"]
    end
    
    subgraph Consumption["消费层"]
        Dashboard["Dashboard"]
        Alerts["Alerts"]
        Reports["Reports"]
        API["API"]
    end
    
    Sources --> Collection
    Collection --> Processing
    Processing --> Storage
    Storage --> Consumption
```

## 7. 通知路由流程

```mermaid
flowchart TB
    Alert["告警事件"] --> Router["路由引擎"]
    
    Router --> Condition1{"Severity == Critical?"}
    Condition1 -->|是| Immediate["立即发送"]
    Condition1 -->|否| Condition2{"工作时间?"}
    
    Condition2 -->|是| Batch["批量处理"]
    Condition2 -->|否| Silence["静默/延迟"]
    
    Immediate --> Slack["Slack"]
    Immediate --> PagerDuty["PagerDuty"]
    Immediate --> SMS["SMS"]
    
    Batch --> Email["Email"]
    Batch --> Dashboard["Dashboard"]
    
    Silence --> Schedule["定时汇总"]
    Schedule --> Email

    style Alert fill:#ffebee
    style Immediate fill:#ffebee
    style PagerDuty fill:#ffebee
    style SMS fill:#ffebee
```

## 8. 多层级配置架构

```mermaid
flowchart TB
    subgraph ConfigLayers["配置层级"]
        direction TB
        L1["L1: 系统默认\n/etc/opsinspector/defaults.yaml"]
        L2["L2: 全局配置\nConfigMap / 环境变量"]
        L3["L3: 命名空间配置\nnamespace ConfigMap"]
        L4["L4: Inspector配置\nCRD spec.parameters"]
        L5["L5: 运行时参数\nAPI参数 / CLI参数"]
    end
    
    L1 --> L2
    L2 --> L3
    L3 --> L4
    L4 --> L5
    
    style L5 fill:#e8f5e9
```

## 9. 自动修复决策流程

```mermaid
flowchart TB
    Trigger["告警触发"] --> Enabled{"自动修复\n已启用?"}
    
    Enabled -->|否| NotifyOnly["仅通知"]
    Enabled -->|是| Window{"在修复窗口?"}
    
    Window -->|否| ScheduleLater["计划稍后执行"]
    Window -->|是| RateLimit{"频率限制\n检查通过?"}
    
    RateLimit -->|否| RateLimitMsg["跳过(频率限制)"]
    RateLimit -->|是| Policy{"需要审批?"}
    
    Policy -->|是| Approval["发送审批请求"]
    Policy -->|否| Execute["执行修复"]
    
    Approval -->|批准| Execute
    Approval -->|拒绝| Rejected["修复被拒绝"]
    
    Execute --> Success{"执行成功?"}
    Success -->|是| Record["记录变更"]
    Success -->|否| Rollback["尝试回滚"]
    
    NotifyOnly --> End["结束"]
    ScheduleLater --> End
    RateLimitMsg --> End
    Rejected --> End
    Record --> End
    Rollback --> End

    style Trigger fill:#ffebee
    style Execute fill:#e8f5e9
    style Record fill:#e1f5fe
    style Rejected fill:#fff3e0
```

## 10. Skill生命周期

```mermaid
stateDiagram-v2
    [*] --> Registered: Register Skill
    Registered --> Validated: Validate
    Validated --> Ready: Load Dependencies
    
    Ready --> Executing: Trigger Inspection
    Executing --> Succeeded: Success
    Executing --> Failed: Error
    Executing --> Timeout: Timeout
    
    Succeeded --> Ready: Reset
    Failed --> Retrying: Retry
    Timeout --> Retrying: Retry
    
    Retrying --> Executing: Retry Attempt
    Retrying --> Failed: Max Retries
    
    Failed --> [*]: Archive
    Succeeded --> [*]: Archive
```

## 11. 技术栈映射

```mermaid
flowchart LR
    subgraph Lang["语言"]
        Go["Go"]
    end
    
    subgraph Framework["框架"]
        Kubebuilder["Kubebuilder"]
        ControllerRuntime["controller-runtime"]
    end
    
    subgraph Messaging["消息"]
        NATS["NATS JetStream"]
        CE["CloudEvents"]
    end
    
    subgraph Storage["存储"]
        VM["VictoriaMetrics"]
        PG["PostgreSQL"]
        Redis["Redis"]
    end
    
    subgraph Observability["可观测性"]
        OTel["OpenTelemetry"]
        Prometheus["Prometheus"]
        Jaeger["Jaeger"]
    end
    
    subgraph Notification["通知"]
        Webhook["Webhook"]
        SlackSDK["Slack SDK"]
        EmailLib["Email"]
    end
    
    Lang --> Framework
    Framework --> Messaging
    Framework --> Storage
    Framework --> Observability
    Framework --> Notification
```
