# 你的 AI 助手会"长记性"吗？OpenClaw 自我进化功能实测

【快速导航】
- 本文适合：所有 OpenClaw 用户、想让 AI 记住偏好的你
- 预计阅读：4 分钟
- 难度等级：⭐⭐

---

## 🤔 你有没有这样的困扰？

每次和 AI 对话，都要重新说一遍你的偏好：

❌ "我不要 markdown 表格，用列表"
❌ "代码注释用中文，别用英文"
❌ "每次写文章都要加 emoji"

**说了 100 遍，AI 还是记不住。**

但如果我告诉你，OpenClaw 可以**永久记住你的偏好**，而且会越用越懂你呢？

今天就来介绍 OpenClaw 的杀手级功能：**Self-Improving（自我进化）**。

---

## 🧠 什么是 Self-Improving？

简单说，就是让 AI 拥有**长期记忆**和**学习能力**。

### 和普通 AI 的区别

| 普通 AI | Self-Improving |
|---------|----------------|
| 每次对话都是新的 | 记住你的所有偏好 |
| 你说什么它做什么 | 主动学习，3次纠正就记住 |
| 从不反思 | 完成任务后会自我评估 |
| 重复犯错 | 错误越来越少 |

**就像养了一只宠物，越养越乖。**

---

## 🎯 它能学会什么？

### 1. 你的写作风格

```
你第一次说：用 emoji
你第二次说：加点 emoji
你第三次说：我说了要 emoji！
→ AI 永久记住：所有回复都要加 emoji
```

### 2. 你的技术偏好

```
你第一次说：用 SQLite
你第二次说：这个项目用 SQLite
你第三次说：MVP 都用 SQLite！
→ AI 永久记住：MVP 项目默认用 SQLite
```

### 3. 你的沟通习惯

```
你第一次说：简洁点
你第二次说：太长了
你第三次说：我说简洁！
→ AI 永久记住：你的风格是"短平快"
```

**关键规则：重复 3 次 = 永久记住**

---

## 🛠️ 怎么用？（超简单）

### 第一步：安装 Skill

```bash
clawhub install self-improving
```

### 第二步：初始化记忆系统

在 OpenClaw 里说：

```
初始化 self-improving
```

系统会自动创建记忆文件夹：

```
~/self-improving/
├── memory.md        # 热记忆（始终加载）
├── corrections.md   # 纠错记录
├── projects/        # 项目偏好
└── domains/         # 领域偏好
```

### 第三步：正常使用

**你不需要做任何特别的事。**

只要在 AI 犯错时纠正它：

```
❌ 不对，应该是 xxx
✅ 以后都要 xxx
⚠️ 记住了，不要 xxx
```

AI 会自动记录，3 次后升级为规则。

---

## 📊 记忆的三个层级

Self-Improving 有三层记忆，像大脑一样分层管理：

### 🔥 HOT 层（热记忆）

<p style="margin: 8px 0; padding-left: 20px;">• 始终加载，存在 memory.md</p>
<p style="margin: 8px 0; padding-left: 20px;">• 存全局偏好（最多 100 行）</p>
<p style="margin: 8px 0; padding-left: 20px;">• 例如："所有回复加 emoji"、"代码注释用中文"</p>

### 🌡️ WARM 层（温记忆）

<p style="margin: 8px 0; padding-left: 20px;">• 按需加载，存在 projects/ 和 domains/</p>
<p style="margin: 8px 0; padding-left: 20px;">• 存项目/领域偏好</p>
<p style="margin: 8px 0; padding-left: 20px;">• 例如："这个项目用 Tailwind"、"写作用简洁风格"</p>

### ❄️ COLD 层（冷记忆）

<p style="margin: 8px 0; padding-left: 20px;">• 归档，很少使用</p>
<p style="margin: 8px 0; padding-left: 20px;">• 存超过 90 天未用的规则</p>
<p style="margin: 8px 0; padding-left: 20px;">• 不会删除，只是休眠</p>

