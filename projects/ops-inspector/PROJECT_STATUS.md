# OpsInspector - 运维巡检Agent系统

## ✅ 项目状态：核心功能已完善

### 📊 已完成内容

#### 1. 巡检插件（新增 4 个）

| 插件 | 文件 | 功能 |
|------|------|------|
| **HTTP** | `plugins/inspectors/http.go` | HTTP/HTTPS 健康检查，支持状态码、响应时间、内容匹配 |
| **K8s Pod** | `plugins/inspectors/k8s_pod.go` | Kubernetes Pod 状态检查，支持重启次数、资源使用监控 |
| **磁盘** | `plugins/inspectors/system.go` | 磁盘空间使用率检查，可配置告警阈值 |
| **内存** | `plugins/inspectors/system.go` | 内存使用率检查，支持可用内存监控 |

#### 2. SOP 引擎

**文件**: `pkg/sop/engine.go`

**功能**:
- YAML 定义标准操作流程
- 条件执行（支持步骤条件判断）
- 变量替换和传递
- 失败处理策略（abort/continue）
- 异步执行
- 内置动作：
  - `http:request` - HTTP 请求
  - `k8s:get` - K8s 资源获取
  - `k8s:delete` - K8s 资源删除
  - `notify:send` - 发送通知
  - `exec:command` - 执行命令

**示例**: `examples/sops/restart-crashloop-pod.yaml`

#### 3. Prometheus 指标

**文件**: `pkg/observability/metrics.go`

**指标列表**:

| 指标 | 类型 | 说明 |
|------|------|------|
| `opsinspector_inspection_runs_total` | Counter | 巡检执行次数，标签: inspector, status |
| `opsinspector_inspection_duration_seconds` | Histogram | 巡检执行时长，标签: inspector |
| `opsinspector_inspection_queue_size` | Gauge | 队列大小 |
| `opsinspector_sop_executions_total` | Counter | SOP 执行次数，标签: sop_name, status |
| `opsinspector_sop_execution_duration_seconds` | Histogram | SOP 执行时长，标签: sop_name |
| `opsinspector_worker_tasks_processed_total` | Counter | Worker 处理任务数，标签: worker_id, status |
| `opsinspector_worker_active_tasks` | Gauge | 活跃任务数 |
| `opsinspector_worker_pool_size` | Gauge | Worker 池大小 |
| `opsinspector_notifications_total` | Counter | 通知发送次数，标签: channel, status |
| `opsinspector_api_requests_total` | Counter | API 请求数，标签: method, path, status |
| `opsinspector_api_request_duration_seconds` | Histogram | API 请求时长，标签: method, path |
| `opsinspector_db_connections_active` | Gauge | 活跃数据库连接数 |
| `opsinspector_db_connections_idle` | Gauge | 空闲数据库连接数 |

**端点**: `http://localhost:9091/metrics`

---

### 🚀 快速开始

#### 1. 启动 MySQL
```bash
kubectl apply -f deploy/kubernetes/mysql.yaml
```

#### 2. 运行迁移
```bash
cd projects/ops-inspector
go run ./cmd/migrate
```

#### 3. 启动服务
```bash
# 终端 1: API Server
go run ./cmd/api

# 终端 2: Scheduler
go run ./cmd/scheduler

# 终端 3: Worker
go run ./cmd/worker
```

#### 4. 查看指标
```bash
# Prometheus 指标
curl http://localhost:9091/metrics

# 健康检查
curl http://localhost:8080/health
curl http://localhost:8080/ready
```

---

### 📡 API 使用示例

#### 创建 HTTP 巡检任务
```bash
curl -X POST http://localhost:8080/api/v1/inspections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "google-health-check",
    "type": "http",
    "schedule": "*/5 * * * *",
    "config": {
      "url": "https://www.google.com",
      "method": "GET",
      "timeout": 10,
      "expected_status": 200
    },
    "notify_channels": ["webhook"]
  }'
```

#### 创建磁盘巡检任务
```bash
curl -X POST http://localhost:8080/api/v1/inspections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "disk-usage-check",
    "type": "disk",
    "schedule": "0 */1 * * *",
    "config": {
      "paths": ["/", "/data"],
      "warning_threshold": 80,
      "critical_threshold": 90
    }
  }'
```

#### 创建 K8s Pod 巡检任务
```bash
curl -X POST http://localhost:8080/api/v1/inspections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "k8s-pod-check",
    "type": "k8s-pod",
    "schedule": "*/10 * * * *",
    "config": {
      "namespace": "default",
      "selector": "app=web",
      "max_restarts": 3,
      "check_status": true,
      "check_resources": true
    }
  }'
```

