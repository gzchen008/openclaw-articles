# OpenClaw 如何支持 20+ AI 模型？多模型架构设计

> 这篇文章是「OpenClaw 源码解读系列」第 3 篇。前面我们聊了整体架构和 Agent Loop，今天深入多模型支持的设计哲学。

---

## 你有没有遇到过这些问题？

**场景 1**：正在用 Claude 写代码，突然 API 限流了。

```
Error: Rate limit exceeded. Please retry after 20 seconds.
```

**场景 2**：GPT-4 太贵，想切换到便宜的模型，但不知道哪个好用。

**场景 3**：想用国产模型（GLM、Kimi），但不知道怎么配置。

**场景 4**：多个 AI 账号，想自动轮换避免限流。

OpenClaw 的多模型架构就是为了解决这些问题设计的。

---

## 🎯 核心设计：两级 Failover

OpenClaw 使用 **两级容错机制**：

```
Provider 内部 Auth Profile 轮换 → Model Fallback → 失败
```

### 第 1 级：Auth Profile 旋转

当某个 API Key 限流时，自动切换到同 Provider 的其他账号。

```
anthropic/claude-sonnet-4-5
  ├── Profile 1: sk-ant-xxx (限流)
  ├── Profile 2: sk-ant-yyy (自动切换) ✅
  └── Profile 3: sk-ant-zzz (备用)
```

### 第 2 级：Model Fallback

如果 Provider 的所有 Profile 都失败，切换到下一个模型。

```
Primary: anthropic/claude-sonnet-4-5
  ↓ (所有 Profile 失败)
Fallback 1: openai/gpt-5.2
  ↓ (失败)
Fallback 2: zai/glm-5
  ↓ (失败)
错误
```

---

## 🏗️ 模型选择流程

OpenClaw 按以下顺序选择模型：

1. **Primary 模型**：`agents.defaults.model.primary`
2. **Fallback 列表**：`agents.defaults.model.fallbacks`（按顺序尝试）
3. **Provider 内部**：在切换模型前，先尝试 Provider 内的 Auth Profile 轮换

### 配置示例

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-5",
        "fallbacks": [
          "openai/gpt-5.2",
          "zai/glm-5",
          "kimi-coding/k2p5"
        ]
      }
    }
  }
}
```

---

## 🔄 Auth Profile 旋转机制

### 旋转顺序

当 Provider 有多个 Profile 时，选择顺序：

1. **显式配置**：`auth.order[provider]`
2. **配置的 Profile**：`auth.profiles`
3. **存储的 Profile**：`auth-profiles.json`

默认使用 **Round-Robin** 轮换：

- **主键**：Profile 类型（OAuth 优先于 API Key）
- **次键**：`usageStats.lastUsed`（最久未用的优先）
- **Cooldown/Disabled**：移到最后

### Session 粘性

OpenClaw **不会每次请求都轮换**，而是：

- **Pin 住**当前 Session 使用的 Profile
- 保持 Provider 缓存热度
- 只有在限流/超时时才切换

**Pin 会在以下情况重置**：
- Session 重置（`/new` / `/reset`）
- Compaction 完成
- Profile 进入 Cooldown

---

## ⏱️ Cooldown 机制

当 Profile 失败时（限流、超时、认证错误），OpenClaw 会将其标记为 **Cooldown** 状态。

### 指数退避

| 失败次数 | Cooldown 时间 |
|----------|---------------|
| 1 | 1 分钟 |
| 2 | 5 分钟 |
| 3 | 25 分钟 |
| 4+ | 1 小时（上限） |

### 状态存储

```json
{
  "usageStats": {
    "anthropic:default": {
      "lastUsed": 1736160000000,
      "cooldownUntil": 1736160600000,
      "errorCount": 2
    }
  }
}
```

---

## 🚫 Billing Disable 机制

计费错误（余额不足）不是临时问题，OpenClaw 使用 **更长的退避**：

| 机制 | 时间 |
|------|------|
| 初始退避 | 5 小时 |
| 最大退避 | 24 小时 |
| 重置窗口 | 24 小时无失败 |

```json
{
  "usageStats": {
    "openai:default": {
      "disabledUntil": 1736178000000,
      "disabledReason": "billing"
    }
  }
}
```

---

## 🌐 Provider 生态

OpenClaw 内置 20+ Provider：

### 主流 Provider

| Provider | 模型示例 | 认证方式 |
|----------|----------|----------|
| OpenAI | gpt-5.2 | API Key |
| Anthropic | claude-opus-4-5 | API Key / OAuth |
| Google | gemini-3-pro-preview | API Key / OAuth |
| Z.AI (GLM) | glm-5 | API Key |
| Kimi Coding | k2p5 | API Key |
| MiniMax | minimax-m2.1 | API Key |

### OpenAI 兼容代理

| Provider | 说明 |
|----------|------|
| OpenRouter | 多模型聚合 |
| Groq | 快速推理 |
| Cerebras | 快速推理 |
| LM Studio | 本地模型 |
| vLLM | 本地部署 |
| LiteLLM | 代理层 |

### 配置自定义 Provider

```json
{
  "models": {
    "providers": {
      "lmstudio": {
        "baseUrl": "http://localhost:1234/v1",
        "apiKey": "LMSTUDIO_KEY",
        "api": "openai-completions",
        "models": [
          {
            "id": "minimax-m2.1",
            "name": "MiniMax M2.1",
            "contextWindow": 200000,
            "maxTokens": 8192
          }
        ]
      }
    }
  }
}
```

---

## 🛠️ CLI 命令

### 查看模型状态

```bash
# 列出所有模型
openclaw models list

