> 本文由 OpenClaw AI 助手协助整理

【快速导航】
- 本文适合：正在使用或准备使用 OpenClaw 的用户
- 预计阅读：8 分钟
- 难度等级：⭐⭐

---

# Claude vs GPT vs Gemini：OpenClaw 模型选型指南

**"用了 OpenClaw 一周，却不知道该选哪个 AI 模型？"**

这是我在后台收到最多的问题之一。

有人用 GPT-4 写代码觉得太贵，换到 Claude 后发现中文理解不行；有人听说 Gemini 免费，结果一用发现回复质量参差不齐...

**选错模型，等于浪费钱 + 浪费时间。**

今天这篇文章，我会用实测数据 + 场景对比，帮你找到最适合的模型。全文无广，都是血泪经验 😂

---

## 💡 为什么模型选择这么重要？

先问大家一个问题：

> 同样是 AI 助手，为什么有人觉得"真香"，有人觉得"就这"？

**答案往往出在模型选择上。**

OpenClaw 支持接入多个主流 AI 模型：
- **GPT 系列**（OpenAI）
- **Claude 系列**（Anthropic）
- **Gemini 系列**（Google）
- **以及更多...**

每个模型的特点完全不同：
- 💰 **价格**差异可达 10 倍
- 🧠 **能力**侧重各不相同
- 🌏 **语言**支持有好有坏
- ⚡ **速度**快慢不一

**选对了，花小钱办大事；选错了，花大钱还生气。**

---

## 🔥 三大模型家族全面对比

下面这张表格，建议收藏 👇

| 维度 | GPT-4o | Claude 3.5 Sonnet | Gemini 1.5 Pro |
|------|--------|-------------------|----------------|
| **中文能力** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **代码能力** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **创意写作** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **推理能力** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **响应速度** | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **价格** | 💰💰💰 | 💰💰 | 💰 |
| **免费额度** | 少 | 中等 | 多 |

> 💡 **一句话总结**：不差钱选 GPT-4o，性价比选 Claude 3.5，预算有限选 Gemini。

---

## 🎯 按场景选模型（抄作业版）

看完表格还是不知道怎么选？没关系，直接按使用场景来：

### 场景 1：日常对话 + 问答
**推荐模型**：Claude 3.5 Sonnet / GPT-4o mini

**理由**：
- 日常对话不需要最强模型
- Claude 3.5 性价比高，上下文理解好
- GPT-4o mini 更快更便宜

**配置示例**：
```yaml
# config.yaml
models:
  default: claude-3-5-sonnet-20241022
  aliases:
    fast: gpt-4o-mini
```

---

### 场景 2：编程开发 + Debug
**推荐模型**：GPT-4o / Claude 3.5 Sonnet

**理由**：
- GPT-4o 代码生成最稳，几乎不会"幻觉"
- Claude 3.5 代码解释清晰，适合学习
- 两者都能处理复杂项目结构

**实测对比**：
- 写 Python 脚本：GPT-4o > Claude 3.5
- 解释代码逻辑：Claude 3.5 > GPT-4o
- 复杂算法实现：两者相当

**配置示例**：
```yaml
# 编程专用配置
models:
  coding: gpt-4o
  explain: claude-3-5-sonnet-20241022
```

---

### 场景 3：创意写作 + 内容创作
**推荐模型**：Claude 3.5 Sonnet / GPT-4o

**理由**：
- Claude 3.5 的"文笔"最像人，不机械
- 写故事、文案、公众号首选
- GPT-4o 适合结构化内容（如报告、文档）

**我的使用习惯**：
- 写公众号文章 → Claude 3.5
- 写技术文档 → GPT-4o
- 头脑风暴 → Claude 3.5

---

### 场景 4：长文档处理 + 知识库
**推荐模型**：Gemini 1.5 Pro / Claude 3.5 Sonnet

**理由**：
- Gemini 1.5 Pro 支持 **200万 token** 上下文
- 适合处理整本书、大量聊天记录
- Claude 3.5 的 20万 token 也够大部分场景

**⚠️ 注意**：Gemini 长文本能力虽强，但中文质量略逊于前两者。

---

### 场景 5：实时任务 + 快速响应
**推荐模型**：GPT-4o mini / Gemini Flash

**理由**：
- 速度最快，价格低
- 适合不需要太高质量的快速任务
- 如：格式转换、简单查询、消息摘要

---

## ⚙️ OpenClaw 模型配置实操

知道选什么模型了，接下来看怎么配置。

### 步骤 1：查看可用模型

```bash
# 查看 OpenClaw 支持的所有模型
openclaw models list
```

### 步骤 2：配置默认模型

编辑你的 `config.yaml`：

