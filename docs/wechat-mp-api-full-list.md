# 微信公众平台 API 完整梳理

> 研究日期：2026-02-16
> 来源：https://developers.weixin.qq.com/doc/subscription/api/

---

## 📊 API 分类总览

| 分类 | 子分类 | 主要功能 |
|------|--------|---------|
| 基础接口 | - | Token、IP获取 |
| 自定义菜单 | - | 创建/查询/删除菜单 |
| 消息管理 | 群发/订阅/自动回复 | 消息发送 |
| 素材管理 | 永久/临时 | 素材上传下载 |
| 草稿管理 | - | 草稿增删改查 |
| 发布能力 | - | 发布文章 |
| 用户管理 | 标签/信息 | 用户管理 |
| 客服消息 | 管理/会话 | 客服系统 |
| 数据统计 | 用户/图文/消息 | 数据分析 |
| 网页开发 | JS-SDK | 前端调用 |
| 智能接口 | 翻译/OCR | AI 能力 |
| 门店管理 | - | 门店小程序 |

---

## 🔥 最有用的 API（推荐）

### 1. 📝 内容发布相关（已实现）

| API | 用途 | 已实现 |
|-----|------|--------|
| `draft/add` | 新建草稿 | ✅ |
| `draft/update` | 更新草稿 | ✅ |
| `draft/get` | 获取草稿详情 | ✅ |
| `draft/batchget` | 获取草稿列表 | ✅ |
| `draft/delete` | 删除草稿 | ✅ |
| `freepublish/submit` | 发布草稿 | ✅ |
| `material/add_material` | 上传素材 | ✅ |
| `media/uploadimg` | 上传图文图片 | ✅ |

---

### 2. 💬 消息管理（推荐实现）

#### 群发消息
| API | 用途 | 价值 |
|-----|------|------|
| `message/mass/sendall` | 按标签群发 | ⭐⭐⭐⭐⭐ |
| `message/mass/preview` | 预览消息 | ⭐⭐⭐⭐ |
| `message/mass/get` | 查询发送状态 | ⭐⭐⭐ |

#### 客服消息
| API | 用途 | 价值 |
|-----|------|------|
| `message/custom/send` | 发送客服消息 | ⭐⭐⭐⭐⭐ |
| `customservice/getkflist` | 获取客服列表 | ⭐⭐⭐ |
| `customservice/kfsession/create` | 创建会话 | ⭐⭐⭐⭐ |

#### 自动回复
| API | 用途 | 价值 |
|-----|------|------|
| `get_current_autoreply_info` | 获取自动回复规则 | ⭐⭐⭐ |

---

### 3. 🏷️ 用户管理（推荐实现）

#### 用户信息
| API | 用途 | 价值 |
|-----|------|------|
| `user/info` | 获取用户信息 | ⭐⭐⭐⭐⭐ |
| `user/info/batchget` | 批量获取用户信息 | ⭐⭐⭐⭐⭐ |
| `user/get` | 获取关注者列表 | ⭐⭐⭐⭐⭐ |
| `user/info/updateremark` | 设置用户备注名 | ⭐⭐⭐ |

#### 标签管理
| API | 用途 | 价值 |
|-----|------|------|
| `tags/create` | 创建标签 | ⭐⭐⭐⭐ |
| `tags/get` | 获取标签列表 | ⭐⭐⭐⭐ |
| `tags/members/batchtagging` | 批量打标签 | ⭐⭐⭐⭐ |
| `user/tag/get` | 获取标签下粉丝 | ⭐⭐⭐⭐ |

#### 黑名单
| API | 用途 | 价值 |
|-----|------|------|
| `tags/members/getblacklist` | 获取黑名单 | ⭐⭐⭐ |
| `tags/members/batchblacklist` | 拉黑用户 | ⭐⭐⭐ |

---

### 4. 📊 数据统计（很有价值）

#### 用户数据
| API | 用途 | 价值 |
|-----|------|------|
| `datacube/getusersummary` | 用户增减数据 | ⭐⭐⭐⭐⭐ |
| `datacube/getusercumulate` | 累计用户数据 | ⭐⭐⭐⭐⭐ |

