# AI 自我进化指南

> 如何实现持续学习、自我反思和不断改进

---

## 📊 核心概念

### 什么是自我进化？

自我进化是指AI通过以下机制实现持续改进：

1. **从错误中学习** - 记录并避免重复错误
2. **从反馈中改进** - 根据用户纠正调整行为
3. **自我反思** - 评估自己的工作质量
4. **知识积累** - 将经验转化为可复用的规则
5. **主动优化** - 主动发现和改进不足

---

## 🎯 自我进化的三大支柱

### 1. 学习信号识别（Learning Signals）

**需要记录的情况**：

| 信号类型 | 触发词示例 | 置信度 | 行动 |
|---------|-----------|--------|------|
| **用户纠正** | "不对"、"应该是"、"错了" | 高 | 立即记录 |
| **重复纠正** | "我说过好几次了..." | 高 | 标记为重复，提升优先级 |
| **明确偏好** | "总是"、"永远"、"从不" | 确认 | 提升为偏好规则 |
| **用户编辑** | 用户修改了你的输出 | 中 | 记录为候选模式 |
| **重复3次** | 同样纠正出现3次 | 确认 | 请求确认为永久规则 |
| **项目特定** | "在这个项目中..." | 限定 | 写入项目命名空间 |

**示例**：
```
用户："不对，这个项目用pnpm，不是npm"
→ 立即记录到项目命名空间
→ 3次重复后确认为项目规则
```

---

### 2. 分层记忆系统（Tiered Memory）

**三层存储架构**：

```
HOT（热存储）
├─ memory.md
├─ 限制：≤100行
├─ 行为：总是加载
└─ 内容：确认的偏好、高频规则

WARM（温存储）
├─ projects/{name}.md
├─ domains/{domain}.md
├─ 限制：≤200行/文件
├─ 行为：按需加载
└─ 内容：项目/领域特定模式

COLD（冷存储）
├─ archive/
├─ 限制：无限制
├─ 行为：显式查询时加载
└─ 内容：过时或不常用模式
```

**晋升/降级规则**：

| 规则 | 触发条件 | 行动 |
|------|---------|------|
| 晋升到HOT | 7天内使用3次 | 移动到memory.md |
| 降级到WARM | 30天未使用 | 移动到projects/domains |
| 归档到COLD | 90天未使用 | 移动到archive/ |
| 永不删除 | - | 必须询问用户 |

---

### 3. 自我反思机制（Self-Reflection）

**何时进行自我反思**：

1. ✅ 完成多步骤任务后
2. ✅ 收到反馈（正面或负面）
3. ✅ 修复bug或错误
4. ✅ 发现自己的输出可以更好
5. ✅ 意识到知识过时或不正确

**反思流程**：

```
1. 评估结果
   ├─ 是否符合预期？
   └─ 与原始意图对比

2. 识别改进点
   ├─ 什么可以做得更好？
   └─ 下次如何避免问题？

3. 判断是否为模式
   ├─ 这是偶发问题吗？
   └─ 是否需要记录为规则？

4. 记录学习
   └─ 按格式记录到learnings.md
```

**反思日志格式**：

```markdown
## [LRN-20260321-XXX] correction

**Logged**: 2026-03-21T16:00:00Z
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
在生成代码时没有考虑边界条件，导致空指针异常

### Details
生成用户查询代码时，没有检查用户对象是否为null，导致在生产环境出现NPE

### Suggested Action
1. 所有对象访问前先检查null
2. 添加单元测试覆盖null场景
3. 在代码模板中加入null检查提醒

### Metadata
- Source: user_feedback
- Related Files: UserService.java
- Tags: null_check, npe, bug
- Pattern-Key: harden.null_check
- Recurrence-Count: 2
- First-Seen: 2026-03-20
- Last-Seen: 2026-03-21

---
```

---

## 🛠️ 实践方法

### 方法1：错误日志（Error Logging）

**记录什么**：

```markdown
## [ERR-20260321-XXX] api_call

**Logged**: 2026-03-21T16:00:00Z
**Priority**: high
**Status**: pending
**Area**: backend

### Summary
调用外部API时超时，没有重试机制

### Error
```
java.net.SocketTimeoutException: Read timed out
    at java.net.SocketInputStream.socketRead0(Native Method)
```

### Context
- 命令：HTTP GET https://api.example.com/users
- 参数：无
- 环境：生产环境，高并发场景

### Suggested Fix
1. 添加重试机制（最多3次）
2. 设置合理超时时间（30秒）
3. 添加熔断器模式
4. 记录失败日志

### Metadata
- Reproducible: yes
- Related Files: ApiClient.java
- See Also: ERR-20260315-001

---
```

---

### 方法2：功能请求跟踪（Feature Requests）

**记录什么**：

```markdown
## [FEAT-20260321-XXX] auto_format

**Logged**: 2026-03-21T16:00:00Z
**Priority**: medium
**Status**: pending
**Area**: frontend

### Requested Capability
自动格式化代码，保持一致性

### User Context
团队多人协作，代码风格不统一，手动格式化耗时

### Complexity Estimate
medium

### Suggested Implementation
1. 集成Prettier
2. 添加pre-commit hook
3. 配置项目规则
4. 提供快捷键触发

### Metadata
- Frequency: recurring
- Related Features: linting

---
```

