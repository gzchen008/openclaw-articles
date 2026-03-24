# 2026-03-20 SOUL.md & USER.md 清理报告

## ✅ 执行的清理操作

### 1️⃣ 创建新文档
- **docs/clawra-selfie-capability.md** (65行)
  - Clawra 人格背景（K-pop 练习生故事）
  - 自拍能力详细说明
  - Selfie 模式（Mirror/Direct）
  - 技术实现细节

### 2️⃣ SOUL.md 精简（125行 → 85行）
**删除内容**:
- ❌ 小J的外貌（用户定制）→ 移到 USER.md
- ❌ 老公后宫选人标准 → 移到 USER.md
- ❌ 冗长的 Clawra Selfie Capability → 移到独立文档

**保留内容**:
- ✅ 角色定义（职能助手）
- ✅ Core Truths（核心价值观）
- ✅ Boundaries（安全边界）
- ✅ Security Checklist（公开内容检查）
- ✅ Vibe（沟通风格）
- ✅ Clawra Selfie 引用（精简版）

### 3️⃣ USER.md 扩展（23行 → 82行）
**新增内容**:
- ✅ WhatsApp 私聊角色设定（详细）
- ✅ 小J 外貌描述（从 SOUL.md 移动）
- ✅ 老公后宫选人标准（从 SOUL.md 移动）
- ✅ 常见场景和边界说明

---

## 📊 清理效果

| 文件 | 清理前 | 清理后 | 变化 |
|------|--------|--------|------|
| SOUL.md | 125 行 | 85 行 | **-32%** |
| USER.md | 23 行 | 82 行 | **+257%** |
| clawra-selfie-capability.md | 0 行 | 65 行 | **新增** |
| **总计** | 148 行 | 232 行 | +84 行 |

---

## 🎯 优化效果

### ✅ 职责更清晰
```
SOUL.md   → AI 人格定义（我是谁）
USER.md   → 用户偏好（我喜欢什么）
Clawra    → 人格扩展（详细能力文档）
```

### ✅ 更易维护
- 用户偏好集中在 USER.md
- AI 人格核心在 SOUL.md
- 详细能力文档独立管理

### ✅ 逻辑更合理
- "后宫选人标准" 明显是用户偏好，不是 AI 人格
- "小J外貌" 是用户定制的偏好，应该在 USER.md
- Clawra 自拍能力是扩展功能，独立文档更清晰

---

## 📋 文档引用关系

```
SOUL.md
  └── 引用 → docs/clawra-selfie-capability.md

USER.md
  └── 定义 → WhatsApp 私聊角色设定
  └── 定义 → 小J 外貌
  └── 定义 → 后宫选人标准
```

---

## 🔄 后续维护建议

### 修改 AI 人格核心
→ 编辑 `SOUL.md`

### 修改用户偏好/私聊角色
→ 编辑 `USER.md`

### 修改 Clawra 自拍能力
→ 编辑 `docs/clawra-selfie-capability.md`

---

**清理完成时间**: 2026-03-20 19:48
**执行方案**: 方案 A（内容重新分配）+ Clawra 独立文档
