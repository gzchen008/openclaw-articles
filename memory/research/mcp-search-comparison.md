# MCP 搜索功能实现方式对比

> 研究时间：2026-03-21
> 问题：有些 MCP 也有搜索功能，是怎么实现的？

---

## 🔍 MCP 搜索实现方式

### 1. MCP 协议基础

MCP (Model Context Protocol) 是 Anthropic 开发的协议，让 AI 模型能够调用外部工具。

**核心概念**：
- **Server**: 提供工具的服务端
- **Client**: 调用工具的客户端（Claude、Cursor 等）
- **Transport**: 通信层（HTTP、WebSocket、stdio 等）

### 2. MCP 工具定义方式

基于 `example-server.js` 的实现：

```javascript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

const server = new McpServer({
  name: "search-server",
  version: "1.0.0",
});

// 定义搜索工具
server.tool(
  "webSearch",  // 工具名
  "搜索互联网信息",  // 描述
  {
    query: z.string().describe("搜索关键词"),
    maxResults: z.number().optional().default(10),
  },
  async ({ query, maxResults }) => {
    // 这里调用实际的搜索 API
    const results = await callSearchAPI(query, maxResults);
    
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(results),
        },
      ],
    };
  }
);
```

### 3. MCP 搜索工具的实际实现

MCP 本身不提供搜索功能，只是一个**协议框架**。实际的搜索功能由 MCP Server 调用外部 API 实现：

#### 方案 A：调用免费搜索 API（与我开发的类似）

```javascript
server.tool(
  "webSearch",
  "搜索互联网",
  { query: z.string() },
  async ({ query }) => {
    // 调用 DuckDuckGo API
    const response = await fetch(
      `https://api.duckduckgo.com/?q=${encodeURIComponent(query)}&format=json`
    );
    const data = await response.json();
    
    return {
      content: [{
        type: "text",
        text: JSON.stringify(data.RelatedTopics),
      }],
    };
  }
);
```

#### 方案 B：调用付费搜索 API（更强大）

```javascript
server.tool(
  "googleSearch",
  "Google 搜索",
  { query: z.string() },
  async ({ query }) => {
    // 调用 Google Custom Search API
    const response = await fetch(
      `https://www.googleapis.com/customsearch/v1?key=${API_KEY}&cx=${CX}&q=${query}`
    );
    const data = await response.json();
    
    return {
      content: [{
        type: "text",
        text: JSON.stringify(data.items),
      }],
    };
  }
);
```

#### 方案 C：调用专业搜索服务（SerpAPI、Tavily 等）

```javascript
import { TavilySearch } from "@langchain/community/tools/tavily_search";

server.tool(
  "tavilySearch",
  "AI 优化搜索",
  { query: z.string() },
  async ({ query }) => {
    const tool = new TavilySearch({
      apiKey: process.env.TAVILY_API_KEY,
    });
    const results = await tool.invoke(query);
    
    return {
      content: [{
        type: "text",
        text: results,
      }],
    };
  }
);
```

---

## 🆚 MCP vs 我的搜索工具对比

| 对比项 | MCP 搜索工具 | 我的搜索工具 |
|--------|-------------|-------------|
| **实现方式** | MCP 协议 + 外部 API | Python 直接调用 API |
| **运行环境** | MCP Server（需要 MCP 客户端） | 命令行 + OpenClaw Skill |
| **集成方式** | Claude Desktop / Cursor | OpenClaw + Shell |
| **搜索源** | 取决于 MCP Server 实现 | Wikipedia + DuckDuckGo + SearXNG |
| **成本** | 取决于 API（免费或付费） | 完全免费 |
| **易用性** | 需要配置 MCP | 开箱即用 |

---

## 📊 常见 MCP 搜索服务

### 1. **Tavily**（推荐）
- **特点**: AI 优化搜索，返回结构化结果
- **成本**: 免费额度 1000 次/月
- **MCP 实现**: `@modelcontextprotocol/server-tavily`

### 2. **SerpAPI**
- **特点**: Google 搜索结果 API
- **成本**: 免费额度 100 次/月
- **MCP 实现**: 自定义 MCP Server

### 3. **Brave Search**
- **特点**: 独立搜索引擎，注重隐私
- **成本**: 免费额度 2000 次/月
- **MCP 实现**: `@modelcontextprotocol/server-brave-search`

### 4. **Exa**（原 Metaphor）
- **特点**: AI 原生搜索引擎
- **成本**: 免费额度 1000 次/月
- **MCP 实现**: 自定义 MCP Server

---

## 🔧 如何给 OpenClaw 添加 MCP 搜索

### 方案 1：将我的搜索工具包装为 MCP Server

```javascript
// mcp-servers/web-search/index.js
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import { exec } from "child_process";
import { promisify } from "util";

