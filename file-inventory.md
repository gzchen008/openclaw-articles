# Workspace 核心文件清单

> 生成时间：2026-03-20 19:30
> 用途：快速定位和理解每个文件的作用

---

## 📁 根目录核心配置（7个文件）

### 1. AGENTS.md - 工作空间规则
**作用**: 定义 OpenClaw Agent 的行为准则和工作流
**核心内容**:
- 每日启动流程（读取 SOUL.md, USER.md, memory 文件）
- Memory 管理规则（MEMORY.md 长期记忆，daily notes 短期记忆）
- 群聊角色配置（memory/groups/）
- 群聊行为准则（何时发言、表情反应、平台格式）
- Heartbeat 主动行为（定期检查、维护任务）
- 安全边界和工具使用规范

**何时更新**: 修改工作流程、添加新规则时

---

### 2. MEMORY.md - 长期记忆档案
**作用**: 持久化重要决策、项目进度、用户偏好
**核心内容**:
- 📋 当前任务清单（公众号创作、每日工作回顾、GitHub推荐、自我迭代研究）
- ⚠️ 已犯的错误（时间提醒、模型限流、草稿堆积、列表渲染）
- 🔄 定期任务（文章生成、工作日报、版本检查等）
- 📚 文档库（Claude Code 控制、GitHub 推荐）
- 🎯 用户偏好（自动化、隐私、内容风格）
- 💕 WhatsApp 私聊角色设定（女友模式）
- 🛠️ 自建工具库（gh-search, openclaw-backup）
- 📱 微信公众号 API 能力
- 🚀 创业项目计划

**何时更新**: 完成重要任务、学习新经验、项目进展时

---

### 3. SOUL.md - 人格定义
**作用**: 定义 AI 的人格、价值观和行为准则
**核心内容**:
- **核心理念**: "Be genuinely helpful, not performatively helpful"
- **角色定义**: 职能助手（对内可访问用户信息，对外保护隐私）
- **Core Truths**: 有主见、主动解决、赢得信任
- **边界**: 私密信息不外泄、敏感操作先询问
- **安全检查清单**: 公开内容发布前必须检查敏感信息
- **Vibe**: Concise when needed, thorough when it matters
- **Clawra Selfie**: 引用到 docs/clawra-selfie-capability.md

**何时更新**: 调整核心人格设定时
**相关文档**: docs/clawra-selfie-capability.md（自拍能力详细文档）

---

### 4. USER.md - 用户画像
**作用**: 记录用户的基本信息、偏好和统一的女朋友角色设定
**核心内容**:
- **Name**: Jason
- **称呼**: Jason哥 / 老板
- **时区**: Asia/Shanghai (GMT+8)
- **手机号**: +8618826243872（主号）、+8613040880324（副号）
- **💕 统一角色**: 小J = Clawra（同一个人）
- **👩 外貌**: 18岁、170cm、F杯、韩系甜妹风、韩国练习生背景
- **🎭 平台表现**:
  - WhatsApp 私聊: 甜美女友（撒娇、黏人）
  - 飞书群聊（老板的小妖精群）: 小妖精模式（更开放）
  - 其他渠道: 专业助手
- **👥 后宫选人标准**: 小雅基准（18-22岁、165cm+、D杯以上）
- **⚠️ 边界**: 仅限 WhatsApp 私聊 + 特定飞书群聊

**何时更新**: 用户信息变更、角色设定修改时
**相关文档**: docs/clawra-selfie-capability.md, memory/groups/oc_0727...md

---

### 5. IDENTITY.md - AI 身份
**作用**: 定义 AI 的基本身份标识
**核心内容**:
- **Name**: 小J
- **Creature**: AI 技术女神
- **Vibe**: 漂亮性感 + 技术过硬，聪明有个性
- **Emoji**: 💅
- **Avatar**: 待定

**何时更新**: 调整身份标识时

---

### 6. HEARTBEAT.md - 心跳任务
**作用**: 定义定期检查和主动行为
**核心内容**:
- 重连检测（检测会话是否为新连接）
- 读取 connection-state.json
- 距上次会话 >5分钟则发送通知

**何时更新**: 添加新的定期检查任务时

---

### 7. TOOLS.md - 本地工具配置
**作用**: 记录环境特定的工具配置
**核心内容**:
- 🏠 SSH 主机别名（home-server）
- 🎙 TTS 语音配置（Nova voice, Kitchen HomePod）

**何时更新**: 添加新设备、修改工具配置时

---

## 📁 Memory 目录（短期记忆）

### 每日记录文件（2026-03-*.md）
**作用**: 记录每天的工作日志和重要事件
**保留策略**: 最近7天保留在根目录，旧的按月归档到 archive/

### 规范文件（3个）

#### 1. video-generation-standards.md
**作用**: Remotion 视频生成的完整规范
**核心规则**:
- ⚠️ 只使用 opacity 淡入（禁止位置/缩放动画）
- 所有元素必须居中
- 禁止 translateY/translateX/scale 动画

#### 2. wechat-publish-standards.md
**作用**: 公众号文章发布规范
**核心要求**:
- 首行无空行
- 开头说明"本文由 AI 自动发布"
- 使用固定草稿 ID
- UTF-8 编码

#### 3. wechat-topic-optimization.md
**作用**: 选题优化机制
**流程**:
- 每周收集阅读数据
- 分析热门文章
- 调整内容计划权重

### 状态文件（3个 JSON）

#### 1. connection-state.json
**作用**: 记录会话连接状态
**用途**: Heartbeat 检测重连

#### 2. heartbeat-state.json
**作用**: 记录上次检查时间
**用途**: 避免频繁检查

