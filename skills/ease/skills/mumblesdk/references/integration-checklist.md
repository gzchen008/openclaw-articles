# MumbleSDK 集成清单（精准版）

本清单用于在项目中“逐项核对”是否精准对齐 MumbleSDK 企业框架规范。请结合以下参考文档执行：
- 架构与技术参考：`ease_docs/mumble-sdk-architecture-tech.md`
- 框架最佳实践：`ease_docs/mumble-sdk-best-practices.md`
- 质量标准（专项）：`ease_docs/mumble_sdk_quality_standards.md`
- MyBatis 规范：`ease_docs/mybatis-best-practices.md`
- Spring Boot 最佳实践：`ease_docs/springboot-best-practices.md`
- 单测质量：`ease_docs/unit_test_quality_control.md`、`ease_docs/complete_quality_standards.md`

配套技能文件：
- 快速开始：`mumble-sdk/references/quickstart.md`
- 模板样例：`mumble-sdk/templates/*`
- 质量门样例：`mumble-sdk/assets/quality-gates.yml`
- 合规校验脚本：`mumble-sdk/scripts/quick_validate_mumblesdk.py`

---

## 0. 项目初始化
- [ ] 已引入 MumbleSDK 模块（common、biz、web、rmb、test 等）并能编译
- [ ] JDK 21、Spring Boot 3.4.x、Gradle/Maven 构建环境准备完成
- [ ] 统一包结构与命名（controller/service/integration/dao/dto/config/exception）

---

## 1. 控制器层（Web）
- [ ] 控制器类继承 `MumbleAbstractBaseController`
- [ ] 必须实现抽象方法：
  - [ ] `getFrontTaskExecutor()` 返回线程池（来自配置类）
  - [ ] `getBizSeqNo()` 使用 `MumbleSeqService.nextValue("WEB")`
- [ ] 使用 `execute(...)` 模板方法进行 `DeferredResult` 异步处理
- [ ] 统一响应格式 `ResponseMessage<T>`（成功/超时/异常）
- [ ] 参数对象使用 `@Valid` 与金融级校验注解（见校验章节）
- [ ] 接口层日志包含业务流水（MDC：`bizSeqNo`）

参考：`mumble-sdk/templates/controller-template.java`、`ease_docs/mumble-sdk-architecture-tech.md`

---

## 2. 服务层（事务 + 上下文 + 序列）
- [ ] 业务方法标注 `@Transactional(rollbackFor = Exception.class)`（写操作）
- [ ] 查询方法使用 `@Transactional(readOnly = true)`
- [ ] 生成业务/交易流水：
  - [ ] `MumbleSeqService.nextValue("BIZ_TAG")`
  - [ ] `MumbleSeqService.nextValue("TXN")`
- [ ] 上下文设置与清理：
  - [ ] `MumbleContextUtil.setBizSeqNo(...)`
  - [ ] `MumbleContextUtil.setTxnSeqNo(...)`
  - [ ] `finally { MumbleContextUtil.clear(); }` 强制清理
- [ ] 异常分类与转换：业务异常/系统异常/校验异常一致化

参考：`mumble-sdk/templates/service-template.java`、`ease_docs/mumble_sdk_quality_standards.md`

---

## 3. 数据访问（DAO/Mapper/XML）
- [ ] Mapper 接口方法全部声明 `throws SQLException`
- [ ] DAO 实现类必须继承 `AbstractSimpleDAO`，使用 `MumbleSqlSession`
- [ ] `try-with-resources` 管理 Session
- [ ] XML 配置：
  - [ ] 命名空间与接口完全匹配
  - [ ] 定义 `BaseResultMap` 与 `Base_Column_List`
  - [ ] 参数化查询（`#{param,jdbcType=XXX}`），禁止 `select *`
  - [ ] 更新/删除具备明确 where 条件，支持选择性更新
  - [ ] JDBC 类型与时间类型规范（统一 `LocalDateTime`）

参考：`ease_docs/mybatis-best-practices.md`

---

## 4. 配置管理（Properties-only）
- [ ] 配置文件仅使用 `.properties`，禁止 YAML
- [ ] 环境分离：`application-{dev|test|prod}.properties`
- [ ] 数据源与连接池（HikariCP）按最佳实践配置
- [ ] 线程池、分布式锁、序列服务、HTTP 客户端均外部化配置
- [ ] 日志格式包含 `bizSeqNo`（MDC）

参考：`mumble-sdk/templates/application.properties.example`、`ease_docs/springboot-best-practices.md`

