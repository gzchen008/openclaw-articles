# MumbleSDK 集成快速开始

本指南将把 `ease_docs` 中的 MumbleSDK 企业框架知识转化为“工程落地步骤”，用于在 Spring Boot 微服务中精准、规范地集成 MumbleSDK。请严格按照步骤执行，并对齐质量门与测试标准。

参考文档：
- 架构与技术参考：`ease_docs/mumble-sdk-architecture-tech.md`
- 框架最佳实践：`ease_docs/mumble-sdk-best-practices.md`
- MumbleSDK 质量标准：`ease_docs/mumble_sdk_quality_standards.md`
- MyBatis 实践与规范：`ease_docs/mybatis-best-practices.md`
- Spring Boot 最佳实践：`ease_docs/springboot-best-practices.md`
- 单测质量控制：`ease_docs/unit_test_quality_control.md`、`ease_docs/complete_quality_standards.md`

---

## 1. 环境准备与依赖

1) Java/构建工具
- JDK 21、Gradle（推荐）或 Maven（按企业规范）
- Spring Boot 3.4.x

2) 引入 MumbleSDK 模块（占位坐标，按企业仓库替换）
```gradle
dependencies {
  implementation "cn.webank:mumble-sdk-common:4.0.0"
  implementation "cn.webank:mumble-sdk-biz:4.0.0"
  implementation "cn.webank:mumble-sdk-web:4.0.0"
  implementation "cn.webank:mumble-sdk-rmb:4.0.0"
  testImplementation "cn.webank:mumble-sdk-test:4.0.0"
}
```

3) 代码目录建议（示例）
```
com.company.project/
├─ controller/              # 控制器层（继承 MumbleAbstractBaseController）
├─ service/                 # 服务层（事务 + 上下文 + 序列）
│  └─ impl/
├─ integration/
│  └─ dao/                  # Mapper 接口
│     └─ impl/              # 继承 AbstractSimpleDAO
├─ dto/                     # 传输对象（继承 BaseDTO）
│  ├─ request/              # 请求对象（使用 Webank* 校验注解）
│  └─ response/             # 响应对象
├─ config/                  # 配置类（线程池、序列、锁、验证器等）
└─ exception/               # 异常分类（业务/系统/校验）
```

---

## 2. 配置文件（必须使用 .properties）

复制并按需修改：`mumble-sdk/templates/application.properties.example`，然后分环境：
- `application.properties`（通用）
- `application-dev.properties`（开发）
- `application-test.properties`（测试）
- `application-prod.properties`（生产）

关键配置项（局部示例，详见模板）：
```properties
# 系统标识
mumble.system.id=1245
mumble.system.dcn=AA0
mumble.env=DEV

# 数据源（HikariCP）
spring.datasource.url=jdbc:mysql://localhost:3306/your_db?useSSL=false&serverTimezone=Asia/Shanghai
spring.datasource.username=${DB_USERNAME:root}
spring.datasource.password=${DB_PASSWORD:password}

# MyBatis
mybatis.mapper-locations=classpath:mapper/*.xml
mybatis.configuration.map-underscore-to-camel-case=true

# MumbleSDK 线程池
mumble.thread.pool.core-size=10
mumble.thread.pool.max-size=50

# 分布式锁
mumble.distributed.lock.redis.enabled=true

# 序列服务
mumble.sequence.service.enabled=true

# 日志（含 bizSeqNo）
logging.pattern.console=%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level [%X{bizSeqNo}] %logger{50} - %msg%n
```

---

## 3. 控制器开发（异步统一范式）

- 复制 `mumble-sdk/templates/controller-template.java` 并替换包名/类名/路径。
- 继承 `MumbleAbstractBaseController`，实现：
  - `getFrontTaskExecutor()`：返回线程池
  - `getBizSeqNo()`：使用 `MumbleSeqService.nextValue("WEB")` 生成 Web 层流水
- 使用 `execute(...)` 完成 `DeferredResult` 异步处理与统一响应 `ResponseMessage<T>`。

---

## 4. 服务层开发（事务 + 上下文 + 序列）

- 复制 `mumble-sdk/templates/service-template.java` 并替换命名。
- 在 `@Transactional(rollbackFor = Exception.class)` 边界内：
  - 生成业务/交易流水：`MumbleSeqService.nextValue("BIZ_TAG")`、`MumbleSeqService.nextValue("TXN")`
  - 设置上下文：`MumbleContextUtil.setBizSeqNo(...)`、`MumbleContextUtil.setTxnSeqNo(...)`
  - 统一异常分类并在 `finally` 保证 `MumbleContextUtil.clear()`

