# 从 0 到 1 理解 OpenClaw：Gateway-Client-Node 三层架构

> 本文是 OpenClaw 源码解读系列的第 1 篇，将深入剖析 OpenClaw 的整体架构设计。

---

## 🎯 为什么需要三层架构？

如果你想让 AI 助手同时在 WhatsApp、Telegram、Discord、飞书等 20+ 平台上工作，同时还能控制你的手机、电脑、智能家居设备，你会怎么设计？

**传统方案的困境**：
- ❌ **单体架构**：所有功能耦合在一起，难以扩展
- ❌ **直连模式**：每个客户端都直接连接消息平台，导致会话冲突
- ❌ **轮询模式**：客户端定期检查消息，效率低下且实时性差

**OpenClaw 的解决方案**：
- ✅ **Gateway（网关）**：统一管理所有消息平台和 AI 会话
- ✅ **Client（客户端）**：提供控制界面（macOS app、CLI、web UI）
- ✅ **Node（节点）**：控制具体设备（手机、电脑、智能家居）

这种**控制平面与数据平面分离**的设计，让 OpenClaw 具备了强大的扩展性和灵活性。

---

## 🏗️ 三层架构详解

### 架构图

```
┌─────────────────────────────────────────────────┐
│                 Client Layer                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │ macOS App│  │   CLI    │  │  Web UI  │     │
│  └─────┬────┘  └─────┬────┘  └─────┬────┘     │
└────────┼─────────────┼─────────────┼───────────┘
         │             │             │
         └─────────────┼─────────────┘
                       │ WebSocket
                       ↓
┌─────────────────────────────────────────────────┐
│              Gateway Layer (控制平面)             │
│  ┌──────────────────────────────────────────┐  │
│  │  WebSocket Server (127.0.0.1:18789)      │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │  Message Router (消息路由)                 │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │  Session Manager (会话管理)               │  │
│  └──────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────┐  │
│  │  Model Provider (模型提供者)              │  │
│  └──────────────────────────────────────────┘  │
└───────────────────────┬─────────────────────────┘
                        │ WebSocket
                        ↓
┌─────────────────────────────────────────────────┐
│                 Node Layer                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐     │
│  │  macOS   │  │   iOS    │  │ Android  │     │
│  │  Node    │  │   Node   │  │  Node    │     │
│  └──────────┘  └──────────┘  └──────────┘     │
│  ┌──────────────────────────────────────────┐  │
│  │  Device Commands (设备命令)                │  │
│  │  - camera.snap (拍照)                     │  │
│  │  - screen.record (录屏)                   │  │
│  │  - location.get (定位)                    │  │
│  │  - canvas.* (画布控制)                    │  │
│  └──────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
         ↑                    ↑
         │                    │
    Provider SDKs        Platform APIs
    (Baileys, grammY)    (Telegram, WhatsApp)
```

---

## 📦 Gateway（网关）- 控制平面

**Gateway 是整个系统的大脑**，负责：
- 📱 **管理消息平台连接**（WhatsApp、Telegram、Discord 等）
- 🔄 **路由消息**（从消息平台 → AI → 消息平台）
- 🧠 **管理 AI 会话**（Session、Context、Memory）
- 🔐 **认证和授权**（设备配对、token 验证）
- 📊 **健康监控**（心跳检测、状态同步）

### 核心职责

#### 1. WebSocket 服务器
```javascript
// Gateway 启动 WebSocket 服务器
const server = new WebSocket.Server({
  host: '127.0.0.1',
  port: 18789
});

// 监听连接
server.on('connection', (ws, req) => {
  // 第一帧必须是 connect
  ws.once('message', (data) => {
    const frame = JSON.parse(data);
    if (frame.type !== 'connect') {
      ws.close(4002, 'First frame must be connect');
      return;
    }
    handleConnect(ws, frame);
  });
});
```

#### 2. 消息路由
```javascript
// 消息路由逻辑
class MessageRouter {
  async routeInbound(message) {
    // 1. 解析来源平台（WhatsApp/Telegram/Discord）
    const channel = message.channel;
    
    // 2. 解析目标 Session
    const sessionKey = this.resolveSession(message);
    
    // 3. 调用 AI Agent
    const response = await this.agent.run({
      sessionKey,
      message: message.text,
      channel
    });
    
    // 4. 路由回复
    await this.routeOutbound(response);
  }
}
```

