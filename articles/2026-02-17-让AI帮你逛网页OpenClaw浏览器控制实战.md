# 让 AI 帮你「逛」网页：OpenClaw 浏览器控制实战

> 本文由 OpenClaw AI 助手协助整理

【快速导航】
- 本文适合：想自动化重复网页操作的人
- 预计阅读：6 分钟
- 难度等级：⭐⭐⭐⭐

---

## 你是不是也这样？

每天早上打开浏览器，登录后台，检查数据，截图发群里……

每天晚上刷某个网站，看商品有没有降价……

每周都要填一堆重复的表单，复制粘贴到手软……

**如果有个 AI 帮你「逛」网页，自动完成这些操作呢？**

---

## 一、OpenClaw 浏览器控制是什么？

简单说：**你用自然语言发指令，AI 控制浏览器执行操作。**

底层基于 **Playwright** —— 微软开源的浏览器自动化框架，支持 Chrome、Firefox、Safari 三大浏览器。

**核心优势：**
- ✅ 不用写复杂脚本，自然语言即可
- ✅ 支持登录、填表、截图、数据抓取
- ✅ 可定时执行（配合 Cron）
- ✅ 本地运行，隐私安全

---

## 二、环境配置（5 分钟上手）

### 前置条件
- OpenClaw 已安装
- Node.js 18+

### 安装步骤

```bash
# 安装 Playwright 浏览器
npx playwright install chromium

# 验证安装
npx playwright --version
```

OpenClaw 内置 `browser` 工具，配置好后直接用自然语言控制：

```
Prompt: "打开百度，搜索 OpenClaw，截图保存"
```

---

## 三、实战案例 1：自动登录 + 截图

**场景：** 每天要登录某个后台查看数据

**传统方式：** 打开网站 → 输入账号密码 → 点登录 → 截图

**AI 方式：** 一句话搞定

```
Prompt: "打开 example.com/login，用账号 test@example.com 
和密码 123456 登录，登录成功后截图保存为 dashboard.png"
```

**OpenClaw 执行过程：**
1. 启动浏览器（无头模式）
2. 访问登录页
3. 自动填写账号密码
4. 点击登录按钮
5. 等待页面加载完成
6. 截图保存

**效果对比：**
- 手动操作：2-3 分钟
- AI 自动化：10 秒

---

## 四、实战案例 2：定时监控商品价格

**场景：** 某商品降价时自动通知

**实现步骤：**

### 1. 让 AI 抓取价格

```
Prompt: "打开京东商品页 https://item.jd.com/12345.html，
提取商品价格，告诉我当前价格是多少"
```

### 2. 配置定时任务

在 OpenClaw 中设置 Cron：

```json
{
  "name": "监控商品价格",
  "schedule": "0 9 * * *",
  "task": "检查商品价格，如果低于 500 元，发送 Discord 通知"
}
```

### 3. 价格对比逻辑

```
Prompt: "上次价格是 599 元，现在是 499 元，
降价了 100 元，发送通知到 Discord"
```

**效果：** 每天 9 点自动检查，降价立即通知你

---

## 五、实战案例 3：批量填写表单

**场景：** 要填 100 份同样的表单（比如批量注册、批量申请）

**传统方式：** 复制粘贴 100 次，耗时 2 小时

**AI 方式：**

### 1. 准备数据文件

`data.csv`：
```csv
name,email,phone
张三,zhangsan@example.com,13800138001
李四,lisi@example.com,13800138002
王五,wangwu@example.com,13800138003
```

### 2. 让 AI 批量处理

```
Prompt: "读取 data.csv 文件，逐行打开 
https://example.com/form，填写姓名、邮箱、电话，
提交后记录结果"
```

### 3. 查看执行报告

```
完成情况：
- 成功：98 条
- 失败：2 条（网络超时）
- 总耗时：15 分钟
```

**效果：** 2 小时 → 15 分钟，而且可以后台运行

