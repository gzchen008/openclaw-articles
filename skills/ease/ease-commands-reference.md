# Ease 插件命令参考手册

本手册汇总 Ease 插件内所有可用的 Slash Commands 及其用法、输出与适用场景，帮助你在项目中高效集成与使用。

## 命令概览

| 命令                         | 描述                                          | 对应 Skill |
|----------------------------|---------------------------------------------|-----------|
| `/ease:flow-1-analyze-brd` | 【三阶段-阶段1】分析业务需求文档（BRD），生成领域模型、用例与业务规则 | ease-analysis |
| `/ease:flow-1-analyze-trd` | 【三阶段-阶段1】分析技术类非功能需求（NFR），输出标准化 TRD 文档 | ease-analysis |
| `/ease:flow-2-design`      | 【三阶段-阶段2】对用例进行架构与技术设计，生成框架代码 | ease-architecture |
| `/ease:flow-3-implement`   | 【三阶段-阶段3】基于框架代码完成详细实现            | ease-coding |
| `/ease:analyze-code`       | 分析源代码，生成领域模型、用例与业务规则            | ease-analysis |
| `/ease:generate-tests`     | 为源代码生成单元测试                              | ease-testing |
| `/ease:code-review`        | 代码审查与最佳实践指导                             | ease-coding |
| `/ease:write-docs`         | 编写技术文档（README、API、架构等）                 | ease-arch-documentation |
| `/ease:arch-docs`          | 生成架构文档（系统概览、核心模块、API、数据模型等）  | ease-arch-documentation |
| `/ease:ease-agent`         | 启动结对编程助手                                  | ease-agent（agent） |
| `/ease:helper`             | 解答 Ease 插件的知识问答                          | ease-helper |
| `/ease:async-task`         | 提交任务到云端异步执行                             | async-task |
| `/ease:query-async-task`   | 查询最近 3 天异步任务的云端状态                     | async-task |

---

## 详细命令说明

### 1. /ease:flow-1-analyze-brd

功能：【三阶段流程-阶段1】分析业务需求文档（BRD），生成领域模型、用例与业务规则。

用法：
```bash
/ease:flow-1-analyze-brd [业务需求文档路径]
```

示例：
```bash
/ease:flow-1-analyze-brd doc/requirements/01_calculate_24point_game.md
```

输出：
- `doc/analyze/system-domains.md`：系统领域模型
- `doc/analyze/usecases.md`：业务用例与业务规则

相关 Skill：`ease-analysis`

---

### 2. /ease:flow-1-analyze-trd

功能：【三阶段流程-阶段1】分析技术类非功能需求（NFR），输出标准化 TRD 文档。

适用场景：
- 性能优化：接口响应时间优化、数据库查询优化、缓存策略优化
- 高可用改造：服务集群化、故障自动转移、多活架构
- 安全加固：身份认证升级、数据加密、安全漏洞修复
- 可观测性：日志规范化、监控指标建设、链路追踪
- 技术债清理：代码重构、依赖升级、架构解耦
- 中间件升级：数据库版本升级、消息队列迁移、服务框架升级

用法：
```bash
/ease:flow-1-analyze-trd [技术需求描述]
```

示例：
```bash
/ease:flow-1-analyze-trd 优化数据库查询性能，目标 P99 < 100ms
```

输出：
- `docs/trd/[编号]-[模块名].md`：简洁技术需求描述
- `.eases/trd/[编号]-[模块名]/flow-1-analyze-trd/TRD.md`：完整技术需求文档
- `.eases/trd/[编号]-[模块名]/flow-1-analyze-trd/analysis/`：现状分析、问题分析
- `.eases/trd/[编号]-[模块名]/flow-1-analyze-trd/artifacts/`：方案设计、影响分析

相关 Skill：`ease-analysis`

---

### 3. /ease:flow-2-design

功能：【三阶段流程-阶段2】根据业务用例进行架构与技术设计，生成框架代码。

用法：
```bash
/ease:flow-2-design [用例文档路径]
```

示例：
```bash
/ease:flow-2-design doc/analyze/usecase/order/usecases.md
```

输出（示例范围）：
- Controller 层框架代码
- Action 层框架代码
- Service 层框架代码
- Integration 层框架代码
- Entity/DTO 对象框架
- 完整的代码注释与 TODO 标记

相关 Skill：`ease-architecture`

---

### 4. /ease:flow-3-implement