#### 图文数据
| API | 用途 | 价值 |
|-----|------|------|
| `datacube/getarticlesummary` | 图文每日数据 | ⭐⭐⭐⭐⭐ |
| `datacube/getarticletotal` | 图文总数据 | ⭐⭐⭐⭐⭐ |
| `datacube/getuserread` | 图文阅读概况 | ⭐⭐⭐⭐⭐ |
| `datacube/getusershare` | 图文转发概况 | ⭐⭐⭐⭐ |
| `datacube/getarticleread` | 发表内容阅读数据 | ⭐⭐⭐⭐⭐ |

#### 消息数据
| API | 用途 | 价值 |
|-----|------|------|
| `datacube/getupstreammsg` | 消息发送概况 | ⭐⭐⭐⭐ |

---

### 5. 🎛️ 自定义菜单

| API | 用途 | 价值 |
|-----|------|------|
| `menu/create` | 创建菜单 | ⭐⭐⭐⭐⭐ |
| `menu/get` | 获取菜单 | ⭐⭐⭐⭐ |
| `menu/delete` | 删除菜单 | ⭐⭐⭐⭐ |
| `menu/addconditional` | 创建个性化菜单 | ⭐⭐⭐⭐ |

---

### 6. 🤖 智能接口（AI 能力）

#### 翻译
| API | 用途 | 价值 |
|-----|------|------|
| `media/voice/translatecontent` | 文本翻译 | ⭐⭐⭐⭐ |

#### 语音识别
| API | 用途 | 价值 |
|-----|------|------|
| `media/voice/addvoicetorecofortext` | 上传语音识别 | ⭐⭐⭐⭐ |
| `media/voice/queryrecoresultfortext` | 获取识别结果 | ⭐⭐⭐⭐ |

#### OCR 识别
| API | 用途 | 价值 |
|-----|------|------|
| `cv/ocr/idcard` | 身份证识别 | ⭐⭐⭐⭐ |
| `cv/ocr/bankcard` | 银行卡识别 | ⭐⭐⭐ |
| `cv/ocr/bizlicense` | 营业执照识别 | ⭐⭐⭐⭐ |
| `cv/ocr/comm` | 通用印刷体识别 | ⭐⭐⭐⭐ |

#### 图像处理
| API | 用途 | 价值 |
|-----|------|------|
| `cv/img/aicrop` | 图片智能裁剪 | ⭐⭐⭐ |
| `cv/img/qrcode` | 二维码识别 | ⭐⭐⭐⭐ |

---

## 🚀 推荐实现的功能

### 第一优先级（已有基础）
- ✅ 草稿管理
- ✅ 发布能力
- ✅ 素材管理

### 第二优先级（推荐添加）
1. **数据统计** - 自动获取阅读数据，分析文章效果
2. **用户管理** - 获取粉丝列表，管理标签
3. **自定义菜单** - 通过 API 创建菜单

### 第三优先级（可选）
1. **客服消息** - 自动回复用户
2. **群发消息** - 定向推送
3. **智能接口** - OCR、翻译等

---

## 💡 实用场景

### 场景 1：自动化运营
```
1. 每天 9:00 自动发布文章
2. 10:00 获取昨日阅读数据
3. 分析哪些文章受欢迎
4. 自动调整内容策略
```

### 场景 2：用户运营
```
1. 获取粉丝列表
2. 按标签分组
3. 针对不同群体推送不同内容
4. 统计每个群体的反馈
```

### 场景 3：智能客服
```
1. 接收用户消息
2. 自动回复（关键词匹配）
3. 转人工客服
4. 记录对话历史
```

---

## 📝 后续可以实现的 Skill

1. **wechat-analytics** - 数据统计
   - 获取文章阅读数据
   - 获取用户增长数据
   - 生成报告

2. **wechat-menu** - 菜单管理
   - 创建自定义菜单
   - 个性化菜单

3. **wechat-user** - 用户管理
   - 获取粉丝列表
   - 标签管理
   - 用户信息查询

4. **wechat-customer-service** - 客服消息
   - 发送客服消息
   - 会话管理

---

*研究完成，可供后续开发参考*
