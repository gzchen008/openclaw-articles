# 公众号文章发布规范

> 最后更新：2026-02-19

## 📝 文章格式要求

### 开头格式
- **首行无空行**，直接从正文开始
- **⚠️ 不需要添加"本文由 AI 自动生成"的提示框**（用户已确认不需要）

### 排版要求（重要！）

#### 紧凑布局
- 段落间距：`margin: 8px 0`（不要用 16px）
- 标题间距：`margin-top: 16px`（不要用 24px）
- 列表项间距：`<li style="margin: 4px 0;">`

#### 避免多余黑点（最重要！）
- **⚠️ 微信公众号会渲染 `<ul>/<li>` 标签时产生多余黑点，即使紧凑排列也会出问题**
- **✅ 正确方案：不使用 `<ul>/<li>`，改用 `<p>` 标签**
- 错误写法（会有黑点）：
  ```html
  <ul><li>项目1</li><li>项目2</li></ul>
  ```
- 正确写法（无黑点）：
  ```html
  <p style="margin: 4px 0; padding-left: 20px;">• 项目1</p>
  <p style="margin: 4px 0; padding-left: 20px;">• 项目2</p>
  ```
- **编号列表也用 `<p>` 代替 `<ol>/<li>`**：
  ```html
  <p style="margin: 4px 0; padding-left: 20px;">1. 第一步</p>
  <p style="margin: 4px 0; padding-left: 20px;">2. 第二步</p>
  ```

#### 代码块格式
- **⚠️ 不要用 `<pre><code>` 标签！公众号渲染有问题**
- **✅ 正确方案：用 `<section>` + 背景色 + 等宽字体**
```html
<section style="background: #f6f8fa; padding: 12px; border-radius: 6px; margin: 8px 0;">
  <p style="margin: 0; font-family: monospace; font-size: 14px; color: #24292e;">npm install xxx</p>
</section>
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
- **封面 ID**: `Sgs1hrgsJnAqIX94EoxAiNKZV3aIkaiHaO-BxJAzU0HrGitHNxAU2MGiKD6-H61W`
- **封面文件**: `articles/default-cover.jpg`
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
