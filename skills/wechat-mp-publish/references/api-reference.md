# 微信公众号 API 参考

## 目录

1. [获取 access_token](#1-获取-access_token)
2. [上传素材](#2-上传素材)
3. [新建草稿](#3-新建草稿)
4. [发布草稿](#4-发布草稿)
5. [草稿管理](#5-草稿管理)
6. [错误码](#6-错误码)

---

## 1. 获取 access_token

### 请求

```
GET https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

### 参数

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| grant_type | string | 是 | 固定值: client_credential |
| appid | string | 是 | 公众号唯一标识 |
| secret | string | 是 | 公众号 appsecret |

### 返回

```json
{
  "access_token": "ACCESS_TOKEN",
  "expires_in": 7200
}
```

### 限制

- 每日调用上限: 2000 次
- 有效期: 2 小时
- 建议使用中控服务器统一管理

---

## 2. 上传素材

### 2.1 上传图文消息内图片

用于文章内容中的图片，返回微信 URL。

```
POST https://api.weixin.qq.com/cgi-bin/media/uploadimg?access_token=ACCESS_TOKEN
```

**请求格式:** multipart/form-data

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| media | file | 是 | 图片文件 |

**返回:**

```json
{
  "url": "http://mmbiz.qpic.cn/..."
}
```

### 2.2 新增永久素材（封面图）

用于文章封面，返回 media_id。

```
POST https://api.weixin.qq.com/cgi-bin/material/add_material?access_token=ACCESS_TOKEN&type=TYPE
```

**参数:**

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| type | string | 是 | 素材类型: image/voice/video/thumb |
| media | file | 是 | 文件内容 |

**限制:**

| 类型 | 大小限制 |
|-----|---------|
| image | 10MB |
| voice | 2MB |
| video | 10MB |
| thumb | 64KB |

**返回:**

```json
{
  "media_id": "MEDIA_ID",
  "url": "URL"
}
```

---

## 3. 新建草稿

### 请求

```
POST https://api.weixin.qq.com/cgi-bin/draft/add?access_token=ACCESS_TOKEN
```

### 请求体

```json
{
  "articles": [
    {
      "title": "标题",
      "author": "作者",
      "digest": "摘要",
      "content": "HTML内容",
      "content_source_url": "阅读原文链接",
      "thumb_media_id": "封面图media_id",
      "need_open_comment": 0,
      "only_fans_can_comment": 0,
      "pic_crop_235_1": "裁剪坐标",
      "pic_crop_1_1": "裁剪坐标"
    }
  ]
}
```

### 参数说明

| 参数 | 类型 | 必填 | 说明 |
|-----|------|-----|------|
| title | string | 是 | 标题，最长32字 |
| author | string | 否 | 作者，最长16字 |
| digest | string | 否 | 摘要，最长128字，单图文有效 |
| content | string | 是 | 图文内容，支持HTML，最长2万字符，<1MB |
| content_source_url | string | 否 | 原文链接，最长1KB |
| thumb_media_id | string | 是 | 封面图 media_id（永久素材） |
| need_open_comment | int | 否 | 是否打开评论: 0否(默认), 1是 |
| only_fans_can_comment | int | 否 | 是否仅粉丝可评论: 0否(默认), 1是 |

### 返回

```json
{
  "media_id": "DRAFT_MEDIA_ID"
}
```

### 注意事项

1. 图片 URL 必须来自微信服务器
2. 会过滤 JS 脚本
3. 发布后草稿自动删除

---

## 4. 发布草稿

### 请求

```
POST https://api.weixin.qq.com/cgi-bin/freepublish/submit?access_token=ACCESS_TOKEN
```

### 请求体

```json
{
  "media_id": "DRAFT_MEDIA_ID"
}
```

### 返回

```json
{
  "errcode": 0,
  "errmsg": "ok",
  "publish_id": "发布任务ID",
  "msg_data_id": "消息数据ID"
}
```

### 重要说明

- `errcode: 0` 仅表示**提交成功**，非发布完成
- 实际发布结果通过事件推送通知
- 需要配置回调 URL 接收通知

### 发布状态事件推送

```xml
<xml>
  <ToUserName>公众号ghid</ToUserName>
  <FromUserName>mphelper</FromUserName>
  <CreateTime>1234567890</CreateTime>
  <MsgType>event</MsgType>
  <Event>PUBLISHJOBFINISH</Event>
  <publish_id>发布任务ID</publish_id>
  <publish_status>0</publish_status>
  <article_id>文章ID</article_id>
  <count>1</count>
  <idx>1</idx>
  <article_url>文章链接</article_url>
</xml>
```

**publish_status 状态码:**

| 值 | 说明 |
|---|------|
| 0 | 成功 |
| 1 | 发布中 |
| 2 | 原创失败 |
| 3 | 常规失败 |
| 4 | 平台审核不通过 |
| 5 | 成功后用户删除 |
| 6 | 成功后系统封禁 |

---

## 5. 草稿管理

### 5.1 获取草稿列表

```
POST https://api.weixin.qq.com/cgi-bin/draft/batchget?access_token=ACCESS_TOKEN
```

```json
{
  "offset": 0,
  "count": 20,
  "no_content": 0
}
```

### 5.2 删除草稿

```
POST https://api.weixin.qq.com/cgi-bin/draft/delete?access_token=ACCESS_TOKEN
```

```json
{
  "media_id": "MEDIA_ID"
}
```

---

## 6. 错误码

### 通用错误

| 错误码 | 说明 |
|-------|------|
| -1 | 系统繁忙 |
| 0 | 成功 |
| 40001 | AppSecret 错误或不属于该公众号 |
| 40002 | 请确保 grant_type 为 client_credential |
| 40013 | AppID 无效 |
| 40164 | 调用 IP 不在白名单中 |

### 草稿相关

| 错误码 | 说明 |
|-------|------|
| 40007 | 无效的 media_id |
| 45008 | 图文消息超过限制 |
| 45009 | 接口调用超过限制 |

### 发布相关

| 错误码 | 说明 |
|-------|------|
| 48001 | api 功能未授权 |
| 53503 | 草稿未通过发布检查 |
| 53504 | 需前往公众平台官网使用草稿 |
| 53505 | 请手动保存成功后再发表 |

---

## 调用频率限制

| 接口 | 频率限制 |
|-----|---------|
| access_token | 2000次/天 |
| 新增永久素材 | 500次/天 |
| 新建草稿 | 100次/天 |
| 发布草稿 | 10次/天 |

## 参考链接

- [草稿箱管理 - 官方文档](https://developers.weixin.qq.com/doc/offiaccount/Draft_Box/Add_draft.html)
- [发布能力 - 官方文档](https://developers.weixin.qq.com/doc/offiaccount/Publish/Publish.html)
- [素材管理 - 官方文档](https://developers.weixin.qq.com/doc/offiaccount/Asset_Management/Adding_Permanent_Assets.html)
