# 把 ChatGPT 装进 WhatsApp，秒变智能客服

> 本文由 OpenClaw AI 助手协助整理

【快速导航】
- 本文适合：外贸从业者、跨境电商卖家、需要海外客服的人
- 预计阅读：8 分钟
- 难度等级：⭐⭐⭐

---

## 痛点开场：你还在半夜 3 点回客户消息吗？

想象一下这个场景：

凌晨 2 点，你在睡梦中被 WhatsApp 提示音吵醒。打开手机一看，是海外客户的咨询：

> "Hi, could you tell me the shipping time to New York?"

你迷迷糊糊地打字回复，生怕打错一个字影响专业形象。第二天早上醒来，发现又有 3 个客户在不同时间发了消息，你只能一个一个手动回复...

**这就是大部分跨境电商、外贸人的日常。**

如果 WhatsApp 里有个 24 小时在线的 AI 客服，能自动回复常见问题、报价、查物流状态，甚至帮你成交订单，会是什么体验？

今天教你用 **OpenClaw**，把 ChatGPT 装进 WhatsApp，让 AI 帮你全天候守着客户。

---

## 最终效果展示

配置完成后，你的 WhatsApp 会变成这样：

✅ **自动回复常见问题**："什么时候发货？" → 立即回复物流时效
✅ **产品智能报价**：客户发产品图 → 自动计算价格
✅ **多语言支持**：客户发西语 → 自动用西语回复
✅ **24 小时在线**：半夜 3 点也能秒回
✅ **人工接管**：复杂问题一键转人工

效果就像你请了个全职客服，每月还不用发工资 💰

---

## 前置准备

在开始之前，你需要准备：

1️⃣ **一个 WhatsApp 账号**（个人号即可）
2️⃣ **一台安装了 OpenClaw 的服务器**（Mac mini/Linux/VPS 均可）
3️⃣ **Meta Developer 账号**（免费注册）
4️⃣ **10-15 分钟时间**

⚠️ **注意**：OpenClaw 的 WhatsApp 集成需要使用 Meta 的 WhatsApp Business API，但配置过程对普通用户友好，无需编程经验。

---

## 步骤一：注册 Meta 开发者账号

首先，你需要申请 WhatsApp Business API 的访问权限：

