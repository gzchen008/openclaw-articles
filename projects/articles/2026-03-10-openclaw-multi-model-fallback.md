# OpenClaw 如何支持 20+ AI 模型？多模型架构设计

> 本文是 OpenClaw 源码解读系列第 3 篇，深入剖析多模型支持和智能降级机制。

## 🎯 为什么需要多模型支持？

想象一个场景：

你在用 GPT-5 开发一个 Agent，突然遇到 rate limit，整个系统瘫痪。或者你想测试某个功能在 Claude 和 Gemini 上的表现差异，需要手动切换模型...

**痛点**：
- ❌ 单一模型 = 单点故障
- ❌ 手动切换模型 = 效率低下
- ❌ 成本不可控 = 钱包爆炸

**OpenClaw 的解决方案**：
- ✅ 内置 20+ 模型支持
- ✅ 智能降级 + 自动重试
- ✅ 灵活的模型选择策略

---

## 📊 支持的模型生态

### 内置提供商（无需配置）

| 提供商 | Provider ID | 认证方式 | 热门模型 |
|--------|-------------|----------|----------|
| OpenAI | `openai` | API Key | `gpt-5.2` |
| Anthropic | `anthropic` | API Key / Token | `claude-opus-4-5` |
| OpenAI Codex | `openai-codex` | OAuth | `gpt-5.2` |
| Google Gemini | `google` | API Key | `gemini-3-pro-preview` |
| Z.AI (GLM) | `zai` | API Key | `glm-5`, `glm-4.7` |
| OpenRouter | `openrouter` | API Key | 多模型代理 |
| xAI | `xai` | API Key | Grok |
| Groq | `groq` | API Key | 快速推理 |
| Mistral | `mistral` | API Key | Mistral 系列 |
| Cerebras | `cerebras` | API Key | 超快推理 |

### 自定义提供商（需配置）

| 提供商 | Provider ID | 认证方式 | 特点 |
|--------|-------------|----------|------|
| Kimi | `kimi-coding` | API Key | 国产大模型 |
| Moonshot | `moonshot` | API Key | Anthropic 兼容 |
| MiniMax | `minimax` | API Key | 写作/创意强 |
| Qwen | `qwen-portal` | OAuth | 免费额度 |
| Synthetic | `synthetic` | API Key | 多模型代理 |
| Ollama | `ollama` | 无 | 本地模型 |

---

## 🔄 Fallback 机制详解

OpenClaw 的降级策略分为**两层**：

### 第一层：Auth Profile Rotation（认证轮换）

当某个 provider 有多个认证配置时，OpenClaw 会自动轮换：

**轮换顺序**：
1. **显式配置**：`auth.order[provider]`（如果设置）
2. **配置的 profiles**：`auth.profiles` 过滤后的
3. **存储的 profiles**：`auth-profiles.json` 中的

**默认规则**（round-robin）：
- **主排序**：OAuth 优先于 API Key
- **次排序**：最近使用时间（最久未用的优先）

**示例**：你有 3 个 OpenAI API Key
```
Key1 → rate limit → Key2 → rate limit → Key3 → 成功
```

### 第二层：Model Fallback（模型降级）

当**所有认证都失败**时，才触发模型降级：

**降级顺序**：
1. `agents.defaults.model.primary`（首选模型）
2. `agents.defaults.model.fallbacks`（降级列表，按顺序）

**示例配置**：
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "zai/glm-5",
        "fallbacks": [
          "zai/glm-4.7",
          "minimax/MiniMax-M2.5",
          "anthropic/claude-sonnet-4-5"
        ]
      }
    }
  }
}
```

**执行流程**：
```
GLM-5 失败 → GLM-4.7 失败 → MiniMax 成功 ✓
```

---

## 🔐 认证管理

### Auth Profile 类型

**API Key 类型**：
```json
{
  "type": "api_key",
  "provider": "openai",
  "key": "sk-..."
}
```

**OAuth 类型**：
```json
{
  "type": "oauth",
  "provider": "google-antigravity",
  "access": "ya29...",
  "refresh": "1//...",
  "expires": 1736160000000,
  "email": "user@gmail.com"
}
```

### Profile ID 规则

- **默认**：`provider:default`（无邮箱时）
- **OAuth + 邮箱**：`provider:<email>`
  - 示例：`google-antigravity:user@gmail.com`

### 存储位置

所有认证信息存储在：
```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

