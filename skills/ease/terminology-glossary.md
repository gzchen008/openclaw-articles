# 统一术语表（跨 Commands / Agents / Skills）

本术语表用于在中文化文档中统一专业术语的译名与用法，覆盖 DDD、Clean Architecture、架构审查与用例工程等领域。首次出现建议“中英文并列（中文/英文）”，后续统一使用中文译名。

## 1. 核心术语（Core Terms）

| 英文术语 | 中文统一译名 | 定义 / 用法说明 |
|---|---|---|
| Domain-Driven Design (DDD) | 领域驱动设计 | 以领域模型为核心驱动设计、开发与协作的方法论 |
| Ubiquitous Language | 统一语言 | 团队在限界上下文内共享的一致术语与定义 |
| Bounded Context (BC) | 限界上下文 | 模型与语义的边界，服务/模块划分依据 |
| Context Mapping | 上下文映射 | 描述上下文之间关系与集成模式的视图 |
| Core Domain | 核心领域 | 体现业务竞争优势的关键能力区域 |
| Supporting Domain | 支撑领域 | 必要但非差异化的业务能力 |
| Generic Domain | 通用领域 | 行业通用能力，可外包或采购 |
| Aggregate | 聚合 | 一致性边界内的对象集合 |
| Aggregate Root | 聚合根 | 事务入口，强制执行不变式的实体 |
| Entity | 实体 | 具备唯一身份标识、生命周期重要的对象 |
| Value Object (VO) | 值对象 | 不可变、由值定义、无唯一身份的对象 |
| Domain Event | 领域事件 | 过去时命名、不可变、用于跨上下文集成的状态变化 |
| Repository | 仓储 | 面向聚合的持久化抽象（接口层，不含 SQL 实现） |
| DAO | 数据访问对象 | 数据访问抽象（接口），不含具体 SQL 实现 |
| SAO | 服务访问对象 | 外部服务访问的抽象接口 |
| Anemic Model | 贫血模型 | 行为在服务，实体聚焦状态与不变式 |
| Combined Service | 组合服务 | 编排多个应用服务以实现用例，不调用其他组合服务 |
| DTO | 数据传输对象 | 跨层/跨系统传输的数据对象 |
| Idempotency | 幂等性 | 重复执行结果保持一致的能力 |
| Consistency | 数据一致性 | 强一致性或最终一致性选择与保证 |
| Saga | Saga 模式 | 跨服务事务的补偿型流程模式 |
| 2PC / 3PC | 两阶段/三阶段提交 | 分布式事务协议（谨慎使用，权衡可用性） |
| Event | 事件 | 状态变化的消息或记录（领域事件/集成事件） |
| Command | 命令 | 对聚合发起的变更请求 |
| Query | 查询 | 读取数据的请求（在 CQRS 中与命令分离） |
| CQRS | 命令查询职责分离 | 写模型与读模型分离的架构模式 |
| ACL (Anticorruption Layer) | 防腐层 | 上下文间模型转换与隔离层，避免语义污染 |
| OHS (Open Host Service) | 开放主机服务 | 面向多消费者的协议发布 |
| Conformist | 依从者 | 下游按上游模型直接接受，不做转换 |
| Shared Kernel | 共享内核 | 在上下文之间共享的小型模型（谨慎使用） |
| Customer–Supplier | 顾客–供应商关系 | 上游提供、下游消费的协作关系 |
| Partnership | 合作伙伴关系 | 上下文之间的协同演化关系 |
| SLA | 服务等级协议 | 可用性等服务目标的约定 |
| RTO / RPO | 恢复时间/恢复点目标 | 灾备指标，用于衡量恢复能力 |
| NFRs | 非功能性需求 | 可用性、性能、安全性、一致性等质量属性 |
| Trace ID / Correlation ID | 关联 ID | 全链路日志与追踪标识 |
| ADR (Architecture Decision Record) | 架构决策记录 | 记录架构决策的背景、选项与结论 |

## 2. Clean Architecture 分层映射（层级与职责）

建议统一采用如下目录与职责映射，保持与已翻译文档一致：

```
project/
├── controller/             # 接口层：Controller/RPC 入口
├── action/                 # 组合服务层：用例编排
├── service/                # 应用服务层：核心业务逻辑
├── common/                 # 通用层
│   ├── dto/                # 领域层（DTO、业务规则）
│   └── util/               # 工具层（Utilities）
└── integration/
    ├── dao/                # 数据访问层（Repository/DAO 接口）
    └── sao/                # 服务访问层（外部服务）
```

- 组合服务（action）可跨模块调用各类服务（service），但不得调用其他“组合服务”。
- 应用服务采用“贫血模型”模式：业务行为在服务，实体负责不变式与状态。
- DAO/SAO 处于集成层，仅提供接口，不含具体实现。

## 3. 用例工程与业务规则（UC/BR）统一规范

- 用例 ID：`UC-[%03d]`（如 UC-001、UC-042）
- 业务规则 ID：`BR-[%03d]-[rule-name]`（如 BR-001-free-shipping）
- 在用例文档中仅按 ID 引用业务规则，不复制规则细节
- 场景结构（模板参考 `../skills/ease-analysis/templates/usecases-template.md`）：
  - 前置条件 / 基础流程（按步骤编号） / 备选流程 / 异常流程 / 后置条件 / 依赖
  - 在步骤中使用 `[Apply BR-XXX]` 引用业务规则

## 4. 集成与一致性（Integration & Consistency）

- 上下文通信：优先事件驱动（异步），或 REST/gRPC（同步）
- 数据一致性：跨上下文采用最终一致性；每个事务仅更新一个聚合
- 防腐层（ACL）：在上下文边界进行模型转换，避免语义污染
- 版本策略：接口向后兼容，必要时采用语义化版本与兼容适配

## 5. 术语使用规则（Style Guide）

1. 首次出现采用“中文（英文）”，后续仅用中文统一译名  
   例：限界上下文（Bounded Context）→ 后续用“限界上下文”
2. ID/代码/路径使用等宽字体并保持项目相对路径  
   例：`doc/analyze/system-domains.md`（不使用以 `/` 开头的绝对路径）
3. 代码块语言标签与源文一致  
   例：```java、```bash、```markdown 等
4. 跨文档保持一致的大小写与缩写  
   例：DTO、DAO、SAO、ACL、OHS、SLA、RTO/RPO、NFRs

## 6. 参考与对齐（References & Alignment）

- 架构审查指南：`plugins/ease/skills/ease-architecture/references/architecture-review-guide.md`
- 设计模式参考：`plugins/ease/skills/ease-architecture/references/design-patterns.md`
- 用例流程与模板：`plugins/ease/skills/ease-analysis/flows/*`、`plugins/ease/skills/ease-analysis/templates/*`
- 编码规范参考：`plugins/ease/skills/ease-coding/references/java-style-guide.md`（待中文化）

## 7. 维护说明（Maintenance Notes）

- 当引入新术语或变更译名时，先更新本术语表，再在相关文档中统一替换
- 在 PR 中附带“术语变更清单”，确保 Commands/Agents/Skills 三大类一致
- 对术语歧义或冲突，采用“术语审议记录”并在 ADR 中归档