功能：【三阶段流程-阶段3】基于框架代码完成详细实现。

用法：
```bash
# 实现指定文件的代码
/ease:flow-3-implement [file_path]

# 实现整个模块的代码
/ease:flow-3-implement [module_path]

# 实现所有待完成的代码
/ease:flow-3-implement
```

示例：
```bash
/ease:flow-3-implement
```

输出：
- 需求相关的业务代码
- 对应的单元测试代码

相关 Skill：`ease-coding`

---

### 5. /ease:generate-tests

功能：为源代码生成单元测试。

用法：
```bash
# 为指定文件生成测试
/ease:generate-tests [源代码文件路径]

# 为整个项目生成测试
/ease:generate-tests
```

示例：
```bash
/ease:generate-tests src/main/java/com/example/UserService.java
```

特性：
- 遵循 FIRST 原则（Fast、Independent、Repeatable、Self-validating、Timely）
- 覆盖正常场景、边界条件与异常场景
- 自动检查并改进代码可测试性
- 生成 Mock 与 Stub

相关 Skill：`ease-testing`

---

### 6. /ease:code-review

功能：进行代码审查并给出编程最佳实践指导。

用法：
```bash
# 审查指定文件
/ease:code-review [文件路径]

# 实现新功能
/ease:code-review 实现 [功能描述]

# 重构代码
/ease:code-review 重构 [文件路径] [改进目标]
```

示例：
```bash
/ease:code-review src/utils/calculator.ts
/ease:code-review 实现用户认证功能
/ease:code-review 重构 auth.ts 提高可测试性
```

审查维度：
- ✅ 正确性：逻辑、边界条件、错误处理
- 🔒 安全性：SQL 注入、XSS、权限控制
- ⚡ 性能：算法复杂度、查询优化
- 📖 可读性：命名、结构、注释
- 🧪 可测试性：依赖注入、单一职责
- 🔧 可维护性：SOLID 原则、DRY

相关 Skill：`ease-coding`

---

### 7. /ease:write-docs

功能：编写各类技术文档。

用法：
```bash
/ease:write-docs [文档类型] [可选参数]
```

支持的文档类型：

| 文档类型   | 命令                           | 输出位置                 |
|-----------|--------------------------------|--------------------------|
| README    | `/ease:write-docs readme`      | `README.md`             |
| API 文档  | `/ease:write-docs api`         | `docs/API.md`           |
| 架构文档  | `/ease:write-docs architecture`| `docs/ARCHITECTURE.md`  |
| 变更日志  | `/ease:write-docs changelog`   | `CHANGELOG.md`          |
| 贡献指南  | `/ease:write-docs contributing`| `CONTRIBUTING.md`       |
| 开发指南  | `/ease:write-docs development` | `docs/DEVELOPMENT.md`   |
| 部署文档  | `/ease:write-docs deployment`  | `docs/DEPLOYMENT.md`    |

示例：
```bash
/ease:write-docs readme
/ease:write-docs api /users
/ease:write-docs architecture
```

文档原则：
- 📝 清晰性：语言简洁直观
- ✅ 完整性：覆盖核心信息
- 🎯 准确性：示例可运行、可验证
- 🔧 可维护性：文档随代码迭代
- 👥 用户导向：站在读者视角

相关 Skill：`ease-arch-documentation`

---

### 8. /ease:arch-docs

功能：生成架构文档（系统概览、核心模块、API 接口、数据模型、配置管理、工具库）。

用法：
```bash
/ease:arch-docs [文档类型]
```

支持的文档类型：

| 文档类型         | 命令参数                            | 输出文件                          |
|----------------|-----------------------------------|-----------------------------------|
| 所有文档（默认）  | 无参数                              | `docs/system/` 目录下全部 6 份文档  |
| 系统概览        | `system-overview`                  | `docs/system/01_SYSTEM_OVERVIEW.md` |
| 核心模块        | `core-modules`                     | `docs/system/02_CORE_MODULES.md` |
| API 接口        | `api-interface`                    | `docs/system/03_API_INTERFACE.md` |
| 数据模型        | `data-model`                       | `docs/system/04_DATA_MODEL.md` |
| 配置管理        | `config-management`                | `docs/system/05_CONFIG_MANAGEMENT.md` |
| 工具库          | `utils-libraries`                  | `docs/system/06_UTILS_LIBRARIES.md` |

