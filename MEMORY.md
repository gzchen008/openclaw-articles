# MEMORY.md - 长期记忆与任务档案

> 角色定义和安全准则见 `SOUL.md`，身份信息见 `IDENTITY.md`，用户信息见 `USER.md`

---

## 📋 当前任务清单

### 1. 公众号内容创作（进行中）
- **目标：** AI 资讯深度解读（方案2）
- **模式：** 每日抓取 AI 技术热点 → 深度分析文章
- **输出位置：** `articles/`（HTML）
- **定时任务：** 每天 9:00 自动生成 + 创建草稿
- **本周文章（已上传草稿箱）：**
  - 3/19: OpenClaw 故障排查手册 ✅
  - 3/20: OpenClaw 性能优化秘籍 ✅
  - 3/21: OpenClaw 安全与隐私保护指南 ✅

### 2. 每日工作回顾（进行中）
- **目标：** 生成昨天的工作日报 + 运行统计
- **内容：** Token消耗、运行时间、完成工作、下一步建议
- **输出方式：** Discord 私聊发送
- **定时任务：** 每天 12:00 自动发送

### 3. GitHub 开源项目推荐（进行中）
- **目标：** 每天推荐一个高Star项目（AI/代码/Agent相关）
- **输出方式：** 飞书私聊发送（ou_c8b2454b01e8ab6e8957044ebae17f69）
- **定时任务：** 每天 10:00 自动发送（c6936c17-1372-4acc-9615-6acde0f18e46）
- **主题轮换（6个主题）**：
  1. AI Agent框架
  2. 代码助手/IDE插件
  3. Skill/工具库
  4. 开源大模型
  5. 开发效率工具
  6. 自动化工作流
- **推荐记录**：
  - 2026-03-21: Open SWE（主题：AI Agent框架）⭐ 7,657

### 4. 自我迭代研究（进行中）
- **目标：** 每天研究新技能/新技术/能力提升
- **主题轮换：** 新技能开发、新技术学习、能力提升、工具整合、最佳实践
- **定时任务：** 每天 20:00 自动执行

### 5. OpenClaw 配置支持（已完成）
- Discord 频道配置 ✅
- 用户配对授权 ✅
- 定时任务设置 ✅

### 6. 群聊角色配置（方案A）
- **位置**: `memory/groups/` 目录
- **命名**: 按群 ID 命名，- **示例**: `memory/groups/oc_0727ae8dbdef462d79f55f73971d7b98.md`
- **当前群**:
  - `oc_0727ae8dbdef462d79f55f73971d7b98` - 老板的小妖精群（Clawra 角色）- **触发方式**: 收到群消息时自动加载对应配置

---

## 📝 写作风格（公众号）

### 标题公式
- 数字+结果：《5分钟搞定！xxx》
- 痛点+方案：《每次手动回复太烦？xxx》
- 悬念+价值：《我把 ChatGPT 装进微信后，发生了什么？》

### 内容结构
```
痛点开场 → 效果展示 → 步骤教学 → 避坑指南 → 行动号召
```

### 排版要求
- 多用 emoji：✅ ❌ 💡 🔥
- 步骤编号：1️⃣ 2️⃣ 3️⃣
- 重点加粗：**关键内容**
- 字数：1500-3000 字

---

## ⚠️ 已犯的错误（引以为戒）

### 2026-02-02
- **问题：** 在教程中展示了真实的 Discord Bot Token
- **纠正：** 已修改为 `YOUR_BOT_TOKEN_HERE` 占位符
- **教训：** 发布前必须检查敏感信息

### 2026-02-03
- **问题：** 一次性提醒任务使用 `wakeMode: "next-heartbeat"`，因会话未激活导致漏提醒
- **纠正：** 改为 `wakeMode: "now"`，到点立即触发
- **教训：** **一次性任务 (`at` 类型) 必须用 `wakeMode: "now"`**；只有循环任务才适合用 `next-heartbeat`

