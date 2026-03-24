# 工具库

## 1. 公共方法库分析

### 1.1 基础工具类 (base/common/util)

#### 1.1.1 字符串处理工具 (CommonUtils, StringUtils)
提供字符串处理、验证、转换等常用功能，广泛应用于各个模块：

**主要方法**:
- `isEmpty(String str)`: 判断字符串是否为空
- `isNotEmpty(String str)`: 判断字符串是否非空
- `trimToEmpty(String str)`: 去除空格，null转为空字符串
- `substring(String str, int start, int end)`: 安全截取字符串
- `join(Collection<?> collection, String separator)`: 集合转字符串
- `split(String str, String separator)`: 字符串分割
- `toUpperCase(String str)`: 转大写
- `toLowerCase(String str)`: 转小写

#### 1.1.2 日期时间工具 (DateUtils)
提供日期时间处理、格式化、计算等功能，在交易日志和数据处理中广泛使用：

**主要方法**:
- `formatDate(Date date, String pattern)`: 日期格式化
- `parseDate(String dateStr, String pattern)`: 字符串转日期
- `addDays(Date date, int amount)`: 日期加减天数
- `calculateAge(Date birthDate)`: 计算年龄
- `isSameDay(Date date1, Date date2)`: 判断是否同一天
- `getBeginOfDay(Date date)`: 获取当天开始时间
- `getEndOfDay(Date date)`: 获取当天结束时间

#### 1.1.3 身份证处理工具 (IDCard)
专门处理中国身份证号码的验证和信息提取，在个人客户管理模块中核心使用：

**主要方法**:
- `validateIdCard(String idCard)`: 身份证号码验证
- `extractBirthDate(String idCard)`: 提取出生日期
- `extractGender(String idCard)`: 提取性别信息
- `extractAreaCode(String idCard)`: 提取地区代码
- `calculateCheckCode(String idCard)`: 计算校验码
- `getAgeByIdCard(String idCard)`: 根据身份证获取年龄
- `getBirthdayByIdCard(String idCard)`: 根据身份证获取生日

#### 1.1.4 数据脱敏工具 (MaskUtil, StringMaskUtils)
提供敏感数据脱敏处理功能，用于保护客户隐私信息：

**主要方法**:
- `maskMobile(String mobile)`: 手机号脱敏 (138****8000)
- `maskIdCard(String idCard)`: 身份证号脱敏 (1101**********1234)
- `maskName(String name)`: 姓名脱敏 (张*)
- `maskEmail(String email)`: 邮箱脱敏 (z***@example.com)
- `maskBankCard(String bankCard)`: 银行卡号脱敏 (6222****1234)

### 1.2 业务工具类 (personal/common/util)

#### 1.2.1 地址验证服务 (AddressCheckService)
提供地址信息的验证和标准化处理：

**主要方法**:
- `validateProvinceCode(String provinceCode)`: 省份代码验证
- `validateCityCode(String cityCode)`: 城市代码验证
- `validateDistrictCode(String districtCode)`: 区县代码验证
- `standardizeAddress(String address)`: 地址标准化
- `getAreaNameByCode(String areaCode)`: 根据代码获取地区名称

#### 1.2.2 电话验证服务 (TelephoneCheckService)
提供电话号码的验证和格式化：

**主要方法**:
- `validateMobile(String mobile)`: 手机号验证
- `validateLandline(String landline)`: 固定电话验证
- `formatTelephoneNumber(String tel)`: 电话号码格式化
- `getAreaCodeByCity(String city)`: 根据城市获取区号
- `isTelecomNumber(String number)`: 判断电信号码

#### 1.2.3 邮箱验证工具 (EmailAddress)
提供邮箱地址的验证和处理：

**主要方法**:
- `isValidEmail(String email)`: 邮箱格式验证
- `extractDomain(String email)`: 提取邮箱域名
- `maskEmail(String email)`: 邮箱脱敏
- `getMailServer(String email)`: 获取邮件服务器
- `normalizeEmail(String email)`: 邮箱标准化

## 2. 第三方依赖梳理

### 2.1 核心框架依赖

#### 2.1.1 Spring Boot生态系统
```gradle
// Spring Boot核心
implementation 'org.springframework.boot:spring-boot-starter-web:3.5.5'
implementation 'org.springframework.boot:spring-boot-starter-data-redis:3.5.5'
implementation 'org.springframework.boot:spring-boot-starter-jdbc:3.5.5'
implementation 'org.springframework.boot:spring-boot-starter-actuator:3.5.5'

// Spring Boot测试
testImplementation 'org.springframework.boot:spring-boot-starter-test:3.5.5'
```

#### 2.1.2 Webank内部框架
```gradle
// Mumble SDK框架
implementation 'cn.webank:mumble-sdk:4.1.1'
implementation 'cn.webank:mumble-framework-common:4.1.1'

// FPS文件服务客户端
implementation 'cn.webank:fps-client:1.4.6'
```

