---
name: wechat-menu
description: |
  微信公众号自定义菜单管理能力。支持创建、查询、删除自定义菜单。
  
  触发场景：
  - 用户要求创建或修改公众号菜单
  - 需要查看当前菜单配置
  - 动态生成菜单
  
  前置条件：
  - 已认证的公众号
  - 已配置 WECHAT_APPID 和 WECHAT_SECRET 环境变量
---

# 微信公众号菜单管理

## 快速开始

### 查看当前菜单

```bash
python scripts/wechat_menu.py get
```

### 创建菜单

```bash
# 从 JSON 文件创建
python scripts/wechat_menu.py create menu.json

# 直接创建简单菜单
python scripts/wechat_menu.py quick-create \
  --btn1 "首页|https://example.com" \
  --btn2 "关于我们|https://example.com/about"
```

### 删除菜单

```bash
python scripts/wechat_menu.py delete
```

## 菜单格式

### JSON 格式示例

```json
{
  "button": [
    {
      "type": "view",
      "name": "首页",
      "url": "https://example.com"
    },
    {
      "name": "更多",
      "sub_button": [
        {
          "type": "view",
          "name": "关于我们",
          "url": "https://example.com/about"
        },
        {
          "type": "click",
          "name": "联系客服",
          "key": "CONTACT_SERVICE"
        }
      ]
    }
  ]
}
```

### 按钮类型

| 类型 | 说明 | 必填字段 |
|------|------|---------|
| click | 点击推事件 | name, key |
| view | 跳转URL | name, url |
| scancode_push | 扫码推事件 | name, key |
| scancode_waitmsg | 扫码带提示 | name, key |
| pic_sysphoto | 系统拍照发图 | name, key |
| pic_photo_or_album | 拍照或者相册 | name, key |
| location_select | 发送位置 | name, key |
| media_id | 下发消息 | name, media_id |
| view_limited | 跳转图文消息 | name, media_id |

## 注意事项

- 最多 3 个一级菜单，每个一级菜单最多 5 个二级菜单
- 菜单名称最长 16 个字节
- 创建后 24 小时内对所有用户生效
