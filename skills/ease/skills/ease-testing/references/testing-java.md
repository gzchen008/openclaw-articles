# Java 测试生成参考文档

本指南提供了为 Java 项目生成单元测试代码的具体规范和最佳实践。

## 测试框架选择

### 主要测试框架

1. **JUnit 5**: 现代化的测试框架，推荐用于新项目
2. **Mockito**: Mock框架，用于创建和管理Mock对象
3. **AssertJ**: 流畅的断言库，提供更好的断言体验
4. **Testcontainers**: 用于集成测试的容器化依赖管理

### Maven依赖配置

```xml
<dependencies>
    <!-- JUnit 5 -->
    <dependency>
        <groupId>org.junit.jupiter</groupId>
        <artifactId>junit-jupiter</artifactId>
        <version>5.10.0</version>
        <scope>test</scope>
    </dependency>

    <!-- Mockito -->
    <dependency>
        <groupId>org.mockito</groupId>
        <artifactId>mockito-core</artifactId>
        <version>5.7.0</version>
        <scope>test</scope>
    </dependency>

    <!-- AssertJ -->
    <dependency>
        <groupId>org.assertj</groupId>
        <artifactId>assertj-core</artifactId>
        <version>3.24.2</version>
        <scope>test</scope>
    </dependency>
</dependencies>
```

## 测试类结构规范

### 基础测试类模板

```java
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.Mockito.*;

class UserServiceTest {

    // 被测对象
    private UserService userService;

    // Mock依赖
    @Mock
    private UserRepository userRepository;

    @Mock
    private EmailService emailService;

    @BeforeEach
    void setUp() {
        MockitoAnnotations.openMocks(this);
        userService = new UserService(userRepository, emailService);
    }

    @Test
    void testMethodName_Condition_ExpectedBehavior() {
        // Given (准备测试数据)

        // When (执行被测方法)

        // Then (验证结果)
    }
}
```

### 测试方法命名规范

采用 `testMethodName_Condition_ExpectedBehavior` 的命名模式：

```java
@Test
void getUserById_UserExists_ReturnsUser() {
    // 测试getUserById方法，当用户存在时，应该返回用户对象
}

@Test
void getUserById_UserNotFound_ThrowsException() {
    // 测试getUserById方法，当用户不存在时，应该抛出异常
}

@Test
void createUser_ValidUser_SendsWelcomeEmail() {
    // 测试createUser方法，当用户提供有效信息时，应该发送欢迎邮件
}
```

## Mock使用规范

### Mockito基本用法

```java
// Mock对象创建
@Mock
private UserRepository userRepository;

// Stub行为定义
when(userRepository.findById(1L)).thenReturn(Optional.of(user));

// 验证方法调用
verify(userRepository).findById(1L);

// 验证方法调用次数
verify(userRepository, times(1)).findById(1L);
verify(userRepository, never()).deleteById(anyLong());
```

### 常见Mock场景

#### 1. 返回固定值
```java
when(userRepository.findById(1L)).thenReturn(Optional.of(user));
```

#### 2. 抛出异常
```java
when(userRepository.findById(1L)).thenThrow(new UserNotFoundException("User not found"));
```

#### 3. 根据参数返回不同值
```java
when(userRepository.findById(1L)).thenReturn(Optional.of(user1));
when(userRepository.findById(2L)).thenReturn(Optional.of(user2));
```

#### 4. 使用参数匹配器
```java
when(userRepository.save(argThat(user -> user.getEmail().contains("@")))).thenReturn(savedUser);
```

## 断言规范

### 使用AssertJ进行断言

```java
// 基本断言
assertThat(result).isNotNull();
assertThat(name).isEqualTo("John");
assertThat(age).isGreaterThan(18);

// 集合断言
assertThat(users).hasSize(3);
assertThat(names).containsExactly("Alice", "Bob", "Charlie");

// 异常断言
assertThatThrownBy(() -> userService.getUserById(-1L))
    .isInstanceOf(IllegalArgumentException.class)
    .hasMessage("User ID must be positive");

// 对象属性断言
assertThat(user)
    .extracting(User::getName, User::getEmail)
    .containsExactly("John", "john@example.com");
```

