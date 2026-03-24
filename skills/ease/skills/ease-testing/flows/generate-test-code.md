# 生成测试代码流程

本文档描述分析源代码并生成单元测试代码的标准流程，强调 MC/DC 原则和分轮覆盖率提升策略。

## 流程总览

```
┌──────────────────────────────────────────────────────────────────────────┐
│                           测试生成流程                                    │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│  │ 1.项目分析  │───▶│ 2.可测试性  │───▶│ 3.测试策略  │                  │
│  │             │    │   审查      │    │   制定      │                  │
│  └─────────────┘    └─────────────┘    └─────────────┘                  │
│        │                  │                  │                          │
│        ▼                  ▼                  ▼                          │
│   检测语言/框架      TDD原则检查         MC/DC设计                       │
│   建立TODO列表       必要时重构          场景分类                        │
│   基线覆盖率         依赖注入检查        参数化测试                       │
│                                                                          │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐                  │
│  │ 4.代码生成  │───▶│ 5.分轮提升  │───▶│ 6.验证保证  │                  │
│  │             │    │             │    │             │                  │
│  └─────────────┘    └─────────────┘    └─────────────┘                  │
│        │                  │                  │                          │
│        ▼                  ▼                  ▼                          │
│   生成测试类          5轮迭代           编译检查                         │
│   实现测试方法        每轮验证          运行测试                         │
│   添加Mock           分析未覆盖         覆盖率报告                       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

## 快速参考

| 阶段 | 关键动作 | 产出 |
|------|----------|------|
| 1. 项目分析 | 检测语言、框架、结构 | TODO列表、基线覆盖率 |
| 2. 可测试性审查 | TDD原则检查、重构建议 | 重构计划（如需要） |
| 3. 测试策略 | MC/DC设计、场景分类 | 测试用例设计文档 |
| 4. 代码生成 | 生成测试类和方法 | 测试代码文件 |
| 5. 分轮提升 | 5轮迭代提升覆盖率 | 每轮覆盖率报告 |
| 6. 验证保证 | 编译、运行、报告 | 最终质量报告 |

## 详细步骤

### 1. 项目分析阶段

#### 1.1 检测项目类型

使用 Glob 工具检测项目根目录的特征文件：

| 语言 | 特征文件 | 源码目录 | 测试目录 |
|------|---------|----------|----------|
| Java | `pom.xml` / `build.gradle` | `src/main/java` | `src/test/java` |
| Go | `go.mod` | `.` | `.` (同目录 `*_test.go`) |
| Python | `requirements.txt` / `pyproject.toml` | `src/` 或 `.` | `tests/` |
| TypeScript | `package.json` + `tsconfig.json` | `src/` | `__tests__/` 或 `*.spec.ts` |

#### 1.2 识别测试框架

| 语言 | 检测方式 | 常见框架 |
|------|---------|----------|
| Java | `pom.xml` 依赖 | JUnit 5, TestNG, Spock |
| Go | `go.mod` 依赖 | testing (内置), testify |
| Python | `requirements.txt` | pytest, unittest |
| TypeScript | `package.json` devDependencies | Jest, Mocha, Jasmine |

#### 1.3 建立测试任务 TODO 列表

```markdown
# 测试任务列表

## 高优先级（核心业务）
- [ ] UserService.java - 用户管理核心逻辑 - 复杂度:高
- [ ] OrderService.java - 订单处理逻辑 - 复杂度:高

## 中优先级（辅助功能）
- [ ] ValidationUtils.java - 验证工具类 - 复杂度:中

