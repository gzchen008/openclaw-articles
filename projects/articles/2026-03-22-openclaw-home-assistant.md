# OpenClaw + Home Assistant：智能家庭自动化

想象一下：早上醒来，窗帘自动拉开，咖啡机开始工作，音箱播放你喜欢的晨间音乐——而这一切，只需要对 AI 说一句话。

OpenClaw 与 Home Assistant 的结合，让这一切成为可能。

## 🤖 为什么选择这个组合？

Home Assistant 是目前最强大的开源智能家居平台，支持超过 1000 种设备。但它的自动化配置需要写 YAML，学习曲线陡峭。

OpenClaw 的加入改变了这一切：

- **自然语言控制**：不用写代码，说话就能控制设备
- **智能场景联动**：AI 理解你的意图，自动触发多个设备
- **语音远程操控**：通过 WhatsApp、Discord 随时随地控制家里
- **自动化监控**：异常情况自动推送通知

## 🔧 前置准备

在开始之前，你需要：

1. 一台运行 OpenClaw 的设备（Mac/Linux/树莓派）
2. Home Assistant 实例（建议使用 HAOS 或 Docker 部署）
3. 确保两者在同一网络，或通过内网穿透互通

### 获取 Home Assistant 信息

登录 Home Assistant，进入 **设置 → 关于**，记录：

- 访问地址（如 `http://192.168.1.100:8123`）
- 长期访问令牌（用户 → 安全 → 创建令牌）

## ⚙️ 配置 OpenClaw 连接

### 方法一：使用 OpenClaw 节点功能

如果你有树莓派或其他设备，可以通过 `nodes` 工具连接：

```yaml
# ~/.openclaw/openclaw.json
{
  "nodes": {
    "home-pi": {
      "host": "192.168.1.100",
      "type": "raspberry-pi"
    }
  }
}
```

### 方法二：通过 HTTP API 集成

OpenClaw 可以通过 Home Assistant 的 REST API 控制设备：

```yaml
# 在 OpenClaw 中配置
{
  "homeAssistant": {
    "url": "http://192.168.1.100:8123",
    "token": "YOUR_LONG_LIVED_ACCESS_TOKEN"
  }
}
```

## 🏠 实战场景

### 场景一：语音控制灯光

在 WhatsApp 或 Discord 中直接说：

> 打开客厅的灯，亮度 50%

OpenClaw 会自动：

1. 解析你的意图
2. 调用 Home Assistant API
3. 控制对应的灯光设备

### 场景二：离家模式

> 我出门了

AI 自动执行：

- 关闭所有灯光
- 启动安防摄像头
- 调低空调温度
- 发送确认通知

### 场景三：定时自动化

通过 OpenClaw 的 cron 功能设置定时任务：

```yaml
# 每天早上 7:00 自动开窗帘
{
  "name": "morning-routine",
  "schedule": {"kind": "cron", "expr": "0 7 * * *"},
  "payload": {
    "kind": "http",
    "url": "http://HA地址:8123/api/services/cover/open_cover",
    "body": {"entity_id": "cover.living_room_curtain"}
  }
}
```

## 📱 远程控制示例

无论你在家还是外出，都可以通过消息平台控制：

**WhatsApp**：直接发消息给绑定的号码

**Discord**：在配置的频道中 @机器人

**飞书**：群聊中 @机器人 或私聊

## 💡 进阶技巧

### 1. 创建场景脚本

在 Home Assistant 中定义场景，OpenClaw 一键触发：

```yaml
# Home Assistant configuration.yaml
script:
  movie_mode:
    sequence:
      - service: light.turn_off
        target:
          entity_id: light.living_room
      - service: cover.close_cover
        target:
          entity_id: cover.living_room_curtain
      - service: media_player.turn_on
        target:
          entity_id: media_player.tv
```

然后在 OpenClaw 中说：**开启电影模式**

### 2. 条件联动

结合传感器数据实现智能联动：

- 温度超过 28°C 自动开空调
- 检测到人移动自动开灯
- 门窗异常打开推送警报

### 3. 语音播报

配置 OpenClaw 的 TTS 功能，让智能家居"开口说话"：

- 门铃响起时播报"有客人来访"
- 洗衣机完成时提醒"衣服洗好了"
- 安防警报时语音提示

## 🔐 安全建议

1. **不要将 Home Assistant 暴露在公网**，使用 VPN 或内网穿透
2. **定期更换访问令牌**，避免长期使用同一个
3. **限制 OpenClaw 的设备控制权限**，只开放必要的设备
4. **启用 Home Assistant 的双因素认证**

## 🎯 效果展示

配置完成后，你的智能家居体验将升级为：

- **零代码配置**：说话代替写 YAML
- **多平台控制**：一个 AI 统管所有入口
- **智能理解**：AI 理解模糊指令，自动匹配设备
- **主动服务**：异常情况自动通知，不用盯着 App

---

如果觉得有用，点个"在看"吧 👇