1. 访问 [Meta for Developers](https://developers.facebook.com/)
2. 点击右上角 **"Get Started"** 或 **"Log In"**
3. 使用你的 Facebook 账号登录
4. 创建一个新应用：
   - 点击 **"Create App"**
   - 选择 **"Business"** 类型
   - 填写应用名称（如：`MyAIAssistant`）
   - 填写联系方式邮箱
5. 进入应用后，点击 **"Add Product"** → **"WhatsApp"** → **"Continue"**

完成这一步，你就有了一个可以调用 WhatsApp API 的应用凭证。

---

## 步骤二：配置 WhatsApp Business API

在 Meta 开发者后台：

1. 在左侧菜单找到 **"WhatsApp"** → **"Getting Started"**
2. 点击 **"Select a number"**，关联你的 WhatsApp 号码
3. 获取以下信息（重要，请记好）：
   - **Phone Number ID**：类似 `123456789012345`
   - **WhatsApp Business Account ID (WABA ID)**：类似 `987654321098765`
   - **Access Token**：点击 **"Add"** 创建临时访问令牌
     - 选择权限：`whatsapp_business_messaging`、`whatsapp_business`
     - 设置有效期（建议 60 天，到期后可续期）
4. 在 **"Test your setup"** 部分，测试发送一条消息：
   - 发送 "Hello" 到你的 WhatsApp 号码
   - 收到后说明配置成功

🔥 **安全提示**：Access Token 就像你的账号密码，千万不要泄露！

---

## 步骤三：在 OpenClaw 中配置 WhatsApp

现在，打开你的终端，连接到安装了 OpenClaw 的服务器：

```bash
# SSH 连接（如果是远程服务器）
ssh your-user@your-server-ip

# 进入 OpenClaw 配置目录
cd ~/.openclaw
```

编辑配置文件：

```bash
# 编辑配置
vim config/config.yaml
```

添加 WhatsApp 配置：

```yaml
channels:
  whatsapp:
    enabled: true
    # Meta 开发者凭证
    phoneNumberId: "YOUR_PHONE_NUMBER_ID"
    accessToken: "YOUR_ACCESS_TOKEN"
    webhookVerifyToken: "YOUR_VERIFY_TOKEN_HERE"
    # 可选：业务信息
    businessName: "Your Business Name"
    businessHours: "9:00-18:00"
```

**重要参数说明：**
- `phoneNumberId`：步骤二获取的 Phone Number ID
- `accessToken`：步骤二获取的 Access Token
- `webhookVerifyToken`：自定义一个字符串，比如 `my-secret-token-123`

保存并退出编辑器。

---

## 步骤四：配置 Webhook 接收消息

OpenClaw 需要通过 Webhook 接收 WhatsApp 的消息。你需要一个公网地址：

### 如果你的服务器有公网 IP：

直接使用服务器 IP + 端口（默认 3000）：

```yaml
channels:
  whatsapp:
    enabled: true
    phoneNumberId: "YOUR_PHONE_NUMBER_ID"
    accessToken: "YOUR_ACCESS_TOKEN"
    webhookVerifyToken: "YOUR_VERIFY_TOKEN_HERE"
    # Webhook 配置
    webhookUrl: "https://YOUR_SERVER_IP:3000/webhooks/whatsapp"
```

### 如果服务器在内网（没有公网 IP）：

使用 **ngrok** 暴露本地端口：

```bash
# 安装 ngrok（如果没有）
brew install ngrok  # macOS
# 或
curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | \
  sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null && \
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | \
  sudo tee /etc/apt/sources.list.d/ngrok.list && \
  sudo apt update && sudo apt install ngrok  # Linux

# 启动 ngrok
ngrok http 3000
```

ngrok 会显示一个公网 URL，比如 `https://abc123.ngrok.io`，复制这个地址，更新配置：

```yaml
channels:
  whatsapp:
    enabled: true
    phoneNumberId: "YOUR_PHONE_NUMBER_ID"
    accessToken: "YOUR_ACCESS_TOKEN"
    webhookVerifyToken: "YOUR_VERIFY_TOKEN_HERE"
    # 使用 ngrok 提供的公网地址
    webhookUrl: "https://abc123.ngrok.io/webhooks/whatsapp"
```

---

## 步骤五：重启 OpenClaw 生效

配置完成后，重启 OpenClaw：

```bash
# 重启 OpenClaw
openclaw gateway restart
```

查看启动日志，确保没有报错：

```bash
# 查看日志
openclaw gateway logs

# 应该看到类似输出
# [INFO] WhatsApp channel initialized
# [INFO] Webhook listening on :3000/webhooks/whatsapp
```

---

## 步骤六：在 Meta 后台注册 Webhook

回到 Meta 开发者后台：

1. 进入 **WhatsApp** → **Configuration** → **Webhooks**
2. 点击 **"Edit"** 或 **"Setup"**：
   - **Webhook URL**：填入你的 Webhook 地址（如 `https://YOUR_SERVER_IP:3000/webhooks/whatsapp`）
   - **Verify Token**：填入你在配置文件中设置的 `YOUR_VERIFY_TOKEN_HERE`
3. 点击 **"Verify and Save"**，如果显示 ✅ 绿色勾，说明验证成功
4. 订阅 Webhook 事件：
   - 点击 **"Manage"** webhook 字段
   - 勾选以下事件：
     - ✅ `messages`
     - ✅ `message_delivery`
   - 点击 **"Save"**

---

## 步骤七：测试智能客服

现在一切就绪，打开你的 WhatsApp，给关联的号码发一条消息试试：

```
发送：你好

AI 回复：您好！我是 AI 智能客服，有什么可以帮您的吗？
```

如果收到 AI 回复，恭喜你 🎉 配置成功！

---

## 进阶玩法：定制你的 AI 客服

### 1️⃣ 设置客服人设

编辑 OpenClaw 配置，添加客服身份：

```yaml
channels:
  whatsapp:
    enabled: true
    phoneNumberId: "YOUR_PHONE_NUMBER_ID"
    accessToken: "YOUR_ACCESS_TOKEN"
    webhookVerifyToken: "YOUR_VERIFY_TOKEN_HERE"
    webhookUrl: "https://YOUR_SERVER_IP:3000/webhooks/whatsapp"
    # 客服人设
    persona: |
      你是一家跨境电商的客服代表，名叫"小助手"。
      你的特点是：专业、友好、高效。
      常见问题包括：
      - 物流时效：美国7-10天，欧洲5-7天
      - 退换货：30天无理由退换
      - 支付方式：支持PayPal、信用卡、微信支付
      回复要简洁明了，不超过200字。
```

### 2️⃣ 自动回复价格

让 AI 能根据客户发来的产品图片自动报价：

**客户发送：** [产品图片]

**AI 自动回复：**
> 这款产品目前售价 $29.99，支持批量采购优惠：
> - 5-10 件：95折
> - 11-50 件：9折
> - 50+ 件：85折
> 需要下单吗？

### 3️⃣ 多语言自动切换

配置语言检测，客户发什么语言，AI 就用什么语言回复：

```yaml
channels:
  whatsapp:
    enabled: true
    # ... 其他配置 ...
    # 多语言支持
    autoDetectLanguage: true
    supportedLanguages:
      - zh  # 中文
      - en  # 英文
      - es  # 西班牙语
      - pt  # 葡萄牙语
```

---

## 常见问题（避坑指南）

### ❌ Q1：收不到消息，只有 Webhook 验证成功？

**A**：检查是否订阅了 `messages` 事件。在 Meta 后台 → Webhooks → Manage，确保 `messages` 已勾选。

### ❌ Q2：AI 回复太慢，客户等不及？

**A**：调整 OpenClaw 的响应超时时间：

```yaml
channels:
  whatsapp:
    enabled: true
    # ... 其他配置 ...
    timeoutSeconds: 30  # 默认30秒，可根据需要调整
```

### ❌ Q3：Access Token 过期了怎么办？

**A**：Access Token 有效期最长 60 天。过期前，在 Meta 后台重新生成，并更新 OpenClaw 配置：

```bash
# 更新 Access Token 后重启
openclaw gateway restart
```

### ❌ Q4：ngrok 地址每次启动都会变？

**A**：是的，免费版 ngrok 会随机分配地址。两个解决方案：
1. **升级 ngrok 付费版**（$10/月），获得固定域名
2. **使用服务器公网 IP + 域名**（推荐长期使用）

### ❌ Q5：如何处理复杂问题转人工？

**A**：在客服人设中加入转人工指令：

```yaml
persona: |
  ... 客服人设内容 ...
  如果客户的问题涉及：
  - 退款申请
  - 投诉建议
  - 复杂的技术问题
  请回复："您的问题比较复杂，已为您转接人工客服，请稍等..."
  同时在后台通知人工介入。
```

---

## 实战案例：我的一天

配置完成后，我的 WhatsApp 客服是这样工作的：

**早上 8:00**：打开手机，查看昨晚的客服记录
- AI 处理了 23 条客户消息
- 成功回答 18 条常见问题
- 5 条转人工，我逐一跟进

**上午 10:00**：参加商务会议，无需担心漏回消息
- AI 自动响应所有咨询
- 复杂问题记录，会后集中处理

**下午 2:00**：休息时间，客户照样能得到回复
- AI 保持 24 小时在线
- 不用再抱着手机守着

**一天下来**：省下 3-4 小时，客户满意度反而提升。

---

## 下一步建议

🎯 **今天你可以做：**
1. 按照教程完成 WhatsApp + OpenClaw 配置
2. 测试几条消息，确保 AI 正常回复
3. 写下你的客服人设，让 AI 更符合你的品牌调性

📅 **明天预告：**
明天教你配置 **Telegram 机器人**，打造更强大的自动化客服系统，支持群组管理、定时推送等功能！

---

如果这篇文章对你有帮助，欢迎 **点赞、在看、转发** 三连支持！

任何配置问题，欢迎在评论区留言，我会一一回复。

明天见 👋
