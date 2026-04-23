# 4125 Star！这个开源工具让 AI 直接复用你的浏览器登录

**痛点开场**

你是不是也遇到过这些问题：

- 想用 AI 自动抓取小红书数据，结果发现要申请 API Key，流程复杂得要死
- 想让 AI 帮你自动发知乎文章，但 OAuth 登录折腾半天
- 想自动化操作 20 多个平台，每个平台都要单独处理登录凭证

**最致命的是**：把账号密码交给第三方工具，你敢吗？

今天介绍的这个开源项目，完美解决了这些问题——**无需 API Key，直接复用你的浏览器登录状态，凭证永远不出浏览器**。

---

## 🚀 opencli：专为 AI Agent 设计的 CLI 工具

**opencli** 是一个 TypeScript 开发的开源工具，核心能力是把任何 Electron 应用（浏览器、桌面应用）变成 CLI 命令，让 AI Agent 可以直接调用。

**核心数据**：
- ⭐ **4,125 Stars**（GitHub 热门项目）
- 📄 **Apache 2.0 License**（商用友好）
- 🌐 官网：https://opencli.info/
- 📅 最后更新：2026-03-22（今天还在更新！）

---

## 💡 核心特性（太香了）

### 1️⃣ CLI All Electron — 把任何应用变命令行

opencli 可以把 Chrome、Edge、Cursor、Notion 等 Electron 应用变成 CLI 工具。

**这意味着什么？**

你可以在终端里直接操作这些应用：

```bash
# 让 Cursor 打开项目并执行命令
opencli cursor --project ~/myproject --command "refactor this code"

# 让 Notion 创建页面
opencli notion --create-page --title "今日任务" --content "完成项目文档"

# 让 Chrome 打开网页并截图
opencli chrome --url "https://example.com" --screenshot
```

### 2️⃣ Account-safe — 凭证永远不出浏览器

**这是最关键的安全特性**。

opencli 不会提取你的登录凭证（Cookie、Token），而是直接复用浏览器的登录状态。

**原理**：
- opencli 启动浏览器时，直接使用你的 Chrome 用户数据目录
- 所有登录状态都保存在浏览器内部
- opencli 只发送操作指令，不接触凭证

**对比传统方案**：
- ❌ 传统爬虫：需要导出 Cookie，存在泄露风险
- ❌ API 方案：需要申请 API Key，流程复杂
- ✅ opencli：零凭证导出，安全到极致

### 3️⃣ AI Agent ready — 专为 AI 设计

opencli 提供了 **AGENT.md** 协议，让 AI Agent 可以直接调用它的能力。

**这意味着**：
- 你可以让 ChatGPT、Claude 等 AI 直接操作你的浏览器
- AI 可以自动完成跨平台的复杂任务
- 支持多轮对话式的任务编排

**示例场景**：
```
你：帮我抓取小红书上"AI 绘画"关键词的前 10 篇笔记
AI：好的，我来调用 opencli...
    [自动启动 Chrome，访问小红书，执行搜索，提取数据]
    已完成！数据已保存到 results.json
```

### 4️⃣ External CLI Hub — 自动发现外部工具

opencli 会自动发现你系统里安装的 CLI 工具（gh、docker、kubectl、npm 等），并提供统一接口。

**好处**：
- 不用记住每个工具的命令语法
- AI Agent 可以直接调用任何已安装的工具
- 支持跨工具的任务编排

### 5️⃣ Zero Risk — 无需 API Key

**这是最大的亮点**。

传统方案要操作社交平台，通常需要：
1. 申请开发者账号
2. 提交审核材料
3. 等待平台审批（可能要几周）
4. 获取 API Key
5. 还要担心额度限制

**opencli 的方案**：
- 直接复用你的浏览器登录
- 无需申请任何 API Key
- 无需等待审批
- 无需担心额度限制

### 6️⃣ Dual-Engine — YAML + TypeScript 双引擎

opencli 支持两种配置方式：

**YAML 声明式**（适合简单任务）：
```yaml
task:
  app: chrome
  actions:
    - open: "https://xiaohongshu.com"
    - type: "#search-input" "AI 绘画"
    - click: ".search-button"
    - extract: ".note-item"
```

**TypeScript 注入**（适合复杂逻辑）：
```typescript
await page.goto('https://xiaohongshu.com');
await page.type('#search-input', 'AI 绘画');
await page.click('.search-button');
const notes = await page.evaluate(() => {
  return Array.from(document.querySelectorAll('.note-item'))
    .map(el => el.textContent);
});
```

---

## 📦 支持的平台（太丰富了！）

**社交平台**：
- Twitter/X, Reddit, Bilibili, 知乎, 小红书, V2EX, 雪球, BOSS直聘, LinkedIn

**桌面应用**：
- Cursor, Codex, Chatwise, Notion, Discord App, Antigravity

**新闻/资讯**：
- HackerNews, Dev.to, BBC, Bloomberg, Reuters, Wikipedia, ArXiv

**其他**：
- YouTube, Ctrip, Coupang, SMZDM, 小宇宙播客

**总计 20+ 平台**，基本覆盖了主流的社交、资讯、工具类应用。

---

## 🎯 使用场景

### 场景 1：AI Agent 自动化

让 AI 自动完成跨平台任务：

```
你：帮我监控知乎上"OpenClaw"关键词的最新讨论，每天汇总发送到邮箱
AI：好的，我来配置 opencli + cron 任务...
    [自动配置定时任务，每天抓取知乎数据，汇总后发邮件]
```

### 场景 2：数据采集与分析

无需 API Key，直接抓取平台数据：

```bash
# 抓取小红书某关键词的前 100 篇笔记
opencli xiaohongshu search "AI 绘画" --limit 100 --output notes.json

# 抓取 V2EX 某节点的最新主题
opencli v2ex topics --node "share" --limit 50 --output topics.json
```

### 场景 3：自动化工作流

结合其他工具，构建自动化流程：

```bash
# 抓取数据 + AI 分析 + 自动发布
opencli reddit fetch "r/MachineLearning" | \
  ai-analyze --model gpt-4 | \
  opencli notion create-page --database "MyResearch"
```

---

## 🔧 快速上手

### 安装

```bash
npm install -g opencli
```

### 基本使用

```bash
# 查看支持的应用
opencli list

# 操作 Chrome
opencli chrome --url "https://xiaohongshu.com"

# 操作 Cursor
opencli cursor --project ~/myproject

# 查看帮助
opencli --help
```

### AI Agent 集成

如果你在开发 AI Agent，可以直接读取 **AGENT.md** 文件，了解如何让 AI 调用 opencli。

---

## ⚠️ 注意事项

1. **合规使用**：虽然 opencli 技术上可以抓取任何平台，但请遵守平台的使用条款
2. **频率控制**：避免高频请求，以免触发平台的风控机制
3. **账号安全**：虽然是复用浏览器登录，但建议使用专门的账号进行自动化操作

---

## 💭 总结

**opencli 的核心价值**：

1. **零 API Key**：直接复用浏览器登录，无需申请任何凭证
2. **安全第一**：凭证永远不出浏览器，比传统爬虫安全 100 倍
3. **AI 友好**：专为 AI Agent 设计，支持自然语言任务编排
4. **生态丰富**：支持 20+ 平台，覆盖主流应用

**适用人群**：
- AI Agent 开发者
- 自动化工程师
- 数据分析师
- 需要跨平台操作的任何人

**开源地址**：https://github.com/opencli/opencli

**官网**：https://opencli.info/

如果觉得有用，点个"在看"吧 👇
