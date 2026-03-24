---
description: 一键执行完整的 SDD 流程，支持从 docs/domains 目录自动映射到 eases 目录并执行 需求规范 → 需求澄清 → 技术计划 → 任务分解 → 一致性分析 → 执行实现 全流程
skills: ease-spec
scripts:
  sh: scripts/bash/check-prerequisites.sh --json --paths-only
  ps: scripts/powershell/check-prerequisites.ps1 -Json -PathsOnly
---

## 用户输入

```text
$ARGUMENTS
```

在继续之前（如不为空），必须优先考虑用户输入中的目录与标志位。

建议输入格式（自由文本也可）：

```text
<FEATURE_DOC_DIR> [--from-docs] [--with-analyze] [--resume] [--dry-run] [--force-specify] [--desc "功能描述……"]
```

- **<FEATURE_DOC_DIR>**：特性文档目录
  - `docs/domains/<module_name>/`：来自 ease commands 的输出目录（按领域模块组织，自动映射到 .eases）
  - `.eases/<编号-短名>/<command>/`：已存在的 ease-spec 规范目录（按命令隔离）
  - `.` 或省略：自动通过 `{SCRIPT}` 解析当前分支/环境对应的目录
- **--from-docs**：指定输入来自 docs/domains 目录，需要自动映射到 eases
- **--with-analyze**：插入可选的参考 reference/一致性分析.md 阶段
- **--resume**：断点续跑；已就绪/存在的阶段自动跳过
- **--dry-run**：只输出即将执行的阶段与关键动作，不实际写入
- **--force-specify**：即使存在 spec.md 也重新运行 specify
- **--desc**：当需要从 0→1 创建规范时提供"功能描述"

---

## 首次使用必读（不可协商）

> ⚠️ **强制要求**：对于第一次使用 ease-spec 技能的项目，必须优先完成以下初始化工作：

### 1. 检查/创建 constitution.md

```bash
# 检查 /memory/constitution.md 是否存在
if [ ! -f "memory/constitution.md" ]; then
    echo "❌ 错误：未找到 /memory/constitution.md"
    echo "请先执行 reference/项目宪章.md 创建项目宪章"
    # 参考 reference/项目宪章.md 执行创建
    exit 1
fi
```

> **原则**：没有 constitution.md 的项目，不允许执行后续流程。

### 2. 创建必要目录

```bash
mkdir -p memory
mkdir -p docs/domains
mkdir -p .eases
```

---

## 目标

当用户仅给出"相关文档目录"时，一键自动执行完整的 SDD 流程：

1. **环境检查**：确保 constitution.md 存在
2. **目录映射**（如果 --from-docs）：docs/domains/[module_name]/ → .eases/[编号]-[功能名]/[command]/
3. **规范创建**：参考 reference/创建需求规范.md（整合 docs 内容）
4. **需求澄清**：参考 reference/需求澄清.md（如果需要）
5. **技术计划**：参考 reference/制定技术计划.md
6. **任务分解**：参考 reference/生成任务列表.md
7. **一致性分析**：参考 reference/一致性分析.md（可选）
8. **实现执行**：参考 reference/执行实现.md

---

## 核心：docs/domains → eases 映射机制

### 映射表

| Ease Command | Docs 输出 | 映射到 Eases |
|--------------|-----------|--------------|
| /ease:flow-1-analyze-brd | docs/domains/[编号]-[module_name]/analyze-brd-output.md（整体摘要）<br>+ docs/domains/[编号]-[module_name]/usecases/[编号]-[subdomain]/uc-[编号]-[usecase].md（具体用例，带编号） | .eases/[编号]-[功能名]/flow-1-analyze-brd/spec.md |
| /ease:flow-1-analyze-trd | docs/trd/[编号]-[module_name]/TRD.md（技术需求文档）<br>+ docs/trd/[编号]-[module_name]/analysis/<br>+ docs/trd/[编号]-[module_name]/artifacts/ | .eases/[编号]-[功能名]/flow-1-analyze-trd/spec.md |
| /ease:analyze-code | docs/domains/[编号]-[module_name]/analyze-code-output.md | .eases/[编号]-[功能名]/analyze-code/spec.md |
| /ease:flow-2-design | docs/domains/[编号]-[module_name]/design-output.md<br>+ docs/domains/[编号]-[module_name]/architecture/<br>+ docs/domains/[编号]-[module_name]/design/ | .eases/[编号]-[功能名]/flow-2-design/spec.md |
| /ease:flow-3-implement | 代码实现总结 | .eases/[编号]-[功能名]/flow-3-implement/spec.md |

### 编号规则

> ⚠️ **重要**：所有目录和文件都必须带有三位递增编号。

