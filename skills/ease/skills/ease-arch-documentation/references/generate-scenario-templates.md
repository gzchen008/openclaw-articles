# 场景架构模板生成指南

> **适用**: `ease-arch-documentation` 技能在生成架构文档时，额外生成场景架构模板库。

## 概述

在执行 `/ease:arch-docs` 生成系统架构文档的同时，分析项目代码和已有架构文档，为项目生成适用的场景架构模板库。模板将存储在 `docs/system/architecture/templates/` 目录下，供 `/ease:flow-2-design` 使用。

## 触发条件

当以下任一条件满足时，执行场景模板生成：

1. `/ease:arch-docs` 无参数执行（全量生成时附带生成模板）
2. `/ease:arch-docs scenario-templates`（仅生成场景模板）
3. `docs/system/architecture/templates/` 目录不存在
4. `/ease:flow-2-design` 前置检查发现模板缺失时自动调用

## 生成流程

### Step 1: 分析项目场景特征

基于已生成的系统架构文档，识别项目中已存在的业务场景类型：

```
输入:
  - docs/system/architecture/01_SYSTEM_OVERVIEW.md（技术栈）
  - docs/system/architecture/02_CORE_MODULES.md（核心模块）
  - docs/system/architecture/03_API_INTERFACE.md（API 接口）
  - 项目代码结构

分析维度:
  1. 从 API 接口中识别场景类型（CRUD → query, 支付接口 → transaction 等）
  2. 从核心模块中识别业务领域（审批模块 → workflow 等）
  3. 从技术栈中识别基础设施（WebSocket → realtime, MQ → messaging 等）

输出:
  - detected_scenarios: 项目中检测到的场景类型列表
```

### Step 2: 生成项目定制化模板

对于每个检测到的场景类型：

1. **复制基础模板**: 从 `plugins/ease/skills/ease-arch-documentation/references/scenario-templates/` 复制对应模板
2. **技术栈对齐**: 将模板中的推荐技术栈替换为项目实际使用的技术栈
3. **组件对齐**: 根据项目现有组件结构，调整组件命名和路径

### Step 3: 补充缺失的通用模板

对于项目中未检测到但属于通用场景的模板，直接从基础模板库复制：

```
通用场景列表:
  - transaction（交易类）
  - query（查询类）
  - workflow（流程类）
  - messaging（消息类）
  - auth（认证类）
  - generic（通用类，必须存在）
```

可选场景（仅在检测到相关代码时生成）：
  - sync（数据同步类）
  - file（文件处理类）
  - realtime（实时类）

### Step 4: 生成模板索引

创建 `docs/system/architecture/templates/README.md`，包含：
- 可用模板列表（带链接）
- 使用说明
- 项目定制化说明

### Step 5: 质量校验

- 每个模板文件必须包含完整的 10 个标准章节
- 技术栈推荐必须与 `01_SYSTEM_OVERVIEW.md` 不冲突
- `generic-template.md` 必须存在（兜底方案）

## 输出结构

```
docs/system/architecture/
├── 01_SYSTEM_OVERVIEW.md
├── 02_CORE_MODULES.md
├── ...
└── templates/                    # 场景模板目录
    ├── README.md                 # 模板索引
    ├── transaction-template.md   # 交易类
    ├── query-template.md         # 查询类
    ├── workflow-template.md      # 流程类
    ├── messaging-template.md     # 消息类
    ├── sync-template.md          # 同步类（按需）
    ├── auth-template.md          # 认证类
    ├── file-template.md          # 文件类（按需）
    ├── realtime-template.md      # 实时类（按需）
    └── generic-template.md       # 通用类（必须）
```

## 增量更新策略

当项目模板已存在时（`docs/system/architecture/templates/` 已有文件）：

1. **不覆盖**: 已存在的模板文件不会被覆盖（项目可能已定制化）
2. **补充缺失**: 仅补充缺失的模板文件
3. **更新索引**: 重新生成 `README.md` 以反映当前模板列表
4. **强制更新**: 使用 `--force` 参数时覆盖所有模板

## 与 flow-2-design 的集成

`/ease:flow-2-design` 在步骤 0.5（架构文档前置检查）中：

1. 检查 `docs/system/architecture/templates/` 是否存在
2. 如果不存在，自动调用 `/ease:arch-docs scenario-templates` 生成
3. 生成完成后继续 design 流程
