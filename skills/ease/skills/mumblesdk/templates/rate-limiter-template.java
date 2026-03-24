/*
[模板] 请求限流（Redis 令牌桶 + 注解 + AOP 切面）
- 本文件为“模板示例”，为避免在 skills 仓库中触发 IDE/编译错误，示例代码整体置于该单一块注释中，内部不包含会结束注释的字符序列。
- 使用时请复制下方【代码模板】内容到你们实际工程的 Java 源文件（例如：RateLimiterAspect.java、RedisRateLimiter.java、RateLimit.java），然后根据 quickstart.md 完成依赖与配置。

使用指南：
1) 复制【代码模板】到你们工程的 src/main/java 对应包路径下；
2) 引入 Spring AOP、Spring Data Redis 与 SLF4J 依赖；确保 Redis 已部署与连接可用；
3) 在 Web 层方法或 Controller 类上使用 @RateLimit 注解，结合切面自动限流；
4) 支持多维限流（方法维度 + 调用方维度如 IP/User/ClientId），在生成限流 key 时组合维度；
5) 系统异常不暴露内部细节；业务限流抛出统一 BusinessException(code="RATE_LIMITED")。

---------------------------------------------------------------
【代码模板】（复制到你们的工程后使用）
---------------------------------------------------------------

// 文件路径建议：src/main/java/com/yourorg/project/limiter/RateLimit.java
package com.yourorg.project.limiter;

import java.lang.annotation.*;
import java.util.concurrent.TimeUnit;

@Target({ElementType.METHOD, ElementType.TYPE})
@Retention(RetentionPolicy.RUNTIME)
@Documented
public @interface RateLimit {
    // 限流 key 前缀（方法维度），默认使用方法签名
    String key() default "";
    // 每秒令牌产生速率
    double permitsPerSecond() default 50.0;
    // 突发桶容量（最大瞬时并发）
    long burstCapacity() default 100;
    // 时间窗口（毫秒），用于静默或重置逻辑（可选）
    long windowMillis() default 1000;
    // 维度：按 IP / USER / CLIENT 进行组合（可根据实际情况扩展）
    String[] dimensions() default {"IP"};
    // 超时时间（毫秒），用于脚本执行（Redis eval）
    long redisTimeoutMillis() default 50;
    // 是否在超限时抛出 BusinessException，否则返回默认响应
    boolean throwOnLimitExceeded() default true;
}

// 文件路径建议：src/main/java/com/yourorg/project/limiter/RedisRateLimiter.java
package com.yourorg.project.limiter;

import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;

import java.util.Arrays;
import java.util.List;

// 基于 Redis + Lua 的令牌桶限流器（线程安全、跨实例）
// 使用两个键：tokens:{key}（当前令牌数）、ts:{key}（上次补充时间戳）
// 每次请求按时间差补充令牌，令牌数不超过 burstCapacity；若不足，则拒绝；
public class RedisRateLimiter {

    private final StringRedisTemplate redisTemplate;
    private final DefaultRedisScript<List> script;

    public RedisRateLimiter(StringRedisTemplate redisTemplate) {
        this.redisTemplate = redisTemplate;
        this.script = new DefaultRedisScript<>();
        this.script.setResultType(List.class);
        this.script.setScriptText(LUA_TOKEN_BUCKET);
    }

    @SuppressWarnings("unchecked")
    public boolean tryAcquire(String key, double permitsPerSecond, long burstCapacity, long nowMillis) {
        List<String> keys = Arrays.asList("tokens:" + key, "ts:" + key);
        List<String> args = Arrays.asList(
                String.valueOf(permitsPerSecond),
                String.valueOf(burstCapacity),
                String.valueOf(nowMillis),
                "1" // 每次消耗 1 个令牌；如需可拓展为参数
        );
        List result = (List) redisTemplate.execute(script, keys, args.toArray());
        if (result == null || result.size() < 1) {
            return false;
        }
        // 返回 1 表示通过，0 表示拒绝
        Object ok = result.get(0);
        return "1".equals(String.valueOf(ok));
    }

    // 简化版令牌桶脚本：补充令牌并尝试扣减
    private static final String LUA_TOKEN_BUCKET =
            "local tokens_key = KEYS[1]\n" +
            "local ts_key = KEYS[2]\n" +
            "local rate = tonumber(ARGV[1])\n" +
            "local capacity = tonumber(ARGV[2])\n" +
            "local now = tonumber(ARGV[3])\n" +
            "local demand = tonumber(ARGV[4])\n" +
            "local last_ts = tonumber(redis.call('get', ts_key) or '0')\n" +
            "local tokens = tonumber(redis.call('get', tokens_key) or '0')\n" +
            "if last_ts == 0 then\n" +
            "  last_ts = now\n" +
            "  tokens = capacity\n" +
            "end\n" +
            "local delta = math.max(0, now - last_ts)\n" +
            "local refill = delta * rate / 1000.0\n" +
            "tokens = math.min(capacity, tokens + refill)\n" +
            "local allowed = 0\n" +
            "if tokens >= demand then\n" +
            "  tokens = tokens - demand\n" +
            "  allowed = 1\n" +
            "end\n" +
            "redis.call('set', tokens_key, tokens)\n" +
            "redis.call('set', ts_key, now)\n" +
            "return {allowed}\n";
}

// 文件路径建议：src/main/java/com/yourorg/project/limiter/RateLimiterAspect.java
package com.yourorg.project.limiter;

import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;

import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import javax.servlet.http.HttpServletRequest;

// ===== 以下为 MumbleSDK 相关类型，替换为你们项目中的实际包名 =====
// import com.yourorg.mumble.error.BusinessException;
// import com.yourorg.mumble.context.MumbleContextUtil;
// ===============================================================

@Aspect
@Order(10) // 在全局异常之前执行
@Component
class RateLimiterAspect {

    @Resource
    private RedisRateLimiter redisRateLimiter;

    @Resource
    private HttpServletRequest httpServletRequest;

    @Around("@within(rateLimit) || @annotation(rateLimit)")
    public Object around(ProceedingJoinPoint pjp, RateLimit rateLimit) throws Throwable {
        String keyPrefix = rateLimit.key();
        if (keyPrefix == null || keyPrefix.isEmpty()) {
            keyPrefix = pjp.getSignature().toShortString();
        }
        String composedKey = composeKey(keyPrefix, rateLimit.dimensions());

        boolean pass = redisRateLimiter.tryAcquire(
                composedKey,
                rateLimit.permitsPerSecond(),
                rateLimit.burstCapacity(),
                System.currentTimeMillis()
        );

        if (!pass) {
            // 统一业务异常：避免暴露内部实现
            throw new BusinessException("RATE_LIMITED", "请求过于频繁，请稍后重试");
        }
        return pjp.proceed();
    }

    // 组合多维限流键：方法维度 + 调用方维度（IP/USER/CLIENT）
    private String composeKey(String prefix, String[] dims) {
        StringBuilder sb = new StringBuilder(prefix);
        for (String d : dims) {
            if ("IP".equalsIgnoreCase(d)) {
                sb.append(":ip=").append(ip());
            } else if ("USER".equalsIgnoreCase(d)) {
                sb.append(":user=").append(userId());
            } else if ("CLIENT".equalsIgnoreCase(d)) {
                sb.append(":client=").append(clientId());
            }
        }
        return sb.toString();
    }

    private String ip() {
        String v = httpServletRequest.getHeader("X-Forwarded-For");
        if (v == null || v.isEmpty()) {
            v = httpServletRequest.getRemoteAddr();
        }
        return v == null ? "UNKNOWN_IP" : v;
    }

    private String userId() {
        try {
            // 替换为真实上下文：例如从 MumbleContextUtil 或安全上下文中读取
            // return MumbleContextUtil.getUserId();
            return "UNKNOWN_USER";
        } catch (Throwable ignore) {
            return "UNKNOWN_USER";
        }
    }

    private String clientId() {
        // 替换为真实客户端标识来源（如 header: X-Client-Id）
        String v = httpServletRequest.getHeader("X-Client-Id");
        return v == null ? "UNKNOWN_CLIENT" : v;
    }
}

// 文件路径建议：在 Controller 方法上使用
// 示例：
// @RestController
// @RequestMapping("/api/v1/order")
// public class OrderController {
//
//     @PostMapping("/create")
//     @RateLimit(key = "OrderCreate", permitsPerSecond = 20.0, burstCapacity = 50, dimensions = {"IP", "CLIENT"})
//     public ResponseMessage<CreateOrderResp> create(@RequestBody @Validated CreateOrderReq req) {
//         // 正常业务处理
//         return ResponseMessage.success(...);
//     }
// }

// 落地检查清单（对齐 integration-checklist.md 与 best-practices）：
// - [ ] 是否提供 @RateLimit 注解并在 Web 层方法或类上使用
// - [ ] 是否实现 Redis 跨实例令牌桶（Lua 脚本）并组合多维限流键（IP/USER/CLIENT）
// - [ ] 超限时是否统一抛出 BusinessException("RATE_LIMITED", "...")
// - [ ] 是否避免在切面中进行远程调用或耗时操作（仅做限流判断）
// - [ ] 是否考虑网关/代理场景下的真实 IP（X-Forwarded-For）
// - [ ] 配置中是否提供 Redis 连接与限流脚本超时参数

---------------------------------------------------------------
【结束】
---------------------------------------------------------------
*/
