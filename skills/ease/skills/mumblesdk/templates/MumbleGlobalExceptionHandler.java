/*
[模板] 全局异常处理器（@ControllerAdvice + ResponseMessage 标准化）
- 本文件为“模板示例”，为避免在 skills 仓库中触发 IDE/编译错误，示例代码整体置于该单一块注释中。
- 使用时请复制下方【代码模板】内容到你们实际工程的 Java 源文件（例如：MumbleGlobalExceptionHandler.java），然后根据 quickstart.md 完成依赖与配置。

使用指南：
1) 复制【代码模板】到你们工程的 src/main/java 对应包路径下；
2) 替换包名、导入路径中的占位符为你们公司的实际包路径；
3) 引入 Spring Boot/Web、SLF4J 及 MumbleSDK 依赖；
4) 按 quickstart.md 配置 application-*.properties，确保 @ComponentScan 或包结构能扫描到；
5) 放入你们工程后，可将类改为 public 并命名与文件名一致（例如 MumbleGlobalExceptionHandler.java）。

---------------------------------------------------------------
【代码模板】（复制到你们的工程后使用）
---------------------------------------------------------------

// 文件路径建议：src/main/java/com/yourorg/project/web/MumbleGlobalExceptionHandler.java

package com.yourorg.project.web;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.core.Ordered;
import org.springframework.core.annotation.Order;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.BindException;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;

import javax.validation.ValidationException;
import java.util.stream.Collectors;

// ===== 以下为 MumbleSDK 相关类型，替换为你们项目中的实际包名 =====
// import com.yourorg.mumble.context.MumbleContextUtil;
// import com.yourorg.mumble.web.ResponseMessage;
// import com.yourorg.mumble.error.BusinessException;
// import com.yourorg.mumble.error.SystemException;
// ===============================================================

// 注意：复制到你们工程后，建议将类改为 public 并放入与类名同名的文件（MumbleGlobalExceptionHandler.java）
@ControllerAdvice
@Order(Ordered.HIGHEST_PRECEDENCE)
class MumbleGlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(MumbleGlobalExceptionHandler.class);

    /// 业务异常处理
    /// 建议返回 HTTP 200（业务失败由业务码区分），便于前端统一处理
    @ExceptionHandler(BusinessException.class)
    public ResponseEntity<ResponseMessage<?>> handleBusinessException(BusinessException e) {
        String bizSeqNo = safeBizSeqNo();
        log.warn("业务异常 - bizSeqNo={}, code={}, msg={}", bizSeqNo, e.getCode(), e.getMessage());
        ResponseMessage<?> body = ResponseMessage.bizError(e.getCode(), e.getMessage());
        return ResponseEntity.ok(body);
    }

    /// 校验异常处理（JSR-303/手工抛出 ValidationException）
    /// 建议返回 HTTP 400
    @ExceptionHandler(ValidationException.class)
    public ResponseEntity<ResponseMessage<?>> handleValidationException(ValidationException e) {
        String bizSeqNo = safeBizSeqNo();
        log.warn("参数校验异常 - bizSeqNo={}, msg={}", bizSeqNo, e.getMessage());
        ResponseMessage<?> body = ResponseMessage.bizError("VALIDATION_ERROR", e.getMessage());
        return ResponseEntity.badRequest().body(body);
    }

    /// @Valid/@Validated 触发的 MethodArgumentNotValidException
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ResponseMessage<?>> handleMethodArgumentNotValid(MethodArgumentNotValidException e) {
        String bizSeqNo = safeBizSeqNo();
        String msg = e.getBindingResult().getFieldErrors().stream()
                .map(err -> err.getField() + ":" + (err.getDefaultMessage() == null ? "invalid" : err.getDefaultMessage()))
                .collect(Collectors.joining("; "));
        log.warn("方法参数校验异常 - bizSeqNo={}, msg={}", bizSeqNo, msg);
        ResponseMessage<?> body = ResponseMessage.bizError("VALIDATION_ERROR", msg);
        return ResponseEntity.badRequest().body(body);
    }

    /// BindException（例如 @Validated + 表单绑定）处理
    @ExceptionHandler(BindException.class)
    public ResponseEntity<ResponseMessage<?>> handleBindException(BindException e) {
        String bizSeqNo = safeBizSeqNo();
        String msg = e.getBindingResult().getFieldErrors().stream()
                .map(err -> err.getField() + ":" + (err.getDefaultMessage() == null ? "invalid" : err.getDefaultMessage()))
                .collect(Collectors.joining("; "));
        log.warn("绑定异常 - bizSeqNo={}, msg={}", bizSeqNo, msg);
        ResponseMessage<?> body = ResponseMessage.bizError("VALIDATION_ERROR", msg);
        return ResponseEntity.badRequest().body(body);
    }

    /// 系统异常处理（内部异常不直接暴露）
    /// 建议返回 HTTP 200 + 标准系统错误码
    @ExceptionHandler(SystemException.class)
    public ResponseEntity<ResponseMessage<?>> handleSystemException(SystemException e) {
        String bizSeqNo = safeBizSeqNo();
        log.error("系统异常 - bizSeqNo={}, msg={}", bizSeqNo, e.getMessage(), e);
        ResponseMessage<?> body = ResponseMessage.sysError("SYS-999", "系统异常，请稍后重试");
        return ResponseEntity.ok(body);
    }

    /// 兜底异常处理
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ResponseMessage<?>> handleException(Exception e) {
        String bizSeqNo = safeBizSeqNo();
        log.error("未捕获异常 - bizSeqNo={}, msg={}", bizSeqNo, e.getMessage(), e);
        ResponseMessage<?> body = ResponseMessage.sysError("SYS-999", "系统异常，请稍后重试");
        return ResponseEntity.ok(body);
    }

    /// 读取业务流水号（空安全）
    private String safeBizSeqNo() {
        try {
            // return MumbleContextUtil.getBizSeqNo();
            return "UNKNOWN_BIZ_SEQ";
        } catch (Throwable ignore) {
            return "UNKNOWN_BIZ_SEQ";
        }
    }
}

// 落地检查清单（摘自 integration-checklist.md 与 quality-standards）：
// - [ ] 是否使用 @ControllerAdvice + @Order(Ordered.HIGHEST_PRECEDENCE) 提供全局异常处理
// - [ ] 响应统一为 ResponseMessage，业务/校验/系统异常的 code/message 符合规范
// - [ ] 业务异常返回 HTTP 200；校验异常返回 HTTP 400；系统异常避免泄露内部信息
// - [ ] 日志包含 bizSeqNo，结合 logback-spring.xml 的 MDC 格式
// - [ ] 与控制器异步范式（MumbleAbstractBaseController.execute(...)）兼容，前后文一致
// - [ ] 异常处理不做 DB/远程调用，只做格式化与记录

---------------------------------------------------------------
【结束】
---------------------------------------------------------------
*/
