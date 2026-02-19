# Claude Code 状态栏神器！实时监控你的 AI 编程助手

你是不是也遇到过这些问题？

- ❌ Claude Code 用着用着上下文爆了，任务被截断
- ❌ 不知道哪个 Agent 在跑，等半天没反应
- ❌ Token 用了多少？还剩多少？心里没数
- ❌ 工具调用记录看不清，排查问题困难

今天推荐一个**开源神器**，让这些问题全部消失 👇

---

## 🎯 Claude HUD - 实时监控面板

**一句话介绍：** Claude Code 原生状态栏插件，实时显示一切重要信息。

### 能看到什么？

| 显示内容 | 作用 |
|---------|------|
| **项目路径** | 知道自己在哪个项目（可配置1-3层目录）|
| **上下文健康度** | 实时显示上下文使用率（绿→黄→红）|
| **工具活动** | 实时看到读写、搜索等操作 |
| **Agent 追踪** | 看到哪个子 Agent 在跑、在做什么 |
| **Todo 进度** | 任务完成进度实时更新 |
| **Token 用量** | 精确显示已用/剩余（非估算）|

---

## 🖼️ 实际效果

### 默认显示（2行）

```
[Opus | Max] │ my-project git:(main*)
Context █████░░░░░ 45% │ Usage ██░░░░░░░░ 25% (1h 30m / 5h)
```

**第一行：**
- 模型名称（Opus/Max）
- 计划类型
- 项目路径
- Git 分支

**第二行：**
- 上下文进度条（绿→黄→红）
- Token 使用率和剩余时间

---

### 可选显示（3-5行）

```
◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2        ← 工具活动
◐ explore [haiku]: Finding auth code (2m 15s)    ← Agent 状态
▸ Fix authentication bug (2/5)                   ← Todo 进度
```

**工具活动行：**
- 实时显示正在执行的操作
- 读写、搜索、编辑等一目了然

**Agent 状态行：**
- 哪个子 Agent 在跑
- 运行时间
- 当前任务

**Todo 进度行：**
- 任务清单
- 完成数量

---

## 🚀 3步安装

### Step 1: 添加市场源

在 Claude Code 里输入：

```
/plugin marketplace add jarrodwatts/claude-hud
```

### Step 2: 安装插件

```
/plugin install claude-hud
```

⚠️ **Linux 用户注意：**
如果遇到 `EXDEV: cross-device link not permitted` 错误，先执行：
```bash
mkdir -p ~/.cache/tmp && TMPDIR=~/.cache/tmp claude
```

### Step 3: 配置状态栏

```
/claude-hud:setup
```

**完成！** 立即生效，无需重启。

---

## ⚡ 核心优势

### 1. 原生集成，无需额外窗口

- ✅ 使用 Claude Code 原生 **statusline API**
- ✅ 不需要 tmux、分屏
- ✅ 任何终端都能用

### 2. 实时更新（300ms）

- ✅ 每秒更新 3 次
- ✅ 真正的实时监控
- ✅ 不卡顿、不影响性能

### 3. 精确 Token 数据

- ✅ 来自 Claude Code 官方 API
- ✅ **不是估算**，是真实数据
- ✅ 包含输入+输出+缓存

### 4. 智能解析

- ✅ 自动解析 transcript（工具调用记录）
- ✅ 追踪 Agent 状态
- ✅ 识别 Todo 列表

---

## 🎨 高度可定制

### 配置命令

```
/claude-hud:configure
```

**可调整内容：**
- 📏 显示行数（2-5行）
- 🎯 信息类型（工具/Agent/Todo）
- 🎨 颜色主题
- 📁 路径深度（1-3层目录）

---

## 💡 实用场景

### 场景1: 监控上下文使用

**问题：** 任务跑到一半，上下文爆了

**解决：**
```
Context ██████████ 98% │ ⚠️ 快满了！
```
看到警告，主动 `/compact` 或重启任务

---

### 场景2: 追踪 Agent 执行

**问题：** 不知道哪个 Agent 在跑，等半天

**解决：**
```
◐ explore [haiku]: Finding auth code (2m 15s)
```
知道它在做什么，心里有数

---

### 场景3: 监控工具调用

**问题：** AI 在干啥？读文件还是写代码？

**解决：**
```
◐ Edit: auth.ts | ✓ Read ×3 | ✓ Grep ×2
```
实时看到操作记录

---

### 场景4: 跟踪任务进度

**问题：** 任务列表完成度如何？

**解决：**
```
▸ Fix authentication bug (2/5)
```
知道还剩多少工作量

---

## 🔗 相关项目

### Claude HUD Enhanced

**作者：** alwinpaul1

**特点：**
- 增强版 Claude HUD
- 更多颜色主题
- 更精确的 Token 显示

**GitHub：** https://github.com/alwinpaul1/claude-hud-enhanced

---

### CC Statusbar for Claude Relay

**作者：** paceyw

**特点：**
- 为 Claude Relay Service 设计
- 实时状态更新
- 完善的错误恢复

**安装：**
```bash
npm i -g claude-code-statusbar
cc-statusbar --version
cc-statusbar
```

**GitHub：** https://github.com/paceyw/cc-statusbar-for-Claude-Relay-Service

---

## 📊 对比总结

| 特性 | Claude HUD | Claude HUD Enhanced | CC Statusbar |
|------|-----------|---------------------|--------------|
| **原生集成** | ✅ | ✅ | ❌ |
| **实时更新** | 300ms | 300ms | 1s |
| **Token 显示** | ✅ | ✅ 增强版 | ✅ |
| **主题定制** | 基础 | 更多主题 | 基础 |
| **适用场景** | Claude Code | Claude Code | Relay Service |
| **安装难度** | ⭐ | ⭐ | ⭐⭐ |

---

## 🎯 适合谁用？

### ✅ 强烈推荐

- **Claude Code 重度用户**
- **需要长时间运行任务的场景**
- **关心上下文和 Token 消耗**
- **多 Agent 协作开发**

### ⚠️ 可选

- **偶尔用 Claude Code**
- **短任务（<30分钟）**
- **不关心监控数据**

---

## 🛠️ 技术细节

### 工作原理

```
Claude Code → stdin JSON → claude-hud → stdout → 终端显示
           ↘ transcript JSONL (工具/Agent/Todo)
```

**核心技术：**
- TypeScript 开发
- Node.js 18+ / Bun 1.0.80+
- 使用 Claude Code Statusline API

**性能：**
- CPU 占用：<1%
- 内存占用：<50MB
- 更新频率：~300ms

---

## 📝 总结

Claude HUD 是 **Claude Code 必装插件**之一。

**3个理由：**

1️⃣ **实时监控** - 上下文、Token、工具、Agent、Todo 一目了然

2️⃣ **原生集成** - 无需额外窗口，任何终端都能用

3️⃣ **开源免费** - MIT 协议，完全开源

**安装只需3步：**
```
/plugin marketplace add jarrodwatts/claude-hud
/plugin install claude-hud
/claude-hud:setup
```

装上之后，你会想知道之前没有它你是怎么活过来的 😂

---

## 🔗 项目地址

**Claude HUD:** https://github.com/jarrodwatts/claude-hud

**Claude HUD Enhanced:** https://github.com/alwinpaul1/claude-hud-enhanced

**CC Statusbar:** https://github.com/paceyw/cc-statusbar-for-Claude-Relay-Service

---

**觉得有用？点个"在看"，分享给更多开发者！** 👇

#ClaudeCode #AI工具 #开源项目 #开发效率
