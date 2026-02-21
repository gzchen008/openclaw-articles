---
name: wechat-user
description: |
  微信公众号用户管理能力。支持获取粉丝列表、用户信息、标签管理等。
  
  触发场景：
  - 用户要求获取公众号粉丝信息
  - 需要管理用户标签
  - 分析用户数据
  
  前置条件：
  - 已认证的公众号
  - 已配置 WECHAT_APPID 和 WECHAT_SECRET 环境变量
---

# 微信公众号用户管理

## 快速开始

### 获取粉丝列表

```bash
python scripts/wechat_user.py fans
```

### 获取用户信息

```bash
python scripts/wechat_user.py info OPENID
```

### 标签管理

```bash
# 创建标签
python scripts/wechat_user.py tag create "VIP用户"

# 获取标签列表
python scripts/wechat_user.py tag list

# 为用户打标签
python scripts/wechat_user.py tag batch-tag --tag-id 100 --openids OPENID1,OPENID2
```

## 主要功能

### 1. 粉丝管理
- 获取关注者列表
- 批量获取用户信息
- 设置用户备注名

### 2. 标签管理
- 创建/查询/删除标签
- 批量为用户打标签
- 获取标签下的粉丝列表

### 3. 黑名单管理
- 获取黑名单列表
- 拉黑/取消拉黑用户

## API 说明

详细 API 文档见 [references/api-reference.md](references/api-reference.md)

## 注意事项

- 用户信息需要用户关注公众号后才能获取
- 每个用户对每个公众号的 OpenID 是唯一的
- 标签最多创建 100 个
