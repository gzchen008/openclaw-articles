# WebMCP 安装指南

## 📦 已安装内容

### 1. NPM 包
- `@mcp-b/transports` - MCP 传输层
- `@modelcontextprotocol/sdk` - MCP 官方 SDK
- `zod` - 参数验证

### 2. Native Server（全局）
- `@mcp-b/native-server` - 用于连接本地 MCP 客户端

---

## 🚀 使用方法

### 方式一：Chrome 扩展

1. **安装扩展**
   - 访问 [MCP-B Chrome 扩展](https://chromewebstore.google.com/detail/mcp-b/daohopfhkdelnpemnhlekblhnikhdhfa)
   - 点击"添加到 Chrome"

2. **打开示例页面**
   ```bash
   cd /Users/cgz/.openclaw/workspace/webmcp
   # 使用任意本地服务器，例如：
   npx serve .
   # 或
   python3 -m http.server 8080
   ```

3. **测试工具**
   - 打开浏览器访问 `http://localhost:8080`
   - 点击 MCP-B 扩展图标
   - 在 "Tools" 标签页查看可用工具
   - 在聊天界面输入："显示一条通知：Hello WebMCP"

### 方式二：本地 MCP 客户端（Claude/Cursor）

1. **启动 Native Server**
   ```bash
   @mcp-b/native-server
   ```
   默认监听 `http://127.0.0.1:12306`

2. **配置 MCP 客户端**

   **Claude Desktop** (`~/Library/Application Support/Claude/claude_desktop_config.json`):
   ```json
   {
     "mcpServers": {
       "webmcp": {
         "type": "streamable-http",
         "url": "http://127.0.0.1:12306/mcp"
       }
     }
   }
   ```

   **Cursor** (`.cursor/mcp.json`):
   ```json
   {
     "servers": {
       "webmcp": {
         "type": "streamable-http",
         "url": "http://127.0.0.1:12306/mcp"
       }
     }
   }
   ```

---

## 📁 文件结构

```
webmcp/
├── package.json          # NPM 配置
├── example-server.js     # 纯 JS 示例
├── index.html            # 完整网页示例
└── README.md             # 本文档
```

---

## 🛠️ 可用工具

| 工具名 | 描述 | 参数 |
|--------|------|------|
| `getPageInfo` | 获取当前页面信息 | 无 |
| `showNotification` | 显示通知 | `message: string` |
| `addTodo` | 添加待办事项 | `title: string`, `priority?: "low"\|"medium"\|"high"` |
| `getTodos` | 获取待办列表 | 无 |

---

## 🔗 相关链接

- [WebMCP 官方提案](https://github.com/webmachinelearning/webmcp)
- [MCP-B 实现](https://github.com/MiguelsPizza/WebMCP)
- [MCP 协议](https://modelcontextprotocol.io/)
- [文档](https://mcp-b.ai)

---

## 💡 与 OpenClaw 集成

可以将 WebMCP 集成到 OpenClaw 的 Skills 中，让 OpenClaw 能够：
- 控制浏览器中的网页
- 调用网页暴露的 MCP 工具
- 实现更智能的浏览器自动化

---

*安装时间：2026-02-15*