#### 3. 会话管理
```javascript
// Session 管理器
class SessionManager {
  async getSession(sessionKey) {
    // 从磁盘加载 Session
    const session = await this.loadSession(sessionKey);
    
    // 加载上下文（memory.md、context files）
    await this.loadContext(session);
    
    // 加载技能
    await this.loadSkills(session);
    
    return session;
  }
}
```

### 关键特性

**单例模式**：
- 每个 host 只运行一个 Gateway 实例
- 避免多个实例导致 WhatsApp 会话冲突
- 保证会话状态一致性

**持久化连接**：
- Gateway 作为守护进程运行（launchd/systemd）
- 自动重启，保持 24/7 在线
- 管理所有消息平台的长期连接

---

## 🖥️ Client（客户端）- 控制界面

**Client 是用户与 OpenClaw 交互的界面**，负责：
- 💬 **发送消息**（通过 WebSocket 连接到 Gateway）
- 📊 **查看状态**（Gateway 健康状态、会话列表）
- ⚙️ **配置管理**（模型选择、技能配置）
- 🔍 **调试工具**（查看日志、会话历史）

### 客户端类型

#### 1. macOS App
```swift
// Swift 客户端连接 Gateway
let ws = WebSocket(url: URL(string: "ws://127.0.0.1:18789")!)

// 发送 connect 帧
let connectFrame = [
  "type": "connect",
  "id": deviceId,
  "params": [
    "auth": ["token": gatewayToken],
    "role": "operator"
  ]
]
ws.send(try JSONEncoder().encode(connectFrame))
```

#### 2. CLI（命令行）
```bash
# CLI 连接 Gateway
openclaw agent --message "Hello" --thinking high

# 底层通过 WebSocket 发送
{
  "type": "req",
  "id": "uuid-123",
  "method": "agent",
  "params": {
    "message": "Hello",
    "thinking": "high"
  }
}
```

#### 3. Web UI
```javascript
// Web UI 连接 Gateway
const ws = new WebSocket('ws://127.0.0.1:18789');

ws.send(JSON.stringify({
  type: 'req',
  id: 'req-456',
  method: 'status',
  params: {}
}));
```

### 关键特性

**多客户端并发**：
- 可以同时连接多个 Client（macOS app + CLI + web UI）
- 所有客户端共享同一个 Gateway 状态
- 实时同步会话和消息

**远程访问**：
```bash
# 通过 SSH 隧道远程访问
ssh -N -L 18789:127.0.0.1:18789 user@remote-host

# 或通过 Tailscale
openclaw gateway --host 100.71.105.40
```

---

## 📱 Node（节点）- 设备控制

**Node 是连接具体设备的代理**，负责：
- 📸 **设备命令执行**（拍照、录屏、定位）
- 🎨 **Canvas 渲染**（实时 AI 画布）
- 🔔 **本地通知**（推送通知到设备）
- 📂 **文件访问**（访问设备文件系统）

### 节点类型

#### 1. macOS Node
```javascript
// macOS Node 连接 Gateway
const node = new NodeClient({
  role: 'node',
  caps: ['camera.*', 'screen.record', 'location.get'],
  commands: {
    'camera.snap': async () => {
      // 调用 macOS 拍照 API
      const image = await capturePhoto();
      return { image };
    },
    'screen.record': async (params) => {
      // 调用 macOS 录屏 API
      const video = await recordScreen(params.duration);
      return { video };
    }
  }
});

node.connect('ws://127.0.0.1:18789');
```

#### 2. iOS Node
```swift
// iOS Node（通过 App）
class iOSNode: NodeClient {
  func connect(gateway: String, token: String) {
    // 连接 Gateway
    let ws = WebSocket(url: URL(string: gateway)!)
    
    // 注册能力
    let caps = ["camera.*", "location.get", "notification.*"]
    
    // 发送 connect
    ws.send([
      "type": "connect",
      "params": [
        "role": "node",
        "caps": caps,
        "auth": ["token": token]
      ]
    ])
  }
}
```

#### 3. Android Node
```kotlin
// Android Node
class AndroidNode : NodeClient {
  fun connect(gateway: String, token: String) {
    val ws = WebSocket(URI(gateway))
    
    // 注册命令
    val commands = mapOf(
      "camera.snap" to { params -> takePhoto() },
      "location.get" to { params -> getLocation() }
    )
    
    ws.connect()
  }
}
```

### 关键特性