示例：
```bash
# 生成所有架构文档
/ease:arch-docs

# 生成系统概览文档
/ease:arch-docs system-overview

# 生成 API 接口文档
/ease:arch-docs api-interface
```

特性：
- 📊 证据驱动：每个结论引用代码证据 `来源: <path>:<line> (symbol)`
- 🔄 增量更新：基于 Git 差异只更新受影响的文档
- 📈 质量门禁：格式、完整性、一致性三重检查
- 🇨🇳 中文输出：所有文档使用中文，图表使用 Mermaid 语法

相关 Skill：`ease-arch-documentation`

---

### 9. /ease:ease-agent

功能：启动结对编程助手。

用法：
```bash
/ease:ease-agent [任务描述]
```

示例：
```bash
/ease:ease-agent 帮我重构这个函数，提高可读性
/ease:ease-agent 分析 src/main/java/com/example/UserService.java
/ease:ease-agent 我需要设计一个用户认证系统
```

专长领域：
- 💻 新功能/新代码实现
- 🔄 现有代码重构
- 🐛 问题定位与调试
- 🏗️ 架构设计决策
- 📚 学习新技术
- 👀 代码审查

相关 Agent：`ease-agent`

---

### 10. /ease:helper

功能：解答 Ease CC Plugins 的知识问答，帮助用户了解各种 Skills、Commands、工作流程的使用方法。

用法：
```bash
/ease:helper [问题]
```

示例：
```bash
/ease:helper ease-analysis skill 是做什么的？
/ease:helper 有哪些可用的 ease 命令？
/ease:helper Ease 全流程是什么？
/ease:helper 新项目如何接入 Ease？
/ease:helper constitution.md 文件应该放在哪里？
```

适用场景：
- 🔍 了解某个 Skill 的功能和使用方法
- 📖 了解某个 Command 的用法和参数
- 🔄 了解 Ease 的工作流程和最佳实践
- 🛠️ 排查使用 Ease 插件时遇到的问题
- 📚 学习 DDD、Clean Architecture 等概念

相关 Skill：`ease-helper`

---

### 11. /ease:async-task

功能：将任务提交到云端后台异步执行。适用于需要长时间运行、后台处理、排队执行等场景。

用法：
```bash
/ease:async-task [任务描述]
```

#### 显式触发（推荐）

| 触发方式 | 示例 |
|----------|------|
| `--async` 标记 | `--async 分析整个项目代码` |
| `[@ease]` 标记 | `[@ease] 生成性能优化报告` |
| `提交后台:` 前缀 | `提交后台：批量数据迁移` |
| `异步执行:` 前缀 | `异步执行：全量代码审查` |
| `云端处理:` 前缀 | `云端处理：运行回归测试` |

#### 意图识别触发

当用户请求**同时满足**以下条件时触发：
1. 包含异步相关关键词（后台任务、异步执行、云端处理、批量处理、长时间运行等）
2. 包含任务意图动词（分析、生成、处理、审查、重构、优化、迁移等）
3. 排除误命中场景（普通代码问题、日常开发任务、简单查询等）

示例：
```bash
# 显式触发（推荐）
/ease:async-task --async 添加用户导出功能，支持导出 Excel 格式
/ease:async-task [@ease] 分析项目代码，生成性能优化报告

# 意图识别触发
/ease:async-task 提交后台：批量处理用户数据迁移
/ease:async-task 异步执行：全量代码审查并生成报告
/ease:async-task 云端处理：运行完整的回归测试套件
```

**典型场景**：
- 需要长时间运行的分析任务（全项目代码分析、依赖分析）
- 大批量数据处理（数据迁移、批量转换）
- 完整的测试套件执行（回归测试、集成测试）
- 深度代码审查与优化（性能分析、安全扫描）
- 大规模文档生成（API 文档、架构文档）
- 复杂的架构重构（模块拆分、技术栈迁移）

**防误命中**：
- "异步函数报错了" → 使用 `ease:systematic-debugging`
- "写个异步方法" → 直接实现
- "什么是异步" → 使用 `ease:helper`

特性：
- **透明化底层实现**：用户感知的是"任务已提交到云端后台"，不需要了解 GitHub Issue 的存在
- **智能触发**：支持显式标记和意图识别两种触发方式
- **防误命中**：内置规则避免与普通代码问题混淆
- 自动获取系统用户名和项目名
- 智能判断任务类型并设置 `issue_type`（5=任务，6=需求，7=缺陷）
- 生成标准格式的标题：`[feature]`/`[task]`/`[bug]`
- 生成结构化的描述内容
- 自动提交到云端任务队列