---

## 5. 参数校验（金融级注解）

- 复制 `mumble-sdk/templates/validation-template.java`，在 DTO/Request 使用 `@Webank*` 系列注解：
  - `@WebankIdNo`、`@WebankMobilePhone`、`@WebankCardNo`、`@WebankEmail`、`@WebankLength`、`@WebankNotBlank` 等
- 业务特定校验：定义自定义注解 + `WebankConstraintValidator` 实现；开启国际化消息。

---

## 6. RMB 消息服务

- 复制 `mumble-sdk/templates/rmb-service-template.java`，标注：
  - `@MumbleRmbService(serviceId = "xxx")`
  - `@MumbleServiceMethod(methodName = "xxx")`
- 统一错误响应：`ResponseMessage.error(code, msg)`；记录含流水的监控/审计日志。

---

## 7. DAO/Mapper/XML 强制规范

- Mapper 接口方法必须声明 `throws SQLException`。
- DAO 实现类必须继承 `AbstractSimpleDAO`，使用 `MumbleSqlSession`（try-with-resources）。
- XML 必须定义 `BaseResultMap`、`Base_Column_List`，使用参数化查询（防注入），禁止 `select *`。
- 参考：`ease_docs/mybatis-best-practices.md`

---

## 8. 质量门与测试

1) 复制 CI 质量门：`mumble-sdk/assets/quality-gates.yml`
- 覆盖率（≥80%/目标90%）、复杂度、重复率、MumbleSDK 集成分项。

2) 测试编写要点（片段）
- 静态 Mock：`MumbleContextUtil`、`MumbleSeqService`
- 控制器隔离测试：`@WebMvcTest` + `MockMvc`
- 服务/DAO 集成测试：事务 + 回滚；批量/并发路径覆盖
- 参考：`ease_docs/mumble_sdk_quality_standards.md`、`ease_docs/unit_test_quality_control.md`

3) 质量流水线（示例）
```bash
./gradlew clean build
./gradlew jacocoTestReport
./gradlew sonarqube
./gradlew checkstyleMain pmdMain spotbugsMain
```

---

## 9. 合规快速校验（脚本）

- 运行：`python mumble-sdk/scripts/quick_validate_mumblesdk.py <your-project-root>`
- 检查项（示例）：
  - 控制器是否继承 `MumbleAbstractBaseController` 且实现抽象方法
  - 服务是否生成流水、设置/清理上下文，并标注事务
  - DAO 是否继承 `AbstractSimpleDAO`、方法声明 `throws SQLException`
  - 是否存在 `.properties` 配置（非 YAML）
  - 测试中是否静态 Mock 上述 SDK 工具类

---

## 10. 验收清单（最低通过标准）

- [ ] 控制器：异步 `execute(...)` 与统一响应
- [ ] 服务：事务边界、流水生成、上下文清理
- [ ] 校验：使用金融级注解与自定义校验器
- [ ] RMB：统一错误响应与监控日志
- [ ] DAO/Mapper/XML：继承/声明/参数化/ResultMap
- [ ] 配置：仅使用 `.properties`，按环境分离
- [ ] 质量门：CI 启用并通过
- [ ] 测试：覆盖率≥80%，关键路径与异常分支覆盖
- [ ] 合规脚本：通过核心检查项，无阻塞问题

---

## 11. 常见问题定位

- 未清理上下文（ThreadLocal 泄漏）→ 在 `finally` 强制 `MumbleContextUtil.clear()`
- 事务不当边界导致锁持有过长 → 降低锁粒度/优化事务范围
- Mapper/XML 参数未声明 `jdbcType`/未参数化 → 严格使用 `#{param,jdbcType=XXX}`
- 使用 YAML 配置 → 改为 `.properties`
- 测试未 Mock 静态工具类 → 使用 `mockStatic(...)` 并在 `@AfterAll` 关闭

---

## 12. 进一步阅读

- `ease_docs/mumble-sdk-architecture-tech.md`（模块与技术实现）
- `ease_docs/mumble-sdk-best-practices.md`（生命周期与核心特性）
- `ease_docs/mumble_sdk_quality_standards.md`（专项质量标准）
- `ease_docs/complete_quality_standards.md`（完整质量框架）
- `ease_docs/unit_test_quality_control.md`（单测体系）
- `ease_docs/springboot-best-practices.md`（Spring Boot 通用最佳实践）
