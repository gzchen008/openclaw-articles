# 项目索引构建规范

本文档定义“项目索引阶段”的输出口径与字段结构，用于在代码量大、原生文档少、注释缺失时仍能以事实为基础稳定生成架构文档。

## 1. 目标

1. **先索引、后写文档**：文档生成以索引为事实来源，索引未覆盖的信息以“低置信/待确认”方式呈现。
2. **可增量更新**：索引分区可独立更新（例如只更新 API 索引）。
3. **证据可追溯**：每条索引记录必须带 `source`（文件路径与行号）。

## 2. 索引分区

索引写入 `docs/system/metadata.json` 的 `indexes` 字段，建议至少包含以下分区：

> **重要：大索引拆分**
> 当索引分区内容过大时（例如 API/Schema 全量清单），必须将分区内容拆分到独立文件，避免 `metadata.json` 过大导致模型读取占用上下文。
> - 摘要保留在 `metadata.json.indexes.<partition>`
> - 详情落盘到 `docs/system/indexes/<partition>.json`
> - `metadata.json` 通过 `file/hash/size_bytes/counts` 引用详情文件

### 2.1 module_index（模块/目录索引）

用于支撑：`01_SYSTEM_OVERVIEW.md`、`02_CORE_MODULES.md`。

**采集内容**：
- 仓库根目录下的主要工程根（如 `src/`、`apps/`、`packages/`、`server/` 等）
- 模块候选集合（目录/包名前缀/Gradle 子工程等）
- 入口点候选（HTTP Controller、RMB Service、Job、CLI 命令入口等）

**字段建议**：
```json
{
  "module_index": {
    "hash": "<sha256>",
    "generated_at": "YYYY-MM-DDTHH:mm:ss",
    "roots": ["src"],
    "modules": [
      {
        "name": "web",
        "path": "src/main/java/.../web",
        "type": "entrypoint",
        "source": "src/main/java/.../web:1"
      }
    ]
  }
}
```

### 2.2 api_index（接口索引）

用于支撑：`03_API_INTERFACE.md`。

**采集内容**：
- HTTP：Controller 类 + mapping 注解组合后的完整路径、HTTP method、方法签名、请求参数来源（`@RequestBody/@RequestParam/@PathVariable` 等）
- RMB：`@MumbleMessageService` 标注的 serviceId（必须解析到具体数值）、request/response message 类型

**字段建议**：
```json
{
  "api_index": {
    "hash": "<sha256>",
    "generated_at": "YYYY-MM-DDTHH:mm:ss",
    "file": "docs/system/indexes/api_index.json",
    "size_bytes": 123456,
    "counts": {"http": 120, "rmb": 35}
  }
}
```

`docs/system/indexes/api_index.json` 示例（存放大数组详情）：

```json
{
  "http": [
    {
      "method": "POST",
      "path": "/users",
      "controller": "...UserController#createUser",
      "params": [
        {"name": "body", "type": "...CreateUserRequest", "from": "body"}
      ],
      "return": {"type": "...UserResponse"},
      "source": "src/main/java/.../UserController.java:42"
    }
  ],
  "rmb": [
    {
      "serviceId": 120001,
      "service": "...QueryClientInfoService",
      "methods": [
        {
          "name": "query",
          "params": [{"name": "req", "type": "...Req"}],
          "return": {"type": "...Resp"}
        }
      ],
      "source": "src/main/java/.../QueryClientInfoService.java:18"
    }
  ]
}
```

### 2.3 schema_index（数据模型索引）

用于支撑：`04_DATA_MODEL.md`。

**采集内容**：
- DDL 文件路径清单（优先）
- 表、字段、主键、索引、外键（若无外键，允许推导逻辑关系但必须标注为逻辑关系）
- Mapper/SQL 中出现的 join 条件（用于逻辑关系推导）

**字段建议**：
```json
{
  "schema_index": {
    "hash": "<sha256>",
    "generated_at": "YYYY-MM-DDTHH:mm:ss",
    "file": "docs/system/indexes/schema_index.json",
    "size_bytes": 234567,
    "counts": {"tables": 86, "ddl_files": 12}
  }
}
```

## 2.6 索引拆分阈值（建议）

为保证模型上下文预算稳定，建议当出现任意条件时触发拆分：
- `metadata.json` 预计超过 200KB
- 任一索引分区详情超过 100KB
- 任一索引分区条目数超过 500（例如 HTTP endpoints）

拆分后：
- 生成文档时默认只读取 `metadata.json` 摘要
- 需要写 `03/04` 细节时，按需读取 `docs/system/indexes/<partition>.json` 的局部片段

### 2.4 config_index（配置索引）

用于支撑：`05_CONFIG_MANAGEMENT.md`。

**采集内容**：
- 配置文件位置（`application.*`、`env/*`、`config/*`、`.env` 等）
- 代码中的默认值与来源（如 `@Value("${x:default}")`）
- 敏感项 key 清单（只记录 key，不记录 value）

### 2.5 utils_index（工具/可复用代码索引）

用于支撑：`06_UTILS_LIBRARIES.md`。

**采集内容**：
- util/constant/annotation/exception 的类清单
- 跨模块引用频次最高的 Top N 工具类（用于深度说明）

## 3. 证据与追溯

索引中每条记录必须包含：
- `source`: `path:line`
- 可选：`symbol`（类名/方法名/表名）

文档生成时必须将索引的 `source` 透传到对应文档段落（至少在表格或小节末尾提供 1 条）。

## 4. 增量更新策略

1. 从 `metadata.json.last_generation.commit_id` 到当前 commit 做 diff。
2. 将变更文件映射到索引分区：
   - Controller/RMB service 相关：更新 `api_index`
   - DDL/mapper/entity 相关：更新 `schema_index`
   - resources/env/config 相关：更新 `config_index`
   - util/constant/annotation/exception 相关：更新 `utils_index`
   - 目录/包移动/构建文件变更：更新 `module_index`（并触发模块归属重算）
3. 每个分区计算 `hash`；若分区 hash 未变化，可跳过对应文档更新。

## 6. 大模型上下文管理（强制）

> 该 Skill 依赖大模型能力。为避免上下文溢出、乐观跳过步骤和幻觉，索引构建必须遵循以下规则。

1. **分区构建**：一次只构建/更新一个索引分区（module/api/schema/config/utils）。
2. **候选集优先**：先用轻量扫描得到候选文件列表，再逐个精读候选文件内容，以控制输入规模。
3. **最小必要读取**：只读取与当前分区相关的最小片段（例如注解附近、DDL 的 CREATE TABLE 段落）。
4. **写入即记忆**：每完成一个分区，必须落盘写入 `docs/system/metadata.json.indexes.<partition>`，后续阶段只读取索引摘要。
5. **失败回退**：当候选文件过多时，允许采用“分批构建”策略（按目录/模块分批），每批次都必须产出可用的局部索引并带 hash。

## 5. 输出要求

1. 索引 JSON 必须是有效 JSON。
2. 时间字段使用 ISO8601。
3. 所有路径使用相对仓库根路径。
4. 索引中记录敏感配置时只记录 key（例如 password/token/secret 的键名），并省略 value。
