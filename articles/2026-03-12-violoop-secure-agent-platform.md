# Violoop：一个硬核的 AI Agent 安全自动化平台

> 这个项目把 AI Agent 的安全性做到了硬件级别。

---

## 你有没有担心过 AI Agent 的安全问题？

让 AI 帮你操作电脑，确实很方便。但是...

- **万一它误删了重要文件怎么办？**
- **万一它访问了敏感数据怎么办？**
- **万一它执行了危险命令怎么办？**

大多数 AI Agent 平台的解决方案是：**加个确认弹窗**。

但弹窗会被习惯性点击，Token 会被泄露，审批链会被绕过。

**Violoop** 的方案不一样：**硬件级别的安全隔离 + Ed25519 签名审批链**。

---

## 🎯 Violoop 是什么？

Violoop 是一个 **AI Agent 安全自动化平台**，包含硬件 + 软件的完整生态系统。

### 产品线

| 产品 | 硬件 | 说明 |
|------|------|------|
| **Lite** | RV1106 | 智能 KVM 网关（远程控制） |
| **Pro** | RK3576 | 边缘 AI 记忆站（本地推理） |
| **Desktop** | macOS | 控制中心 |
| **Mobile** | iOS | 审批认证器（二次确认） |

**核心理念**：敏感操作必须经过 **物理设备** 确认。

---

## 🔧 核心特性

### 1. Hook 协议 - 拦截危险操作

AI Agent 在执行操作前，会发出结构化的审批请求：

```json
{
  "type": "prompt",
  "action": {
    "type": "shell",
    "command": "rm -rf node_modules",
    "risk_level": "medium"
  },
  "context": {
    "reason": "Cleaning dependencies before reinstall"
  }
}
```

**风险等级**：
- `low` - 自动通过（如 ls、cat）
- `medium` - 需要确认（如 rm、npm install）
- `high` - 必须物理设备确认（如 rm -rf /、部署生产环境）

### 2. Policy Engine - 策略引擎

可配置的允许/拒绝列表：

```json
{
  "allow": [
    { "type": "shell", "pattern": "^ls\\b" },
    { "type": "file_read", "path": "*.md" }
  ],
  "deny": [
    { "type": "shell", "pattern": "rm -rf /" },
    { "type": "network", "domain": "*.suspicious.com" }
  ],
  "require_approval": [
    { "type": "file_write" },
    { "type": "file_delete" }
  ]
}
```

### 3. Ed25519 签名审批链

每次审批都会生成 **Ed25519 签名**：

- 防止伪造审批记录
- 防止重放攻击（Nonce 机制）
- 时间戳验证（防止过期审批）
- 哈希链保证审计完整性

### 4. Folder-as-Agent - 文件夹触发工作流

把文件丢进文件夹，自动触发 AI 处理：

```json
{
  "name": "Video Transcoder",
  "trigger": {
    "type": "folder_watch",
    "path": "/VioloopTasks/Transcode"
  },
  "steps": [
    { "name": "Check Format", "action": "shell", "approval": "auto" },
    { "name": "Transcode", "action": "shell", "approval": "required" }
  ]
}
```

---

## 🆚 与 OpenClaw 对比

| 特性 | Violoop | OpenClaw |
|------|---------|----------|
| **定位** | 安全自动化 | AI Agent 平台 |
| **硬件** | 有（Lite/Pro） | 无 |
| **审批机制** | Ed25519 签名链 | 配对 + Token |
| **消息平台** | 未明确 | 20+ 平台 |
| **Hook 系统** | Hook Protocol | Gateway + Plugin Hooks |
| **工作流** | JSON 定义 | Skills |
| **多模型** | ✅ | ✅ 20+ 模型 |
| **开源** | CLI Agent 开源 | 完全开源 |

**适用场景**：

- **Violoop** - 需要高安全性的企业环境（金融、医疗、政府）
- **OpenClaw** - 需要 20+ 消息平台接入的个人/团队

---

## 🚀 快速开始

### 安装 CLI Agent

```bash
npm install -g @b-vio/agent
```

### 运行

```bash
# 交互模式（需要审批）
bvio-agent run "organize my downloads folder"

# 预览模式（不执行）
bvio-agent plan "update all npm packages"

# 指定模型
bvio-agent run --model claude-3 "refactor this code"

# 自定义策略
bvio-agent run --policy strict.json "deploy to production"
```

---

## 💡 可借鉴的设计

### 1. Ed25519 签名审批链

比 Token 更安全，无法伪造审批记录。

### 2. 风险分级

`risk_level: low/medium/high`，不同操作不同审批级别。

### 3. 硬件隔离

敏感操作必须经过物理设备确认（Mobile iOS 认证器）。

### 4. Folder-as-Agent

文件夹触发自动化，无需编写代码。

### 5. 不可变审计追踪

所有操作记录上链，无法篡改。

---

## 📚 相关链接

- **bvio-agent**: https://github.com/B-VIO/bvio-agent
- **violoop-protocol**: https://github.com/B-VIO/violoop-protocol
- **violoop-workflows**: https://github.com/B-VIO/violoop-workflows

---

如果觉得有用，点个"在看"吧 👇