### 2.2 数据库相关依赖

#### 2.2.1 数据库驱动
```gradle
// MySQL驱动
implementation 'mysql:mysql-connector-java:8.0.33'

// MyBatis框架
implementation 'org.mybatis.spring.boot:mybatis-spring-boot-starter:2.3.1'
implementation 'com.baomidou:mybatis-plus-boot-starter:3.5.3.1'
```

#### 2.2.2 连接池和缓存
```gradle
// Redis客户端
implementation 'org.springframework.boot:spring-boot-starter-data-redis:3.5.5'
implementation 'io.lettuce:lettuce-core:6.2.8.RELEASE'

// 数据库连接池
implementation 'com.alibaba:druid-spring-boot-starter:1.2.16'
```

### 2.3 工具类库依赖

#### 2.3.1 Apache Commons系列
```gradle
implementation 'org.apache.commons:commons-lang3:3.12.0'
implementation 'org.apache.commons:commons-collections4:4.4'
implementation 'org.apache.commons:commons-io:2.11.0'
implementation 'commons-codec:commons-codec:1.15'
```

#### 2.3.2 JSON处理
```gradle
implementation 'com.fasterxml.jackson.core:jackson-databind:2.15.2'
implementation 'com.fasterxml.jackson.datatype:jackson-datatype-jsr310:2.15.2'
```

#### 2.3.3 其他工具库
```gradle
implementation 'org.projectlombok:lombok:1.18.30'
implementation 'com.google.guava:guava:32.1.1-jre'
implementation 'org.apache.httpcomponents:httpclient:4.5.14'
```

## 3. 自定义注解

### 3.1 数据脱敏注解 (@MumbleMaskData)

**注解定义**:
```java
@Target({ElementType.FIELD})
@Retention(RetentionPolicy.RUNTIME)
public @interface MumbleMaskData {
    float maskProportion() default 0.5f;
    MaskType maskType() default MaskType.DEFAULT;
}
```

**使用场景**:
- 个人姓名脱敏: `@MumbleMaskData(maskProportion = 0.5f)`
- 身份证号脱敏: `@MumbleMaskData(maskProportion = 0.6f)`
- 手机号脱敏: `@MumbleMaskData(maskProportion = 0.4f)`

**处理机制**:
- 在数据返回前自动进行脱敏处理
- 支持不同的脱敏比例和类型
- 可配置的脱敏策略

### 3.2 JSON忽略注解 (@JsonIgnore)

**注解定义**:
```java
@Target({ElementType.FIELD, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
public @interface JsonIgnore {
    boolean value() default true;
}
```

**使用场景**:
- 敏感字段不返回给前端: `@JsonIgnore`
- 内部使用字段不序列化: `@JsonIgnore`
- 临时字段忽略处理: `@JsonIgnore`

### 3.3 业务注解

#### 3.3.1 应用ID类型注解 (@AppidType)
用于标识不同的应用ID类型和流量控制：

**主要枚举值**:
- `PERSONAL_CLIENT_QUERY`: 个人客户查询
- `PERSONAL_CLIENT_MODIFY`: 个人客户修改
- `FILE_UPLOAD`: 文件上传
- `BATCH_PROCESS`: 批量处理

## 4. 常量定义

### 4.1 系统常量类 (SystemCode, ErrorStatus)

#### 4.1.1 系统代码常量
```java
public class SystemCode {
    public static final String ECIF_CORE = "ECIFCORE";
    public static final String ECIF_BATCH = "ECIFBATCH";
    public static final String ECIF_WEB = "ECIFWEB";
    
    // 业务系统代码
    public static final String CCIF = "CCIF";
    public static final String FPS = "FPS";
    public static final String GNS = "GNS";
}
```

#### 4.1.2 错误状态码
```java
public class ErrorStatus {
    // 成功状态
    public static final String SUCCESS = "0000";
    public static final String SUCCESS_MSG = "成功";
    
    // 系统错误
    public static final String SYSTEM_ERROR = "9999";
    public static final String SYSTEM_ERROR_MSG = "系统错误";
    
    // 业务错误
    public static final String CLIENT_NOT_FOUND = "1001";
    public static final String CLIENT_NOT_FOUND_MSG = "客户不存在";
    
    public static final String INVALID_PARAMETER = "1002";
    public static final String INVALID_PARAMETER_MSG = "参数无效";
}
```

### 4.2 业务常量类

#### 4.2.1 证件类型常量
```java
public class IdTypeEnum {
    public static final String ID_CARD = "01"; // 身份证
    public static final String PASSPORT = "02"; // 护照
    public static final String MILITARY_ID = "03"; // 军官证
    public static final String HK_PASS = "04"; // 港澳通行证
    public static final String TW_PASS = "05"; // 台湾通行证
}
```

#### 4.2.2 客户状态常量
```java
public class EcifStatusEnum {
    public static final String ACTIVE = "A"; // 有效
    public static final String DISABLED = "D"; // 无效
    public static final String FROZEN = "F"; // 冻结
    public static final String CLOSED = "C"; // 关闭
}
```