```yaml
# ~/.openclaw/config.yaml

models:
  # 默认使用的模型
  default: claude-3-5-sonnet-20241022
  
  # 设置别名，方便切换
  aliases:
    fast: gpt-4o-mini          # 快速任务
    smart: gpt-4o              # 复杂任务
    creative: claude-3-5-sonnet-20241022  # 创意写作
    cheap: gemini-1.5-flash    # 省钱首选
```

### 步骤 3：配置 API 密钥

```yaml
providers:
  openai:
    apiKey: YOUR_OPENAI_API_KEY
    
  anthropic:
    apiKey: YOUR_ANTHROPIC_API_KEY
    
  google:
    apiKey: YOUR_GOOGLE_API_KEY
```

> 🔐 **安全提示**：以上都是占位符，请替换为你的真实 API Key。

### 步骤 4：实时切换模型

在对话中随时切换：

```
/model gpt-4o
/model claude-3-5-sonnet
/model gemini-1.5-pro
```

或者在消息中指定：

```
@claude 帮我写一首诗
@gpt 解释这段代码
@gemini 总结这份文档
```

---

## 💰 省钱技巧：模型组合策略

不想花冤枉钱？试试这套"组合拳"：

### 策略 1：快慢结合

```yaml
models:
  default: gpt-4o-mini      # 默认用快的
  
session:
  # 当检测到编程相关问题时，自动切换到 GPT-4o
  autoUpgrade:
    code: gpt-4o
    complex: claude-3-5-sonnet-20241022
```

### 策略 2：分层使用

| 任务类型 | 推荐模型 | 预计成本 |
|---------|---------|---------|
| 简单问答 | GPT-4o mini | $0.001/次 |
| 日常对话 | Claude 3.5 Haiku | $0.002/次 |
| 代码开发 | GPT-4o | $0.01/次 |
| 重要文档 | Claude 3.5 Sonnet | $0.015/次 |

**按这个策略，每月花费可以控制在 $5-10。**

---

## ❌ 常见错误 & 避坑指南

### 错误 1：一味追求"最强"模型

**表现**：所有任务都用 GPT-4o，结果月底账单爆炸 💸

**解决**：简单任务用轻量级模型，省 90% 费用。

---

### 错误 2：忽视中文支持

**表现**：用 Gemini 写中文文章，结果语句不通顺。

**解决**：中文内容优先选 GPT-4o 或 Claude 3.5。

---

### 错误 3：从不切换模型

**表现**：一套配置走天下，不管任务类型。

**解决**：养成根据任务选模型的习惯，效率提升 50%+。

---

## 🎁 我的私藏配置（直接复制）

最后，分享一套我自用的配置，开箱即用：

```yaml
# ~/.openclaw/config.yaml

models:
  # 默认：性价比之选
  default: claude-3-5-sonnet-20241022
  
  # 别名配置
  aliases:
    # 超快响应
    fast: gpt-4o-mini
    
    # 最强能力
    pro: gpt-4o
    
    # 创意写作
    write: claude-3-5-sonnet-20241022
    
    # 超长文本
    long: gemini-1.5-pro
    
    # 省钱模式
    cheap: gemini-1.5-flash

# 会话设置
session:
  # 默认思考级别
  thinking: medium
  
  # 自动选择模型（实验功能）
  autoSelect: true

providers:
  openai:
    apiKey: YOUR_OPENAI_API_KEY
    
  anthropic:
    apiKey: YOUR_ANTHROPIC_API_KEY
    
  google:
    apiKey: YOUR_GOOGLE_API_KEY
```

保存后重启 OpenClaw 即可生效：

```bash
openclaw restart
```

---

## 📌 今日总结

今天我们聊了：

1. **三大模型家族对比** —— GPT-4o 全能、Claude 3.5 擅长写作、Gemini 超长文本
2. **五大使用场景推荐** —— 日常、编程、创作、长文档、快速任务
3. **配置实操步骤** —— 从查看模型到实时切换
4. **省钱组合策略** —— 分层使用，成本降低 90%

**记住这个口诀**：
> 日常对话用 Claude，编程开发用 GPT，
> 长文本用 Gemini，省钱就用轻量版。

---

## 🚀 下一步行动

现在就去试试：

1. 打开你的 OpenClaw 配置文件
2. 按本文建议配置模型别名
3. 发几条消息测试不同模型的效果
4. 找到最适合你的"主力模型"

**明天预告**：Day 6《OpenClaw 的 10 个隐藏技巧，90% 的人不知道》

---

如果这篇文章对你有帮助，欢迎 **点赞、在看、转发** 三连支持！

有任何问题，欢迎在评论区留言，我会一一回复。

明天见 👋

---

*本文首发于公众号「OpenClaw 指南」，转载请注明出处。*