- **新增 domain**：扫描 `docs/domains/` 获取最大编号 +1
- **新增 subdomain**：扫描 `usecases/` 获取最大编号 +1
- **新增 usecase**：扫描 subdomain 目录获取最大编号 +1

### 自动映射逻辑

1. **检查 constitution.md**：
   - 如果 `/memory/constitution.md` 不存在，中止并提示先创建

2. **检测输入类型**：
   - 如果输入路径包含 `docs/domains/`，启用映射模式
   - 如果输入路径包含 `.eases/`，直接处理

3. **创建 eases 目录**（按命令隔离）：
   ```bash
   # docs/domains/001-user-management → .eases/001-user-auth/[command]/
   # 实际映射：docs/domains/[编号]-[module_name]/ → .eases/[编号]-[功能名]/[command]/
   mkdir -p .eases/001-user-auth/{flow-1-analyze-brd,analyze-code,flow-2-design,flow-3-implement}
   mkdir -p .eases/001-user-auth/flow-1-analyze-brd/checklists
   mkdir -p .eases/001-user-auth/contracts
   ```

4. **内容整合**：
   - 读取 docs/domains 目录下所有 .md 文件
   - 按映射表提取关键内容
   - 生成初始的 spec.md 到对应的命令目录

---

## 详细流程

### 1. 解析输入与环境

```bash
# 示例：处理 docs/domains/001-user-management 目录并应用 --from-docs 参数
INPUT_DIR="docs/domains/001-user-management"
COMMAND="flow-1-analyze-brd"  # 根据触发命令确定
OUTPUT_DIR=".eases/001-user-auth/$COMMAND"  # 按命令隔离
```

### 2. 目录映射（--from-docs 时）

```bash
# 2.1 创建 .eases 目录结构（按命令隔离）
mkdir -p "$OUTPUT_DIR"/checklists
mkdir -p ".eases/001-user-auth/contracts"
mkdir -p ".eases/001-user-auth/artifacts"

# 2.2 整合文档到 spec.md
cat > "$OUTPUT_DIR/spec.md" << EOF
# Feature Specification: User Authentication

## Business Requirements
$(cat "$INPUT_DIR/analyze-brd-output.md" | sed -n '/## 业务需求/,/##/p')

## Current State Analysis
$(cat "$INPUT_DIR/analyze-code-output.md" | sed -n '/## 现状分析/,/##/p' 2>/dev/null || echo "N/A")

## Success Criteria
- Users can register with email/password
- Users can login and logout
- Password reset functionality works
EOF

# 2.3 复制 artifacts 到共享目录
if [ -d "$INPUT_DIR/artifacts" ]; then
    cp -r "$INPUT_DIR/artifacts"/* ".eases/001-user-auth/contracts/"
fi
```

### 3. 执行 SDD 阶段

#### 需求规范阶段
- 如果 spec.md 不存在或 --force-specify
- 从整合的内容创建完整的需求规范

#### 需求澄清阶段
- 检查规范中的 `[NEEDS CLARIFICATION]` 标记
- 参考 reference/需求澄清.md 进行交互式澄清

#### 技术计划阶段
- 基于规范创建技术计划
- 生成 research.md、data-model.md
- 创建 contracts/ 目录

#### 任务分解阶段
- 分解为可执行的任务列表
- 标记依赖关系和并行任务

#### 一致性分析阶段（可选）
- 检查文档一致性
- 验证覆盖率

#### 执行实现阶段
- 按任务列表执行
- 标记完成状态

---

## 跳过/重入规则（幂等）

| 阶段 | 存在条件 | 默认行为 | --resume 行为 |
|------|----------|----------|--------------|
| 需求规范 | spec.md 存在 | 跳过 | 跳过 |
| 需求澄清 | 无 NEEDS_CLARIFICATION | 跳过 | 跳过 |
| 技术计划 | plan.md 存在且更新 | 跳过 | 检查时间戳 |
| 任务分解 | tasks.md 更新于 plan.md | 跳过 | 检查时间戳 |
| 一致性分析 | --with-analyze 且有变化 | 执行 | 执行 |
| 执行实现 | tasks.md 中有未完成项 | 执行 | 继续未完成项 |

---

## 示例场景

### 场景1：从 docs/domains 自动映射并执行

```bash
# 用户执行了 BRD 分析
/ease:analyze-brd docs/requirements/user-auth.md

# 输出位置：
# - docs/domains/001-user-management/analyze-brd-output.md（整体摘要）
# - docs/domains/001-user-management/usecases/001-authentication/001-login.md（带编号）

# 一键执行完整流程
# 参考本文档处理 docs/domains/001-user-management --from-docs --desc "用户认证系统"
```