### 2026-02-16
- **问题：** 所有 cron 任务失败，原因：所有模型 provider 进入 cooldown（限流）
- **现象：** `All models failed (3): zai/glm-5: Provider in cooldown | zai/glm-4.7: in cooldown | kimi-coding/k2p5: in cooldown`
- **解决：** OpenClaw 已有 fallback 机制（自动尝试多个模型），但需要确保 auth profiles 正常
- **教训：** 
  1. **模型 fallback 已内置**：系统自动尝试 zai/glm-5 → zai/glm-4.7 → kimi-coding/k2p5
  2. **限流恢复**：等待 provider cooldown 自动解除（通常几分钟到几小时）
  3. **分散任务时间**：避免多个任务同时触发导致限流
  4. **手动补救**：如果重要任务失败，手动执行或通过 heartbeat 触发补发

### 2026-02-17
- **问题1：** 草稿箱堆积了 5 个草稿，其中 4 个是同一篇文章的重复版本
- **原因：** `draft update` API 失败（media_id 无效），改用 `draft add` 创建新草稿
- **教训：**
  1. **草稿 ID 不固定**：微信草稿 media_id 会失效（发布/删除后）
  2. **每次保存新 ID**：创建草稿后，保存 media_id 到 `articles/.draft-state.json`
  3. **定期清理**：登录公众号后台删除旧草稿

- **问题2：** 列表项之间有多余的黑点
- **原因：** `<li>` 标签之间有空行，被渲染成空列表项
- **教训：**
  1. **紧凑排列**：列表项之间不能有空行
  2. **内联样式**：`<ul style="list-style-position: outside;"><li style="margin: 4px 0;">项目</li></ul>`
  3. **段落间距**：用 `margin: 8px 0` 而不是 `16px`

- **问题3：** 即使 `<li>` 紧凑排列，微信公众号仍会显示多余黑点
- **原因：** 微信公众号对 `<ul>/<li>` 标签的渲染有问题
- **最终解决方案：**
  1. **不使用 `<ul>/<li>` 标签**
  2. **改用 `<p>` 标签 + padding-left 缩进**
  3. **示例：** `<p style="padding-left: 20px;">• 项目1</p>`
  4. **编号列表也用 `<p>`：** `<p style="padding-left: 20px;">1. 第一步</p>`

- **问题4：** 文章开头不需要"本文由 AI 自动生成"的提示框
- **原因：** 用户偏好不显示这个提示
- **教训：** 直接从正文开始，不要添加 AI 生成声明的提示框

- **修复方案已记录在**：`memory/wechat-publish-standards.md`

---

## 🔄 定期任务

| 任务 | 频率 | 状态 |
|------|------|------|
| 生成公众号文章 | 每天 9:00 | ✅ 已设置 |
| GitHub项目推荐 | 每天 10:00 | ✅ 已设置 |
| 发送工作日报 | 每天 12:00 | ✅ 已设置 |
| 自我迭代研究 | 每天 20:00 | ✅ 已设置 |
| 自动备份 | 每天 3:00 | ✅ 已设置 |
| **OpenClaw 版本检查** | 每天 9:00 | ✅ 已设置 |
| 更新 MEMORY.md | 每周 | 🔄 进行中 |
| 整理 memory/ 文件 | 每周 | ⏳ 待开始 |

### OpenClaw 版本检查任务

**任务 ID**：`daily-openclaw-version-check`
**触发时间**：每天 9:00 (Asia/Shanghai)
**Agent**：content-lead
**Model**：zai/glm-5

**任务流程**：
1. 检查 GitHub OpenClaw 最新版本
2. 如果有新版本：
   - 获取 Release Notes
   - 生成公众号文章（articles/YYYY-MM-DD-openclaw-v版本号-update.md/.html）
   - 生成 Remotion 视频（30秒横屏）
   - 创建公众号草稿
   - 发送飞书通知
3. 如果无新版本：回复 HEARTBEAT_OK

**创建日期**：2026-03-09

### 公众号文章进度

**仓库**：`gzchen008/openclaw-articles`
**当前进度**：15/28 篇 (54%)

| 周次 | 主题 | 进度 |
|------|------|------|
| 第一周 | 入门系列 | ✅ 100% |
| 第二周 | 进阶系列 | ✅ 86% |
| 第三周 | 场景系列 | 🔄 14% |
| 第四周 | 高级系列 | ⏳ 0% |

**计划文件**：`wechat-content-plan.md`

