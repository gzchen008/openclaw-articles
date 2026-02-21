---
name: wechat-mp-publish
description: |
  微信公众号推文发布能力。支持通过 API 自动发布文章到已认证的公众号。
  
  触发场景：
  - 用户要求发布公众号文章、发推文、同步文章到微信
  - 用户提到"公众号"、"微信文章"、"公众号发布"
  - 自动化任务需要发布到公众号（如每日文章生成后发布）
  
  前置条件：
  - 已认证的订阅号或服务号
  - 已配置 WECHAT_APPID 和 WECHAT_SECRET 环境变量
  - 服务器 IP 已加入公众号后台白名单
---

# 微信公众号推文发布

## 快速开始

### 1. 配置凭证

在 OpenClaw 中配置公众号凭证（只需一次）：

```bash
# 设置环境变量
export WECHAT_APPID="your_appid"
export WECHAT_SECRET="your_secret"
```

或在 OpenClaw 配置文件中添加：

```json
{
  "env": {
    "WECHAT_APPID": "your_appid",
    "WECHAT_SECRET": "your_secret"
  }
}
```

### 2. 一键发布

```bash
python scripts/wechat_publisher.py auto \
  --title "文章标题" \
  --content articles/2026-02-16-title.html \
  --thumb assets/default-cover.jpg \
  --author "作者名"
```

## 核心命令

### auto - 一键发布（推荐）

完整的发布流程：上传封面 → 创建草稿 → 发布

```bash
python scripts/wechat_publisher.py auto \
  --title "标题" \
  --content "内容.html" \
  --thumb "封面.jpg" \
  --author "作者" \
  --digest "摘要" \
  --source-url "原文链接" \
  --dry-run  # 仅创建草稿，不发布
```

### draft - 仅创建草稿

```bash
# 封面可以是文件路径或已有的 media_id
python scripts/wechat_publisher.py draft \
  --title "标题" \
  --content "内容.html" \
  --thumb "封面.jpg"
```

### publish - 发布已有草稿

```bash
python scripts/wechat_publisher.py publish MEDIA_ID
```

### upload - 上传图片

```bash
# 上传封面缩略图（用于草稿封面）
python scripts/wechat_publisher.py upload cover.jpg --type thumb

# 上传图文内图片（用于文章内容中的图片）
python scripts/wechat_publisher.py upload image.jpg --type image
```

### list - 查看草稿列表

```bash
python scripts/wechat_publisher.py list
```

## 文章内容格式

### HTML 格式要求

文章内容必须是 HTML 格式，支持常见标签：

```html
<h1>标题</h1>
<p>段落内容</p>
<blockquote>引用文字</blockquote>
<ul>
  <li>列表项</li>
</ul>
<img src="微信图片URL" />
```

### 图片处理

**重要：** 文章中的图片 URL 必须来自微信服务器！

```bash
# 1. 先上传图片
python scripts/wechat_publisher.py upload image.jpg --type image
# 返回: {"url": "https://mmbiz.qpic.cn/..."}

# 2. 在 HTML 中使用返回的 URL
<img src="https://mmbiz.qpic.cn/..." />
```

### Markdown 转 HTML

如果源文件是 Markdown，使用以下工具转换：

```bash
# 使用 pandoc
pandoc article.md -o article.html

# 或使用 Python
python -c "
import markdown
content = open('article.md').read()
html = markdown.markdown(content)
open('article.html', 'w').write(html)
"
```

## 在 OpenClaw 中自动化

### 集成到每日文章生成

在 `wechat-content-plan.md` 生成文章后自动发布：

```python
# 伪代码示例
1. 生成 Markdown 文章
2. 转换为 HTML
3. 上传封面图
4. 调用 wechat_publisher.py auto
5. 发送 Discord 通知
```

### Cron 定时任务

```json
{
  "name": "daily-wechat-publish",
  "schedule": {"kind": "cron", "expr": "0 9 * * *"},
  "payload": {
    "kind": "agentTurn",
    "message": "生成今日公众号文章并发布到微信..."
  }
}
```

## 常见问题

### 1. 发布后显示"提交成功"但没看到文章？

发布是异步的，需要等待审核。配置回调 URL 可接收发布结果通知。

### 2. 图片显示不出来？

确保图片 URL 来自微信服务器，外部 URL 会被过滤。

### 3. 未认证订阅号无法发布？

API 发布功能仅支持已认证的订阅号/服务号。未认证账号只能创建草稿，需手动发布。

### 4. access_token 过期？

脚本会自动缓存 token，过期前自动刷新。

## API 参考

详细的 API 文档见 [references/api-reference.md](references/api-reference.md)

## 相关配置

### 公众号后台设置

1. **获取凭证**
   - 登录 mp.weixin.qq.com
   - 设置与开发 → 基本配置
   - 复制 AppID 和 AppSecret

2. **配置 IP 白名单**
   - 设置与开发 → 基本配置 → IP白名单
   - 添加服务器 IP

3. **配置回调 URL**（可选）
   - 用于接收发布状态通知
   - 需要公网可访问的服务器