---

## 5. 参数校验与异常处理
- [ ] DTO/Request 使用金融级注解：
  - [ ] `@WebankIdNo`、`@WebankMobilePhone`、`@WebankCardNo`、`@WebankEmail`
  - [ ] `@WebankLength`、`@WebankNotBlank` 等
- [ ] 自定义业务校验：注解 + `WebankConstraintValidator`，支持 i18n
- [ ] 全局异常处理：`@ControllerAdvice` + `ResponseMessage.error(code, msg)`
- [ ] 异常日志携带业务流水

参考：`mumble-sdk/templates/validation-template.java`、`ease_docs/mumble_sdk_quality_standards.md`

---

## 6. RMB 消息服务
- [ ] 使用 `@MumbleRmbService(serviceId = "...")` 标注服务类
- [ ] 使用 `@MumbleServiceMethod(methodName = "...")` 标注方法
- [ ] 统一错误响应并记录监控/审计日志（含业务流水）
- [ ] 支持版本、超时、重试等配置（按企业规范）

参考：`mumble-sdk/templates/rmb-service-template.java`、`ease_docs/mumble-sdk-best-practices.md`

---

## 7. 分布式锁
- [ ] 使用 `MumbleDistributedLock.tryLock(key, timeout)` 获取锁
- [ ] 无论成功/异常，始终在 `finally` 中执行 `unlock(key)`
- [ ] 结合事务合理设置锁粒度与持有时长

参考：`ease_docs/mumble-sdk-architecture-tech.md`、分布式锁示例

---

## 8. 序列服务
- [ ] 按业务域定义序列类型（如 `ORDER`, `ORDER_CREATE`, `TXN`）
- [ ] 使用 `MumbleSeqService.nextValue(type)` 生成
- [ ] 记录并透传到日志/响应/上下文；支持日期重置与段式缓存（由框架实现）

参考：`ease_docs/mumble-sdk-architecture-tech.md`（序列服务）

---

## 9. 日志与监控
- [ ] 入口日志：请求参数 + 业务流水（脱敏后）
- [ ] 业务日志：关键操作点与耗时
- [ ] 异常日志：堆栈 + 上下文
- [ ] 性能日志：慢操作记录与阈值预警
- [ ] 审计日志：敏感操作与数据变更

参考：`ease_docs/complete_quality_standards.md`、`ease_docs/mumble_sdk_quality_standards.md`

---

## 10. 测试与质量门
- [ ] 启用 CI 质量门：`mumble-sdk/assets/quality-gates.yml`
  - [ ] 覆盖率 ≥ 80%（目标 ≥ 90%）
  - [ ] 圈复杂度、重复率、代码异味阈值
  - [ ] MumbleSDK 集成评分分项（上下文、Web、服务、校验、锁、序列、配置）
- [ ] 单测规范：
  - [ ] 静态 Mock：`MumbleContextUtil`、`MumbleSeqService`
  - [ ] 控制器隔离测试：`@WebMvcTest` + `MockMvc`
  - [ ] 服务/DAO 集成测试：事务 + 回滚 + 批量/异常/并发分支
- [ ] 质量流水线：
  - [ ] `./gradlew clean build`
  - [ ] `./gradlew jacocoTestReport`
  - [ ] `./gradlew sonarqube`
  - [ ] `./gradlew checkstyleMain pmdMain spotbugsMain`

参考：`ease_docs/unit_test_quality_control.md`、`ease_docs/complete_quality_standards.md`

---

## 11. 合规快速校验（脚本）
- [ ] 已运行 `python mumble-sdk/scripts/quick_validate_mumblesdk.py <project-root>`
- [ ] 对应项全部通过或给出修复建议并完成整改

---

## 12. 交付验收（最低标准）
- [ ] 控制器：异步统一响应、抽象方法实现、校验生效
- [ ] 服务：事务边界、流水生成、上下文清理
- [ ] DAO/Mapper/XML：继承/异常声明/参数化/ResultMap
- [ ] 配置：仅 `.properties`，分环境配置
- [ ] RMB：统一错误响应与日志
- [ ] 锁与序列：使用规范与日志记录
- [ ] 日志：带业务流水的结构化日志
- [ ] 测试：覆盖率与关键分支完整
- [ ] 质量门：CI 通过
- [ ] 合规脚本：核心检查项通过，无阻塞问题

---

完成上述清单后，即可判定项目已“精准对齐” MumbleSDK 企业框架规范，具备上线级工程质量与可维护性。