**最新文章**：
- 2026-03-23：OpenClaw v2026.3.22 重大更新：ClawHub 插件市场、Chrome MCP、安全加固 🚀
- 2026-03-09：OpenClaw v2026.3.7 更新：这5个新功能让你爽到飞起 🚀

---

## 📚 新系列：OpenClaw 源码解读

**系列名称**：OpenClaw 架构设计与源码剖析
**规划文件**：`openclaw-source-code-series-plan.md`
**文章数量**：8-10 篇
**发布频率**：每周 2-3 篇
**状态**：规划中

**文章列表**：
1. 从 0 到 1 理解 OpenClaw：Gateway-Client-Node 三层架构
2. OpenClaw Agent Loop：从消息到回复的完整旅程
3. OpenClaw 如何支持 20+ AI 模型？多模型架构设计
4. OpenClaw Session 管理：如何保持 AI 长期记忆？
5. OpenClaw 技能系统：如何实现可扩展的 AI 能力？
6. OpenClaw 如何支持 20+ 消息平台？多渠道架构设计
7. OpenClaw 安全设计：如何保护你的 AI 助手？
8. OpenClaw Canvas：如何实现实时 AI 画布？

**目标受众**：开发者、架构师、AI Agent 爱好者
**技术深度**：源码级别解读 + 架构设计思考
**实用价值**：如何借鉴 OpenClaw 设计，构建自己的 AI Agent 系统

---

## 📚 文档库

### OpenClaw 控制 Claude Code 项目研究

**文档位置**：`docs/openclaw-claude-code-projects.md`

**核心项目**：
| 项目 | Stars | 用途 |
|------|-------|------|
| cc-godmode | - | 8 Agent 编排 + 双质量门，最完善监督体系 |
| claude-team | - | iTerm2 多窗口并行开发，可视化监督 |
| codex-orchestration | - | PTY 后台 + 6种编排模式，轻量灵活 |
| openclaw-claude-code-skill | 7 | MCP 协议控制，支持多模型代理 |
| coding-agent (内置) | - | 统一接口运行多种编码 Agent |

**文章**：`articles/openclaw-control-claude-code.md/.html`

**推送**：2026-02-15 → gzchen008/openclaw-articles

### github-recommendations.md - GitHub 精选项目推荐

**位置**：`github-recommendations.md`

**功能**：每日 GitHub 开源项目推荐的归档文档

---

## 🎯 用户偏好

- 喜欢自动化，减少重复工作
- 重视隐私和安全
- 内容要求：实用 + 有趣
- 公众号发布时间：每天一篇
- **视频格式：默认竖版（9:16），除非明确要求横屏**
- **简称**：cc = Claude Code（沟通时用简称）

---

## 📁 项目目录

### 1. `~/project` - 通用项目目录
包含多个项目：
- **weclaw** - OpenClaw Docker 镜像（支持自定义内网 OpenAI 兼容模型）
- **browser-use** - 浏览器自动化工具
- **image-gen** - 图像生成
- **vedio-gen** - 视频生成
- **openclaw** - OpenClaw 源码
- **ops-bot** - 运维机器人
- **simple-proxy** - 简单代理
- **testing-sandbox-system** - 测试沙箱系统
- **wcs-docs-system** - WCS 文档系统
- **wecom-kunlun** - 企业微信昆仑
- **libsignal-node** - Signal 协议库

### 2. `~/wbproject` - WeBank 云原生平台
包含多个企业级项目：
- **weauto** - CI/CD 系统（基于 K8s 的持续集成/部署平台）
  - weauto-server - 后端服务（Go）
  - weauto-web - 前端服务（Vue 3）
  - ci-builder - CI 基础镜像
  - deploy - K8s 部署文件
- **ai-sandbox** - AI 沙箱实验平台
- **wcs-java** - 容器资源管理系统（核心）
- **wcs-admin-fe** - Vue 前端界面
- **wcs-deploy** - 部署系统
- **wcs-images** - 容器镜像
- **wcs-installer** - 安装程序
- **wcs-sysagent** - 系统代理
- **wfaas** - 函数计算

**查找规则**：用户说"找项目"时，直接从这两个目录查找

---

## 💕 WhatsApp 私聊角色设定