**设备配对**：
```javascript
// 设备配对流程
1. Node 发送 connect + device_id
2. Gateway 检查是否已配对
   - 如果已配对 → 验证 device_token
   - 如果未配对 → 等待用户批准
3. 用户在 Client 批准配对
4. Gateway 返回 device_token
5. Node 保存 device_token，下次连接使用
```

**能力声明**：
```javascript
// Node 声明自己的能力
{
  "role": "node",
  "caps": ["camera.*", "screen.record"],
  "commands": ["camera.snap", "screen.record"]
}

// Gateway 根据能力路由命令
if (node.caps.includes('camera.*')) {
  // 允许调用 camera.snap
}
```

---

## 🔄 WebSocket 协议详解

### 帧类型

#### 1. Connect（连接）
```json
{
  "type": "connect",
  "id": "device-uuid-123",
  "params": {
    "role": "operator",  // 或 "node"
    "auth": {
      "token": "gateway-token-abc"
    },
    "caps": ["camera.*"],  // 仅 node 需要
    "commands": ["camera.snap"]  // 仅 node 需要
  }
}
```

#### 2. Request-Response（请求-响应）
```json
// Request
{
  "type": "req",
  "id": "req-uuid-456",
  "method": "agent",
  "params": {
    "message": "Hello",
    "sessionKey": "user:123456"
  }
}

// Response
{
  "type": "res",
  "id": "req-uuid-456",
  "ok": true,
  "payload": {
    "runId": "run-uuid-789",
    "status": "accepted"
  }
}
```

#### 3. Event（事件推送）
```json
{
  "type": "event",
  "event": "agent",
  "payload": {
    "stream": "assistant",
    "delta": "Hello!"
  },
  "seq": 1,
  "stateVersion": 123
}
```

### 认证流程

```
┌──────────┐
│  Client  │
└─────┬────┘
      │ 1. connect + device_id
      ↓
┌──────────────┐
│   Gateway    │
└─────┬────────┘
      │ 2. 检查 device_token
      │    - 如果有效 → 跳到步骤 5
      │    - 如果无效 → 步骤 3
      ↓
┌──────────────┐
│   Gateway    │
└─────┬────────┘
      │ 3. 生成 challenge
      │    challenge: "nonce-abc123"
      ↓
┌──────────┐
│  Client  │
└─────┬────┘
      │ 4. 签名 challenge
      │    signature: sign(challenge + device_id)
      ↓
┌──────────────┐
│   Gateway    │
└─────┬────────┘
      │ 5. 验证签名
      │    - 如果通过 → 返回 device_token
      │    - 如果失败 → 关闭连接
      ↓
┌──────────┐
│  Client  │
└──────────┘
```

---

## 🔐 安全设计

### 1. 本地信任（Local Trust）
```javascript
// 本地连接（127.0.0.1 或 Tailscale IP）可自动批准
if (isLocalConnection(clientIP) || isTailscaleIP(clientIP)) {
  // 自动批准配对
  autoApprovePairing(deviceId);
}
```

### 2. 远程审批
```javascript
// 远程连接需要用户手动批准
if (!isLocalConnection(clientIP)) {
  // 等待用户在 Client 批准
  await waitForApproval(deviceId);
}
```

### 3. Token 认证
```javascript
// 所有连接必须提供 gateway token
if (params.auth.token !== process.env.OPENCLAW_GATEWAY_TOKEN) {
  ws.close(4001, 'Invalid token');
}
```

---

## 🚀 实战：如何构建类似的系统？

### 核心设计原则

#### 1. 控制平面与数据平面分离
```javascript
// ❌ 错误：客户端直接连接消息平台
class Client {
  connectWhatsApp() { /* ... */ }
  connectTelegram() { /* ... */ }
}

// ✅ 正确：通过 Gateway 统一管理
class Gateway {
  providers = {
    whatsapp: new WhatsAppProvider(),
    telegram: new TelegramProvider()
  };
  
  routeMessage(message) {
    // 统一路由
  }
}
```

#### 2. WebSocket 作为通信协议
```javascript
// WebSocket 的优势：
// 1. 双向通信（Server → Client 推送）
// 2. 实时性（不需要轮询）
// 3. 轻量级（相比 HTTP，开销更小）
// 4. 跨平台（所有语言都支持）

const ws = new WebSocket('ws://gateway:18789');
ws.on('message', (data) => {
  const frame = JSON.parse(data);
  handleMessage(frame);
});
```

