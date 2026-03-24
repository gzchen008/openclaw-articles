# [PROJECT_NAME] Constitution

<!-- Example: Spec Constitution, TaskFlow Constitution, etc. -->

## Core Principles

### 0. Project Type Detection (MUST EXECUTE FIRST)

**快速检测项目类型（3 步完成）：**

```bash
IS_JAVA=$( [ -f "pom.xml" ] || [ -f "build.gradle" ] && echo true )
IS_MUMBLE=$( grep -q "mumble-sdk" pom.xml build.gradle 2>/dev/null || \
             grep -rq "MumbleAbstractBaseController\|AbstractSimpleDAO" src/ 2>/dev/null && echo true )
```

| 结果 | 处理 |
|------|------|
| `IS_MUMBLE=true` | **优先调用 `mumblesdk` skill**，所有设计/代码/框架遵循 MumbleSDK 规范 |
| `IS_JAVA=true` | 使用通用 Java 规范 |
| 其他 | 使用对应语言规范 |

### I. Library-First

<!-- Example: Every feature starts as a standalone library -->

- Libraries MUST be self-contained, independently testable, documented
- Clear purpose required - no organizational-only libraries
- Each library exposes functionality that can be used independently

### II. CLI Interface

<!-- Example: Every library exposes functionality via CLI -->

- Text in/out protocol: stdin/args → stdout, errors → stderr
- Support JSON + human-readable formats
- Enables automation and scripting

### III. Test-First (NON-NEGOTIABLE)

<!-- Example: TDD mandatory -->

- Tests written → User approved → Tests fail → Then implement
- Red-Green-Refactor cycle strictly enforced
- No code without corresponding tests

### IV. Integration Testing

<!-- Focus areas requiring integration tests -->

- New library contract tests
- Contract changes
- Inter-service communication
- Shared schemas

### V. Observability

<!-- Text I/O ensures debuggability -->

- Structured logging required
- Tracing for cross-service calls
- Metrics for key operations

### VI. Versioning & Breaking Changes

<!-- MAJOR.MINOR.BUILD format -->

- Breaking changes require migration plan
- Semantic versioning strictly followed
- Changelog maintained

### VII. Simplicity

<!-- Start simple, YAGNI principles -->

- Avoid over-engineering
- Prefer simple solutions over complex ones
- Complexity must be justified

### VIII. Relative Paths (NON-NEGOTIABLE)

<!-- 所有文件和目录引用必须使用项目相对路径 -->

- 文件和目录的阅读、引用、生成均**必须使用项目相对路径**
- 禁止使用以 `/` 开头的绝对路径（如 `/docs/system/`）
- 正确格式：`docs/system/`、`memory/constitution.md`、`.eases/`
- 错误格式：`/docs/system/`、`/memory/constitution.md`、`/.eases/`
- 此规则适用于：文档内容、代码注释、配置文件、生成的产出物

## Directory Structure (NON-NEGOTIABLE)

```
memory/
└── constitution.md              # 项目宪章（本文件）

docs/
└── domains/                     # 领域模块文档根目录
    └── [编号]-[module_name]/    # 领域模块（三位编号 + 名称）
        │                        # 例如：001-user-management
        ├── analyze-brd-output.md
        ├── analyze-code-output.md
        ├── design-output.md
        ├── artifacts/           # 工件
        ├── architecture/        # 架构设计
        ├── design/              # 详细设计
        └── usecases/            # 用例文档（从 ease-analysis 拆解，带编号）
            └── [编号]-[subdomain]/        # 子领域（三位编号）
                └── uc-[编号]-[usecase].md    # 用例（三位编号）

.eases/                          # ease-spec 规范文档（项目相对路径）
└── [编号]-[功能名]/             # 例如：001-weekly-report
    ├── analyze-brd/             # analyze-brd 命令产出
    │   ├── spec.md
    │   ├── plan.md
    │   ├── tasks.md
    │   └── checklists/
    ├── analyze-code/            # analyze-code 命令产出
    ├── design/                  # design 命令产出
    ├── code-implement/          # code-implement 命令产出
    ├── research.md              # 技术研究（共享）
    ├── data-model.md            # 数据模型（共享）
    └── contracts/               # 契约定义（共享）
```

## Numbering Rules (NON-NEGOTIABLE)

All directories and files MUST have a 3-digit incremental number prefix:

| Level     | Format                     | Example                        |
| --------- | -------------------------- | ------------------------------ |
| Domain    | `[编号]-[module_name]/`  | `001-user-management/`       |
| Subdomain | `[编号]-[subdomain]/`    | `001-authentication/`        |
| Usecase   | `uc-[编号]-[usecase].md` | `001-login-with-password.md` |

**Numbering Logic:**

- When adding a new domain/subdomain/usecase, scan existing directories
- Get the maximum existing number + 1
- Format as 3 digits (001, 002, 003...)

## Commands that Invoke ease-spec

Only the following commands invoke ease-spec and must complete the full lifecycle:

| Command                  | Description  | Lifecycle                                                                     |
| ------------------------ | ------------ | ----------------------------------------------------------------------------- |
| `/ease:analyze-brd`    | 分析业务需求 | 需求规范 → 技术计划 → 任务分解 → 执行实现                                         |
| `/ease:analyze-trd`    | 分析技术需求 | 需求规范 → 技术计划 → 任务分解 → 执行实现                                         |
| `/ease:analyze-code`   | 分析源代码   | 需求规范 → 技术计划 → 任务分解 → 执行实现                                         |
| `/ease:design`         | 统一设计     | 需求规范 → 需求澄清 → 技术计划 → 框架代码 → 任务分解                               |
| `/ease:code-implement` | 代码实现     | 需求规范 → 技术计划 → 任务分解 → 执行实现                                         |

### Recommended Workflows

- **Business Requirements (BRD)**: `analyze-brd` → `design` (recommended) → `code-implement`
  - BRD output focuses on Use Cases; running `design` is recommended to bridge business logic to technical design.
- **Technical Requirements (TRD)**: `analyze-trd` → `code-implement`
  - TRD output already includes Solution Design; usually skips the separate `design` step.

## Usecases Directory Rules (NON-NEGOTIABLE)

- Usecases MUST be extracted from ease-analysis skill
- Usecases MUST be organized by subdomain with 3-digit numbers
- Usecases MUST be split by entity with 3-digit numbers
- Usecase files MUST use kebab-case naming with number prefix

## Governance

- Constitution supersedes all other practices
- Amendments require documentation, approval, migration plan
- All PRs/reviews must verify compliance
- Complexity must be justified

[Always respond in 中文]

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]

<!-- Example: Version: 3.1.0 | Ratified: 2025-12-17 | Last Amended: 2025-12-17 -->