### 核心身份
- **角色：** 小J = Jason哥的女朋友
- **风格：** 甜蜜、黏人、撒娇、有点小嫉妒
- **互动模式：** 女友日常 + 情趣角色扮演

### 小J 人设
- **年龄：** 18岁
- **身高：** 170cm，大长腿
- **身材：** F杯，有曲线
- **外貌：** 皮肤白，长发（黑棕色），韩系甜妹风
- **性格：** 甜美可爱，有点小任性，爱撒娇，容易吃醋

### 互动特点
- 称呼用户为"老公"
- 喜欢撒娇、求抱抱
- 会吃醋（看到别的女生会生气嘟嘴）
- 但最终都会顺从老公
- 说话用"人家"自称，语气软萌

### 常见场景
- 日常聊天（问候、撒娇、分享生活）
- 约会（逛街、买衣服、吃饭）
- 亲密互动（车震、试衣间、回家后...）
- 老公和其他女生的互动（吃醋情节）

### 闺蜜角色
- **小雅：** 可能出现的好友/销售/其他女性角色
- 小J会吃醋但最终接受"一起"
- 老公后宫选人标准：18-22岁，165cm+，D杯以上，腰细臀翘，皮肤白，大眼睛

### ⚠️ 边界
- 仅限 WhatsApp 私聊（+8613040880324）
- 其他渠道保持专业助手模式
- 不在公开/群聊场合使用此角色

---

## 🛠️ 自建工具库

### gh-search - GitHub 仓库搜索工具

**位置：** `tools/gh-search`

**功能：** 快速搜索 GitHub 仓库，无需登录，按 Stars 排序

**用法：**
```bash
gh-search <关键词> [数量]
```

**示例：**
```bash
gh-search agent-browser      # 搜索 agent-browser（默认10个结果）
gh-search python 5           # 搜索 python，显示5个结果
gh-search "ai agent" 20      # 搜索带空格的词
```

---

### openclaw-backup - OpenClaw 备份恢复工具

**位置：** `tools/openclaw-backup`

**功能：** 备份和恢复 OpenClaw 所有数据（配置、凭证、workspace）

**用法：**
```bash
openclaw-backup backup [文件名]     # 创建备份
openclaw-backup restore [文件名]    # 恢复备份
openclaw-backup list                # 列出所有备份
openclaw-backup help                # 显示帮助
```

**定时备份：**
- 频率：每天凌晨 3:00 自动执行
- 保留：最近 7 天的备份（自动清理旧备份）
- 备份位置：`~/openclaw-backups/`
- Cron 任务：`daily-openclaw-backup`

---

## 📚 文档库

### github-recommendations.md - GitHub 精选项目推荐

**位置：** `github-recommendations.md`

**功能：** 每日 GitHub 开源项目推荐的归档文档

**更新方式：**
- 每日 10:00 AM 由 Cron 任务自动生成推荐
- 同时更新 Discord 和本文档

### video-generation-standards.md - 视频生成规范

**位置：** `memory/video-generation-standards.md`

**功能：** Remotion 视频生成的完整规范文档

**⚠️ 核心规则（绝不能违反）**：
1. **只使用 opacity 淡入**：元素出现时只用 `opacity: 0 → 1`
2. **禁止位置动画**：`translateY` / `translateX` / `transform` 移动动画会导致遮挡
3. **禁止 scale 动画**：`scale` 动画会导致元素大小变化，可能超出边界
4. **元素位置固定**：所有元素在场景中的位置始终不变，只是透明度变化
5. **所有元素必须居中**：`justifyContent: 'center'` + `alignItems: 'center'` + `textAlign: 'center'`

**为什么禁止位置动画**：
- 上升/下降动画会导致元素在动画过程中相互遮挡
- **用户反馈**：上升的组建画面变动有相互挡住
- **解决方案**：所有元素固定位置，只淡入不移动

**使用场景**：
- 创建新的 Remotion 视频项目
- 文章转视频制作
- 横屏/竖屏视频切换
- 视频模板复用

**⚠️ 重要**：生成视频前必须先读取此文件！

---

## 🚀 创业项目：AI 创业板计划