## 测试数据管理

### 测试数据工厂

```java
public class UserTestDataFactory {

    public static User createUser() {
        return createUser("John", "john@example.com");
    }

    public static User createUser(String name, String email) {
        User user = new User();
        user.setId(1L);
        user.setName(name);
        user.setEmail(email);
        user.setCreatedAt(LocalDateTime.now());
        return user;
    }

    public static List<User> createUsers(int count) {
        List<User> users = new ArrayList<>();
        for (int i = 1; i <= count; i++) {
            User user = new User();
            user.setId((long) i);
            user.setName("User " + i);
            user.setEmail("user" + i + "@example.com");
            users.add(user);
        }
        return users;
    }
}
```

### 使用@TestInstance管理测试实例

```java
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class UserServiceIntegrationTest {

    private DatabaseContainer dbContainer;

    @BeforeAll
    void setUpAll() {
        dbContainer = new DatabaseContainer();
        dbContainer.start();
    }

    @AfterAll
    void tearDownAll() {
        dbContainer.stop();
    }
}
```

## 不同类型代码的测试策略

### 1. Service层测试

```java
@Test
void createUser_ValidUser_CreatesUserAndSendsEmail() {
    // Given
    UserDto userDto = new UserDto("John", "john@example.com");
    User user = UserTestDataFactory.createUser("John", "john@example.com");

    when(userRepository.save(any(User.class))).thenReturn(user);

    // When
    User result = userService.createUser(userDto);

    // Then
    assertThat(result).isNotNull();
    assertThat(result.getName()).isEqualTo("John");

    verify(userRepository).save(argThat(u ->
        u.getName().equals("John") && u.getEmail().equals("john@example.com")));
    verify(emailService).sendWelcomeEmail("john@example.com");
}
```

### 2. Controller层测试

```java
@WebMvcTest(UserController.class)
class UserControllerTest {

    @Autowired
    private MockMvc mockMvc;

    @MockBean
    private UserService userService;

    @Test
    void getUserById_UserExists_ReturnsUser() throws Exception {
        // Given
        User user = UserTestDataFactory.createUser();
        when(userService.getUserById(1L)).thenReturn(user);

        // When & Then
        mockMvc.perform(get("/users/1"))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("John"))
                .andExpect(jsonPath("$.email").value("john@example.com"));

        verify(userService).getUserById(1L);
    }
}
```

### 3. Repository层测试

```java
@DataJpaTest
class UserRepositoryTest {

    @Autowired
    private TestEntityManager entityManager;

    @Autowired
    private UserRepository userRepository;

    @Test
    void findByEmail_UserExists_ReturnsUser() {
        // Given
        User user = UserTestDataFactory.createUser();
        entityManager.persistAndFlush(user);

        // When
        Optional<User> result = userRepository.findByEmail("john@example.com");

        // Then
        assertThat(result).isPresent();
        assertThat(result.get().getName()).isEqualTo("John");
    }
}
```

## 测试覆盖率要求

### 代码覆盖率指标

- **行覆盖率**: ≥ 80%
- **分支覆盖率**: ≥ 70%
- **方法覆盖率**: ≥ 85%

### 覆盖率检查配置

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.11</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
        <execution>
            <id>check</id>
            <goals>
                <goal>check</goal>
            </goals>
            <configuration>
                <rules>
                    <rule>
                        <element>BUNDLE</element>
                        <limits>
                            <limit>
                                <counter>LINE</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.80</minimum>
                            </limit>
                            <limit>
                                <counter>BRANCH</counter>
                                <value>COVEREDRATIO</value>
                                <minimum>0.70</minimum>
                            </limit>
                        </limits>
                    </rule>
                </rules>
            </configuration>
        </execution>
    </executions>