## 5. 异常处理

### 5.1 自定义异常类

#### 5.1.1 业务异常 (BusinessException)
```java
public class BusinessException extends Exception {
    private String errorCode;
    private Object[] args;
    
    public BusinessException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }
    
    public BusinessException(String errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }
    
    // getters and setters
}
```

#### 5.1.2 系统异常 (SystemException)
```java
public class SystemException extends RuntimeException {
    private String errorCode;
    
    public SystemException(String errorCode, String message) {
        super(message);
        this.errorCode = errorCode;
    }
    
    public SystemException(String errorCode, String message, Throwable cause) {
        super(message, cause);
        this.errorCode = errorCode;
    }
    
    // getters and setters
}
```

### 5.2 异常处理工具方法

#### 5.2.1 异常转换工具
```java
public class ExceptionUtils {
    public static BusinessException convertToBusinessException(Exception e) {
        if (e instanceof BusinessException) {
            return (BusinessException) e;
        }
        return new BusinessException(ErrorStatus.SYSTEM_ERROR, e.getMessage(), e);
    }
    
    public static String getStackTraceAsString(Throwable throwable) {
        StringWriter sw = new StringWriter();
        PrintWriter pw = new PrintWriter(sw);
        throwable.printStackTrace(pw);
        return sw.toString();
    }
}
```

#### 5.2.2 错误码管理
```java
public class ErrorCodeManager {
    private static final Map<String, String> ERROR_MESSAGES = new HashMap<>();
    
    static {
        ERROR_MESSAGES.put(ErrorStatus.SUCCESS, ErrorStatus.SUCCESS_MSG);
        ERROR_MESSAGES.put(ErrorStatus.SYSTEM_ERROR, ErrorStatus.SYSTEM_ERROR_MSG);
        ERROR_MESSAGES.put(ErrorStatus.CLIENT_NOT_FOUND, ErrorStatus.CLIENT_NOT_FOUND_MSG);
        // 更多错误码映射
    }
    
    public static String getMessage(String errorCode) {
        return ERROR_MESSAGES.getOrDefault(errorCode, "未知错误");
    }
}
```

## 6. 工具类使用示例

### 6.1 身份证处理示例
```java
@Service
public class ClientValidationService {
    
    public boolean validateClientId(String idCard) {
        // 身份证格式验证
        if (!IDCard.validateIdCard(idCard)) {
            throw new BusinessException("INVALID_ID_CARD", "身份证格式不正确");
        }
        
        // 提取出生日期
        Date birthDate = IDCard.extractBirthDate(idCard);
        if (birthDate == null) {
            throw new BusinessException("INVALID_BIRTH_DATE", "无法提取出生日期");
        }
        
        // 年龄验证
        int age = DateUtils.calculateAge(birthDate);
        if (age < 18 || age > 150) {
            throw new BusinessException("INVALID_AGE", "年龄不在有效范围内");
        }
        
        return true;
    }
}
```

### 6.2 数据脱敏示例
```java
@RestController
public class ClientInfoController {
    
    @GetMapping("/client/{ecifNo}")
    public PersonalClient getClientInfo(@PathVariable String ecifNo) {
        PersonalClient client = clientService.queryClient(ecifNo);
        
        // 敏感信息脱敏已在DTO中通过注解自动处理
        // @MumbleMaskData(maskProportion = 0.5f) private String personalName;
        // @MumbleMaskData(maskProportion = 0.6f) private String personalIdentificationNumber;
        
        return client;
    }
}
```

### 6.3 配置工具使用示例
```java
@Component
public class ConfigurableService {
    
    @Value("${ecif.cache.expire-time:3600}")
    private int cacheExpireTime;
    
    @Value("${ecif.file.upload.max-size:10MB}")
    private String maxFileSize;
    
    @Autowired
    private DatabaseConfig databaseConfig;
    
    public void processData() {
        // 使用配置的缓存过期时间
        redisTemplate.expire(key, cacheExpireTime, TimeUnit.SECONDS);
        
        // 使用配置的最大文件大小
        long maxSize = parseFileSize(maxFileSize);
        if (file.getSize() > maxSize) {
            throw new BusinessException("FILE_TOO_LARGE", "文件大小超过限制");
        }
    }
    
    private long parseFileSize(String sizeStr) {
        // 解析文件大小配置
        return FileUtils.parseFileSize(sizeStr);
    }
}
```

## 7. 性能优化建议

### 7.1 工具类缓存
- 常用的工具方法结果可以缓存
- 避免重复计算相同的结果
- 使用ThreadLocal优化线程安全

### 7.2 资源管理
- 及时释放不需要的资源
- 合理使用连接池
- 避免内存泄漏

### 7.3 并发安全
- 工具类设计考虑线程安全
- 使用不可变对象
- 合理使用同步机制