---

## 六、GitHub 开源项目推荐

浏览器自动化生态非常成熟，以下是最值得关注的几个项目：

### 🔥 核心框架

| 项目 | Stars | 简介 |
|------|-------|------|
| **[Playwright](https://github.com/microsoft/playwright)** | 68k+ | 微软出品，OpenClaw 底层用的就是这个 |
| **[Puppeteer](https://github.com/puppeteer/puppeteer)** | 89k+ | Google 官方，Chrome 自动化首选 |
| **[Selenium](https://github.com/SeleniumHQ/selenium)** | 30k+ | 老牌框架，企业级测试常用 |

### 🤖 AI + 浏览器（新趋势）

| 项目 | Stars | 简介 |
|------|-------|------|
| **[browser-use](https://github.com/browser-use/browser-use)** | 50k+ | 🔥 用自然语言控制浏览器，AI Agent 自动操作 |
| **[Skyvern](https://github.com/Skyvern-AI/skyvern)** | 12k+ | AI 驱动自动化，无需写 CSS 选择器 |
| **[playwright-mcp](https://github.com/microsoft/playwright-mcp)** | 2k+ | Playwright 的 MCP 服务器，AI 直接控制浏览器 |

### 💡 推荐理由

- **Playwright** — 技术最先进，跨浏览器支持最好
- **browser-use** — 最适合小白，自然语言即可
- **playwright-mcp** — 和 OpenClaw 的 MCP 协议完美配合

---

## 七、进阶技巧

### 1. 反爬虫应对

```bash
# 随机 User-Agent
const userAgents = [
  'Mozilla/5.0 (Windows NT 10.0; Win64; x64)...',
  'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...'
];

# 请求间隔随机化
await page.waitForTimeout(Math.random() * 3000 + 1000);
```

### 2. 验证码处理

- **简单验证码**：用 OCR 识别（Tesseract.js）
- **复杂验证码**：暂停等待人工处理，或接入第三方打码平台

### 3. Headless 模式

服务器上后台运行，不弹出浏览器窗口：

```bash
# 启动时默认就是 headless
# 如需调试，临时关闭
HEADLESS=false openclaw start
```

### 4. 错误处理

```
Prompt: "如果 10 秒内没找到登录按钮，
截图保存错误现场，并发送通知"
```

---

## 八、常见问题 FAQ

**Q：和 Selenium 有什么区别？**
> Playwright 更现代，API 更简洁，自动等待元素，不需要手动 sleep。

**Q：会被网站封 IP 吗？**
> 合理设置间隔时间，随机化 User-Agent，大部分网站没问题。

**Q：支持哪些浏览器？**
> Chrome、Firefox、Safari（Playwright 原生支持）

**Q：能在服务器上无界面运行吗？**
> 可以，Headless 模式，无需显示器。

**Q：复杂交互怎么办？**
> 多步骤操作可以拆分，每步让 AI 确认后再继续。

---

## 九、总结

**浏览器自动化能帮你：**
- 自动登录、填表、截图
- 定时监控价格、库存
- 批量处理重复操作
- 数据采集和结构化

**时间对比：**
| 任务 | 手动 | AI 自动化 |
|------|------|----------|
| 每日登录截图 | 3 分钟 | 10 秒 |
| 监控 10 个商品 | 30 分钟 | 后台自动 |
| 填 100 份表单 | 2 小时 | 15 分钟 |

**下一步建议：**
1. 今天就试试让 OpenClaw 打开一个网页并截图
2. 找一个你每天重复做的网页操作，尝试自动化
3. 配合 Cron 定时任务，彻底解放双手

---

**明天预告：** 7x24 小时盯着网站变化，OpenClaw 自动化监控实战

---

如果这篇文章对你有帮助，欢迎 **点赞、在看、转发** 三连支持！

有任何问题，欢迎在评论区留言，我会一一回复。

明天见 👋
