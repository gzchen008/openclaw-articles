# OpenClaw 安全设置指南：保护你的 AI 助手

昨天有个朋友问我："把 AI 助手接入这么多服务，安全吗？"

这个问题问得好。OpenClaw 能访问你的文件、日历、消息，甚至能执行命令，安全配置必须到位。

今天就来讲讲 OpenClaw 的安全机制，以及如何正确配置。

---

## 🔐 OpenClaw 的安全边界

首先了解 OpenClaw 能做什么、不能做什么。

### ✅ AI 能做的

读取你授权的文件、调用你配置的工具、执行你允许的命令、访问你连接的服务

### ❌ AI 不能做的

绕过权限控制、修改系统核心配置、访问未授权的资源、向外发送敏感数据

---

## ⚙️ 核心安全配置

### 1️⃣ 认证保护

OpenClaw 的配置文件包含敏感信息，必须保护好。

**配置文件位置**

~/.openclaw/openclaw.json

**安全建议**

不要提交到 Git、不要分享给他人、定期更换 token、使用环境变量存储敏感值

### 2️⃣ 命令执行控制

OpenClaw 可以执行 shell 命令，但有安全限制。

**查看 AGENTS.md 中的红线命令**

红线命令需要人工确认才能执行，包括：

rm -rf /、mkfs、dd if=、修改认证文件、外发敏感数据、crontab -e、eval "$(curl ...)"

**如何自定义红线**

编辑 ~/.openclaw/workspace/AGENTS.md，在"红线命令"部分添加你的规则。

### 3️⃣ 工具权限控制

不是所有工具都应该开启。

**在 openclaw.json 中配置**

```json
{
  "tools": {
    "policy": "allowlist",
    "allow": ["read", "write", "web_search"]
  }
}
```

这样只允许使用白名单中的工具。

---

## 🛡️ 高级安全设置

### 外部访问控制

如果你通过 ngrok 或 frp 暴露服务：

**必须做**

设置强密码、启用 HTTPS、限制访问 IP、关闭不必要的端口

**推荐配置**

```json
{
  "gateway": {
    "auth": {
      "enabled": true,
      "token": "YOUR_STRONG_TOKEN_HERE"
    },
    "cors": {
      "origins": ["https://your-domain.com"]
    }
  }
}
```

### 日志审计

开启日志记录，方便追溯问题。

```json
{
  "logging": {
    "level": "info",
    "file": "~/.openclaw/logs/openclaw.log",
    "maxSize": "10MB"
  }
}
```

---

## ⚠️ 常见安全隐患

### 密码明文存储

❌ 错误：直接写在配置文件

```json
{
  "password": "my-password-123"
}
```

✅ 正确：使用环境变量

```json
{
  "password": "${MY_PASSWORD}"
}
```

### 过度授权

❌ 错误：给 AI 过多权限

```json
{
  "exec": {
    "security": "full"
  }
}
```

✅ 正确：按需授权

```json
{
  "exec": {
    "security": "deny",
    "allowlist": ["ls", "cat", "git"]
  }
}
```

### 忽略红线警告

当 AI 提示"需要确认"时，不要习惯性点同意。看清楚要执行什么命令。

---

## 📋 安全检查清单

定期检查这些项目：

• openclaw.json 没有提交到 Git
• token 定期更换
• 红线命令配置正确
• 日志审计已开启
• 外部访问有认证保护
• 敏感信息使用环境变量

---

## 💡 总结

OpenClaw 的安全机制很完善，关键是你配置要正确：

1. 保护好配置文件
2. 理解红线命令
3. 按需授权工具
4. 开启日志审计
5. 定期检查配置

安全不是一次性的事，而是持续的过程。

如果觉得有用，点个"在看"吧 👇