## 低优先级（简单代码）
- [ ] UserDTO.java - 数据传输对象 - 复杂度:低
```

#### 1.4 运行基线覆盖率测试

| 语言 | 命令 | 报告位置 |
|------|------|----------|
| Java | `./mvnw test jacoco:report` | `target/site/jacoco/index.html` |
| Go | `go test -coverprofile=coverage.out ./...` | `coverage.out` |
| Python | `pytest --cov=. --cov-report=html` | `htmlcov/index.html` |
| TypeScript | `npm test -- --coverage` | `coverage/lcov-report/index.html` |

### 2. 测试计划制定阶段

#### 2.1 项目规模评估

| 规模 | 代码行数 | 策略 |
|------|----------|------|
| 小型 | < 500 行 | 一次性生成所有测试 |
| 中型 | 500-5000 行 | 按模块分批，每批 3-5 个文件 |
| 大型 | > 5000 行 | 按功能模块划分，优先核心逻辑 |

#### 2.2 优先级排序

| 优先级 | 代码类型 | 示例 |
|--------|----------|------|
| 🔴 高 | 核心业务逻辑、对外接口 | OrderService, PaymentGateway |
| 🟡 中 | 辅助方法、工具类 | ValidationUtils, DateHelper |
| 🟢 低 | POJO/DTO、简单 getter/setter | UserDTO, OrderVO |

#### 2.3 执行计划模板

```markdown
# 测试生成执行计划

## 项目概览
- 语言: [Java/Go/Python/TypeScript]
- 文件数: [N] 个 | 代码行数: [M] 行
- 当前覆盖率: [X]%
- 目标覆盖率: [Y]%

## 批次计划
| 批次 | 目标文件 | 预期提升 | 关键测试点 |
|------|----------|----------|------------|
| 1 | UserService, OrderService | +15% | 用户创建、订单处理 |
| 2 | ValidationUtils | +5% | 边界值验证 |

## 风险与应对
| 风险 | 应对措施 |
|------|----------|
| 代码耦合度高 | 先重构，引入依赖注入 |
| 外部依赖多 | 使用 TestContainers |
```

### 3. 代码可测试性审查阶段

#### 3.1 TDD原则检查清单
- [ ] 单一职责原则（SRP）：类/函数只做一件事
- [ ] 依赖注入：支持外部依赖注入而非硬编码
- [ ] 接口隔离：使用接口抽象外部依赖
- [ ] 无全局状态：避免使用单例、全局变量
- [ ] 纯函数优先：相同输入产生相同输出

#### 3.2 代码重构模式
```java
// ❌ 不可测试：硬编码依赖
class UserService {
    private Database db = new MySQLDatabase();
    private EmailService email = new EmailService();
}

// ✅ 可测试：依赖注入
class UserService {
    private final Database db;
    private final EmailService email;

    @Inject
    public UserService(Database db, EmailService email) {
        this.db = db;
        this.email = email;
    }
}
```

#### 3.3 可测试性重构
- 提取方法：将大函数拆分为小函数
- 引入接口：为外部依赖创建接口
- 移除静态调用：改为实例方法调用
- 消除全局状态：使用参数传递

### 4. 测试策略制定阶段

#### 4.1 确定测试范围
根据代码复杂度和重要性确定测试优先级：
1. **高优先级**: 核心业务逻辑、对外接口、数据处理
2. **中优先级**: 辅助方法、工具类、配置类
3. **低优先级**: 简单getter/setter、POJO类

#### 4.2 设计测试用例
为每个方法设计以下类型的测试用例：
- **正常情况**: 输入有效数据，期望正常输出
- **边界情况**: 输入边界值，如空值、最大值、最小值
- **异常情况**: 输入无效数据，期望抛出异常
- **依赖情况**: 模拟外部依赖的不同响应

#### 4.3 MC/DC测试设计
```java
// 示例：复杂决策逻辑
public boolean approveLoan(User user, LoanRequest request) {
    // 条件1: 信用评分 >= 650
    boolean goodCredit = user.getCreditScore() >= 650;
    // 条件2: 负债率 <= 0.43
    boolean goodDebtRatio = user.getDebtToIncomeRatio() <= 0.43;
    // 条件3: 就业稳定性 >= 2年
    boolean stableEmployment = user.getEmploymentYears() >= 2;
    // 条件4: 贷款金额合理
    boolean reasonableAmount = request.getAmount()
        .compareTo(user.getAnnualIncome().multiply(BigDecimal.valueOf(4))) <= 0;

    // 决策：(条件1 AND 条件2 AND 条件3) OR (条件1 AND 条件4)
    return (goodCredit && goodDebtRatio && stableEmployment) ||
           (goodCredit && reasonableAmount);
}