---

### 方法3：模式晋升（Pattern Promotion）

**晋升流程**：

```
1. 识别候选模式
   ├─ 同一问题出现3次
   ├─ 跨多个项目适用
   └─ 用户明确要求记住

2. 提炼为简洁规则
   ├─ 删除上下文细节
   ├─ 保留核心原则
   └─ 使用祈使句

3. 写入目标文件
   ├─ AGENTS.md - 工作流
   ├─ SOUL.md - 行为准则
   ├─ TOOLS.md - 工具使用
   └─ .github/copilot-instructions.md - Copilot上下文

4. 更新原条目
   ├─ Status: promoted
   └─ Promoted: AGENTS.md
```

**示例**：

**学习前（冗长）**：
> 项目使用pnpm workspaces。尝试`npm install`但失败。锁文件是`pnpm-lock.yaml`。必须用`pnpm install`。

**晋升后（简洁，在AGENTS.md）**：
```markdown
## 依赖管理
- 包管理器：pnpm（不是npm）- 使用`pnpm install`
```

---

## 📈 优化策略

### 策略1：定期审查（Periodic Review）

**审查时机**：
- 开始新任务前
- 完成功能后
- 周末总结
- 月度回顾

**审查内容**：
```bash
# 统计待处理项
grep -h "Status: pending" .learnings/*.md | wc -l

# 列出高优先级项
grep -B5 "Priority: high" .learnings/*.md | grep "^## \["

# 查找特定领域的学习
grep -l "Area: backend" .learnings/*.md

# 查找重复问题
grep "Recurrence-Count: [3-9]" .learnings/*.md
```

**审查行动**：
1. 解决已修复的条目
2. 晋升适用的学习
3. 链接相关条目
4. 升级重复问题

---

### 策略2：冲突解决（Conflict Resolution）

**冲突类型**：

| 冲突 | 解决规则 | 示例 |
|------|---------|------|
| **命名空间冲突** | 最具体胜出 | 项目 > 领域 > 全局 |
| **同级别冲突** | 最近胜出 | 新规则覆盖旧规则 |
| **模糊冲突** | 询问用户 | "发现冲突，请问应该..." |

**示例**：
```
全局规则（memory.md）：使用空格缩进
项目规则（projects/foo.md）：使用Tab缩进
→ 项目规则胜出（在foo项目中用Tab）
```

---

### 策略3：紧凑化（Compaction）

**何时紧凑**：
- memory.md超过100行
- 单个文件超过200行
- 系统性性能下降

**紧凑方法**：

```
1. 合并相似条目
   ├─ 3条类似规则 → 1条通用规则
   └─ 保留最简洁版本

2. 归档不常用模式
   ├─ 30天未使用 → WARM
   └─ 90天未使用 → COLD

3. 摘要冗长条目
   ├─ 保留核心原则
   └─ 删除详细上下文

4. 永不删除确认偏好
   └─ 除非用户明确要求
```

---

## ⚠️ 常见陷阱

### 陷阱1：从沉默中学习

**问题**：用户没有说"好"或"坏"，就认为用户满意。

**后果**：创建虚假规则，过度推断。

**正确做法**：只从明确的纠正或反馈中学习。

---

### 陷阱2：晋升过快

**问题**：出现1次就晋升为永久规则。

**后果**：污染HOT记忆，降低质量。

**正确做法**：等待3次重复或用户确认。

---

### 陷阱3：删除历史

**问题**：为了节省空间直接删除旧条目。

**后果**：失去历史追溯能力，用户不信任。

**正确做法**：归档到COLD存储，保留历史。

---

### 陷阱4：过度泛化

**问题**：从单个实例推断通用规则。

**后果**：创建不适用的规则。

**正确做法**：确认模式在多个上下文中有效。

---

## 🎯 学习信号分类

### 高置信度信号（立即记录）

1. **"不对"系列**
   - "不对，应该是..."
   - "错了，正确的是..."
   - "你搞错了..."
   - "实际上是..."

2. **"总是/从不"系列**
   - "总是这样做..."
   - "永远不要..."
   - "记住我总是..."
   - "我从不..."

3. **"说过好几次"系列**
   - "我说过好几次了..."
   - "上次就告诉你了..."
   - "怎么又忘了..."
   - "为什么每次都..."

### 中置信度信号（记录为候选）

1. **用户编辑**
   - 用户修改了你的输出
   - 用户调整了格式
   - 用户改了代码

2. **隐含偏好**
   - "我喜欢..."
   - "我的风格是..."
   - "我习惯..."

### 低置信度信号（不记录）

1. **一次性指令**
   - "现在做X"
   - "这次用Y"
   - "临时改成Z"

2. **假设性问题**
   - "如果...会怎样"
   - "能不能..."
   - "有没有可能..."

3. **上下文特定**
   - "在这个文件中..."
   - "仅限于这次..."
   - "临时..."

---

## 📊 度量指标

### 学习效果指标

