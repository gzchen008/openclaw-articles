/*
MumbleSDK Validation 模板（说明）
- 本文件为“模板示例”，为避免在 skills 仓库中触发 IDE/编译错误，示例代码整体置于该单一块注释中，且内部不包含任何会结束注释的字符序列。
- 使用时请复制下方【代码模板】内容到你们实际工程的 Java 源文件（例如：UserRegisterReq.java / CustomValidators.java），然后根据 quickstart.md 完成依赖与配置。

使用指南：
1) 复制【代码模板】到你们工程的 src/main/java 对应包路径下；
2) 替换包名、导入路径中的占位符为你们公司的实际包路径；
3) 引入 MumbleSDK、Spring Boot（validation）、Hibernate Validator 等依赖；
4) 在 Controller 上使用 @Validated，并在入参 DTO 上声明金融级校验注解；
5) 保证国际化 messages.properties 中包含对应的提示 Key。

---------------------------------------------------------------
【代码模板】（复制到你们的工程后使用）
---------------------------------------------------------------

// 文件路径建议：src/main/java/com/yourorg/project/dto/UserRegisterReq.java

package com.yourorg.project.dto;

import javax.validation.constraints.*;
import org.hibernate.validator.constraints.Length;

// ===== 以下为 MumbleSDK 金融级注解与校验器，替换为真实包名 =====
// import com.yourorg.mumble.validation.WebankNotBlank;
// import com.yourorg.mumble.validation.WebankMobilePhone;
// import com.yourorg.mumble.validation.WebankIdNo;
// import com.yourorg.mumble.validation.WebankEmail;
// import com.yourorg.mumble.validation.WebankCardNo;
// import com.yourorg.mumble.validation.WebankLength;
// ===============================================================

// 入参 DTO 示例：在 Controller 中通过 @Validated 进行校验
class UserRegisterReq {

    // 金融级非空（去空格后判断），消息 Key 建议写入 i18n 资源文件
    // @WebankNotBlank(message = "{user.mobile.required}")
    // @WebankMobilePhone(message = "{user.mobile.invalid}")
    private String mobile;

    // 身份证校验
    // @WebankIdNo(message = "{user.idno.invalid}")
    private String idNo;

    // 邮箱校验（如需要）
    // @WebankEmail(message = "{user.email.invalid}")
    private String email;

    // 银行卡号校验（如需要）
    // @WebankCardNo(message = "{user.cardno.invalid}")
    private String cardNo;

    // 长度校验示例（如用户名）
    // @WebankLength(min = 2, max = 30, message = "{user.username.length}")
    private String username;

    // 标准 Bean Validation 也可并用（如密码复杂度进一步校验）
    // @NotBlank(message = "{user.password.required}")
    // @Length(min = 8, max = 64, message = "{user.password.length}")
    private String password;

    // TODO: 其他字段与校验
}

// 文件路径建议：src/main/java/com/yourorg/project/validation/validators/MobilePhoneValidator.java

package com.yourorg.project.validation.validators;

// ===== 以下为 MumbleSDK 校验器基类/接口，替换为真实包名 =====
// import com.yourorg.mumble.validation.WebankConstraintValidator;
// import com.yourorg.mumble.validation.WebankMobilePhone;
// ===============================================================

import java.util.regex.Pattern;

// 示例：自定义手机号校验器（如需扩展/覆盖）
class MobilePhoneValidator { // [implements WebankConstraintValidator<WebankMobilePhone, String>]

    // 规则示例：以 1 开头的中国大陆手机号，长度 11
    private static final Pattern P = Pattern.compile("^1\\d{10}$");

    // public void initialize(WebankMobilePhone constraintAnnotation) {
    //     // 可读取注解上的参数，如地区码、允许的号段等
    // }

    // public boolean isValid(String value, javax.validation.ConstraintValidatorContext context) {
    //     if (value == null) return true; // 交由 NotBlank/NotNull 控制是否允许为空
    //     String v = value.trim();
    //     return P.matcher(v).matches();
    // }
}

// 文件路径建议：src/main/java/com/yourorg/project/controller/UserController.java

package com.yourorg.project.controller;

import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

// ===== 以下为统一响应、上下文与抽象控制器（替换为真实包名） =====
// import com.yourorg.mumble.web.MumbleAbstractBaseController;
// import com.yourorg.mumble.web.ResponseMessage;
// import com.yourorg.mumble.context.MumbleContextUtil;
// import com.yourorg.mumble.seq.MumbleSeqService;
// ===============================================================

class ResponseMessage<T> {
    public static <T> ResponseMessage<T> success(T data) { return new ResponseMessage<>(); }
    public static <T> ResponseMessage<T> bizError(String code, String msg) { return new ResponseMessage<>(); }
}

@RestController
@RequestMapping("/api/v1/user")
@Validated
class UserController { // [extends MumbleAbstractBaseController]

    // @PostMapping("/register")
    // public ResponseMessage<Void> register(@Validated @RequestBody UserRegisterReq req) {
    //     // Service 执行业务，校验失败将抛出 ConstraintViolationException 或 MethodArgumentNotValidException
    //     return ResponseMessage.success(null);
    // }
}

// i18n 示例（messages.properties）：
// user.mobile.required=手机号不能为空
// user.mobile.invalid=手机号格式不正确
// user.idno.invalid=身份证号码格式不正确
// user.email.invalid=邮箱格式不正确
// user.cardno.invalid=银行卡号格式不正确
// user.username.length=用户名长度需在 2 到 30 之间
// user.password.required=密码不能为空
// user.password.length=密码长度需在 8 到 64 之间

// 落地检查清单（摘自 integration-checklist.md）：
// - [ ] Controller 使用 @Validated 并对入参 DTO 进行校验
// - [ ] 使用金融级注解（WebankNotBlank/WebankMobilePhone/WebankIdNo 等）
// - [ ] 自定义校验器实现 WebankConstraintValidator（如需扩展）
// - [ ] 提示信息使用 i18n Key（messages.properties）
// - [ ] 校验失败时统一异常转换为标准错误响应（全局异常处理或抽象控制器）
// - [ ] 避免在校验器中进行数据库调用或耗时操作（仅做轻量规则校验）

---------------------------------------------------------------
【结束】
---------------------------------------------------------------
*/