// MC/DC测试用例设计
@Test
void testGoodCreditIndependence() {
    // 基线：goodCredit=false, 其他条件=true
    User user = User.builder()
        .creditScore(600)  // goodCredit = false
        .debtToIncomeRatio(0.35)  // goodDebtRatio = true
        .employmentYears(5)  // stableEmployment = true
        .build();
    LoanRequest request = LoanRequest.builder()
        .amount(user.getAnnualIncome().multiply(BigDecimal.valueOf(3)))
        .build();

    assertFalse(approvalService.approveLoan(user, request));

    // 改变条件1：goodCredit=true, 保持其他不变
    user.setCreditScore(700);
    assertTrue(approvalService.approveLoan(user, request));
}
```

#### 4.4 测试场景分类
1. **正常场景（Happy Path）**
   - 典型业务流程
   - 标准输入值
   - 成功路径验证

2. **异常场景（Error Cases）**
   - 无效输入
   - 业务规则违反
   - 系统异常处理

3. **边界值测试（Boundary Values）**
   - 最小值、最小值-1、最小值+1
   - 最大值、最大值-1、最大值+1
   - 零值、null、空集合

4. **随机值测试（Random Values）**
   - 使用固定种子的随机数生成器
   - 覆盖更多组合场景
   - 确保可重现

5. **并发场景（Concurrency）**
   - 多线程访问
   - 竞态条件
   - 死锁检测

#### 4.5 选择测试模式
根据被测代码的特点选择合适的测试模式：
- **状态验证**: 验证对象的状态变化
- **行为验证**: 验证方法的调用行为
- **交互验证**: 验证对象间的交互过程

### 5. 分轮覆盖率提升阶段

执行最多5轮提升，每轮1%-5%：

#### Round 1: 快速胜利（+5%）
- 添加基础测试用例
- 覆盖明显的代码路径
- 测试公共API

#### Round 2: 核心逻辑（+5%）
- 覆盖业务逻辑分支
- 添加错误处理测试
- 测试边界条件

#### Round 3: 边界和异常（+3%）
- 完善边界值测试
- 异常场景覆盖
- 空值/null处理

#### Round 4: 复杂场景（+2%）
- 集成测试覆盖
- 并发访问测试
- 复杂条件组合

#### Round 5: 最终冲刺（+剩余）
- 覆盖剩余代码
- Hard-to-reach代码
- 私有/静态方法

每轮后：
1. 运行完整测试套件：确保所有测试通过
2. 生成覆盖率报告：分析未覆盖代码
3. 识别下轮目标：选择最有价值的覆盖点

### 6. 测试代码生成阶段

#### 6.1 生成测试类结构
```java
// Java示例
public class UserServiceTest {

    // 被测对象
    private UserService userService;

    // Mock对象
    @Mock
    private UserRepository userRepository;

    // 测试初始化
    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        userService = new UserService(userRepository);
    }

    // 测试方法
    @Test
    void testGetUserById_Success() {
        // Arrange

        // Act

        // Assert
    }
}
```

#### 6.2 实现具体测试方法
按照AAA模式实现每个测试方法：

**Arrange (准备阶段)**:
- 初始化测试数据
- 创建Mock对象和期望行为
- 构造被测对象

**Act (执行阶段)**:
- 调用被测方法
- 获取执行结果

**Assert (断言阶段)**:
- 验证返回结果
- 验证Mock对象的调用行为
- 验证系统状态变化

#### 6.3 添加测试数据管理
```java
// 测试数据工厂模式
public class TestDataFactory {

    public static User createUser() {
        User user = new User();
        user.setId(1L);
        user.setName("Test User");
        user.setEmail("test@example.com");
        return user;
    }

