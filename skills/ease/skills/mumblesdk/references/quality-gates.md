# 质量门速查（MumbleSDK 项目）

本速查基于 `ease_docs/complete_quality_standards.md` 与 `ease_docs/mumble_sdk_quality_standards.md`，用于在 CI/CD 中设定可执行的质量门（Quality Gates），确保代码在通用质量 + MumbleSDK 专项集成两大维度达标。

参考：
- 完整质量标准：`ease_docs/complete_quality_standards.md`
- MumbleSDK 专项质量：`ease_docs/mumble_sdk_quality_standards.md`
- 单测质量控制：`ease_docs/unit_test_quality_control.md`
- Spring Boot 最佳实践：`ease_docs/springboot-best-practices.md`

配套：
- CI 配置示例：`mumble-sdk/assets/quality-gates.yml`
- 执行命令参考：
  ```bash
  ./gradlew clean build
  ./gradlew jacocoTestReport
  ./gradlew sonarqube
  ./gradlew checkstyleMain pmdMain spotbugsMain
  ```

---

## 1. 质量门分层结构

### 1.1 通用代码质量（50% 权重）
- 覆盖率（JaCoCo）
  - 最低：80%
  - 目标：90%
- 圈复杂度（SonarQube）
  - 单方法最大：10（目标 5）
  - 类平均：≤ 6
- 代码重复率（SonarQube）
  - 最低：≤ 3%（目标 ≤ 1%）
- 代码异味（SonarQube）
  - Critical：0（阻断 Gate）
  - Major：≤ 5
- 静态分析（Checkstyle/PMD/SpotBugs）
  - 阻断：任何 `Error` 等级违规
  - 警告：≤ 阈值（建议 ≤ 50，按项目规模调整）

### 1.2 MumbleSDK 专项质量（50% 权重）
- 上下文管理
  - 必须存在：`MumbleContextUtil.setBizSeqNo(...)` 与 `clear()`（服务层）
- Web 层集成
  - 控制器必须继承 `MumbleAbstractBaseController`
  - 必须使用 `execute(...)` 异步范式
- 服务层规范
  - 写操作：`@Transactional(rollbackFor = Exception.class)`
  - 读操作：`@Transactional(readOnly = true)`
  - 流水生成：`MumbleSeqService.nextValue("BIZ_TAG"|"TXN")`
- 校验框架
  - DTO/Request 使用 `@Webank*` 金融级注解
  - 自定义校验器实现 `WebankConstraintValidator`
- 中间件集成
  - RMB：`@MumbleRmbService` / `@MumbleServiceMethod` 使用一致
  - 分布式锁：`tryLock(...)` + `finally unlock(...)`
  - 序列服务：统一调用规范与日志透传
- 配置管理
  - 仅 `.properties`（禁止 YAML）
  - 按环境拆分：`application-{dev|test|prod}.properties`

---

## 2. 指标与工具映射

| 指标 | 工具 | 规则/阈值 | 阻断 |
|-----|------|-----------|------|
| 覆盖率 | JaCoCo | ≥ 80%（目标 90%） | 是 |
| 圈复杂度 | SonarQube | 单方法 ≤ 10（目标 5） | 否（超阈建议） |
| 代码重复率 | SonarQube | ≤ 3%（目标 ≤ 1%） | 否（超阈建议） |
| Critical 违规 | SonarQube | 0 | 是 |
| Major 违规 | SonarQube | ≤ 5 | 否（超阈建议） |
| Checkstyle | Checkstyle | 不允许 Error | 是 |
| PMD | PMD | 不允许 Error | 是 |
| SpotBugs | SpotBugs | 报告等级 ≤ medium，禁止高危 | 是 |
| Mumble 上下文 | 代码扫描 | `setBizSeqNo` + `clear` | 是 |
| 控制器继承 | 代码扫描 | `extends MumbleAbstractBaseController` | 是 |
| execute 异步 | 代码扫描 | `execute(` 调用存在 | 是 |
| 事务边界 | 代码扫描 | `@Transactional` 使用 | 是 |
| 金融校验注解 | 代码扫描 | `@Webank*` 使用 | 否（建议） |
| DAO 规范 | 代码扫描 | `throws SQLException` + `AbstractSimpleDAO` | 是 |
| Properties-only | 文件扫描 | 存在 `.properties`，无 YAML | 是 |

---

## 3. CI 建议配置（Gradle 片段）

