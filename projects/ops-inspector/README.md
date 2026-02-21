# OpsInspector - 运维巡检Agent系统

基于 Go + MySQL 的运维巡检平台，实现主动发现、自动诊断、智能修复。

## 快速开始

### 1. 启动 MySQL

```bash
# 在 Kubernetes 中启动 MySQL
kubectl run mysql \
  --image=mysql:8.0 \
  --env="MYSQL_ROOT_PASSWORD=opsinspector" \
  --env="MYSQL_DATABASE=opsinspector" \
  --port=3306 \
  --expose=true

# 或使用 deployment
kubectl apply -f deploy/kubernetes/mysql.yaml
```

### 2. 配置数据库连接

编辑 `configs/config.yaml`：
```yaml
database:
  dsn: "root:opsinspector@tcp(mysql.default.svc.cluster.local:3306)/opsinspector?charset=utf8mb4&parseTime=True&loc=Local"
```

### 3. 运行数据库迁移

```bash
make migrate
```

### 4. 启动服务

```bash
# 方式1: 本地启动（开发模式）
make dev

# 方式2: Docker 启动
make docker-build
make docker-run

# 方式3: Kubernetes 部署
make k8s-deploy
```

## 架构组件

```
┌─────────────────────────────────────────────────────────────┐
│  API Server (cmd/api)        │  提供 REST API 和 WebSocket   │
├─────────────────────────────────────────────────────────────┤
│  Scheduler (cmd/scheduler)   │  定时任务调度和事件处理        │
├─────────────────────────────────────────────────────────────┤
│  Worker (cmd/worker)         │  执行巡检任务和 SOP           │
└─────────────────────────────────────────────────────────────┘
```

## 项目结构

```
.
├── cmd/                    # 可执行程序入口
│   ├── api/               # API 服务器
│   ├── scheduler/         # 调度器服务
│   └── worker/            # Worker 节点
├── pkg/                   # 核心库
│   ├── config/           # 配置管理
│   ├── models/           # 数据模型
│   ├── store/            # 数据库操作
│   ├── queue/            # 任务队列
│   ├── scheduler/        # 调度逻辑
│   ├── worker/           # 任务执行
│   ├── inspector/        # 巡检插件接口
│   ├── notification/     # 通知渠道
│   ├── sop/              # SOP 引擎
│   └── observability/    # 可观测性
├── plugins/              # 插件目录
│   ├── inspectors/       # 巡检插件
│   ├── channels/         # 通知渠道插件
│   └── actions/          # 执行动作插件
├── database/             # 数据库相关
│   └── migrations/       # 迁移脚本
├── deploy/               # 部署文件
│   ├── docker/           # Docker 配置
│   └── kubernetes/       # K8s 配置
└── configs/              # 配置文件
```

## 核心特性

- **插件化架构**: 支持 Go Plugin/WASM 扩展
- **SOP 引擎**: YAML 定义的标准操作流程
- **多渠道通知**: 钉钉、飞书、邮件、Slack、Webhook
- **可观测性**: Prometheus + OpenTelemetry
- **云原生**: Kubernetes Native 设计

## 开发

```bash
# 安装依赖
make deps

# 运行测试
make test

# 代码检查
make lint

# 构建所有组件
make build
```

## API 示例

### 创建巡检任务

```bash
curl -X POST http://localhost:8080/api/v1/inspections \
  -H "Content-Type: application/json" \
  -d '{
    "name": "api-health-check",
    "type": "http",
    "schedule": "*/5 * * * *",
    "config": {
      "url": "https://api.example.com/health",
      "method": "GET",
      "timeout": 10
    },
    "notify_channels": ["dingtalk"]
  }'
```

### 手动触发巡检

```bash
curl -X POST http://localhost:8080/api/v1/inspections/{id}/trigger
```

### 查询巡检结果

```bash
curl http://localhost:8080/api/v1/inspections/{id}/runs
```

## License

MIT