执行过程：
1. 检查 `/memory/constitution.md` 是否存在
2. 检测到 `docs/domains/001-user-management`，创建 `.eases/001-user-auth/analyze-brd/`
3. 整合 `analyze-brd-output.md` 和带编号的 `usecases/` 目录下的用例文档到 `spec.md`
4. 参考 reference/需求澄清.md → reference/制定技术计划.md → reference/生成任务列表.md → reference/执行实现.md

### 场景2：断点续跑

```bash
# 上次在执行实现阶段中断
# 参考本文档处理 .eases/001-user-auth/analyze-brd --resume
```

执行过程：
1. 跳过已完成的 需求规范/需求澄清/技术计划/任务分解 阶段
2. 继续执行未完成的执行实现任务

### 场景3：带分析阶段

```bash
# 需要进行架构评审的场景
# 参考本文档处理 docs/domains/payment-processing --from-docs --with-analyze
```

执行过程：
1. 检查 constitution.md
2. 映射 docs/domains → eases
3. 执行完整流程
4. 额外执行 analyze 阶段进行一致性检查

---

## 集成到 Ease Commands

### 自动触发机制

> ⚠️ **重要**：只有以下五个命令会调用 ease-spec 并完整执行生命周期：
> - `/ease:flow-1-analyze-brd` (Phase 1 - Business)
> - `/ease:flow-1-analyze-trd` (Phase 1 - Technical)
> - `/ease:analyze-code`
> - `/ease:flow-2-design` (Phase 2)
> - `/ease:flow-3-implement` (Phase 3)

在每个命令的输出最后添加：

```markdown
## 下一步

规范驱动开发已就绪，参考以下文档继续：

```bash
# 自动映射并执行完整流程：参考本文档（一键执行.md）处理 docs/domains/[module_name] --from-docs

# 或分步执行：
# 1. 参考 reference/创建需求规范.md 处理 docs/domains/[module_name] 目录
# 2. 参考 reference/制定技术计划.md
# 3. 参考 reference/生成任务列表.md
# 4. 参考 reference/执行实现.md
```
```

### Ease命令输出标准化

每个调用 ease-spec 的命令应输出：

1. **主文档**：`{command}-output.md`（到 `docs/domains/[module_name]/`）
2. **工件目录**：`artifacts/`
   - API 设计：`api-design.md`
   - 数据库设计：`db-schema.sql`
   - 架构图：`architecture-diagram.png`
3. **清单**：`checklist.md`
4. **ease-spec 产出**：`.eases/[编号]-[功能名]/[command]/`
   - `spec.md`
   - `plan.md`
   - `tasks.md`
   - `checklists/`

---

## 错误处理

### 常见错误及解决方案

1. **constitution.md 不存在**
   ```
   ❌ 错误：/memory/constitution.md 不存在
   解决：请先执行 reference/项目宪章.md 创建项目宪章
   ```

2. **docs/domains 目录不存在**
   ```
   错误：docs/domains/[module_name] 目录不存在
   解决：请先执行相应的 ease command
   ```

3. **映射冲突**
   ```
   错误：.eases/001-xxx/[command] 已存在
   解决：使用 --force 强制覆盖或删除现有目录
   ```

4. **内容不足**
   ```
   警告：docs/domains 内容不足以生成完整规范
   建议：提供更多需求细节或使用 --desc 补充
   ```

---

## 产出

### 主要工件（按命令隔离）

```
.eases/[编号]-[功能名]/
├── analyze-brd/                     # analyze-brd 命令产出
│   ├── spec.md                      # 需求规范
│   ├── plan.md                      # 技术计划
│   ├── tasks.md                     # 任务列表
│   └── checklists/                  # 质量检查清单
├── analyze-code/                    # analyze-code 命令产出
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   └── checklists/
├── design/                          # design 命令产出
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   ├── architecture/
│   ├── detail/
│   └── checklists/
├── code-implement/                  # code-implement 命令产出
│   ├── spec.md
│   ├── plan.md
│   ├── tasks.md
│   └── checklists/
├── research.md                      # 技术研究（共享）
├── data-model.md                    # 数据模型（共享）
├── quickstart.md                    # 快速验证指南
└── contracts/                       # 契约定义（共享）
    ├── api-spec.json
    └── event-spec.md
```

### 实现代码

- 按照任务列表生成的实际代码
- 测试文件
- 配置文件
- 文档更新

---

## 最佳实践

1. **首次使用必须创建 constitution.md**（不可协商）
2. **命名规范**：保持 docs/domains 和 eases 的命名一致
3. **命令隔离**：每个命令的产出放在独立的子目录
4. **内容同步**：修改 docs/domains 后重新映射
5. **版本控制**：每个阶段提交一次
6. **质量检查**：每个阶段后运行 checklist
7. **文档更新**：实现完成后更新所有文档
