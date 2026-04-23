# OpenClaw 多Agent多Workspace实战：让AI团队协同工作

一个 AI 助手不够用？那就来一支 AI 团队！

今天教你用 OpenClaw 搭建**多 Agent 多 Workspace** 架构，让你的 AI 助手变成 AI 团队！

---

## 一、什么是多 Agent 多 Workspace？

### 单 Agent 的痛点

你是不是遇到过这些问题：

❌ **权限混乱**：AI 既能读写文件，又能执行命令，还能发消息，太危险了
❌ **任务冲突**：写代码的 AI 和发通知的 AI 争抢资源
❌ **数据隔离**：个人助理和工作助理混在一起，隐私堪忧
❌ **性能瓶颈**：一个 AI 处理所有任务，响应慢

### 多 Agent 多 Workspace 的解决方案

**多 Agent**：
- 每个 Agent 有独立身份和权限
- 不同 Agent 负责不同任务
- Agent 之间可以协作

**多 Workspace**：
- 每个 Agent 有独立工作空间
- 数据和配置完全隔离
- 互不干扰，安全可控

---

## 二、OpenClaw 的多 Agent 架构

### 核心概念

OpenClaw 支持 **3 种 Agent 类型**：

#### 1️⃣ Main Agent（主智能体）

**角色**：你的私人助理
**特点**：
- 完全权限（读写、执行、网络）
- 访问你的所有数据
- 响应你的所有消息

**配置示例**：
```json
{
  "id": "main",
  "default": true,
  "workspace": "~/.openclaw/workspace",
  "sandbox": { "mode": "off" }
}
```

#### 2️⃣ Specialized Agent（专用智能体）

**角色**：专项任务专家
**特点**：
- 受限权限（只读、仅消息等）
- 独立工作空间
- 绑定特定渠道（群聊、频道）

**配置示例**：
```json
{
  "id": "family",
  "name": "Family Bot",
  "workspace": "~/.openclaw/workspace-family",
  "sandbox": { "mode": "all", "scope": "agent" },
  "tools": {
    "allow": ["read"],
    "deny": ["exec", "write", "edit"]
  }
}
```

#### 3️⃣ Subagent（子智能体）

**角色**：临时任务执行者
**特点**：
- 从主 Agent 派生
- 执行完成后自动报告结果
- 后台运行，不阻塞主流程

**使用场景**：
- 长时间任务（代码审查、数据分析）
- 并行任务（同时搜索多个来源）
- 隔离任务（测试危险命令）

---

## 三、实战案例：打造你的 AI 团队

### 案例1：个人 + 工作双助理

**需求**：
- 个人助理：处理私事，完全权限
- 工作助理：处理工作，受限权限

**配置**：
```json
{
  "agents": {
    "list": [
      {
        "id": "personal",
        "default": true,
        "workspace": "~/.openclaw/workspace-personal",
        "sandbox": { "mode": "off" },
        "tools": { "profile": "default" }
      },
      {
        "id": "work",
        "workspace": "~/.openclaw/workspace-work",
        "sandbox": {
          "mode": "all",
          "scope": "shared",
          "workspaceRoot": "/tmp/work-sandboxes"
        },
        "tools": {
          "allow": ["read", "write", "exec"],
          "deny": ["browser", "gateway"]
        }
      }
    ]
  },
  "bindings": [
    {
      "agentId": "work",
      "match": {
        "provider": "feishu",
        "accountId": "*",
        "peer": { "kind": "group", "id": "oc_work_group" }
      }
    }
  ]
}
```

**效果**：
- 飞书群聊 → 工作助理（沙箱隔离）
- 私聊 → 个人助理（完全权限）

---

### 案例2：客服 + 销售双机器人

**需求**：
- 客服机器人：回答常见问题，只读权限
- 销售机器人：跟进客户，可以发消息

**配置**：
```json
{
  "agents": {
    "list": [
      {
        "id": "support",
        "workspace": "~/.openclaw/workspace-support",
        "sandbox": { "mode": "all" },
        "tools": {
          "profile": "messaging",
          "allow": ["slack"]
        }
      },
      {
        "id": "sales",
        "workspace": "~/.openclaw/workspace-sales",
        "sandbox": { "mode": "off" },
        "tools": {
          "allow": ["read", "sessions_send", "message"],
          "deny": ["exec", "write"]
        }
      }
    ]
  }
}
```

---

### 案例3：使用子智能体并行处理

**场景**：同时搜索多个技术文档

**命令**：
```bash
/subagents spawn main "搜索 React 18 新特性" --model glm-5
/subagents spawn main "搜索 Vue 3.4 更新" --model glm-5
/subagents spawn main "搜索 Next.js 14 功能" --model glm-5
```