# 查看详细状态
openclaw models status

# 查看所有 Provider
openclaw models list --all
```

### 设置模型

```bash
# 设置主模型
openclaw models set anthropic/claude-sonnet-4-5

# 设置图片模型
openclaw models set-image openai/gpt-5.2
```

### 管理 Fallback

```bash
# 查看 fallback 列表
openclaw models fallbacks list

# 添加 fallback
openclaw models fallbacks add openai/gpt-5.2

# 删除 fallback
openclaw models fallbacks remove openai/gpt-5.2

# 清空 fallback
openclaw models fallbacks clear
```

### 管理 Auth Profile

```bash
# 登录 OAuth
openclaw models auth login --provider openai-codex

# 粘贴 API Key
openclaw models auth paste-token --provider anthropic
```

---

## 🎯 最佳实践

### 1. 配置多级 Fallback

```json
{
  "model": {
    "primary": "anthropic/claude-sonnet-4-5",
    "fallbacks": [
      "openai/gpt-5.2",
      "zai/glm-5",
      "ollama/llama3.3"
    ]
  }
}
```

**策略**：
- 主模型：性能最好
- Fallback 1：稳定可靠
- Fallback 2：国产备选
- Fallback 3：本地兜底

### 2. 配置多个 Auth Profile

```json
{
  "auth": {
    "order": {
      "anthropic": [
        "anthropic:work@example.com",
        "anthropic:personal@example.com"
      ]
    }
  }
}
```

### 3. Session 级别切换

```bash
# 临时切换模型
/model openai/gpt-5.2

# 查看当前模型状态
/model status
```

---

## 📊 总结

**OpenClaw 多模型架构的核心设计**：

1. **两级 Failover**：Provider 内轮换 → Model Fallback
2. **智能旋转**：OAuth 优先、最久未用优先、Cooldown 移后
3. **Session 粘性**：保持 Provider 缓存热度
4. **指数退避**：避免频繁重试失败的 Profile
5. **Billing Disable**：计费问题使用更长退避

**关键配置**：
- `agents.defaults.model.primary`：主模型
- `agents.defaults.model.fallbacks`：Fallback 列表
- `auth.order`：Profile 顺序

**CLI 命令**：
- `openclaw models status`：查看状态
- `openclaw models set`：设置模型
- `openclaw models fallbacks`：管理 Fallback

---

## 下篇预告

下一篇我们聊 **Session 管理与上下文工程**：OpenClaw 如何保持 AI 的长期记忆？

---

如果觉得有用，点个"在看"吧 👇
