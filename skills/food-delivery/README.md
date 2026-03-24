# 外卖助手 - 快速开始指南

## 🚀 快速使用

### 1. 基础推荐
```bash
# 推荐3家餐厅（默认）
python scripts/recommend.py

# 预算30元内
python scripts/recommend.py --budget 30

# 指定口味
python scripts/recommend.py --taste 面食

# 随机推荐
python scripts/recommend.py --random

# 根据时间推荐
python scripts/recommend.py --time
```

### 2. 生成链接
```bash
# 生成所有平台链接
python scripts/link_generator.py 黄焖鸡

# 只生成美团链接
python scripts/link_generator.py 黄焖鸡 --platform meituan
```

### 3. 记录订单
```bash
# 添加订单
python scripts/order_tracker.py --add 老乡鸡 "鸡汤,米饭" 25 meituan

# 分析偏好
python scripts/order_tracker.py --analyze

# 查看最近7天订单
python scripts/order_tracker.py --recent 7

# 避免重复（最近3天吃过的）
python scripts/order_tracker.py --avoid 3
```

---

## 🎯 常见场景

### 场景1：不知道吃什么
```bash
python scripts/recommend.py --random
```

### 场景2：预算有限
```bash
python scripts/recommend.py --budget 30
```

### 场景3：想吃特定口味
```bash
python scripts/recommend.py --taste 川菜
```

### 场景4：看看最近吃了啥
```bash
python scripts/order_tracker.py --recent 7
```

---

## 📝 数据文件

- `data/user-preferences.json` - 用户偏好设置
- `data/order-history.json` - 订单历史（自动生成）
- `references/chains.md` - 连锁餐厅数据库
- `references/food-categories.md` - 餐厅分类

---

## 🔄 集成到 OpenClaw

### 方式1：作为 Skill 使用
```bash
# 在 OpenClaw 对话中
"帮我推荐个外卖，预算30"
"中午吃啥？"
"生成黄焖鸡的美团链接"
```

### 方式2：定时提醒
```bash
# 在 OpenClaw cron 中添加
# 每天11:30提醒午餐
openclaw cron add lunch-reminder \
  --schedule "30 11 * * *" \
  --command "python skills/food-delivery/scripts/recommend.py --time"
```

---

## 🌟 示例输出

### 推荐餐厅
```
🍜 推荐餐厅：
1. 老乡鸡 - 中式快餐 (人均25元，评分4.5)
2. 黄焖鸡米饭 - 盖浇饭 (人均22元，评分4.4)
3. 重庆小面 - 面食 (人均18元，评分4.3)
```

### 生成链接
```
🔗 搜索「黄焖鸡」：
- [美团外卖](https://waimai.meituan.com/search?keyword=黄焖鸡)
- [饿了么](https://www.ele.me/search?keyword=黄焖鸡)
- [大众点评](https://www.dianping.com/search?keyword=黄焖鸡)
```

### 订单记录
```
✅ 已记录订单：老乡鸡 - 25元
```

---

## ⚙️ 自定义配置

### 修改用户偏好
编辑 `data/user-preferences.json`：
```json
{
  "taste_preference": ["川菜", "粤菜"],
  "budget_range": [20, 50],
  "avoid": ["香菜"],
  "favorites": [
    {"name": "老乡鸡", "category": "中式快餐"}
  ]
}
```

### 添加餐厅数据
编辑 `references/chains.md`，添加新餐厅信息。

---

**最后更新**：2026-03-21
