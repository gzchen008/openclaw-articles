# 公众号文章发布规范

> 最后更新：2026-02-19

## 📝 文章格式要求

### 开头格式
- **首行无空行**，直接从正文开始
- **⚠️ 不需要添加"本文由 AI 自动生成"的提示框**（用户已确认不需要）

### 结尾格式
- **⚠️ 不添加"本文由 AI 自动生成"声明**
- **✅ 用自然结尾**：例如"如果觉得有用，点个'在看'吧 👇"
- **模拟真人风格**，不要有机器感

### 排版要求（重要！）

#### 紧凑布局
- 段落间距：`margin: 8px 0`（不要用 16px）
- 标题间距：`margin-top: 16px`（不要用 24px）
- 列表项间距：`<li style="margin: 4px 0;">`

#### 避免多余黑点（最重要！）
- **⚠️ 微信公众号会渲染 `<ul>/<li>` 标签时产生多余黑点，即使紧凑排列也会出问题**
- **✅ 正确方案：不使用 `<ul>/<li>`，改用 `<p>` + `▸` 符号**
- 错误写法（会有黑点）：
  ```html
  <ul><li>项目1</li><li>项目2</li></ul>
  ```
- 正确写法（无黑点，用 ▸ 符号）：
  ```html
  <p style="margin: 6px 0; padding-left: 12px;">▸ 项目1</p>
  <p style="margin: 6px 0; padding-left: 12px;">▸ 项目2</p>
  ```
- **编号列表也用 `<p>` 代替 `<ol>/<li>`**：
  ```html
  <p style="margin: 6px 0; padding-left: 12px;">1. 第一步</p>
  <p style="margin: 6px 0; padding-left: 12px;">2. 第二步</p>
  ```

#### 代码块格式
- **⚠️ 不要用 `<pre><code>` 标签！公众号渲染有问题**
- **⚠️ 不要用 pandoc 转 HTML！pandoc 输出不适合公众号**
- **✅ 正确方案：手写 HTML，用 `<section>` + 灰底 + 蓝色左边框 + 等宽字体**
```html
<section style="margin: 12px 0; padding: 12px 16px; background: #F6F8FA; border-left: 3px solid #2B579A; font-size: 14px; line-height: 2; font-family: 'Menlo', monospace; color: #24292e;">git clone https://github.com/xxx<br>cd xxx<br>npm install</section>
```
- 多行内容用 `<br>` 换行，不用多个 `<p>`

#### 章节标题格式
- **用 `<h2>` + 蓝色背景条**：
```html
<h2 style="margin: 24px 0 12px; padding: 8px 12px; background: #2B579A; color: #fff; font-size: 18px;">📖 章节标题</h2>
```

#### 多项目/模块分隔（重要！）
- **⚠️ 不要用 CSS class（如 `.tool-card`），公众号不支持！**
- **⚠️ 不要只用 `<hr>` 分隔线，不够醒目**
- **✅ 正确方案：用背景色标题条**
```html
<!-- 项目标题：蓝底白字，非常醒目 -->
<p style="margin: 20px 0 4px 0; padding: 8px; background: #0366d6; color: #fff; font-weight: 600; text-align: center; border-radius: 4px;">━ 1️⃣ 项目名 ━</p>

<!-- 作者信息：小字灰色 -->
<p style="margin: 4px 0; font-size: 13px; color: #586069;">by 作者</p>

<!-- 描述 -->
<p style="margin: 8px 0;">项目描述...</p>
```

#### 加粗文字
- **⚠️ 不要只用 CSS `font-weight: 600/700`，公众号可能不生效**
- **✅ 必须用 `<strong>` 标签**
```html
<!-- 错误 -->
<p style="font-weight: 600;">加粗文字</p>

<!-- 正确 -->
<p><strong style="font-weight: 600;">加粗文字</strong></p>
```

### 排版风格
- **GitHub Pages 风格**
- 蓝色主题（#0366d6）
- 代码块灰色背景（#f6f8fa）
- 成功提示绿色（#28a745）
- 警告提示红色（#f66）
- 信息提示蓝色（#1890ff）

### Emoji 使用
- 📖 章节、效果展示
- 📋 前置条件、清单
- 🔧 代码、技术
- 🤖 AI、自动化
- ⏰ 定时任务
- ⚙️ 配置
- ❓ 问题
- ✅ 成功、完成
- ⚠️ 警告
- 💡 提示

---

## 🔄 自动发布流程

### 草稿管理（重要！）

**⚠️ 关键问题**：微信草稿 media_id 会失效，不能使用固定的草稿 ID

**正确流程**：
1. **每次创建草稿**：使用 `draft add` 创建新草稿
2. **保存 media_id**：创建成功后，保存到 `articles/.draft-state.json`
3. **尝试更新**：下次先尝试 `draft update`，如果失败则创建新草稿
4. **定期清理**：登录公众号后台删除旧草稿（草稿箱有上限）

**为什么不能固定草稿 ID？**
- 草稿发布后，media_id 会失效
- 草稿删除后，media_id 也会失效
- 每次创建新草稿会生成新的 media_id

### 固定资源
- **封面 ID**: `Sgs1hrgsJnAqIX94EoxAiGjxID8T5kW0p9NaZBe4sc5-vVJz3cEvJdHq7IoV66Ge`（2026-04-19 更新）
- **封面文件**: 之前文件已丢失，使用 SVG 生成的封面
- **最新草稿 ID**: 保存在 `articles/.draft-state.json`