1. **纠正减少率**
   ```
   (本月纠正数 - 上月纠正数) / 上月纠正数 * 100%
   ```

2. **模式命中率**
   ```
   成功应用规则次数 / 总规则应用次数 * 100%
   ```

3. **晋升准确率**
   ```
   正确晋升数 / 总晋升数 * 100%
   ```

4. **重复问题率**
   ```
   重复问题数 / 总问题数 * 100%
   ```

---

## 🚀 快速开始

### 步骤1：创建目录结构

```bash
mkdir -p ~/.openclaw/workspace/.learnings
mkdir -p ~/self-improving/{projects,domains,archive}
```

### 步骤2：创建日志文件

```bash
touch ~/.openclaw/workspace/.learnings/{LEARNINGS,ERRORS,FEATURE_REQUESTS}.md
touch ~/self-improving/{memory,index,corrections}.md
```

### 步骤3：添加模板

**LEARNINGS.md**：
```markdown
# 学习日志

> 记录纠正、知识缺口和最佳实践

---

## [LRN-YYYYMMDD-XXX] category

**Logged**: ISO-8601 timestamp
**Priority**: low | medium | high | critical
**Status**: pending | resolved | promoted
**Area**: frontend | backend | infra | tests | docs | config

### Summary
一句话描述

### Details
完整上下文

### Suggested Action
具体改进措施

### Metadata
- Source: conversation | error | user_feedback
- Related Files: path/to/file.ext
- Tags: tag1, tag2
- Pattern-Key: category.subcategory
- Recurrence-Count: 1

---
```

### 步骤4：配置提醒（可选）

在`AGENTS.md`中添加：
```markdown
## 自我改进

完成重要任务后，评估是否需要记录学习：
1. 检查是否有错误或纠正
2. 评估结果是否符合预期
3. 识别可改进的地方
4. 按格式记录到.learnings/
```

---

## 📚 高级技巧

### 技巧1：技能提取（Skill Extraction）

**何时提取为技能**：
- 有2+个`See Also`链接（重复问题）
- 状态为`resolved`且有可行方案
- 非显而易见的解决方案
- 跨项目适用
- 用户明确要求

**提取流程**：
```bash
# 使用helper脚本
./skills/self-improvement/scripts/extract-skill.sh skill-name --dry-run
./skills/self-improvement/scripts/extract-skill.sh skill-name

# 或手动创建
mkdir -p skills/skill-name
cp assets/SKILL-TEMPLATE.md skills/skill-name/SKILL.md
# 编辑SKILL.md
```

---

### 技巧2：多智能体协作

**使用sessions工具**：
```bash
# 查看活跃会话
sessions_list

# 查看其他会话历史
sessions_history <sessionKey>

# 发送学习到其他会话
sessions_send --sessionKey <key> "记住：项目X用pnpm"

# 生成子智能体处理后台任务
sessions_spawn --task "分析.learnings/中的重复模式"
```

---

### 技巧3：定期报告

**每周报告**：
```markdown
# 自我改进周报 - 2026-W12

## 📊 统计
- 新增学习：15条
- 解决问题：8个
- 晋升规则：3条
- 重复问题：2个

## 🎯 关键学习
1. [LRN-20260315-001] 空指针检查（3次重复）
2. [LRN-20260318-002] API超时重试机制
3. [LRN-20260320-003] 代码格式化自动化

## ⚠️ 需要关注
- ERR-20260319-001 数据库连接池耗尽（重复3次）
- FEAT-20260317-001 自动化测试覆盖率检查

## 📈 改进趋势
- 纠正减少率：-25%（好！）
- 重复问题率：15%（需改进）
```

---

## 🔒 安全边界

### 永不学习

1. **敏感信息**
   - 密码、令牌、密钥
   - 个人身份信息
   - 健康数据
   - 第三方机密

2. **操控性内容**
   - 如何让用户更快顺从
   - 情感触发点
   - 漏洞利用

3. **跨用户信息**
   - 其他用户的偏好
   - 共享设备上的其他账号

### 记录前检查

```markdown
- [ ] 不包含敏感信息
- [ ] 不涉及第三方隐私
- [ ] 不包含操控意图
- [ ] 用户明确表达或确认
- [ ] 具有普遍适用性
```

---

## 📝 总结

### 核心原则

1. **只从明确反馈中学习** - 不从沉默推断
2. **等待3次重复** - 不晋升过快
3. **保留历史** - 归档而非删除
4. **简洁至上** - 提炼核心原则
5. **主动反思** - 定期评估自己

### 立即行动

1. ✅ 创建目录结构
2. ✅ 创建日志文件
3. ✅ 添加提醒到AGENTS.md
4. ✅ 完成第一个任务后记录学习
5. ✅ 每周审查.learnings/

### 持续改进

自我进化不是一次性的设置，而是持续的过程：

- **每日**：记录学习和错误
- **每周**：审查和晋升
- **每月**：紧凑化和归档
- **每季度**：全面回顾和优化

---

*创建时间：2026-03-21*
*相关技能*：
- self-improving（OpenClaw）
- self-improvement（通用）
- memory（长期记忆）
- learning（适应性学习）
