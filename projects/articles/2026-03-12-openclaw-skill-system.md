# OpenClaw 技能系统：如何实现可扩展的 AI 能力？

> 这篇文章是「OpenClaw 源码解读系列」第 5 篇。上一篇我们聊了 Session 管理与上下文工程，今天深入技能系统的设计哲学。

---

你有没有想过，一个 AI 助手是怎么学会新技能的？

不是靠训练——那太慢、太贵。真正的方式是**插件化扩展**：给 AI 装上"工具说明书"，它就知道怎么用新工具了。

OpenClaw 的技能系统就是这样一套优雅的扩展机制。今天我们来拆解它的设计。

---

## 🛠️ 技能是什么？

**一个技能 = 一个目录 + 一个 SKILL.md 文件**

最简单的技能长这样：

```
skills/
└── hello-world/
    └── SKILL.md
```

SKILL.md 里写着：

```markdown
---
name: hello_world
description: A simple skill that says hello.
---

# Hello World Skill

When the user asks for a greeting, say "Hello from your custom skill!".
```

就这么简单。

**没有复杂的配置，没有注册表，没有编译。** 写完就能用。

---

## 🏗️ 三层加载机制

OpenClaw 从三个地方加载技能，优先级从高到低：

| 位置 | 优先级 | 用途 |
|------|--------|------|
| `<workspace>/skills/` | 最高 | 当前 Agent 专属技能 |
| `~/.openclaw/skills/` | 中 | 所有 Agent 共享的本地技能 |
| Bundled（内置） | 最低 | OpenClaw 自带的 50+ 技能 |

**为什么这样设计？**

- **Bundled**：开箱即用，零配置
- **Managed**：你自己装的技能，所有项目都能用
- **Workspace**：项目专属，比如某个项目需要访问特定 API

如果同名技能存在多处，**高优先级覆盖低优先级**。这样你可以：
- 覆盖内置技能（修复 bug 或定制行为）
- 为不同项目配置不同版本

---

## 📦 技能格式：AgentSkills 标准

