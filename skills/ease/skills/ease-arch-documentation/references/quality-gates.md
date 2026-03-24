# 质量门禁与一致性校验规范

本文档定义架构文档生成后的强制校验规则，用于保证在“大项目/少注释/少原生文档”场景下仍能稳定交付“完整、一致、可验证”的文档。

## 1. 门禁目标

1. **完整性**：6 份文档齐全，且章节结构符合要求。
2. **一致性**：跨文档的模块名、接口归属、数据实体引用一致。
3. **可追溯**：关键结论可定位到代码/配置/DDL 的证据来源。
4. **不确定性可见**：无法证明的内容必须以“低置信/待确认”表达。

## 1.1 面向大模型的额外目标

1. **防止上下文溢出**：生成过程必须可分块执行，且中间结果可落盘复用。
2. **防止乐观跳步**：阶段完成后进入下游阶段，并在元数据中记录阶段轨迹。
3. **防止幻觉**：所有关键结论必须能被反向定位到证据。

## 2. 强制检查（Fail 级）

### 2.1 文件存在性

必须存在以下文件（路径与文件名固定）：
- `docs/system/01_SYSTEM_OVERVIEW.md`
- `docs/system/02_CORE_MODULES.md`
- `docs/system/03_API_INTERFACE.md`
- `docs/system/04_DATA_MODEL.md`
- `docs/system/05_CONFIG_MANAGEMENT.md`
- `docs/system/06_UTILS_LIBRARIES.md`
- `docs/system/metadata.json`

### 2.2 章节结构

每份文档必须包含固定二级标题集合（可根据项目调整，但必须在生成器中固化并校验）。

建议最低要求：
- `01_SYSTEM_OVERVIEW.md`：技术栈说明、整体架构图、系统特性、部署环境、项目结构说明
- `02_CORE_MODULES.md`：模块职责说明、代码结构图、模块间关系
- `03_API_INTERFACE.md`：接口分类说明、RMB 接口详情列表、HTTP 接口详情列表
- `04_DATA_MODEL.md`：ER 图设计、核心表结构说明、数据关系分析、约束和安全
- `05_CONFIG_MANAGEMENT.md`：环境配置分析、配置文件说明、配置加载机制、安全管理
- `06_UTILS_LIBRARIES.md`：公共方法库分析、第三方依赖梳理、自定义注解、常量定义、异常处理

### 2.3 Mermaid 可渲染

所有 Mermaid 代码块必须能通过 Mermaid 语法校验（渲染失败则判定 Fail，或回退为文本图并记录 Warning）。

### 2.4 API 索引对齐

以 `metadata.json.indexes.api_index` 为准：
- `03_API_INTERFACE.md` 中的 HTTP endpoint 数量必须与 `api_index.http` 数量一致。
- `03_API_INTERFACE.md` 中的 RMB service 数量必须与 `api_index.rmb` 数量一致。
- 随机抽样 5%（至少 5 条）校验：method/path/serviceId 与 `source` 指向的代码一致。

### 2.5 Schema 索引对齐

以 `metadata.json.indexes.schema_index` 为准：
- `04_DATA_MODEL.md` 中的表清单数量必须与 `schema_index.tables` 数量一致。
- 每张表至少包含：表描述、字段表格（>=1 字段）、主键说明。

### 2.6 证据覆盖率

对以下“关键结论”要求 100% 证据覆盖（缺 1 条即 Fail）：
- 技术栈版本（语言版本、主要框架版本）
- 每个核心模块的目录/包位置
- 每个 HTTP endpoint 的 method/path
- 每个 RMB service 的 serviceId
- 每张核心表的 DDL 来源

证据格式：`来源: <path>:<line> (symbol)`

### 2.7 随机反向验证（Anti-hallucination）

为对抗“模型凭经验补全”，必须执行随机抽样回查：
- 每份文档至少抽样 3 条“关键条目”（API/serviceId/表字段/配置 key 等）
- 对每条条目，必须能在 `source` 指向的代码/DDL/配置中找到对应事实
- 若任意 1 条回查失败：本次质量门禁 Fail，必须回退修正索引并重新生成

### 2.8 阶段完成性（Anti-skip）

在 `metadata.json` 中记录各阶段完成情况（建议 `generation_trace`），并校验：
- 对应 `indexes` 分区就绪后再标记对应文档为生成完成
- `quality_gates.last_run.result=pass` 之前确保 6 份文档已生成/更新并落盘

### 2.9 索引分区文件一致性（Large-metadata safe）

当 `metadata.json.indexes.<partition>.file` 存在时：
- `file` 指向的文件必须存在
- `hash` 必须与分区详情文件的内容 hash 一致
- `counts` 必须与分区详情文件的统计一致（允许误差 0）

否则质量门禁 Fail。

## 3. 一致性检查（Fail 或 Warning）

### 3.1 模块名一致

`02_CORE_MODULES.md` 定义的模块名集合是“权威集合”。
- `03_API_INTERFACE.md` 的“归属模块”必须属于该集合，否则 Fail。
- `06_UTILS_LIBRARIES.md` 的“归属模块/所在目录”必须能映射到 module_index，否则 Warning。

### 3.2 数据实体引用一致

`04_DATA_MODEL.md` 中出现的表/实体名是“权威集合”。
- `02/03` 引用实体时必须能在 `04` 中找到；找不到则标注“未收录”并 Warning。

### 3.3 术语一致

同一概念（如 RMB、服务注册、配置中心）必须使用统一中文名与缩写。建议维护 `glossary`（可放入 `metadata.json` 扩展字段）。

## 4. 不确定性表达检查（Fail 级）

当文档出现以下词汇但没有“低置信/待确认”标识时，判定 Fail（示例关键词）：
- “应该/可能/大概/推测/估计/通常/一般来说”

正确写法：
- `结论(低置信)` + `现有证据` + `待确认问题(<=3)`

## 5. 产出物：门禁报告

门禁执行后必须输出报告（可写入 `metadata.json.quality_gates.last_run`，也可额外生成 `docs/system/quality-report.md`）：

```json
{
  "quality_gates": {
    "last_run": {
      "timestamp": "YYYY-MM-DDTHH:mm:ss",
      "result": "pass|fail",
      "failed_checks": [
        {"id": "API_INDEX_MISMATCH", "message": "..."}
      ],
      "warnings": [
        {"id": "ENTITY_REFERENCE_MISSING", "message": "..."}
      ]
    }
  }
}
```

## 6. 建议的实现顺序

1. 先做 2.1/2.2（结构性问题最常见）。
2. 再做 2.4/2.5（确保核心事实不漂移）。
3. 最后做 2.6/3.x/4（确保可信与一致）。