</plugin>
```

## 常见测试模式

### 1. Builder模式测试

```java
@Test
void userBuilder_BuildsUserWithCorrectProperties() {
    User user = User.builder()
            .id(1L)
            .name("John")
            .email("john@example.com")
            .build();

    assertThat(user.getId()).isEqualTo(1L);
    assertThat(user.getName()).isEqualTo("John");
    assertThat(user.getEmail()).isEqualTo("john@example.com");
}
```

### 2. 异常测试

```java
@Test
void createUser_NullName_ThrowsIllegalArgumentException() {
    assertThatThrownBy(() -> userService.createUser(null, "john@example.com"))
            .isInstanceOf(IllegalArgumentException.class)
            .hasMessage("Name cannot be null or empty");
}
```

### 3. 时间相关测试

```java
@Test
void userCreation_SetsCreatedAt() {
    // Given
    LocalDateTime before = LocalDateTime.now();

    // When
    User user = userService.createUser("John", "john@example.com");
    LocalDateTime after = LocalDateTime.now();

    // Then
    assertThat(user.getCreatedAt()).isBetween(before, after);
}
```

## 最佳实践

### 1. 测试隔离

```java
// 每个测试方法独立运行，不共享状态
@Test
void test1() {
    // 测试逻辑
}

@Test
void test2() {
    // 独立的测试逻辑，不受test1影响
}
```

### 2. 避免测试间依赖

```java
// 不要在测试间共享数据或状态
class BadExample {
    private static User sharedUser; // 避免这样做

    @Test
    void test1() {
        sharedUser = createUser(); // 避免这样做
    }

    @Test
    void test2() {
        assertThat(sharedUser).isNotNull(); // 避免这样做
    }
}
```

### 3. 清晰的测试意图

```java
// 好的命名清楚表达了测试意图
@Test
void calculateDiscount_OrderOver100_Returns10PercentDiscount() {
    // 测试逻辑
}

// 避免模糊的命名
@Test
void test1() { // 不推荐
    // 测试逻辑
}
```

## MC/DC测试设计

### MC/DC原则说明

MC/DC (Modified Condition/Decision Coverage) 是一种严格的测试覆盖准则，要求：
- **条件独立性**：每个条件独立影响决策结果
- **分支全覆盖**：所有分支路径都被测试
- **边界值测试**：测试输入域的边界及其附近值

### 复杂决策逻辑的MC/DC测试示例

```java
// 贷款审批决策逻辑
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
```

### MC/DC测试用例设计

```java
@Test
void testGoodCreditIndependence() {
    // 基线：goodCredit=false, 其他条件=true
    User user = User.builder()
        .id(1L)
        .name("Test User")
        .creditScore(600)  // goodCredit = false
        .debtToIncomeRatio(0.35)  // goodDebtRatio = true
        .employmentYears(5)  // stableEmployment = true
        .annualIncome(new BigDecimal("50000"))
        .build();

    LoanRequest request = LoanRequest.builder()
        .id(1L)
        .amount(new BigDecimal("150000"))  // 合理金额
        .build();

    assertFalse(loanService.approveLoan(user, request));

    // 改变条件1：goodCredit=true, 保持其他不变
    user.setCreditScore(700);  // goodCredit = true
    assertTrue(loanService.approveLoan(user, request));
}

@Test
void testGoodDebtRatioIndependence() {
    // 基线：goodDebtRatio=false, 其他条件=true
    User user = User.builder()
        .id(1L)
        .name("Test User")
        .creditScore(700)  // goodCredit = true
        .debtToIncomeRatio(0.50)  // goodDebtRatio = false
        .employmentYears(5)  // stableEmployment = true
        .annualIncome(new BigDecimal("50000"))
        .build();

    LoanRequest request = LoanRequest.builder()
        .id(1L)
        .amount(new BigDecimal("150000"))  // 合理金额
        .build();

    assertFalse(loanService.approveLoan(user, request));

    // 改变条件2：goodDebtRatio=true, 保持其他不变
    user.setDebtToIncomeRatio(0.35);  // goodDebtRatio = true
    assertTrue(loanService.approveLoan(user, request));
}

@Test
void testStableEmploymentIndependence() {
    // 基线：stableEmployment=false, 其他条件=true
    User user = User.builder()
        .id(1L)
        .name("Test User")
        .creditScore(700)  // goodCredit = true
        .debtToIncomeRatio(0.35)  // goodDebtRatio = true
        .employmentYears(1)  // stableEmployment = false
        .annualIncome(new BigDecimal("50000"))
        .build();

    LoanRequest request = LoanRequest.builder()
        .id(1L)
        .amount(new BigDecimal("150000"))  // 合理金额
        .build();

    assertFalse(loanService.approveLoan(user, request));

    // 改变条件3：stableEmployment=true, 保持其他不变
    user.setEmploymentYears(3);  // stableEmployment = true
    assertTrue(loanService.approveLoan(user, request));
}