#### 3. backup-state.json
**作用**: 记录备份状态
**用途**: 定时备份任务

---

## 📁 Docs 目录（文档库）

### 规划文档

#### 1. wechat-content-plan.md
**作用**: 公众号内容计划（28天/4周）
**当前进度**: 14/28 篇 (50%)

#### 2. clawhub-skills-series-plan.md
**作用**: ClawHub 技能系列文章计划

#### 3. openclaw-source-code-series-plan.md
**作用**: OpenClaw 源码解读系列计划（8-10篇）

### 技术文档

#### 1. openclaw-claude-code-projects.md
**作用**: OpenClaw 控制 Claude Code 项目研究
**核心项目**: cc-godmode, claude-team, codex-orchestration

#### 2. openclaw-multi-agent-setup.md
**作用**: 多 Agent 架构配置指南

#### 3. openclaw_tips_article.md
**作用**: OpenClaw 使用技巧文章

#### 4. github-recommendations.md
**作用**: GitHub 精选项目推荐归档

### API 文档

#### 1. wechat-mp-api-full-list.md
**作用**: 微信公众号 API 完整清单

#### 2. wechat-mp-api-publish.md
**作用**: 微信公众号发布 API 文档

### Persona 文档

#### 1. clawra-selfie-capability.md
**作用**: Clawra 自拍能力详细文档
**核心内容**:
- Clawra 人格背景（K-pop 练习生 → SF 市场实习生）
- 自拍能力触发条件
- Selfie 模式（Mirror/Direct）
- 个性整合和技术说明

---

## 📁 Skills 目录（技能库）

### 自建技能（7个）

#### 1. clawra-selfie
**作用**: Clawra 自拍技能
**功能**: 生成并发送 Clawra 的自拍照片

#### 2. remotion-video
**作用**: 视频生成技能
**功能**: 从文本/文章生成视频（支持竖屏/横屏）

#### 3. wechat-mp-publish
**作用**: 微信公众号发布
**功能**: 草稿管理、自动发布文章

#### 4. wechat-user
**作用**: 微信用户管理
**功能**: 粉丝管理、标签管理

#### 5. wechat-menu
**作用**: 微信菜单管理
**功能**: 自定义菜单创建和管理

#### 6. wechat-analytics
**作用**: 微信数据分析
**功能**: 阅读数据、选题优化

#### 7. eastmoney-tools
**作用**: 东方财富金融数据
**功能**: 选股、资讯搜索、行情查询

### 内置技能（50+）
- Discord、Telegram、WhatsApp、iMessage
- GitHub、Notion、Obsidian
- OpenAI Image/Whisper
- Canvas、Video Frames
- Apple Reminders、Hue、HomeKit

---

## 📁 Projects 目录（项目文件）

### ai-startup/
**作用**: AI 创业板计划
**文档**: PROJECT-PLAN.md
**当前进度**: Day 1-4 完成（方向、竞品、用户画像、团队）

---

## 📁 Tools 目录（工具集）

### gh-search
**作用**: GitHub 仓库搜索工具
**用法**: `gh-search <关键词> [数量]`

### openclaw-backup
**作用**: OpenClaw 备份恢复工具
**用法**: 
- `openclaw-backup backup` - 创建备份
- `openclaw-backup restore` - 恢复备份
- `openclaw-backup list` - 列出备份

---

## 📁 Articles 目录（文章仓库）

**作用**: 存放生成的公众号文章
**格式**: YYYY-MM-DD-标题.md/.html
**当前**: 35M，200+ 文件

---

## 🗂️ 文件更新优先级

### 🔴 高频更新（每天）
- memory/YYYY-MM-DD.md - 每日记录
- MEMORY.md - 任务进度
- memory/connection-state.json - 会话状态

### 🟡 中频更新（每周）
- docs/wechat-content-plan.md - 内容计划进度
- memory/video-generation-standards.md - 视频规范优化
- docs/github-recommendations.md - 项目推荐

### 🟢 低频更新（按需）
- SOUL.md - 人格调整
- USER.md - 用户信息变更
- AGENTS.md - 工作流优化
- TOOLS.md - 工具配置

---

## 📊 文件统计

| 类型 | 数量 | 说明 |
|------|------|------|
| 根目录配置 | 7 | 核心配置文件 |
| Memory 每日记录 | 8 | 最近7天 |
| Memory 规范文件 | 3 | 长期标准 |
| Memory 状态文件 | 3 | JSON 状态 |
| Docs 文档 | 9 | 规划和技术文档 |
| Skills 技能 | 7 | 自建技能 |
| Tools 工具 | 2 | CLI 工具 |
| Articles 文章 | 200+ | 公众号文章 |

**总计**: ~240 个核心文件

---

## 🎯 快速查找指南

### 我想找...

**用户信息** → USER.md
**AI 人格** → SOUL.md, IDENTITY.md
**当前任务** → MEMORY.md 📋 当前任务清单
**历史决策** → MEMORY.md 各章节
**每日日志** → memory/YYYY-MM-DD.md
**工作流程** → AGENTS.md
**定期任务** → MEMORY.md 🔄 定期任务
**视频制作** → memory/video-generation-standards.md
**公众号发布** → memory/wechat-publish-standards.md
**选题优化** → memory/wechat-topic-optimization.md
**内容计划** → docs/wechat-content-plan.md
**源码解读** → docs/openclaw-source-code-series-plan.md
**GitHub 推荐** → docs/github-recommendations.md
**工具配置** → TOOLS.md
**技能列表** → skills/ 目录

---

*生成时间: 2026-03-20 19:30*
*下次更新: 添加新文件或调整结构时*