**⚠️ 安全提示**：
- 该文件包含敏感凭证，不要提交到 Git
- OpenClaw 会自动处理 token 刷新
- OAuth token 过期前 24 小时会收到警告

---

## 🚫 Cooldown 机制

当认证失败时，OpenClaw 会将 profile 标记为 cooldown 状态。

### 普通失败（rate limit / timeout）

**指数退避**：
- 1 分钟
- 5 分钟
- 25 分钟
- 1 小时（上限）

**状态存储**：
```json
{
  "usageStats": {
    "openai:default": {
      "lastUsed": 1736160000000,
      "cooldownUntil": 1736160600000,
      "errorCount": 2
    }
  }
}
```

### 计费失败（余额不足）

**特殊处理**：
- ❌ 不认为是临时错误
- 🔄 标记为 **disabled**（长期禁用）
- ⏰ 起始退避：5 小时
- 📈 每次失败翻倍，上限 24 小时
- 🔄 24 小时无失败则重置

**状态存储**：
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

## 🎯 模型选择逻辑

### 选择顺序

1. **Primary 模型**：`agents.defaults.model.primary`
2. **Fallbacks**：`agents.defaults.model.fallbacks`（按顺序）
3. **Provider 内部降级**：auth profile rotation

### 配置示例

**基础配置**：
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "zai/glm-5"
      }
    }
  }
}
```

**完整降级链**：
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "zai/glm-5",
        "fallbacks": [
          "zai/glm-4.7",
          "zai/glm-4.7-flash",
          "minimax/MiniMax-M2.5"
        ]
      }
    }
  }
}
```

### 模型允许列表

如果你想**限制可用模型**，可以设置 allowlist：

```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "anthropic/claude-sonnet-4-5"
      },
      "models": {
        "anthropic/claude-sonnet-4-5": { "alias": "Sonnet" },
        "anthropic/claude-opus-4-5": { "alias": "Opus" },
        "zai/glm-5": { "alias": "GLM-5" }
      }
    }
  }
}
```

**效果**：
- ✅ 用户只能选择列表中的模型
- ❌ 选择其他模型会提示：`Model "xxx" is not allowed`

---

## 💰 成本优化建议

### 1. 按场景选择模型

**快速响应**：
```
cerebras/zai-glm-4.7  ← 超快推理
groq/llama-3.3        ← 免费 + 快速
```

**高质量输出**：
```
anthropic/claude-opus-4-5  ← 最强推理
zai/glm-5                  ← 代码能力强
```

**创意写作**：
```
minimax/MiniMax-M2.5  ← 写作风格好
```

### 2. 合理配置 Fallback

**原则**：
- 🎯 Primary 模型选择**最适合任务**的
- 💸 Fallback 模型选择**成本更低**的
- 🔄 同一 provider 的模型优先（减少延迟）

**示例**：
```json
{
  "primary": "anthropic/claude-opus-4-5",  // 最强但贵
  "fallbacks": [
    "anthropic/claude-sonnet-4-5",         // 同 provider，便宜
    "zai/glm-4.7"                          // 不同 provider，最便宜
  ]
}
```

### 3. 利用本地模型

**Ollama** 完全免费，适合：
- 🧪 开发测试
- 📊 数据处理
- 🔍 简单推理

**配置**：
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/llama3.3",
        "fallbacks": ["zai/glm-4.7"]
      }
    }
  }
}
```

---

## 🛠️ CLI 命令速查

### 查看模型状态

```bash
# 查看当前配置
openclaw models status

# 查看所有模型
openclaw models list --all

# 查看 OAuth 状态
openclaw models status --check
```

### 切换模型

```bash
# 设置主模型
openclaw models set zai/glm-5

# 设置图片模型
openclaw models set-image openai/gpt-4-vision

# 在会话中切换
/model 3                    # 按编号选择
/model zai/glm-5            # 按名称选择
/model status               # 查看详情
```

### 管理 Fallback

```bash
# 查看 fallback 列表
openclaw models fallbacks list

