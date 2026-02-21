# 微信公众号 API 发布推文技术方案

> 研究日期：2026-02-16
> 状态：技术调研完成

---

## 一、核心结论

**可以实现！** 微信公众号提供了完整的 API 接口来发布推文，但有一些限制：

| 账号类型 | 新建草稿 | 发布草稿 |
|---------|---------|---------|
| 订阅号（未认证） | ✅ | ❌ |
| 订阅号（已认证） | ✅ | ✅ |
| 服务号 | ✅ | ✅（需认证） |

**关键点：** 发布功能需要**已认证**的公众号才能使用 API 直接发布。

---

## 二、完整流程（3 步）

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  1. 获取    │ ──▶ │  2. 新建    │ ──▶ │  3. 发布    │
│ access_token│     │   草稿      │     │   草稿      │
└─────────────┘     └─────────────┘     └─────────────┘
```

### 步骤 1：获取 access_token

```bash
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

**返回：**
```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

**注意事项：**
- 有效期 2 小时，需要缓存
- 每天调用限制 2000 次
- 建议使用中控服务器统一管理

---

### 步骤 2：上传封面图片（永久素材）

**先上传封面图，获取 `media_id`：**

```bash
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=thumb

# FormData:
# media: 图片文件（PNG/JPG，最大 64KB）
```

**返回：**
```json
{
  "media_id": "THUMB_MEDIA_ID",
  "url": "封面图URL"
}
```

---

### 步骤 3：新建草稿

```bash
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN

# Body:
{
  "articles": [
    {
      "title": "文章标题",
      "author": "作者名",
      "digest": "文章摘要（选填）",
      "content": "图文消息的具体内容，支持HTML标签",
      "content_source_url": "阅读原文链接（选填）",
      "thumb_media_id": "封面图的media_id（必填）",
      "need_open_comment": 0,
      "only_fans_can_comment": 0
    }
  ]
}
```

**返回：**
```json
{
  "media_id": "DRAFT_MEDIA_ID"
}
```

**注意：**
- `content` 支持 HTML，但会过滤 JS
- 图片 URL 必须来自微信服务器（需先上传）
- 最大 1MB，少于 2 万字符

---

### 步骤 4：发布草稿

```bash
POST https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=ACCESS_TOKEN

# Body:
{
  "media_id": "DRAFT_MEDIA_ID"
}
```

**返回：**
```json
{
  "errcode": 0,
  "errmsg": "ok",
  "publish_id": "发布任务ID",
  "msg_data_id": "消息数据ID"
}
```

**重要：** 
- 返回 `errcode: 0` 只表示**提交成功**，不是发布完成
- 实际发布结果通过事件推送通知（需配置回调 URL）

---

## 三、前置准备

### 1. 公众号配置

在微信公众平台后台完成：

1. **获取 AppID 和 AppSecret**
   - 路径：设置与开发 → 基本配置
   - 复制保存（AppSecret 只显示一次）

2. **配置 IP 白名单**
   - 路径：设置与开发 → 基本配置 → IP白名单
   - 添加服务器 IP（调用 API 的机器）

3. **配置服务器回调 URL**（可选，用于接收发布结果）
   - 路径：设置与开发 → 基本配置 → 服务器配置
   - 用于接收发布状态事件推送

### 2. 权限要求

| 功能 | 订阅号（未认证） | 订阅号（已认证） | 服务号 |
|-----|---------------|---------------|-------|
| 新建草稿 | ✅ | ✅ | ✅ |
| 发布草稿 | ❌ | ✅ | ✅（需认证） |
| 群发消息 | ❌ | ✅（每天1条） | ✅（每月4条） |

---

## 四、Python 示例代码

```python
import requests
import json

class WeChatPublisher:
    def __init__(self, appid, secret):
        self.appid = appid
        self.secret = secret
        self.token = None
    
    def get_access_token(self):
        """获取 access_token"""
        url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={self.appid}&secret={self.secret}"
        res = requests.get(url).json()
        self.token = res.get("access_token")
        return self.token
    
    def upload_thumb(self, image_path):
        """上传封面图片"""
        url = f"https://api.weixin.qq.com/cgi-bin/material/add_material?access_token={self.token}&type=thumb"
        with open(image_path, "rb") as f:
            res = requests.post(url, files={"media": f}).json()
        return res.get("media_id")
    
    def create_draft(self, title, content, thumb_media_id, author="", digest=""):
        """新建草稿"""
        url = f"https://api.weixin.qq.com/cgi-bin/draft/add?access_token={self.token}"
        data = {
            "articles": [{
                "title": title,
                "author": author,
                "digest": digest,
                "content": content,
                "thumb_media_id": thumb_media_id,
                "need_open_comment": 0,
                "only_fans_can_comment": 0
            }]
        }
        res = requests.post(url, json=data).json()
        return res.get("media_id")
    
    def publish(self, media_id):
        """发布草稿"""
        url = f"https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token={self.token}"
        data = {"media_id": media_id}
        res = requests.post(url, json=data).json()
        return res


# 使用示例
if __name__ == "__main__":
    publisher = WeChatPublisher("YOUR_APPID", "YOUR_SECRET")
    
    # 1. 获取 token
    publisher.get_access_token()
    
    # 2. 上传封面
    thumb_id = publisher.upload_thumb("cover.jpg")
    
    # 3. 创建草稿
    draft_id = publisher.create_draft(
        title="测试文章",
        content="<p>这是文章内容</p>",
        thumb_media_id=thumb_id
    )
    
    # 4. 发布草稿
    result = publisher.publish(draft_id)
    print(result)
```

---

## 五、注意事项与坑点

### ⚠️ 1. 图片必须先上传
文章内容中的图片 URL 必须来自微信服务器，外部 URL 会被过滤。

**解决方案：** 使用「上传图文消息内的图片获取URL」接口
```bash
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=ACCESS_TOKEN
```

### ⚠️ 2. 封面图必须是永久素材
`thumb_media_id` 必须是**永久素材**的 media_id，临时素材不行。

### ⚠️ 3. 发布是异步的
调用发布接口后，需要等待事件推送才能确认最终状态。

### ⚠️ 4. 未认证订阅号无法 API 发布
如果是未认证的订阅号，只能创建草稿，需要手动去后台发布。

### ⚠️ 5. 群发 vs 发布
- **发布（freepublish）**：公开发布，粉丝可在历史消息中查看
- **群发（mass）**：推送到粉丝聊天列表，有次数限制

---

## 六、OpenClaw 集成方案

可以将此能力封装成 OpenClaw Skill：

```yaml
# skills/wechat-publish/SKILL.md
name: wechat-publish
description: 通过 API 自动发布微信公众号推文
triggers:
  - cron: "0 9 * * *"  # 每天 9 点
  - manual: "发布文章"
```

**实现思路：**
1. 从 `articles/` 目录读取生成的文章
2. 转换 Markdown → HTML（适配公众号格式）
3. 上传图片到微信素材库
4. 创建草稿 + 发布

**依赖配置：**
- 公众号 AppID / AppSecret（存在 OpenClaw 凭证中）
- 服务器 IP 已加白名单

---

## 七、参考文档

- [草稿箱管理 - 微信官方文档](https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html)
- [发布能力 - 微信官方文档](https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html)
- [素材管理 - 微信官方文档](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html)

---

*研究完成，可供后续开发参考*
