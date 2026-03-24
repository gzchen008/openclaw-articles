/*
MumbleSDK Controller 模板（说明）
- 本文件是“模板示例”，为避免在 skills 仓库中触发 IDE/编译错误，示例代码整体被置于该单一块注释中。
- 使用时请复制下方【代码模板】内容到你们实际工程的 Java 源文件（例如：OrderController.java），然后根据 quickstart.md 完成依赖与配置。

使用指南：
1) 复制【代码模板】到你们工程的 src/main/java 对应包路径下；
2) 替换包名、导入路径中的占位符为你们公司的实际包路径；
3) 引入 MumbleSDK 及 Spring Boot/Web、SLF4J 依赖；
4) 按 quickstart.md 配置 application-*.properties；
5) 代码放入你们工程后，可将类改为 public 并命名与文件名一致（例如 OrderController.java）。

---------------------------------------------------------------
【代码模板】（复制到你们的工程后使用）
---------------------------------------------------------------

// 文件路径建议：src/main/java/com/yourorg/project/controller/OrderController.java

package com.yourorg.project.controller;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.context.request.async.DeferredResult;

import java.util.concurrent.Executor;
import java.util.concurrent.ForkJoinPool;

import javax.annotation.Resource;

// ===== 以下为 MumbleSDK 相关类型，替换为你们项目中的实际包名 =====
// import com.yourorg.mumble.web.MumbleAbstractBaseController;
// import com.yourorg.mumble.web.ResponseMessage;
// import com.yourorg.mumble.context.MumbleContextUtil;
// import com.yourorg.mumble.seq.MumbleSeqService;
// import com.yourorg.mumble.error.BusinessException;
// ===============================================================

// 占位：请替换为你们实际的 SDK 类型
class ResponseMessage<T> {
    public static <T> ResponseMessage<T> success(T data) { return new ResponseMessage<>(); }
    public static <T> ResponseMessage<T> success(T data, String bizSeqNo, String txnSeqNo) { return new ResponseMessage<>(); }
    public static <T> ResponseMessage<T> bizError(String code, String msg) { return new ResponseMessage<>(); }
    public static <T> ResponseMessage<T> sysError(String code, String msg) { return new ResponseMessage<>(); }
}

// 占位：请替换为你们实际的 SDK 类型
class MumbleContextUtil {
    public static void setBizSeqNo(String v) {}
    public static void setTxnSeqNo(String v) {}
    public static String getBizSeqNo() { return null; }
    public static void clear() {}
}

// 占位：请替换为你们实际的 SDK 类型
class MumbleSeqService {
    public String nextValue(String key) { return "SEQ_PLACEHOLDER"; }
}

// 占位：请替换为你们实际的 SDK 类型
class BusinessException extends RuntimeException {
    private final String code;
    public BusinessException(String code, String message) { super(message); this.code = code; }
    public String getCode() { return code; }
}

// 占位请求/响应 DTO，替换为你们的实际类型
class CreateOrderReq {
    // TODO: 使用金融级校验注解，如 @WebankNotBlank, @WebankMobilePhone 等
    // private String mobile;
}
class CreateOrderResp {
    // TODO: 填充响应字段
}

// 占位 Service，替换为你们的实际 Service
interface OrderService {
    CreateOrderResp createOrder(CreateOrderReq req);
}

// 注意：复制到你们工程后，建议将类改为 public 并放入与类名同名的文件（OrderController.java）
@RestController
@RequestMapping("/api/v1/order")
@Validated
class OrderController extends MumbleAbstractBaseController {

    private static final Logger log = LoggerFactory.getLogger(OrderController.class);

    // 推荐使用你们统一的序列服务
    @Resource
    private MumbleSeqService seqService;

    // 业务 Service
    @Resource
    private OrderService orderService;

    // Web 层线程池：可替换为你们在配置中定义的专用线程池
    @Override
    protected Executor getFrontTaskExecutor() {
        return ForkJoinPool.commonPool();
    }

    // 如果你们的 SDK 要求重写获取 BizSeqNo 的方式，可在此覆盖
    // @Override
    // protected String getBizSeqNo() { return MumbleContextUtil.getBizSeqNo(); }

    @PostMapping("/create")
    public DeferredResult<ResponseMessage<CreateOrderResp>> create(@Validated @RequestBody CreateOrderReq req) {
        return execute("OrderCreate", () -> {
            // 1) 生成并设置业务/交易流水
            final String bizSeqNo = seqService.nextValue("BIZ_SEQ_ORDER_CREATE");
            final String txnSeqNo = seqService.nextValue("TXN_SEQ_ORDER_CREATE");
            MumbleContextUtil.setBizSeqNo(bizSeqNo);
            MumbleContextUtil.setTxnSeqNo(txnSeqNo);

            try {
                // 2) 调用 Service 执行业务逻辑（事务在 Service 层）
                CreateOrderResp resp = orderService.createOrder(req);

                // 3) 统一成功返回，建议将流水号写入响应或放入响应头，便于排障追踪
                return ResponseMessage.success(resp, bizSeqNo, txnSeqNo);

            } catch (BusinessException be) {
                // 4) 业务异常：统一转换为标准业务错误响应
                log.warn("Business error, bizSeqNo={}, code={}, msg={}", bizSeqNo, be.getCode(), be.getMessage());
                return ResponseMessage.bizError(be.getCode(), be.getMessage());

            } catch (Exception ex) {
                // 5) 系统异常：统一错误码，避免将内部异常信息直接暴露
                log.error("System error, bizSeqNo={}", bizSeqNo, ex);
                return ResponseMessage.sysError("SYS-999", "Internal error");

            } finally {
                // 6) 清理上下文，避免 ThreadLocal 泄漏
                MumbleContextUtil.clear();
            }
        });
    }
}

// 落地检查清单（摘自 integration-checklist.md）：
// - [ ] 控制器是否继承 MumbleAbstractBaseController 并通过 execute(...) 封装入口
// - [ ] 是否生成并设置 bizSeqNo/txnSeqNo，且最终 clear
// - [ ] 是否使用 @Validated 及金融级校验注解
// - [ ] 是否将事务边界放在 Service 层
// - [ ] 是否统一使用 ResponseMessage 成功/失败返回
// - [ ] 日志是否包含 bizSeqNo 便于排障
// - [ ] 是否避免在 Controller 层进行数据库访问、远程调用或锁控制（这些应在 Service 层）

---------------------------------------------------------------
【结束】
---------------------------------------------------------------
*/