**任务类型映射**：
| 用户输入类型 | issue_type | 标题前缀 |
|------------|-----------|---------|
| 新功能请求/改进建议 | 6 | [feature] |
| 技术任务/重构/优化 | 5 | [task] |
| Bug 报告/问题修复 | 7 | [bug] |

**用户反馈格式**：
```
✅ 任务已成功提交到云端后台

任务识别码: <ABC123>
任务 ID: #123
追踪链接: <url>

状态: 已排队，等待云端处理
本地记录: .eases/ease_tasks/<YYYYMMDDHHMMSS>-<ABC123>.json
```

相关 Skill：`async-task`

---

### 12. /ease:query-async-task

功能：从项目内最近 3 天的本地异步任务记录中选择目标任务，并查询云端最新状态。

用法：
```bash
/ease:query-async-task
```

特性：
- 从 `.eases/ease_tasks/` 读取本地任务索引
- 只展示最近 3 天且带 6 位识别码的记录
- 通过编号选择任务，避免输入歧义
- 调用查询接口并读取 `data.status_description`
- 以更友好、专业的中文反馈任务最新进展

典型场景：
- 刚通过 `/ease:async-task` 提交了耗时任务，想跟进当前处理进展
- 想从最近的异步任务里快速选一个查看状态
- 希望把“任务提交”和“结果跟进”串成闭环

查询结果示例：
```
✅ 已为你查询到这条异步任务的最新进展

- 任务识别码：ABC123
- 任务标题：[feature] <ABC123> 添加用户导出功能
- 当前状态：正在排队，预计稍后开始执行
```

相关 Skill：`async-task`

---

## 工作流示例

### 场景 1：从需求到代码实现（业务需求）

```bash
# 1. 分析业务需求，生成领域模型和用例
/ease:flow-1-analyze-brd doc/requirements/user-management.md

# 2. 根据用例进行架构设计并生成框架代码
/ease:flow-2-design doc/analyze/usecase/user/usecases.md

# 3. 基于框架代码实现业务逻辑
/ease:flow-3-implement

# 4. 生成单元测试
/ease:generate-tests src/main/java/com/example/UserService.java

# 5. 代码审查
/ease:code-review src/main/java/com/example/UserService.java

# 6. 编写文档
/ease:write-docs api
```

### 场景 1b：从技术需求到代码实现（NFR）

```bash
# 1. 分析技术需求，生成 TRD 文档
/ease:flow-1-analyze-trd 优化数据库查询性能，目标 P99 < 100ms

# 2. 根据技术方案进行架构设计
/ease:flow-2-design .eases/trd/001-performance-optimization/flow-1-analyze-trd

# 3. 基于设计实现技术改进
/ease:flow-3-implement

# 4. 代码审查
/ease:code-review src/main/java/com/example/UserService.java
```

### 场景 2：代码质量改进

```bash
# 1. 审查现有代码
/ease:code-review src/services/payment.ts

# 2. 重构代码
/ease:ease-agent 重构 payment.ts，提高可维护性

# 3. 生成测试
/ease:generate-tests src/services/payment.ts

# 4. 更新文档
/ease:write-docs api /payment
```

---

## 注意事项

1. 重启 CLI：添加新命令后需重启 Claude Code CLI 会话方可生效
2. UTF-8 编码：所有生成文件统一使用 UTF-8 字符集
3. 项目规范：Commands 遵循项目 `CLAUDE.md` 中定义的规范
4. 任务跟踪：所有命令均使用 TodoWrite 工具记录执行进度
5. 并行使用：同一项目中可组合并行使用多个命令

---

## 文件位置

- Commands 目录：`plugins/ease/commands/`
- Skills 目录：`plugins/ease/skills/`
- Agents 目录：`plugins/ease/agents/`
- Plugin 配置：`plugins/ease/.claude-plugin/plugin.json`

---

## 更新日志

### v1.0.2（2026-01-08）
- ✨ 新增 `/ease:helper` 命令，用于解答 Ease 插件知识问答
- 📚 新增 `ease-helper` skill，提供插件使用指南和知识库

### v1.0.1（2025-01-23）
- ✨ 新增 7 个 Slash Commands
- 📝 为所有 Skills 创建对应命令
- 📚 完成命令参考手册

### v1.0.0
- 🎉 初始版本
- ✅ 基础 Skills 与 Commands