#### 创建 SOP
```bash
curl -X POST http://localhost:8080/api/v1/sops \
  -H "Content-Type: application/json" \
  -d '{
    "name": "restart-crashloop-pod",
    "description": "自动处理 CrashLoopBackOff 状态的 Pod",
    "version": "1.0.0",
    "definition": {
      "timeout": "10m",
      "onFailure": "abort",
      "variables": {
        "namespace": {"type": "string", "default": "default"},
        "max_restarts": {"type": "integer", "default": 3}
      },
      "steps": [
        {"id": "get-pod-info", "name": "获取 Pod 信息", "action": "k8s:get", "input": {"resource": "pod", "namespace": "${namespace}"}},
        {"id": "delete-pod", "name": "删除 Pod", "action": "k8s:delete", "condition": "restartCount > ${max_restarts}", "input": {"resource": "pod", "namespace": "${namespace}"}},
        {"id": "notify", "name": "发送通知", "action": "notify:send", "input": {"channels": ["dingtalk"], "title": "Pod 已自动恢复"}}
      ]
    }
  }'
```

#### 执行 SOP
```bash
curl -X POST http://localhost:8080/api/v1/sops/{sop-id}/execute \
  -H "Content-Type: application/json" \
  -d '{
    "namespace": "production",
    "max_restarts": 5
  }'
```

---

### 📈 Grafana 仪表盘配置

Prometheus 指标采集配置：

```yaml
scrape_configs:
  - job_name: 'opsinspector'
    static_configs:
      - targets: ['localhost:9091']
    metrics_path: /metrics
```

建议监控的图表：
1. **巡检成功率** - `opsinspector_inspection_runs_total` by status
2. **平均执行时长** - `opsinspector_inspection_duration_seconds`
3. **队列积压** - `opsinspector_inspection_queue_size`
4. **Worker 负载** - `opsinspector_worker_active_tasks`
5. **API QPS** - rate(`opsinspector_api_requests_total`[1m])

---

### 🏗️ 项目结构

```
projects/ops-inspector/
├── cmd/
│   ├── api/                    # API 服务器 (端口 8080)
│   ├── scheduler/              # 定时调度器
│   ├── worker/                 # 任务执行器（带 Prometheus 指标）
│   └── migrate/                # 数据库迁移工具
├── pkg/
│   ├── config/                 # 配置管理
│   ├── models/                 # 数据模型 (MySQL)
│   ├── store/                  # GORM 数据库操作
│   ├── queue/                  # 任务队列
│   ├── scheduler/              # Cron 调度器
│   ├── worker/                 # Worker 执行器
│   ├── inspector/              # 巡检器接口
│   ├── notification/           # 通知渠道
│   ├── sop/                    # ✅ SOP 引擎
│   └── observability/          # ✅ Prometheus 指标
├── plugins/
│   └── inspectors/
│       ├── http.go             # ✅ HTTP 检查
│       ├── k8s_pod.go          # ✅ K8s Pod 检查
│       └── system.go           # ✅ 磁盘/内存检查
├── examples/
│   └── sops/                   # ✅ SOP 示例
├── database/migrations/        # MySQL 迁移脚本
├── deploy/kubernetes/          # K8s 部署文件
└── configs/config.yaml         # 配置文件
```

---

### ⚠️ 注意事项

1. **数据库**: 默认使用 `kubectl run` 启动的 MySQL，DNS 地址为 `mysql.default.svc.cluster.local`
2. **队列**: 当前使用内存队列，生产环境建议使用 Redis
3. **K8s 检查**: 需要 kubectl 在 PATH 中，或使用 service account 权限
4. **SOP 动作**: 当前为简化实现，生产环境需要完善错误处理和重试逻辑
5. **通知渠道**: 当前仅支持 Webhook，可扩展钉钉/飞书等

---

### 📚 后续优化方向

- [ ] Redis 队列实现
- [ ] 钉钉/飞书通知渠道
- [ ] 更多 SOP 动作（Shell 执行、API 调用）
- [ ] SOP 执行状态查询 API
- [ ] Web Dashboard
- [ ] 告警降噪策略
- [ ] 分布式锁（防止重复执行）
- [ ] 巡检结果历史趋势分析

---

**状态**: 核心框架已完成，支持 HTTP/K8s/系统资源巡检，SOP 引擎可用，Prometheus 指标已暴露
**位置**: `projects/ops-inspector/`