### 任务流程
```
1. 生成文章内容（按内容计划）
2. 转换为 HTML（紧凑布局，避免多余黑点）
3. 读取 .draft-state.json 中的草稿 ID
4. 尝试 draft update（如果失败则 draft add）
5. 保存新的草稿 ID 到 .draft-state.json
6. 发送 Discord 通知给用户
7. 用户手动发布
```

---

## 🖼️ 架构图生成（fireworks-tech-graph）

### 触发场景
- 文章涉及系统架构、项目结构、流程设计时
- 用户明确要求画架构图
- 介绍开源项目时，补充架构图能提升可读性

### Skill 位置
- **架构图 Skill**: `skills/fireworks-tech-graph/`
- **依赖**: `rsvg-convert`（brew install librsvg）
- **输出**: SVG + PNG（1920px 宽）

### 工作流程
```
1. 分析项目/系统结构（源码包结构、README、文档）
2. 提取模块、层级、关系
3. 加载 Skill 参考文件（references/style-N.md）
4. 用 Python 生成 SVG（避免字符截断）
5. rsvg-convert 导出 1920px PNG
6. 上传图片到微信素材库
7. 嵌入文章 HTML
```

### 架构图嵌入文章格式
```html
<!-- 架构图：居中，圆角，最大宽度 100% -->
<p style="margin: 12px 0; text-align: center;">
  <img src="微信图片URL" style="max-width: 100%; border-radius: 6px;"/>
</p>
<p style="margin: 4px 0; font-size: 12px; color: #8b949e; text-align: center;">图注说明（作者绘制）</p>
```

### 上传图片到微信
```bash
python3 skills/wechat-mp-publish/scripts/wechat_publisher.py upload /tmp/architecture.png
# 返回 media_id 和 url，用 url 嵌入文章
```

### SVG 生成规范
- **必须用 Python list 方法**生成 SVG（避免字符截断）
- ViewBox 推荐 `0 0 960 600` 或 `0 0 960 800`
- 导出 PNG 宽度固定 1920px（2x Retina）
- 验证命令：`rsvg-convert file.svg -o /dev/null 2>&1`
- 导出命令：`rsvg-convert -w 1920 file.svg -o file.png`

### 常见图型
- **架构图**：分层设计，水平/垂直布局
- **流程图**：业务流程、决策分支
- **时序图**：API 调用时序
- **数据流图**：数据在各模块间的流转
- **对比矩阵**：方案/产品功能对比

### 默认风格
- Style 1（Flat Icon）：白底简洁，适合公众号
- 可根据文章调性选择 Dark（技术文章）或 Blueprint（架构文档）

### 注意事项
- 架构图节点不宜超过 20 个，太多会拥挤
- 中文标签用 PingFang SC / Microsoft YaHei
- 导出前务必验证 SVG 语法
- 图片 URL 使用微信返回的 mmbiz 域名，不要用本地路径

---

## 🛠️ 技术要点

### 编码处理
```python
headers = {"Content-Type": "application/json; charset=utf-8"}
json_data = json.dumps(payload, ensure_ascii=False).encode('utf-8')
```

### 创建草稿 API
```python
url = "https://api.weixin.qq.com/cgi-bin/draft/add?access_token={token}"
payload = {
    "articles": [{
        "title": "标题",
        "content": "HTML内容",
        "thumb_media_id": "封面ID"
    }]
}
# 返回新的 media_id，保存到 .draft-state.json
```

### 更新草稿 API（可能失败）
```python
url = "https://api.weixin.qq.com/cgi-bin/draft/update?access_token={token}"
payload = {
    "media_id": "草稿ID（可能已失效）",
    "index": 0,
    "articles": {
        "title": "标题",
        "content": "HTML内容",
        "thumb_media_id": "封面ID"
    }
}
# 如果失败（invalid media_id），改用 draft add
```

---

## 📂 文件位置

- **Skill**: `skills/wechat-mp-publish/`
- **脚本**: `skills/wechat-mp-publish/scripts/wechat_publisher.py`
- **状态**: `articles/.draft-state.json`
- **封面**: `articles/default-cover.jpg`
- **内容计划**: `wechat-content-plan.md`

---

## 🎯 每日任务

1. 生成文章内容
2. 转换为 HTML（紧凑布局）
3. 创建/更新草稿（保存新 media_id）
4. 发送 Discord 通知
5. 用户手动发布

---

## ⚠️ 常见问题

### Q: 为什么 CSS class 样式不生效？
A: **公众号不支持 CSS class！** 必须用内联 style。所有样式都要写在 `style="..."` 属性里。

### Q: 为什么加粗不显示？
A: **必须用 `<strong>` 标签**，不能只靠 CSS `font-weight`。正确写法：`<strong style="font-weight: 600;">文字</strong>`

### Q: 为什么代码框显示有问题？
A: **不要用 `<pre><code>` 标签**，改用 `<section style="background: #f6f8fa;">` + 等宽字体 `font-family: monospace`。

### Q: 为什么多个项目混在一起分不清？
A: **不要只用 `<hr>` 或边框分隔**，用背景色标题条：`<p style="background: #0366d6; color: #fff;">━ 1️⃣ 项目名 ━</p>`

### Q: 为什么草稿箱有很多重复草稿？
A: 因为每次创建新草稿会生成新的 media_id，旧的 media_id 会失效。需要定期清理。

### Q: 为什么列表项之间有多余的黑点？
A: 因为 `<li>` 标签之间有空行。必须紧凑排列，不能有空行。

### Q: 如何清理草稿箱？
A: 登录公众号后台 → 素材管理 → 草稿箱 → 删除旧草稿

---

*此规范适用于所有后续公众号文章*
