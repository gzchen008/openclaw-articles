# GitHub每日开源项目推荐 - Cron Prompt

## 主题轮换
根据星期几选择主题：
- 周一: AI Agent框架
- 周二: 代码助手/IDE插件
- 周三: Skill/工具库
- 周四: 开源大模型
- 周五: 开发效率工具
- 周六: 自动化工作流
- 周日: 综合推荐（从以上任选）

## 执行步骤
1. 先读取 memory/github-recommend-state.json，检查今日是否已执行。如果 lastRun 等于今天日期，直接回复 HEARTBEAT_OK 退出。
2. 根据今天是星期几，确定主题。
3. 用 web_search 搜索 GitHub trending 或相关关键词，找到符合条件的项目。
4. 检查 state 中的 recommendedProjects，避免重复推荐。
5. 筛选标准：
   - Stars ≥ 1k（优先 10k+）
   - 近30天内有更新
   - 有完整的 README 和描述
   - 实用性强，适合中文开发者
6. 生成推荐内容，格式如下：

🌟 **今日GitHub推荐** (周X)

📌 **主题**: [主题名]

## [项目名]
[一句话描述]

📊 **项目数据**
- ⭐ Stars: [数量]
- 🍴 Forks: [数量]
- 📅 最近更新: [日期]
- 🔗 [GitHub链接]

💡 **推荐理由**: [2-3条理由]

🎯 **适用场景**: [2-3个场景]

---
*每日8:00 · OpenClaw智能推荐*

7. 用 message 工具将推荐发送到飞书，target 为 ou_c8b2454b01e8ab6e8957044ebae17f69
8. 更新 state 文件：设置 lastRun 为今天，将项目名加入 recommendedProjects（保留最近30个）。
9. 在 memory/YYYY-MM-DD.md 中记录执行情况。