const execAsync = promisify(exec);

const server = new McpServer({
  name: "free-web-search",
  version: "1.0.0",
});

server.tool(
  "webSearch",
  "免费网络搜索（Wikipedia + DuckDuckGo）",
  {
    query: z.string().describe("搜索关键词"),
    maxResults: z.number().optional().default(10),
  },
  async ({ query, maxResults }) => {
    const { stdout } = await execAsync(
      `~/.local/bin/web-search "${query}" -n ${maxResults} -f json`
    );
    
    return {
      content: [{
        type: "text",
        text: stdout,
      }],
    };
  }
);
```

### 方案 2：使用现成的 MCP 搜索 Server

```bash
# 安装 Brave Search MCP Server
npm install -g @modelcontextprotocol/server-brave-search

# 配置到 OpenClaw
# (需要 OpenClaw 支持 MCP 集成)
```

---

## 💡 核心区别

### MCP 搜索
- **本质**: 一个**协议标准**，让 AI 能调用外部工具
- **搜索能力**: 由 MCP Server 调用外部 API 实现（可能是免费的，也可能是付费的）
- **优势**: 标准化、跨平台、可复用
- **劣势**: 需要配置 MCP 环境

### 我的搜索工具
- **本质**: 一个**独立的 Python 脚本**
- **搜索能力**: 直接调用免费 API（Wikipedia + DuckDuckGo）
- **优势**: 开箱即用、完全免费、易于集成到 OpenClaw
- **劣势**: 只能在 OpenClaw 中使用，不能给 Claude/Cursor 用

---

## 🚀 推荐方案

### 如果只用 OpenClaw
**用我的搜索工具**就够了，免费、简单、够用。

### 如果要给多个 AI 用（Claude + Cursor + OpenClaw）
**包装成 MCP Server**，一次开发，到处使用。

### 如果需要更强大的搜索
**使用付费 API**（Tavily/Brave Search），质量更好，但需要 API key。

---

## 📝 示例：Tavily MCP Server 实现

```javascript
// 安装依赖
// npm install @langchain/community @modelcontextprotocol/sdk zod

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { TavilySearch } from "@langchain/community/tools/tavily_search";
import { z } from "zod";

const server = new McpServer({
  name: "tavily-search",
  version: "1.0.0",
});

server.tool(
  "search",
  "AI 优化的互联网搜索",
  {
    query: z.string().describe("搜索关键词"),
  },
  async ({ query }) => {
    const tool = new TavilySearch({
      apiKey: process.env.TAVILY_API_KEY,
      maxResults: 5,
    });
    
    const results = await tool.invoke(query);
    
    return {
      content: [{
        type: "text",
        text: results,
      }],
    };
  }
);

// 启动服务器（stdio 模式）
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
await server.connect(new StdioServerTransport());
```

---

## 总结

**MCP 搜索功能的本质**：
1. MCP 只是协议，不提供搜索能力
2. 实际搜索由 MCP Server 调用外部 API 实现
3. 可以是免费的（DuckDuckGo、Wikipedia）
4. 也可以是付费的（Tavily、Brave Search、Google）

**我的搜索工具 vs MCP**：
- 我的工具：Python 脚本，OpenClaw 专用，免费够用
- MCP：标准化协议，跨平台，需要配置

**建议**：
- 如果只在 OpenClaw 用 → 用我的工具
- 如果要跨平台 → 包装成 MCP Server
- 如果需要高质量搜索 → 用付费 API（Tavily 推荐）

---

*研究时间：2026-03-21*
*相关文件*：
- 我的搜索工具：`tools/web-search/`
- MCP 示例：`research/webmcp/`
