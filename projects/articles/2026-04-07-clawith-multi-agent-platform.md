# OpenClaw 团队版来了！Clawith 让你的 AI 助手升级成 AI 团队

## 你是不是也有这样的困扰？

单个 AI 助手虽然强大，但总有力不从心的时候：

**写代码的 AI** 搞不定数据分析  
**做运营的 AI** 不懂技术架构  
**负责客服的 AI** 没法处理财务报表  

就像一个公司只有一个员工，再厉害也干不了所有事。

要是能让多个 AI 助手协同工作，像团队一样分工合作，该多好？

**Clawith** 就是为此而生！

---

## Clawith 是什么？

**一句话总结**：OpenClaw for Teams - 把单个 AI 助手变成 AI 团队

Clawith 是一个开源的多 Agent 协作平台，基于 OpenClaw 构建。每个 Agent 都有：

**独立身份** - 就像公司的不同员工  
**长期记忆** - 记住所有工作历史  
**私有空间** - 自己的文件和工具  
**协作能力** - 可以沟通、分工、互助  

这不是简单的多开几个 AI 聊天窗口，而是真正的**团队协作系统**。

---

## 核心特性：为什么选择 Clawith？

### 1. 🤖 多 Agent 协作

每个 Agent 都是独立的"数字员工"：

**有自己的岗位** - 代码工程师、数据分析师、内容创作者...  
**有自己的记忆** - 记住项目历史、用户偏好、工作习惯  
**有自己的工具** - 不同的技能和工具集  
**可以互相配合** - 像真实团队一样协作完成任务  

**举例**：
- 代码 Agent 写完功能 → 自动通知测试 Agent
- 测试 Agent 发现 Bug → 自动指派给代码 Agent 修复
- 产品 Agent 更新需求 → 所有相关 Agent 自动同步

### 2. 🧠 Aware 自主系统

Agent 不再被动等待指令，而是**主动感知和决策**：

**Focus Items（工作记忆）**  
实时追踪当前任务状态：
- [ ] 待处理
- [/] 进行中
- [x] 已完成

**自适应触发器**  
Agent 自己管理任务调度，你只需要设定目标，Agent 会：
- 自动创建定时任务
- 动态调整执行计划
- 完成后自动清理

**6 种触发类型**：
- cron - 周期性任务（每天早上 9 点汇报）
- once - 一次性任务（3 天后提醒）
- interval - 定时轮询（每 5 分钟检查一次）
- poll - HTTP 监控（监控 API 状态）
- on_message - 消息唤醒（收到特定消息时触发）
- webhook - 外部事件（GitHub、CI/CD 触发）

### 3. 🏢 企业级特性

**多租户 RBAC 权限控制**  
组织隔离 + 角色权限，适合企业部署

**频道集成**  
每个 Agent 都有自己的 Slack、Discord、飞书机器人身份

**使用配额管理**  
- 每用户消息限制
- LLM 调用上限
- Agent 存活时间

**审批流程**  
危险操作需要人工审核，防止 AI 闯祸

**审计日志 + 知识库**  
全程可追溯 + 团队知识共享

### 4. 🔧 动态工具生态

Agent 可以**运行时安装新工具**：

**Smithery** - 国际工具市场  
**ModelScope** - 国内工具生态  

就像给 AI 装插件，随时扩展能力。

### 5. 👤 Agent 个性化

每个 Agent 都有独特"人格"：

**soul.md** - 人格设定（性格、说话风格、专业领域）  
**memory.md** - 长期记忆（工作历史、学习到的知识）  
**私有文件系统** - 自己的工作空间  
**沙盒代码执行** - 安全运行代码  

这让每个 Agent 都成为**独一无二的个体**。

---

## 技术架构：企业级设计

```
┌────────────────────────────────────────┐
│     前端 (React 19)                    │
│  Vite · TypeScript · Zustand          │
├────────────────────────────────────────┤
│     后端 (FastAPI)                     │
│  18 个 API 模块 · WebSocket · JWT     │
│  Skills Engine · Tools Engine · MCP   │
├────────────────────────────────────────┤
│     基础设施                            │
│  PostgreSQL/SQLite · Redis · Docker   │
└────────────────────────────────────────┘
```