@Test
void testReasonableAmountIndependence() {
    // 基线：reasonableAmount=false, 其他条件=true（除了条件3）
    User user = User.builder()
        .id(1L)
        .name("Test User")
        .creditScore(700)  // goodCredit = true
        .debtToIncomeRatio(0.35)  // goodDebtRatio = true
        .employmentYears(1)  // stableEmployment = false
        .annualIncome(new BigDecimal("50000"))
        .build();

    LoanRequest request = LoanRequest.builder()
        .id(1L)
        .amount(new BigDecimal("250000"))  // 不合理金额 (> 4倍年收入)
        .build();

    assertFalse(loanService.approveLoan(user, request));

    // 改变条件4：reasonableAmount=true, 保持其他不变
    request.setAmount(new BigDecimal("150000"));  // 合理金额
    assertTrue(loanService.approveLoan(user, request));
}
```

### 边界值测试示例

```java
@Test
void testCreditScoreBoundaryValues() {
    User user = User.builder()
        .id(1L)
        .name("Test User")
        .debtToIncomeRatio(0.35)
        .employmentYears(5)
        .annualIncome(new BigDecimal("50000"))
        .build();

    LoanRequest request = LoanRequest.builder()
        .id(1L)
        .amount(new BigDecimal("150000"))
        .build();

    // 边界值测试：649 (失败)
    user.setCreditScore(649);
    assertFalse(loanService.approveLoan(user, request));

    // 边界值测试：650 (成功)
    user.setCreditScore(650);
    assertTrue(loanService.approveLoan(user, request));

    // 边界值测试：651 (成功)
    user.setCreditScore(651);
    assertTrue(loanService.approveLoan(user, request));
}

@Test
void testDebtToIncomeRatioBoundaryValues() {
    User user = User.builder()
        .id(1L)
        .name("Test User")
        .creditScore(700)
        .employmentYears(5)
        .annualIncome(new BigDecimal("50000"))
        .build();

    LoanRequest request = LoanRequest.builder()
        .id(1L)
        .amount(new BigDecimal("150000"))
        .build();

    // 边界值测试：0.44 (失败)
    user.setDebtToIncomeRatio(0.44);
    assertFalse(loanService.approveLoan(user, request));

    // 边界值测试：0.43 (成功)
    user.setDebtToIncomeRatio(0.43);
    assertTrue(loanService.approveLoan(user, request));

    // 边界值测试：0.42 (成功)
    user.setDebtToIncomeRatio(0.42);
    assertTrue(loanService.approveLoan(user, request));
}
```

## 测试生成模板

### Service测试模板

```java
@Test
void methodName_Condition_ExpectedResult() {
    // Given
    // 准备测试数据和Mock行为

    // When
    // 调用被测方法

    // Then
    // 验证结果和Mock调用
}
```

### Controller测试模板

```java
@Test
void endpoint_Condition_ReturnsExpectedResponse() throws Exception {
    // Given
    // 准备测试数据和Mock行为

    // When & Then
    mockMvc.perform(post("/endpoint")
            .contentType(MediaType.APPLICATION_JSON)
            .content("{\"key\":\"value\"}"))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.result").value("expected"));
}
```

### MC/DC测试模板

```java
@Test
void testConditionIndependence() {
    // 基线：目标条件=false, 其他条件=true
    TestData testData = TestData.builder()
        .targetCondition(false)  // 目标条件设为false
        .otherConditions(true)   // 其他条件设为true
        .build();

    assertFalse(service.evaluateDecision(testData));

    // 改变目标条件：目标条件=true, 保持其他不变
    testData.setTargetCondition(true);  // 目标条件设为true
    assertTrue(service.evaluateDecision(testData));
}
```

通过遵循这些规范和最佳实践，可以生成高质量、可维护的Java单元测试代码。