# OpenClaw 插件开发入门：打造你的专属技能

OpenClaw 的强大不仅在于本身的功能，更在于它的可扩展性。今天我们来学习如何开发自己的插件，让 AI 助手获得新技能。

## 🤔 为什么要开发插件？

OpenClaw 的 Skills 系统让你可以：

• **扩展能力** - 添加原生不支持的功能
• **封装复杂流程** - 把多步操作变成一条命令
• **集成外部服务** - 连接你的私有 API、数据库
• **个性化定制** - 打造完全符合你需求的助手

## 📁 插件结构

一个标准的 Skill 目录结构：

```
~/.openclaw/skills/
└── my-skill/
    ├── SKILL.md          # 插件说明（必需）
    ├── scripts/          # 脚本文件
    │   └── main.sh
    └── assets/           # 资源文件
        └── example.png
```

## 📝 SKILL.md 核心要素

这是插件的"身份证"，告诉 AI 如何使用：

```markdown
# My Skill

## Description
简短描述这个插件做什么

## Usage
如何使用这个插件

## Triggers
- 触发关键词1
- 触发关键词2

## Script
scripts/main.sh
```

## 🎯 实战：创建天气查询插件

让我们创建一个简单的天气查询插件。

### 1. 创建目录

```bash
mkdir -p ~/.openclaw/skills/weather/scripts
```

### 2. 编写 SKILL.md

```markdown
# Weather Skill

## Description
获取指定城市的天气信息

## Usage
weather <城市名>

## Triggers
- 天气
- weather
- 查天气

## Script
scripts/weather.sh
```

### 3. 编写脚本

```bash
#!/bin/bash
CITY="${1:-Beijing}"
curl -s "wttr.in/$CITY?format=3"
```

### 4. 添加执行权限

```bash
chmod +x ~/.openclaw/skills/weather/scripts/weather.sh
```

## 🔧 高级技巧

### 使用环境变量

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "weather": {
      "apiKey": "YOUR_API_KEY"
    }
  }
}
```

脚本中通过环境变量访问：

```bash
#!/bin/bash
API_KEY="${WEATHER_API_KEY}"
# 使用 API_KEY 调用服务
```

### 支持多平台通知

```bash
#!/bin/bash
MESSAGE="任务完成！"

# 发送到 Discord
curl -X POST "$DISCORD_WEBHOOK" \
  -d "{\"content\": \"$MESSAGE\"}"

# 发送到飞书
curl -X POST "$FEISHU_WEBHOOK" \
  -H "Content-Type: application/json" \
  -d "{\"msg_type\": \"text\", \"content\": {\"text\": \"$MESSAGE\"}}"
```

## ⚠️ 注意事项

• **安全性** - 不要在脚本中硬编码敏感信息
• **错误处理** - 添加适当的错误检查和提示
• **日志记录** - 使用 `logger` 或写入日志文件
• **幂等性** - 脚本应该可以安全地重复执行

## 📚 学习资源

• OpenClaw 官方文档
• 内置 Skills 示例（`~/.npm-global/lib/node_modules/openclaw/skills/`）
• GitHub 社区贡献的 Skills

---

如果觉得有用，点个"在看"吧 👇
