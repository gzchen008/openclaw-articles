/**
 * WebMCP 示例服务器
 * 
 * 这个示例展示了如何在网页中创建 MCP 工具
 * 需要配合 MCP-B Chrome 扩展使用
 */

import { TabServerTransport } from "@mcp-b/transports";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";

// 创建 MCP 服务器
const server = new McpServer({
  name: "openclaw-webmcp",
  version: "1.0.0",
});

// 工具 1: 获取当前页面信息
server.tool("getPageInfo", "获取当前页面的标题和 URL", {}, async () => {
  return {
    content: [
      {
        type: "text",
        text: JSON.stringify({
          title: document.title,
          url: window.location.href,
        }),
      },
    ],
  };
});

// 工具 2: 显示通知
server.tool(
  "showNotification",
  "在页面上显示一条通知消息",
  {
    message: z.string().describe("要显示的通知内容"),
  },
  async ({ message }) => {
    // 在实际网页中，这里可以调用你的 UI 通知组件
    console.log("📢 通知:", message);
    return {
      content: [
        {
          type: "text",
          text: `已显示通知: ${message}`,
        },
      ],
    };
  }
);

// 工具 3: 添加待办事项（示例）
server.tool(
  "addTodo",
  "添加一个待办事项",
  {
    title: z.string().describe("待办事项标题"),
    priority: z.enum(["low", "medium", "high"]).optional().describe("优先级"),
  },
  async ({ title, priority = "medium" }) => {
    const todo = {
      id: Date.now(),
      title,
      priority,
      completed: false,
      createdAt: new Date().toISOString(),
    };
    console.log("✅ 新待办:", todo);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(todo),
        },
      ],
    };
  }
);

// 连接传输层
async function start() {
  try {
    await server.connect(
      new TabServerTransport({
        allowedOrigins: ["*"], // 生产环境应限制为特定域名
      })
    );
    console.log("✅ WebMCP 服务器已启动");
  } catch (error) {
    console.error("❌ 启动失败:", error);
  }
}

start();
