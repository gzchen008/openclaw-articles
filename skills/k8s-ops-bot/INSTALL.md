# K8s Ops Bot - 安装运行指南

## 简介

K8s Ops Bot 是一个深度集成 OpenClaw 的 Kubernetes 运维机器人，提供实时告警、定时巡检、交互命令和自动修复功能。

## 目录

1. [环境准备](#环境准备)
2. [安装步骤](#安装步骤)
3. [配置说明](#配置说明)
4. [运行方式](#运行方式)
5. [验证测试](#验证测试)
6. [日常运维](#日常运维)

---

## 环境准备

### 系统要求

- Python 3.9+
- Kubernetes 集群访问权限
- OpenClaw 已配置消息渠道（Discord/Telegram/Slack）

### 依赖安装

```bash
# 安装 Python 依赖
pip install kubernetes pyyaml

# 验证安装
python3 -c "import kubernetes; print(kubernetes.__version__)"
```

### 准备 Kubeconfig

确保你有有效的 kubeconfig 文件：

```bash
# 检查默认 kubeconfig
ls -la ~/.kube/config

# 测试连接
kubectl cluster-info
kubectl get nodes
```

---

## 安装步骤

### 1. 解压 Skill 包

```bash
# 创建安装目录
mkdir -p ~/k8s-ops-bot
cd ~/k8s-ops-bot

# 解压 skill 文件（假设 skill 文件在当前目录）
unzip k8s-ops-bot.skill -d .

# 查看目录结构
ls -la
```

目录结构：
```
k8s-ops-bot/
├── scripts/
│   ├── bot.py           # 主程序
│   ├── watcher.py       # 事件监听
│   ├── inspector.py     # 巡检
│   ├── commander.py     # 命令处理
│   └── remediator.py    # 自动修复
├── assets/
│   ├── config.template.yaml      # 配置模板
│   ├── k8s-deployment.yaml       # K8s 部署文件
│   ├── k8s-ops-bot.service       # Systemd 服务文件
│   └── playbooks/                # 修复剧本
│       ├── oom-killed.yaml
│       ├── crashloop.yaml
│       ├── imagepull.yaml
│       └── pending-pod.yaml
└── references/
    ├── config.md                 # 配置参考
    └── troubleshooting.md        # 故障排查
```

### 2. 创建配置文件

```bash
# 复制配置模板
cp assets/config.template.yaml ~/.openclaw/k8s-ops-bot.yaml

# 编辑配置文件
nano ~/.openclaw/k8s-ops-bot.yaml
```

### 3. 配置关键参数

编辑 `~/.openclaw/k8s-ops-bot.yaml`：

```yaml
# === 必填项 ===

# kubeconfig 路径
kubeconfig: "/Users/YOUR_USERNAME/.kube/config"

# 监控的 namespace，用 "all" 表示全集群
namespace: "default"

# === OpenClaw 消息渠道 ===

messaging:
  # 告警发送频道（根据你的 OpenClaw 配置修改）
  alert_channel: "discord://k8s-alerts"
  
  # 命令监听频道（可以 same as alert_channel）
  command_channel: "discord://ops-channel"
  
  # Critical 告警时 @ 提醒
  mention_on_critical: true

# === 功能开关 ===

watcher:
  enabled: true           # 实时事件监听
  
inspector:
  enabled: true           # 定时巡检
  
commander:
  enabled: true           # 交互命令
  
remediator:
  enabled: false          # 自动修复（建议先熟悉后再开启）
```

---

## 配置说明

### 告警冷却期（防止刷屏）

```yaml
watcher:
  alerting:
    cooldowns:
      critical: 300    # 5分钟
      high: 600        # 10分钟  
      warning: 1800    # 30分钟
```

### 巡检检查项

```yaml
inspector:
  checks:
    pod_status: true        # CrashLoopBackOff, Pending, Failed
    restart_count: true     # 重启次数 > 5
    deployment_health: true # Deployment 副本状态
    node_health: true       # Node Ready 状态
    resource_usage: false   # 需要 metrics-server
```

### 命令权限控制（生产环境建议开启）

```yaml
commander:
  authorization:
    allowed_users:          # 允许使用命令的用户
      - "admin"
      - "your-discord-username"
    
    restricted_commands:    # 需要管理员权限的命令
      - "restart"
      - "scale"
```

---

## 运行方式

### 方式一：手动运行（开发测试）

```bash
cd ~/k8s-ops-bot

# 前台运行（带日志输出）
python3 scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --daemon

# 测试单次巡检
python3 scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --once

# 测试单个命令
python3 scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --command "/k8s status"
```

### 方式二：Systemd 服务（推荐用于服务器）

```bash
# 1. 复制服务文件
sudo cp assets/k8s-ops-bot.service /etc/systemd/system/

# 2. 修改服务文件中的路径
sudo nano /etc/systemd/system/k8s-ops-bot.service
# 修改：
# - WorkingDirectory=/home/YOUR_USERNAME/k8s-ops-bot
# - ExecStart=/usr/bin/python3 /home/YOUR_USERNAME/k8s-ops-bot/scripts/bot.py ...
# - User=YOUR_USERNAME

# 3. 启动服务
sudo systemctl daemon-reload
sudo systemctl enable k8s-ops-bot
sudo systemctl start k8s-ops-bot

# 4. 查看状态
sudo systemctl status k8s-ops-bot
sudo journalctl -u k8s-ops-bot -f
```

### 方式三：Kubernetes 内部署（推荐生产环境）

```bash
# 1. 创建 namespace
kubectl create namespace monitoring

# 2. 应用部署文件
kubectl apply -f assets/k8s-deployment.yaml

# 3. 查看状态
kubectl get pods -n monitoring -l app=k8s-ops-bot
kubectl logs -n monitoring -l app=k8s-ops-bot -f
```

### 方式四：OpenClaw Cron 定时巡检

```bash
# 添加定时任务（每30分钟巡检一次）
openclaw cron add \
  --name "k8s-health-check" \
  --schedule "*/30 * * * *" \
  --command "python3 ~/k8s-ops-bot/scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --once"
```

---

## 验证测试

### 1. 测试连接

```bash
# 检查集群状态
python3 scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --command "/k8s status"
```

预期输出：
```
✅ **Cluster Status**

**Nodes:** 3/3 ready
**Pods:** 12/12 running
**Deployments:** 5/5 healthy
```

### 2. 测试 Pod 列表

```bash
python3 scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --command "/k8s pods"
```

### 3. 触发测试告警

创建一个会 CrashLoopBackOff 的 Pod 来测试告警：

```bash
kubectl run test-crash --image=busybox --restart=Never -- /bin/false
```

等待 1-2 分钟，检查是否收到告警通知。

清理：
```bash
kubectl delete pod test-crash
```

### 4. 测试交互命令

在 Discord/Slack 频道发送：

```
/k8s status
/k8s nodes
/k8s get pods
```

---

## 日常运维

### 查看日志

```bash
# 手动运行模式
tail -f ~/k8s-ops-bot/bot.log

# Systemd 模式
sudo journalctl -u k8s-ops-bot -f

# K8s 模式
kubectl logs -n monitoring -l app=k8s-ops-bot -f
```

### 更新配置

```bash
# 修改配置
nano ~/.openclaw/k8s-ops-bot.yaml

# 重启服务
sudo systemctl restart k8s-ops-bot
```

### 临时关闭告警

```bash
# 编辑配置，关闭 watcher
nano ~/.openclaw/k8s-ops-bot.yaml
# watcher:
#   enabled: false

# 重启生效
sudo systemctl restart k8s-ops-bot
```

### 升级版本

```bash
# 1. 备份配置
cp ~/.openclaw/k8s-ops-bot.yaml ~/.openclaw/k8s-ops-bot.yaml.bak

# 2. 停止服务
sudo systemctl stop k8s-ops-bot

# 3. 解压新版本
unzip -o k8s-ops-bot-v2.skill -d ~/k8s-ops-bot

# 4. 恢复配置
cp ~/.openclaw/k8s-ops-bot.yaml.bak ~/.openclaw/k8s-ops-bot.yaml

# 5. 启动服务
sudo systemctl start k8s-ops-bot
```

---

## 故障排查

### 常见问题

| 问题 | 解决方案 |
|------|----------|
| "kubernetes client not installed" | `pip install kubernetes pyyaml` |
| "Unauthorized" | 检查 kubeconfig 权限 |
| 收不到告警 | 检查 `alert_channel` 配置 |
| 命令无响应 | 检查 `command_channel` 和用户权限 |
| 告警太多 | 增加 cooldown 时间或启用 grouping |

### 调试模式

```yaml
# 在配置中开启 DEBUG 日志
advanced:
  log_level: "DEBUG"
```

更多排查方法请参考：`references/troubleshooting.md`

---

## 安全建议

1. **RBAC 最小权限**：为 bot 创建专用 ServiceAccount
2. **生产环境**：开启 commander.authorization 限制命令执行
3. **敏感操作**：restart/scale/delete 命令需要管理员确认
4. **自动修复**：建议先在测试环境验证 remediation 功能

---

## 相关文档

- `references/config.md` - 完整配置参考
- `references/troubleshooting.md` - 故障排查指南
- `assets/playbooks/*.yaml` - 自动修复剧本

---

## 快速命令速查

```bash
# 启动
python3 scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --daemon

# 状态检查
python3 scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --command "/k8s status"

# 查看问题 Pod
python3 scripts/bot.py --config ~/.openclaw/k8s-ops-bot.yaml --command "/k8s pods"

# 重启服务
sudo systemctl restart k8s-ops-bot

# 查看日志
sudo journalctl -u k8s-ops-bot -f
```