OpenClaw 遵循 [AgentSkills](https://agentskills.io) 规范，核心是 YAML frontmatter：

```markdown
---
name: discord
description: Use when you need to control Discord from OpenClaw
metadata: {"openclaw":{"emoji":"🎮","requires":{"config":["channels.discord"]}}}
---

# Discord Actions

[技能使用说明...]
```

### 关键字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | 技能唯一标识 |
| `description` | ✅ | 何时使用（Agent 会根据这个判断） |
| `metadata` | ❌ | OpenClaw 扩展配置（gating、安装器等） |
| `homepage` | ❌ | 技能官网链接 |
| `user-invocable` | ❌ | 是否可作为 `/slash` 命令（默认 true） |

---

## 🔒 Gating：技能准入控制

不是所有技能都应该被加载。OpenClaw 用 **gating 机制** 过滤：

```markdown
---
metadata:
  {
    "openclaw": {
      "requires": {
        "bins": ["summarize"],        # 需要 CLI 工具
        "env": ["DISCORD_BOT_TOKEN"], # 需要环境变量
        "config": ["channels.discord"] # 需要配置项
      }
    }
  }
---
```

**只有满足所有条件，技能才会被加载。**

### 常见 Gating 规则

| 条件 | 含义 |
|------|------|
| `bins: ["claude"]` | 系统必须安装 `claude` 命令 |
| `env: ["OPENAI_API_KEY"]` | 必须设置环境变量 |
| `config: ["channels.discord"]` | OpenClaw 配置中必须启用 Discord |
| `os: ["darwin"]` | 仅 macOS 可用 |

**为什么这样设计？**

避免技能加载失败。比如你没有安装 `summarize` CLI，这个技能就不应该出现，否则 Agent 会调用失败。

---

## 🚀 一键安装：Installer 机制

OpenClaw 内置安装器，用户点一下就能装好依赖：

```markdown
---
metadata:
  {
    "openclaw": {
      "install": [
        {
          "id": "brew",
          "kind": "brew",
          "formula": "steipete/tap/summarize",
          "bins": ["summarize"],
          "label": "Install summarize (brew)"
        }
      ]
    }
  }
---
```

### 支持的安装器类型

| Kind | 用途 | 示例 |
|------|------|------|
| `brew` | Homebrew 包 | `formula: "python@3.11"` |
| `node` | npm 全局包 | `package: "clawhub"` |
| `go` | Go 包 | `package: "github.com/user/cli"` |
| `download` | 直接下载 | `url: "https://..."` |

**智能选择**：如果同时提供 brew 和 node，OpenClaw 会优先用 brew（macOS 更稳定）。

---

## 🌐 ClawHub：技能生态中心

[ClawHub](https://clawhub.com) 是 OpenClaw 的技能市场。

### 安装技能

```bash
# 搜索
clawhub search "discord"

# 安装到当前项目
clawhub install discord-skill

# 安装特定版本
clawhub install discord-skill --version 1.2.3
```

### 更新技能

```bash
# 更新单个
clawhub update discord-skill

# 更新全部
clawhub update --all
```

### 发布技能

```bash
clawhub publish ./my-skill --slug my-skill --name "My Skill" --version 1.0.0
```

---

## 🎯 实战：写一个技能

假设你要让 OpenClaw 访问公司的内部 API。

### Step 1：创建目录

```bash
mkdir -p ~/.openclaw/workspace/skills/company-api
```

### Step 2：写 SKILL.md

```markdown
---
name: company_api
description: Access company internal API for user data and reports.
metadata:
  {
    "openclaw": {
      "requires": { "env": ["COMPANY_API_KEY"] },
      "primaryEnv": "COMPANY_API_KEY"
    }
  }
---

# Company API Skill

Use the `exec` tool to call the company API.

## Get User Info

```bash
curl -H "Authorization: Bearer $COMPANY_API_KEY" \
  https://api.company.com/users/{user_id}
```

## Generate Report

```bash
curl -X POST -H "Authorization: Bearer $COMPANY_API_KEY" \
  -d '{"type": "monthly"}' \
  https://api.company.com/reports
```
```

### Step 3：配置 API Key

在 `~/.openclaw/openclaw.json` 中：

```json
{
  "skills": {
    "entries": {
      "company_api": {
        "apiKey": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

### Step 4：刷新技能

重启 Gateway 或新建 Session，技能就生效了。

---

## 🔧 高级特性

### 环境变量注入

技能可以定义需要的环境变量：

```json
{
  "skills": {
    "entries": {
      "gemini": {
        "env": {
          "GEMINI_API_KEY": "YOUR_KEY_HERE"
        }
      }
    }
  }
}
```

**安全设计**：环境变量只在 Agent 运行时注入，结束后恢复。不会污染系统环境。

### Slash 命令

设置 `user-invocable: true`，用户可以直接调用：

```
/summarize https://example.com
```

### 工具直连

设置 `command-dispatch: tool`，命令直接转发给工具，不经过模型：

```markdown
---
user-invocable: true
command-dispatch: tool
command-tool: summarize
---
```

---

## 📊 Token 消耗

技能会增加 System Prompt 的长度。公式：

```
总字符 = 195 + Σ (97 + name + description + location)
```

- **基础开销**：195 字符（只要有 ≥1 个技能）
- **每个技能**：97 字符 + 字段长度

估算：**每个技能约 24 tokens**（按 OpenAI tokenizer）

---

## 🎨 设计哲学总结

OpenClaw 技能系统的设计原则：

1. **简单优先**：一个文件就是一个技能
2. **渐进增强**：从最简单的开始，需要时再加 metadata
3. **安全可控**：gating 机制防止无效加载
4. **生态开放**：ClawHub 让技能可共享、可版本化
5. **Agent 友好**：description 帮助 Agent 正确判断何时使用

---

## 下篇预告

下一篇我们聊 **多渠道消息路由**：OpenClaw 如何同时支持 WhatsApp、Telegram、Discord、飞书等 20+ 平台？

---

如果觉得有用，点个"在看"吧 👇