**效果**：
- 3 个子智能体并行搜索
- 主智能体继续响应用户
- 搜索完成后自动汇总结果

---

## 四、多 Agent 协作模式

### 模式1：路由分发

**场景**：根据消息来源路由到不同 Agent

**配置**：
```json
{
  "bindings": [
    {
      "agentId": "personal",
      "match": { "provider": "whatsapp", "accountId": "*" }
    },
    {
      "agentId": "work",
      "match": { "provider": "feishu", "accountId": "*" }
    },
    {
      "agentId": "support",
      "match": { "provider": "discord", "accountId": "*" }
    }
  ]
}
```

**流程**：
1. WhatsApp 消息 → personal Agent
2. 飞书消息 → work Agent
3. Discord 消息 → support Agent

---

### 模式2：层级协作

**场景**：主 Agent 调度子 Agent

**流程**：
```
用户请求
   ↓
Main Agent（决策）
   ↓
   ├→ Subagent A（执行任务1）
   ├→ Subagent B（执行任务2）
   └→ Subagent C（执行任务3）
   ↓
汇总结果返回用户
```

**优势**：
- 主 Agent 专注决策
- 子 Agent 并行执行
- 结果自动汇总

---

### 模式3：技能分工

**场景**：不同 Agent 负责不同技能

**配置**：
```json
{
  "agents": {
    "list": [
      {
        "id": "coder",
        "tools": { "profile": "coding" }
      },
      {
        "id": "writer",
        "tools": { "profile": "content" }
      },
      {
        "id": "analyst",
        "tools": { "profile": "analytics" }
      }
    ]
  }
}
```

**效果**：
- coder Agent：代码生成、调试
- writer Agent：内容创作、翻译
- analyst Agent：数据分析、报表

---

## 五、安全最佳实践

### 1️⃣ 沙箱隔离

**原则**：不受信任的 Agent 必须沙箱隔离

**配置**：
```json
{
  "sandbox": {
    "mode": "all",        // 所有操作都在沙箱
    "scope": "agent",     // 每个 Agent 独立容器
    "docker": {
      "image": "openclaw/sandbox:latest"
    }
  }
}
```

---

### 2️⃣ 工具限制

**原则**：最小权限原则

**只读 Agent**：
```json
{
  "tools": {
    "allow": ["read"],
    "deny": ["exec", "write", "edit", "process"]
  }
}
```

**仅消息 Agent**：
```json
{
  "tools": {
    "allow": ["sessions_send", "message"],
    "deny": ["exec", "write", "read"]
  }
}
```

---

### 3️⃣ 认证隔离

**原则**：每个 Agent 独立认证

**路径**：
```
~/.openclaw/agents/<agentId>/agent/auth-profiles.json
```

**注意**：
- 凭证不共享
- 敏感数据隔离
- 定期轮换密钥

---

## 六、常见问题

### Q1：Agent 之间如何通信？

**A**：使用 `sessions_send` 工具：
```bash
sessions_send --session-key "agent:work:main" --message "任务完成"
```

### Q2：如何查看子智能体状态？

**A**：使用 `/subagents` 命令：
```bash
/subagents list      # 列出所有子智能体
/subagents log #1    # 查看日志
/subagents kill #1   # 终止运行
```

### Q3：如何监控多 Agent 系统？

**A**：使用 `openclaw agents` 命令：
```bash
openclaw agents list --bindings    # 查看 Agent 绑定
openclaw status                     # 查看运行状态
```

---

## 七、总结：多 Agent 多 Workspace 的价值

### ✅ 安全性

- 权限隔离
- 沙箱保护
- 认证分离

### ✅ 效率

- 并行处理
- 专项专精
- 资源优化

### ✅ 灵活性

- 动态扩容
- 按需配置
- 场景定制

### ✅ 可维护性

- 职责清晰
- 易于调试
- 独立升级

---

## 写在最后

OpenClaw 的多 Agent 多 Workspace 架构，让你的 AI 助手从"一个人"变成"一支团队"。

**核心思想**：
- 专人专岗：每个 Agent 专注自己的任务
- 权限最小化：只给必要的权限
- 隔离运行：沙箱保护，互不干扰

**下一步**：
1. 规划你的 Agent 团队（需要几个 Agent？每个负责什么？）
2. 配置 Workspace 隔离
3. 设置工具权限
4. 测试协作流程

记住：好的架构不是一次设计完成，而是在实践中不断优化！

---

*你的 AI 团队正在等你召唤。开始构建你的多 Agent 王国吧！* 🏰