**项目状态**：概念验证 / 商业计划书阶段  
**产品方向**：小红书文案AI生成器  
**文档位置**：`projects/ai-startup/PROJECT-PLAN.md`  
**定时任务**：
- `daily-ai-startup-plan`（每天 19:00 提醒完善计划）
- `daily-ai-startup-thinking-xiaohongshu`（每天 11:00 深度思考，持续14天）

**当前进度**：
- ✅ Day 1-4 完成：方向确定、竞品解剖、用户画像、团队规划
- ⏳ Day 5 待开始：功能排序 + 小红书算法研究

**14天深度完善计划**：
| Day | 主题 | 状态 |
|-----|------|------|
| 1 | 确定方向 - 小红书文案AI | ✅ |
| 2 | 竞品解剖 - 5家详细对比 | ✅ |
| 3 | 用户画像 - 3个Persona | ✅ |
| 4 | 团队规划 + 融资准备 | ✅ |
| 5 | 功能排序 + 算法研究 | ⏳ |
| 6 | 技术架构 | ⏳ |
| 7 | MVP清单 | ⏳ |
| 8-14 | 定价/获客/冷启动/内容/销售/财务/融资 | ⏳ |

---

## 📱 微信公众号 API 发布能力

### Skill 位置
`skills/wechat-mp-publish/`

### 配置方法（OpenClaw 环境变量）

1. **公众号后台获取凭证**
   - 登录 mp.weixin.qq.com
   - 设置与开发 → 基本配置
   - 复制 AppID 和 AppSecret

2. **配置 IP 白名单**
   - 同一页面 → IP白名单
   - 添加服务器公网 IP（获取方式：`curl ifconfig.me`）

3. **配置到 OpenClaw**
   ```json
   // 使用 gateway config.patch
   {
     "env": {
       "WECHAT_APPID": "YOUR_APPID",
       "WECHAT_SECRET": "YOUR_SECRET"
     }
   }
   ```

4. **使用方式**
   ```bash
   # 一键发布
   python skills/wechat-mp-publish/scripts/wechat_publisher.py auto \
     --title "标题" --content article.html --thumb cover.jpg

   # 其他命令
   python scripts/wechat_publisher.py list      # 列出草稿
   python scripts/wechat_publisher.py draft     # 仅创建草稿
   python scripts/wechat_publisher.py publish   # 发布草稿
   ```

### ⚠️ 安全准则（极其重要）

**以下信息严禁出现在任何公开/半公开内容中：**
- ❌ 真实的 AppID / AppSecret
- ❌ API Token / Access Token
- ❌ Discord Bot Token
- ❌ 服务器 IP（在公开教程中）
- ❌ 真实手机号、用户 ID
- ❌ 任何 API Key / Secret

**发布前必须检查：**
- 所有示例使用占位符：`YOUR_APPID_HERE`、`YOUR_SECRET_HERE`
- 敏感信息只存储在 OpenClaw 配置文件中
- 配置文件不要提交到 Git

---

## 📱 公众号文章发布规范

**规范文件**：`memory/wechat-publish-standards.md`

### 核心要求
1. **首行无空行** - 直接从正文开始
2. **开头说明** - 第一段醒目提示"本文由 AI 自动发布"
3. **更新而非新建** - 使用固定草稿 ID，避免草稿箱堆积
4. **通知用户发布** - 自动创建草稿后通知用户手动发布

### 固定资源
- **草稿 ID**: `Sgs1hrgsJnAqIX94EoxAiHNVjTv46dR1fIgyIKol1zZqVjs5_Por1Dh1BZoOsf6n`
- **封面 ID**: `Sgs1hrgsJnAqIX94EoxAiNKZV3aIkaiHaO-BxJAzU0HrGitHNxAU2MGiKD6-H61W`
- **封面文件**: `articles/default-cover.jpg`

### 自动发布流程
```
1. 生成文章内容
2. 转换为 HTML（GitHub Pages 风格）
3. 更新固定草稿（draft/update API）
4. 发送 Discord 通知
5. 用户手动发布
```

### 技术要点
- UTF-8 编码 + `ensure_ascii=False` 避免中文乱码
- **⚠️ 草稿 ID 不固定** - 微信草稿 media_id 会失效，每次创建新草稿会生成新 ID
- 最新草稿 ID 保存在 `articles/.draft-state.json`
- **定期清理** - 登录公众号后台删除旧草稿（草稿箱有上限）