```gradle
plugins {
  id 'org.springframework.boot' version '3.4.4'
  id 'io.spring.dependency-management' version '1.1.4'
  id 'java'
  id 'jacoco'
  id 'org.sonarqube' version '3.5.0'
  id 'checkstyle'
  id 'pmd'
  id 'com.github.spotbugs' version '5.0.13'
}

sonarqube {
  properties {
    property "sonar.projectKey", "ease-framework"
    property "sonar.projectName", "EASE Framework"
    property "sonar.coverage.jacoco.xmlReportPaths", "${buildDir}/reports/jacoco/test/jacocoTestReport.xml"
    property "sonar.java.checkstyle.reportPaths", "${buildDir}/reports/checkstyle/main.xml"
    property "sonar.java.pmd.reportPaths", "${buildDir}/reports/pmd/main.xml"
    property "sonar.java.spotbugs.reportPaths", "${buildDir}/reports/spotbugs/main.xml"
  }
}

jacoco {
  toolVersion = "0.8.8"
}

jacocoTestReport {
  dependsOn test
  reports {
    xml.required = true
    html.required = true
    csv.required = false
  }
  afterEvaluate {
    classDirectories.setFrom(files(classDirectories.files.collect {
      fileTree(dir: it, exclude: [
        '**/config/**',
        '**/dto/**',
        '**/entity/**',
        '**/exception/**',
        '**/*Application*'
      ])
    }))
  }
}

checkstyle {
  toolVersion = '10.3'
  configFile = file("${rootProject.projectDir}/config/checkstyle/checkstyle.xml")
  ignoreFailures = false
}

pmd {
  toolVersion = '6.47.0'
  ruleSetFiles = files("${rootProject.projectDir}/config/pmd/pmd-rules.xml")
  ignoreFailures = false
}

spotbugs {
  toolVersion = '4.7.3'
  ignoreFailures = false
  reportLevel = 'medium'
}
```

---

## 4. MumbleSDK 集成评分（建议模型）

将专项质量拆分为 6 个组件分值，加权求和形成“集成评分”，最低通过线建议：70/100。

- 上下文管理（25）
  - `setBizSeqNo`/`setTxnSeqNo`/`clear` 使用（10）
  - ThreadLocal 安全（8）
  - 业务序列记录（7）
- Web 层（25）
  - 控制器基类继承（10）
  - `execute(...)` 异步范式（8）
  - 统一异常响应（7）
- 服务层（20）
  - 事务边界/回滚（8）
  - 事务传播与只读（7）
  - 业务逻辑分层（5）
- 校验框架（15）
  - 金融校验注解覆盖（8）
  - 业务自定义校验（4）
  - 错误消息/i18n（3）
- 中间件集成（10）
  - RMB 标注与错误处理（5）
  - 锁使用模式（3）
  - 序列服务使用（2）
- 配置管理（5）
  - properties-only（3）
  - 多环境配置（2）

---

## 5. Gate 触发与动作（示例）

- 阻断类（Fail the build）：
  - 覆盖率 < 80%
  - SonarQube Critical > 0
  - Checkstyle/PMD/SpotBugs 有 Error
  - 任一 MumbleSDK 硬性规则失败（控制器继承、execute 异步、上下文清理、DAO 规范、properties-only）
- 预警类（Warn + 任务创建）：
  - 圈复杂度/重复率超阈
  - Major 违规 > 5
  - 校验注解覆盖不足
  - 集成评分 < 70/100

动作：
- 在 CI 中强制失败并输出修复建议（链接到本速查与 `integration-checklist.md`）
- 创建质量任务（Jira/Issue），附带 `quick_validate_mumblesdk.py` 输出报告

---

## 6. 执行与报告

- 执行顺序（建议）：
  1) `./gradlew clean build`
  2) `./gradlew jacocoTestReport`
  3) `./gradlew checkstyleMain pmdMain spotbugsMain`
  4) `./gradlew sonarqube`
  5) 运行 `mumble-sdk/scripts/quick_validate_mumblesdk.py`
- 汇总报告：
  - 覆盖率与复杂度/重复率
  - 静态分析违规清单
  - MumbleSDK 专项检查结果与集成评分
  - 修复建议与责任人

---

## 7. 常见失败原因与修复路径

- 未清理上下文 → 在服务层 `finally` 强制 `MumbleContextUtil.clear()`
- 控制器未继承/未使用 execute → 统一迁移到 `MumbleAbstractBaseController` 模板
- DAO 未声明 `throws SQLException` → 补全签名并修正 XML 参数化
- 使用 YAML 配置 → 全面替换为 `.properties`
- 未启用金融校验注解 → 在 DTO/Request 补充 `@Webank*` 并编写自定义校验器
- 覆盖率不足 → 增加异常/边界/并发/批量路径的单测

---

在 `mumble-sdk/assets/quality-gates.yml` 中提供了开箱可用的 CI Gate 配置示例；结合本速查与 `integration-checklist.md` 可快速定位与修复质量门失败。