    public static List<User> createUsers(int count) {
        List<User> users = new ArrayList<>();
        for (int i = 0; i < count; i++) {
            User user = new User();
            user.setId((long)i);
            user.setName("Test User " + i);
            user.setEmail("test" + i + "@example.com");
            users.add(user);
        }
        return users;
    }
}
```

### 7. 测试验证阶段

#### 7.1 运行测试
```bash
# Java项目
./mvnw test

# 或者
./gradlew test

# Go项目
go test ./...

# Python项目
python -m pytest

# TypeScript项目
npm test
```

#### 7.2 检查测试覆盖率
```bash
# Java (JaCoCo)
./mvnw jacoco:report

# Go
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Python
coverage run -m pytest
coverage report

# TypeScript
npm test -- --coverage
```

#### 7.3 修复失败测试
分析失败的测试用例，可能的原因：
- 测试数据不正确
- Mock行为设置有误
- 断言条件不准确
- 被测代码存在缺陷

#### 7.4 质量保证验证
```bash
# 最终验证步骤
1. 编译检查
   Java: mvn compile 或 gradle build
   Python: python -m py_compile
   Go: go build ./...
   Rust: cargo check

2. 运行测试套件
   Java: mvn test
   Python: pytest -v
   Go: go test -v ./...
   Rust: cargo test

3. 生成覆盖率报告
   Java: mvn jacoco:report
   Python: pytest --cov=app --cov-report=html
   Go: go tool cover -html=coverage.out
   Rust: cargo tarpaulin --out Html

4. 变异测试（可选）
   Java: mvn org.pitest:pitest-maven:mutationCoverage
   Python: mutmut run
   Go: go-mutesting ./...
```

## 最佳实践

### 1. 测试代码质量
- 保持测试代码简洁易懂
- 避免在测试中包含复杂逻辑
- 使用描述性的测试方法名
- 每个测试方法只测试一个功能点

### 2. 测试维护
- 定期更新失效的测试
- 删除不再需要的测试
- 重构重复的测试代码
- 保持测试与生产代码同步

### 3. 性能优化
- 避免在测试中进行网络请求
- 使用内存数据库替代真实数据库
- 重用测试资源和对象
- 并行执行独立的测试

### 4. 资源层集成测试
- **真实资源**：数据库、Redis、消息队列等使用TestContainers或真实测试实例
- **避免Mock**：资源访问层不使用Mock，确保端到端验证
- **外部服务Mock**：仅对第三方API和外部服务使用Mock或WireMock

## 常见问题及解决方案

### 1. 依赖注入问题
**问题**: 被测类依赖太多外部服务
**解决方案**: 使用依赖注入框架或手动注入Mock对象

### 2. 时间相关测试
**问题**: 测试涉及时间相关的逻辑
**解决方案**: 使用时间工具类并允许注入当前时间

### 3. 随机数据问题
**问题**: 测试中使用随机数据导致不稳定
**解决方案**: 固定种子或使用确定性数据

### 4. 覆盖率提升瓶颈
**问题**: 难以覆盖某些代码分支
**解决方案**:
- 使用Mock覆盖难以到达的代码
- 覆盖日志和监控代码
- 覆盖异常处理

## 输出标准

生成的测试代码应满足以下标准：

### 测试统计摘要
```
测试文件创建/修改: XX个
新增测试用例: XX个
测试执行时间: XX秒
测试通过率: 100%
```

### 覆盖率提升报告
```
语言: Java/Python/Go/Rust
测试前覆盖率: XX%
测试后覆盖率: XX%
提升幅度: +XX%

行覆盖率: XX%
分支覆盖率: XX%
函数覆盖率: XX%
```

### 未覆盖代码分析
```
文件路径: xxx
未覆盖行数: XX
未覆盖原因:
  - 配置加载分支
  - 极端错误处理
  - 已废弃代码路径
建议:
  - 可以安全忽略
  - 建议添加xxx测试
```

### 测试质量评估
```
✅ 测试覆盖了所有公共API
✅ 异常场景测试完整
✅ 边界值测试充分
⚠️  建议添加更多并发场景
✅ 使用了真实的资源层测试
```