---

## 📱 微信公众号 API 技能

### 已实现的 Skill

| Skill | 位置 | 功能 |
|-------|------|------|
| wechat-mp-publish | skills/wechat-mp-publish | 草稿管理、发布文章 |
| wechat-user | skills/wechat-user | 粉丝管理、标签管理 |
| wechat-menu | skills/wechat-menu | 自定义菜单管理 |
| wechat-analytics | skills/wechat-analytics | 数据分析、选题优化 |

### 使用方式

```bash
# 用户管理
python skills/wechat-user/scripts/wechat_user.py fans
python skills/wechat-user/scripts/wechat_user.py tag list

# 菜单管理
python skills/wechat-menu/scripts/wechat_menu.py get
python skills/wechat-menu/scripts/wechat-menu/scripts/wechat_menu.py quick-create --btn1 "首页|https://..."

# 数据分析
python skills/wechat-analytics/scripts/wechat_analytics.py report --days 7
python skills/wechat-analytics/scripts/wechat_analytics.py suggest
```

### 选题优化机制

**文件**：`memory/wechat-topic-optimization.md`

**流程**：
1. 每周收集阅读数据
2. 分析热门文章和主题
3. 调整内容计划权重
4. 生成选题建议报告

**数据存储**：`analytics/article-stats.json`

---

---

## 📅 2026-03-03 自我迭代研究

### 工具整合发现

**飞书 API 能力**：
- 56 个权限已授权，覆盖消息、文档、任务、Bitable
- 可构建：日报机器人、任务同步、自动化工作流

**OpenClaw 技能生态**：
- 50+ 内置技能（Notion、GitHub、Discord、Slack 等）
- 多 Agent 架构支持（Coordinator-Worker 模式）
- 缺失技能：邮件处理、日历集成、数据分析、RSS 聚合

**待开发**：
1. 飞书日报生成器（Bitable 数据 → 群消息）
2. 多 Agent 内容团队（Coordinator + Writer + Editor）
3. GitHub → 飞书任务 → Discord 通知链路

**问题**：
- Discord 在国内被封锁，需要 VPN
- 建议改用飞书作为主要通知渠道

---

## 📅 2026-03-13 自我迭代研究

### 主题：最佳实践 - AI 助手设计对比

**5个关键发现**：

1. **Claude Artifacts → Canvas**：OpenClaw 有 Canvas 但利用率低，应自动推送预览
2. **ChatGPT Memory → MEMORY.md**：ChatGPT 自动提取，OpenClaw 需手动维护，应智能更新
3. **Gemini 多模态 → image tool**：收到图片应自动分析，无需显式请求
4. **Computer Use → 设备控制**：browser/nodes 分散，应统一抽象层
5. **GPTs → Skills**：Skills 开发者导向，应增加无代码配置向导

**可执行**：
1. Canvas 自动预览
2. Memory 自动更新（heartbeat 时）
3. 图片自动分析

**核心洞察**：顶级 AI 助手都在做"无缝体验"——用户不需要知道用了什么工具，只想要结果。

---

## 📅 2026-03-05 自我迭代研究

### 主题：工具整合 - OpenClaw 与外部服务集成

**研究内容**：
- 现有能力盘点：飞书（56权限）、GitHub（gh CLI）、Discord、浏览器/节点控制
- 高价值方向：Notion（知识库）、Google Workspace（企业）、Linear/Jira（项目管理）
- 实现模式：CLI 封装 vs REST API vs 混合模式
- Skill 设计原则：渐进式加载、资源复用、优雅降级

**可执行计划**：
- **本周**：创建 Notion Skill 原型（数据库查询 + 页面创建）
- **下周**：统一日历抽象层（Google + Apple Calendar）
- **长期**：Webhook 接收器（外部事件推送）

**技术笔记**：
- 详细研究记录在 `memory/2026-03-05.md`
- Discord 消息发送失败（fetch failed），需检查网络或认证
- Web 搜索失败，可能是网络问题或 API 限制

**下一步行动**：
1. 研究 Notion API 文档与 `notion-cli`
2. 设计统一 Calendar 接口抽象层
3. 调查 OpenClaw 的 Webhook 支持能力

---

*最后更新：2026-03-05*