# 添加 fallback
openclaw models fallbacks add zai/glm-4.7

# 移除 fallback
openclaw models fallbacks remove zai/glm-4.7

# 清空 fallback
openclaw models fallbacks clear
```

### 管理别名

```bash
# 查看别名
openclaw models aliases list

# 添加别名
openclaw models aliases add GLM zai/glm-5

# 移除别名
openclaw models aliases remove GLM
```

---

## 📝 实战案例

### 案例 1：多账号负载均衡

**场景**：你有 3 个 OpenAI 账号，想自动轮换

**配置**：
```json
{
  "env": {
    "OPENAI_API_KEY_1": "sk-...",
    "OPENAI_API_KEY_2": "sk-...",
    "OPENAI_API_KEY_3": "sk-..."
  },
  "auth": {
    "profiles": {
      "openai:account1": {
        "provider": "openai",
        "type": "api_key",
        "key": "${OPENAI_API_KEY_1}"
      },
      "openai:account2": {
        "provider": "openai",
        "type": "api_key",
        "key": "${OPENAI_API_KEY_2}"
      },
      "openai:account3": {
        "provider": "openai",
        "type": "api_key",
        "key": "${OPENAI_API_KEY_3}"
      }
    }
  }
}
```

**效果**：
- 自动轮换 3 个账号
- rate limit 时自动切换
- 失败账号进入 cooldown

### 案例 2：混合云 + 本地

**场景**：优先用本地模型，失败时切换到云端

**配置**：
```json
{
  "agents": {
    "defaults": {
      "model": {
        "primary": "ollama/llama3.3",
        "fallbacks": [
          "zai/glm-4.7-flash",
          "anthropic/claude-sonnet-4-5"
        ]
      }
    }
  }
}
```

**效果**：
- 日常用本地模型（免费）
- 本地模型失败时自动切换云端
- 保证服务可用性

### 案例 3：按成本优化

**场景**：高质量任务用 Opus，普通任务用 Sonnet

**配置**：
```json
{
  "agents": {
    "list": [
      {
        "id": "high-quality",
        "model": "anthropic/claude-opus-4-5"
      },
      {
        "id": "daily",
        "model": {
          "primary": "anthropic/claude-sonnet-4-5",
          "fallbacks": ["zai/glm-4.7"]
        }
      }
    ]
  }
}
```

**使用**：
```bash
# 高质量任务
openclaw run --agent high-quality "分析这段代码"

# 日常任务
openclaw run --agent daily "翻译这段文字"
```

---

## 🔧 自定义 Provider

### 添加 Moonshot (Kimi)

```json
{
  "models": {
    "mode": "merge",
    "providers": {
      "moonshot": {
        "baseUrl": "https://api.moonshot.ai/v1",
        "apiKey": "${MOONSHOT_API_KEY}",
        "api": "openai-completions",
        "models": [
          { "id": "kimi-k2.5", "name": "Kimi K2.5" }
        ]
      }
    }
  }
}
```

### 添加本地代理 (LM Studio)

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

## 🎓 总结

### 核心要点

1. **两层降级**：先轮换认证，再降级模型
2. **智能 Cooldown**：临时错误快速恢复，计费错误长期禁用
3. **灵活配置**：支持多账号、混合云、成本优化
4. **本地优先**：Ollama 完全免费，适合测试

### 最佳实践

- ✅ **配置降级链**：至少 2-3 个 fallback
- ✅ **分离场景**：不同任务用不同模型
- ✅ **监控成本**：定期检查 usage stats
- ✅ **利用本地**：Ollama 适合开发测试

### 相关命令

```bash
# 快速上手
openclaw onboard

# 查看状态
openclaw models status

# 设置模型
openclaw models set zai/glm-5

# 管理 fallback
openclaw models fallbacks list
```

---

## 📚 相关文档

- [Models CLI](/concepts/models.md)
- [Model Failover](/concepts/model-failover.md)
- [Model Providers](/concepts/model-providers.md)
- [Gateway Configuration](/gateway/configuration.md)

---

**下一篇**：OpenClaw Session 管理：如何保持 AI 长期记忆？

---

*本文由 AI 生成，内容基于 OpenClaw 官方文档*