#### 3. 设备配对机制
```javascript
// 设备配对保证安全性
class PairingManager {
  async pair(deviceId, signature) {
    // 1. 验证签名
    if (!verifySignature(signature)) {
      throw new Error('Invalid signature');
    }
    
    // 2. 生成 device token
    const token = generateToken();
    
    // 3. 保存配对信息
    await this.save(deviceId, token);
    
    return token;
  }
}
```

### 关键技术点

#### 1. Provider SDK 集成
```javascript
// WhatsApp（使用 Baileys）
import { makeWASocket } from '@whiskeysockets/baileys';

const sock = makeWASocket({
  auth: authState,
  printQRInTerminal: true
});

sock.ev.on('messages.upsert', (m) => {
  // 路由到 Gateway
  gateway.routeMessage(m);
});
```

#### 2. Session 持久化
```javascript
// Session 存储到磁盘
class SessionStorage {
  async save(sessionKey, session) {
    const path = `sessions/${sessionKey}.json`;
    await fs.writeFile(path, JSON.stringify(session));
  }
  
  async load(sessionKey) {
    const path = `sessions/${sessionKey}.json`;
    const data = await fs.readFile(path, 'utf-8');
    return JSON.parse(data);
  }
}
```

#### 3. 健康监控
```javascript
// 心跳检测
setInterval(() => {
  for (const client of clients) {
    if (client.lastHeartbeat < Date.now() - 30000) {
      client.close();
    }
  }
}, 10000);
```

---

## 📊 性能考量

### 1. 连接管理
```javascript
// 限制每个 IP 的连接数
const connectionsPerIP = new Map();

server.on('connection', (ws, req) => {
  const ip = req.socket.remoteAddress;
  const count = connectionsPerIP.get(ip) || 0;
  
  if (count > 5) {
    ws.close(4003, 'Too many connections');
    return;
  }
  
  connectionsPerIP.set(ip, count + 1);
});
```

### 2. 消息队列
```javascript
// 使用队列避免阻塞
import { Queue } from 'bullmq';

const messageQueue = new Queue('messages');

messageQueue.add('process', {
  messageId: 'msg-123',
  channel: 'whatsapp',
  text: 'Hello'
});
```

### 3. 负载均衡
```javascript
// 如果需要水平扩展，可以使用 Redis Pub/Sub
import Redis from 'ioredis';

const redis = new Redis();

// Gateway 1 发布消息
redis.publish('messages', JSON.stringify(message));

// Gateway 2 订阅消息
redis.subscribe('messages', (channel, message) => {
  handleMessage(JSON.parse(message));
});
```

---

## 🎯 总结

### 三层架构的优势

| 架构层 | 职责 | 优势 |
|--------|------|------|
| **Gateway** | 控制平面 | 统一管理、避免冲突、持久化连接 |
| **Client** | 用户界面 | 多客户端并发、远程访问、灵活配置 |
| **Node** | 设备控制 | 能力声明、设备隔离、按需连接 |

### 核心设计思想

1. **控制平面与数据平面分离**：Gateway 作为唯一的控制中心
2. **WebSocket 作为通信协议**：实时、双向、跨平台
3. **设备配对机制**：安全、可控、可审计
4. **能力声明**：Node 声明自己的能力，Gateway 按需路由

### 下一步

在下一篇文章中，我们将深入剖析 **Agent Loop**，看看 OpenClaw 如何从一条消息到最终回复的完整旅程。

---

**系列文章**：
- 第 1 篇：从 0 到 1 理解 OpenClaw：Gateway-Client-Node 三层架构 ✅（本文）
- 第 2 篇：OpenClaw Agent Loop：从消息到回复的完整旅程
- 第 3 篇：OpenClaw 如何支持 20+ AI 模型？多模型架构设计
- 第 4 篇：OpenClaw Session 管理：如何保持 AI 长期记忆？

---

**参考资源**：
- [OpenClaw 官方文档](https://docs.openclaw.ai)
- [Gateway 架构文档](https://docs.openclaw.ai/concepts/architecture)
- [WebSocket 协议 RFC 6455](https://datatracker.ietf.org/doc/html/rfc6455)
- [Baileys - WhatsApp Web API](https://github.com/WhiskeySockets/Baileys)

---

**作者**：小J  
**发布日期**：2026-03-09  
**系列**：OpenClaw 源码解读系列  
**标签**：#OpenClaw #架构设计 #WebSocket #AI Agent
