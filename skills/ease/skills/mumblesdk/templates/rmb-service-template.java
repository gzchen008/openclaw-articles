/*
MumbleSDK RMB 消息服务模板（说明）
- 本文件为“模板示例”，为避免在 skills 仓库中触发 IDE/编译错误，示例代码整体置于该单一块注释中，内部不包含会结束注释的字符序列。
- 使用时请复制下方【代码模板】内容到你们实际工程的 Java 源文件（例如：OrderRmbService.java），然后根据 quickstart.md 完成依赖与配置。

使用指南：
1) 复制【代码模板】到你们工程的 src/main/java 对应包路径下；
2) 替换包名、导入路径中的占位符为你们公司的实际包路径；
3) 引入 MumbleSDK RMB 相关依赖（如 @MumbleRmbService/@MumbleServiceMethod 等），以及 SLF4J、Spring 上下文；
4) 严格区分业务异常与系统异常，返回统一的 ResponseMessage；
5) 保证幂等（基于业务唯一键或消息唯一ID），并做好监控与审计日志。

---------------------------------------------------------------
【代码模板】（复制到你们的工程后使用）
---------------------------------------------------------------

// 文件路径建议：src/main/java/com/yourorg/project/rmb/OrderRmbService.java

package com.yourorg.project.rmb;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.annotation.Resource;

// ===== 以下为 MumbleSDK RMB 相关类型，替换为你们实际包名 =====
// import com.yourorg.mumble.rmb.MumbleRmbService;
// import com.yourorg.mumble.rmb.MumbleServiceMethod;
// import com.yourorg.mumble.web.ResponseMessage;
// import com.yourorg.mumble.context.MumbleContextUtil;
// import com.yourorg.mumble.seq.MumbleSeqService;
// import com.yourorg.mumble.error.BusinessException;
// ===============================================================

// 占位响应类型，复制到工程后请替换为 SDK 的 ResponseMessage
class ResponseMessage<T> {
    public static <T> ResponseMessage<T> success(T data) { return new ResponseMessage<>(); }
    public static <T> ResponseMessage<T> bizError(String code, String msg) { return new ResponseMessage<>(); }
    public static <T> ResponseMessage<T> sysError(String code, String msg) { return new ResponseMessage<>(); }
}

// 占位上下文/序列/异常类型，复制到工程后请替换为真实类型
class MumbleContextUtil {
    public static void setBizSeqNo(String v) {}
    public static void setTxnSeqNo(String v) {}
    public static String getBizSeqNo() { return "BIZ_SEQ_PLACEHOLDER"; }
    public static void clear() {}
}
class MumbleSeqService {
    public String nextValue(String key) { return "SEQ_PLACEHOLDER"; }
}
class BusinessException extends RuntimeException {
    private final String code;
    public BusinessException(String code, String message) { super(message); this.code = code; }
    public String getCode() { return code; }
}

// 示例消息 DTO（按需替换）
class OrderCreatedMsg {
    // String orderId;
    // String userId;
    // long timestamp;
}

 // RMB 服务示例：订单创建消息消费
 // - 幂等：基于消息唯一ID或订单ID + 业务唯一键
 // - 审计：记录消费状态与错误原因
 // - 事务：根据场景决定是否开启（如落库或下游调用）
// @MumbleRmbService(topic = "order.created", group = "order-service")
class OrderRmbService {

    private static final Logger log = LoggerFactory.getLogger(OrderRmbService.class);

    @Resource
    private MumbleSeqService seqService;

    // @MumbleServiceMethod
    public ResponseMessage<Void> consume(OrderCreatedMsg msg) {
        // 1) 生成并设置业务/交易流水（用于日志链路与排障）
        final String bizSeqNo = seqService.nextValue("BIZ_SEQ_RMB_ORDER_CREATED");
        final String txnSeqNo = seqService.nextValue("TXN_SEQ_RMB_ORDER_CREATED");
        MumbleContextUtil.setBizSeqNo(bizSeqNo);
        MumbleContextUtil.setTxnSeqNo(txnSeqNo);

        try {
            // 2) 幂等检查（示例）
            // if (已经处理过该消息ID或订单ID) { return ResponseMessage.success(null); }

            // 3) 业务处理（如更新订单状态、发通知、写审计）
            // updateOrderStatus(msg.orderId, "CREATED");
            // auditLog(...);

            // 4) 统一成功返回
            log.info("Consume order.created success, bizSeqNo={}, txnSeqNo={}, msg={}", bizSeqNo, txnSeqNo, msg);
            return ResponseMessage.success(null);

        } catch (BusinessException be) {
            // 5) 业务异常：记录并返回业务错误，不重试或按策略重试
            log.warn("Business error in RMB consume, bizSeqNo={}, code={}, msg={}", bizSeqNo, be.getCode(), be.getMessage());
            return ResponseMessage.bizError(be.getCode(), be.getMessage());

        } catch (Exception ex) {
            // 6) 系统异常：记录并返回系统错误，通常由 MQ 或框架进行重试/死信处理
            log.error("System error in RMB consume, bizSeqNo={}", bizSeqNo, ex);
            return ResponseMessage.sysError("SYS-999", "Internal error");

        } finally {
            // 7) 清理上下文，避免 ThreadLocal 泄漏
            MumbleContextUtil.clear();
        }
    }
}

// 设计要点与最佳实践：
// - [ ] 幂等：以消息ID或业务唯一键作为幂等键，落库或使用分布式缓存标记已处理
// - [ ] 重试：系统异常情况下由 MQ 重试，业务异常通常不重试或采用限次重试
// - [ ] 监控：记录消费耗时、成功/失败、重试次数、关键字段（orderId/userId）
// - [ ] 审计：保留审计日志，便于事后排查（携带 bizSeqNo/txnSeqNo）
// - [ ] 事务：根据处理内容决定是否开启事务，避免长事务，必要时拆分为两个阶段
// - [ ] 锁控：如存在竞态，使用分布式锁保证同一幂等键串行处理
// - [ ] 配置：topic/group 等通过配置文件下发，避免硬编码

---------------------------------------------------------------
【结束】
---------------------------------------------------------------
*/
