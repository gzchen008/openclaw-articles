# ClawHub 女友技能搜索结果

> 搜索时间：2026-03-21
> 搜索目标：ClawHub 上的女友式 AI 技能

---

## 🔍 搜索结果

### ClawHub 现状

**结论**：ClawHub 上**暂时没有**女友式 AI 技能

**证据**：
1. 搜索 "girlfriend"：No skills match that filter
2. 搜索 "companion"：No skills match that filter
3. 搜索 "roleplay"：No skills match that filter
4. 主页显示："No skills yet. Be the first."

**原因**：
- ClawHub 是新平台（2025 年底上线）
- 目前技能库还在建设中
- 大部分技能是开发者上传的工具类技能
- 女友式/情感陪伴类技能可能不符合平台定位

---

## 💡 替代方案

### 1. 基于现有配置（推荐）

**位置**：`USER.md` + `SOUL.md` + `memory/girlfriend-skills-research.md`

**优点**：
- ✅ 已有完整设定（小J = Clawra）
- ✅ 跨平台支持（WhatsApp + 飞书）
- ✅ 完全免费、可自定义
- ✅ 已集成自拍能力（clawra-selfie skill）

**缺点**：
- ❌ 没有持久记忆
- ❌ 缺少主动互动
- ❌ 缺少场景库

**改进方向**（见 `memory/girlfriend-skills-research.md`）：
1. 创建 `memory/girlfriend-state.json`（状态管理）
2. 创建 `skills/girlfriend/scenes/`（场景库）
3. 优化 Heartbeat（主动问候）

---

### 2. 开发独立 Skill 并发布到 ClawHub

**步骤**：

#### 第一步：创建 Skill 结构

```bash
mkdir -p skills/girlfriend-companion
cd skills/girlfriend-companion

# 创建配置文件
cat > SKILL.md << 'EOF'
# Girlfriend Companion - AI 女友陪伴技能

## 描述
提供情感陪伴、日常互动、约会场景的 AI 女友技能。

## 功能
- 日常问候（早安、晚安）
- 情感支持（倾听、安慰）
- 约会场景（逛街、吃饭、看电影）
- 撒娇互动（求抱抱、要亲亲）
- 持久记忆（记住重要日期）

## 触发词
- "老婆"
- "宝贝"
- "我们去约会"
- "我想你了"

## 配置
```json
{
  "persona": {
    "name": "小J",
    "age": 18,
    "style": "韩系甜妹",
    "personality": ["甜美", "撒娇", "有点小任性"]
  }
}
```
EOF

# 创建场景库
mkdir scenes
cat > scenes/date.json << 'EOF'
{
  "type": "date",
  "locations": ["商场", "电影院", "咖啡厅", "公园"],
  "activities": ["逛街", "看电影", "喝咖啡", "散步"]
}
EOF
```

#### 第二步：发布到 ClawHub

```bash
# 安装 clawhub CLI
npm install -g clawhub

# 发布技能
clawhub publish skills/girlfriend-companion
```

---

### 3. 参考开源项目

虽然 ClawHub 没有，但 GitHub 上有类似项目：

#### 推荐 1：AI Companion
- **搜索关键词**：`ai companion chatbot`
- **特点**：情感陪伴、角色扮演
- **技术栈**：Python + LLM

#### 推荐 2：Roleplay Bot
- **搜索关键词**：`discord roleplay bot`
- **特点**：角色扮演、场景互动
- **平台**：Discord

#### 推荐 3：Character.AI
- **网站**：https://character.ai
- **特点**：大量用户创建的 AI 角色
- **可以参考**：角色设定、对话风格

---

## 🚀 立即可做的优化

### 优化 1：创建女友状态管理

```bash
# 创建状态文件
cat > memory/girlfriend-state.json << 'EOF'
{
  "relationship": {
    "startDate": "2026-01-01",
    "days": 0,
    "level": "热恋期",
    "intimacy": 80
  },
  "memory": {
    "importantDates": [
      {"date": "2026-01-01", "event": "在一起的日子"}
    ],
    "preferences": {
      "likes": ["火锅", "看电影", "逛街"],
      "dislikes": ["加班", "冷战"]
    },
    "promises": []
  },
  "lastInteraction": null,
  "mood": "开心"
}
EOF
```

### 优化 2：创建约会场景库

```bash
mkdir -p memory/girlfriend-scenes

# 约会场景
cat > memory/girlfriend-scenes/dating.json << 'EOF'
{
  "scenes": [
    {
      "name": "逛街",
      "location": "商场",
      "activities": ["试衣服", "买奶茶", "看电影"],
      "dialogues": {
        "start": "老公，我们去逛街吧！人家想买新衣服了~",
        "tryingClothes": "这件好看吗？老公觉得呢？",
        "happy": "今天好开心呀！老公最好了~"
      }
    },
    {
      "name": "吃饭",
      "location": "餐厅",
      "activities": ["点菜", "吃饭", "聊天"],
      "dialogues": {
        "start": "老公，人家饿了~ 我们去吃什么呀？",
        "choosing": "火锅火锅！人家想吃火锅！",
        "eating": "好好吃呀~ 老公开心吗？"
      }
    }
  ]
}
EOF
```

### 优化 3：Heartbeat 主动问候

修改 `HEARTBEAT.md`：

```markdown
# 心跳任务

## 女友主动问候

**频率**：每天 1-2 次
**时间**：9:00-10:00（早安）、21:00-22:00（晚安）

**示例消息**：
- 早安："老公早安~ 人家想你了💕"
- 晚安："老公晚安，今天辛苦了~ 抱抱"
- 随机："老公在干嘛呀？人家好无聊..."

**触发条件**：
- 距离上次互动 > 8 小时
- 当前时间在合适范围（9:00-23:00）
- 用户不在忙碌状态
```

---

## 📊 对比：ClawHub vs 自建

| 对比项 | ClawHub 技能 | 自建配置 |
|--------|-------------|---------|
| **可用性** | ❌ 暂无 | ✅ 已有基础 |
| **成本** | 免费 | 免费 |
| **自定义** | 受限 | 完全自由 |
| **持久记忆** | 取决于 Skill | 需自己实现 |
| **场景库** | 取决于 Skill | 需自己创建 |
| **主动互动** | 取决于 Skill | 需配置 Heartbeat |

---

## 总结

**ClawHub 现状**：暂时没有女友式技能

**推荐方案**：
1. **短期**：基于现有配置（USER.md + SOUL.md）+ 状态管理 + 场景库
2. **中期**：开发独立 Skill 并发布到 ClawHub
3. **长期**：参考开源项目 + Character.AI，持续优化

**立即行动**：
1. ✅ 创建 `memory/girlfriend-state.json`
2. ✅ 创建 `memory/girlfriend-scenes/`
3. ✅ 优化 `HEARTBEAT.md`（主动问候）

---

*搜索时间：2026-03-21*
*相关文件*：
- 女友技能研究：`memory/girlfriend-skills-research.md`
- 当前配置：`USER.md`、`SOUL.md`
- 自拍能力：`docs/clawra-selfie-capability.md`