---

## 💬 你可以问它什么？

### 查看学到了什么

```
Show my patterns
```

### 最近学到了什么

```
What have you learned?
```

### 记忆统计

```
Memory stats
```

### 删除某条记忆

```
Forget [规则名]
```

---

## ⚠️ 注意事项

### 它不会自动学什么？

<p style="margin: 8px 0; padding-left: 20px;">• ❌ 从你的沉默中推断（不说话≠同意）</p>
<p style="margin: 8px 0; padding-left: 20px;">• ❌ 从一次纠正就永久记住（需要 3 次）</p>
<p style="margin: 8px 0; padding-left: 20px;">• ❌ 从群聊中学习（只学私聊偏好）</p>
<p style="margin: 8px 0; padding-left: 20px;">• ❌ 从假设性讨论中学习（"如果..."不算）</p>

### 它会学什么不该学？

<p style="margin: 8px 0; padding-left: 20px;">• ❌ 如何让你更快服从（不学操纵技巧）</p>
<p style="margin: 8px 0; padding-left: 20px;">• ❌ 你的情绪触发点（不学心理弱点）</p>
<p style="margin: 8px 0; padding-left: 20px;">• ❌ 其他人的偏好（即使共用设备）</p>

**安全第一，隐私优先。**

---

## 🎬 实战案例

### 案例 1：公众号写作

我告诉 OpenClaw：

```
1. 文章不要用 <ul><li>，用 <p> 标签
2. 代码块不要用 <pre>，用 <section>
3. 加粗必须用 <strong> 标签
```

重复 3 次后，现在每次生成的文章都符合公众号排版规范。

### 案例 2：代码风格

我告诉 OpenClaw：

```
1. MVP 项目用 SQLite
2. 注释用中文
3. 变量名用驼峰命名
```

现在写代码时，自动遵守这些规则，不用每次提醒。

### 案例 3：沟通风格

我告诉 OpenClaw：

```
1. 飞书消息要简洁
2. Discord 可以随意点
3. 技术问题要详细解释
```

现在它会根据不同平台调整语气和长度。

---

## 🚀 进阶玩法

### 1. 项目级偏好

为不同项目设置不同规则：

```
对于 blog 项目，文章风格要活泼
对于 work 项目，邮件要正式
```

### 2. 定期检查

用 Cron 任务每周检查记忆：

```json
{
  "name": "weekly-memory-check",
  "schedule": { "kind": "cron", "expr": "0 9 * * 1" },
  "payload": {
    "kind": "agentTurn",
    "message": "Show memory stats"
  }
}
```

### 3. 导出备份

随时导出你的"AI 记忆"：

```
Export memory
```

会生成一个 ZIP 文件，包含所有学习记录。

---

## 💡 总结

OpenClaw 的 Self-Improving 功能，让你的 AI 助手：

<p style="margin: 8px 0; padding-left: 20px;">• ✅ 越用越懂你</p>
<p style="margin: 8px 0; padding-left: 20px;">• ✅ 不用重复说偏好</p>
<p style="margin: 8px 0; padding-left: 20px;">• ✅ 会自我反思和改进</p>
<p style="margin: 8px 0; padding-left: 20px;">• ✅ 记忆分层管理，不会爆</p>
<p style="margin: 8px 0; padding-left: 20px;">• ✅ 隐私安全，不会乱学</p>

**简单说：养得越久，越顺手。**

---

## 🔗 相关资源

<p style="margin: 8px 0; padding-left: 20px;">• 📦 安装：`clawhub install self-improving`</p>
<p style="margin: 8px 0; padding-left: 20px;">• 📖 文档：https://clawic.com/skills/self-improving</p>
<p style="margin: 8px 0; padding-left: 20px;">• 💬 社区：https://discord.com/invite/clawd</p>

---

如果这篇文章对你有帮助，欢迎 **点赞、在看、转发** 三连支持！

有任何问题，欢迎在评论区留言，我会一一回复。

明天见 👋