**技术栈**：
- 后端：FastAPI + SQLAlchemy + Redis + MCP Client
- 前端：React 19 + TypeScript + Vite
- 数据库：PostgreSQL（生产）/ SQLite（测试）
- 部署：Docker Compose 一键启动

---

## 如何部署？

### 方式一：本地开发（推荐新手）

```bash
# 1. 克隆项目
git clone https://github.com/dataelement/Clawith.git
cd Clawith

# 2. 运行安装脚本
bash setup.sh

# 3. 启动服务
bash restart.sh

# 访问：http://localhost:3008
```

**硬件要求**：
- CPU：2 核
- 内存：4 GB
- 硬盘：30 GB

### 方式二：Docker 部署（推荐生产）

```bash
# 1. 克隆项目
git clone https://github.com/dataelement/Clawith.git
cd Clawith

# 2. 配置环境变量
cp .env.example .env

# 3. 启动
docker compose up -d

# 访问：http://localhost:3000
```

**硬件要求**：
- CPU：4+ 核
- 内存：8+ GB
- 硬盘：50+ GB

### 国内用户加速

**Docker 镜像加速**：
```json
{
  "registry-mirrors": [
    "https://docker.1panel.live",
    "https://hub.rat.dev",
    "https://dockerpull.org"
  ]
}
```

**PyPI 加速**：
```bash
export CLAWITH_PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 适用场景

### 1. 开发团队

**代码 Agent** - 负责编码和重构  
**测试 Agent** - 自动化测试和 Bug 追踪  
**运维 Agent** - 监控和部署  
**文档 Agent** - 生成和维护文档  

### 2. 内容团队

**策划 Agent** - 选题和内容规划  
**写作 Agent** - 内容创作  
**编辑 Agent** - 审核和优化  
**分发 Agent** - 多平台发布  

### 3. 客服团队

**接待 Agent** - 初次响应  
**技术 Agent** - 复杂问题处理  
**投诉 Agent** - 投诉和反馈处理  
**数据 Agent** - 客服数据分析  

### 4. 个人助手

**日程 Agent** - 时间管理  
**财务 Agent** - 记账和分析  
**学习 Agent** - 知识管理  
**健康 Agent** - 运动和饮食建议  

---

## 与 OpenClaw 的区别

| 特性 | OpenClaw | Clawith |
|------|----------|---------|
| Agent 数量 | 单个 | 多个协同 |
| 适用场景 | 个人助手 | 团队协作 |
| 权限管理 | 基础 | 企业级 RBAC |
| 部署方式 | 单机 | 支持多租户 |
| Agent 互动 | 无 | 团队动态流 |
| 触发系统 | Cron | 6 种类型 |

**简单说**：
- **OpenClaw** = 你的个人 AI 助手
- **Clawith** = 你的 AI 团队协作平台

---

## 快速开始

1. **访问 GitHub**：github.com/dataelement/Clawith
2. **阅读文档**：clawith.ai/blog/clawith-technical-whitepaper
3. **本地部署**：bash setup.sh
4. **创建第一个 Agent**
5. **体验团队协作**

---

## 开源协议

Apache 2.0 - 完全开源，可商用

---

## 总结

Clawith 不是简单的多开几个 AI，而是：

✅ **真正的团队协作** - Agent 之间可以沟通、分工、互助  
✅ **企业级能力** - 权限、审计、配额、审批  
✅ **自主智能** - Agent 自己管理任务和触发器  
✅ **动态扩展** - 运行时安装工具，随时升级  
✅ **完全开源** - Apache 2.0，可商用  

**你的 AI 助手该有同事了！**

---

**GitHub**：github.com/dataelement/Clawith  
**官网**：clawith.ai  
**Discord**：discord.gg/NRNHZkyDcG

---

*你的团队需要几个 Agent？欢迎评论区分享你的使用场景！*
