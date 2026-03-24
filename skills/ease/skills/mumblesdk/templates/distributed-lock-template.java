/*
[模板] 分布式锁（Redis + Lua，tryLock 超时 + finally unlock）
- 本文件为“模板示例”，为避免在 skills 仓库中触发 IDE/编译错误，示例代码整体置于该单一块注释中，内部不包含会结束注释的字符序列。
- 使用时请复制下方【代码模板】内容到你们实际工程的 Java 源文件（例如：MumbleDistributedLock.java、RedisDistributedLock.java、LockContext.java、AccountService.java），然后根据 quickstart.md 完成依赖与配置。

适用场景与原则：
- 在存在并发竞争的关键业务（转账、库存扣减、订单状态流转等）使用分布式锁保护临界区。
- 获得锁后务必在 finally 块中释放；释放操作需校验“锁的持有者”（token），避免误删他人锁。
- 锁粒度尽量细，持有时长尽量短；避免在持锁期间做远程调用或大事务。
- 锁超时（lease）仅作为兜底，正常释放必须依赖 finally unlock。

依赖建议：
- Spring Data Redis（StringRedisTemplate）
- Spring Boot、SLF4J
- 可选：监控埋点（慢锁、锁等待失败次数）

---------------------------------------------------------------
【代码模板】（复制到你们的工程后使用）
---------------------------------------------------------------

// 文件路径建议：src/main/java/com/yourorg/project/lock/MumbleDistributedLock.java
package com.yourorg.project.lock;

import java.util.concurrent.TimeUnit;

/// 分布式锁接口（简化版）
/// tryLock: 尝试在指定超时时间内获取锁（设置租约过期时间），成功返回 true；失败返回 false
/// unlock: 释放锁（需要确保仅释放当前持有者）
public interface MumbleDistributedLock {

    boolean tryLock(String lockKey, long timeout, TimeUnit unit);

    void unlock(String lockKey);
}

// 文件路径建议：src/main/java/com/yourorg/project/lock/LockContext.java
package com.yourorg.project.lock;

import java.util.HashMap;
import java.util.Map;

/// 线程内锁上下文：记录 lockKey 对应的持有者 token
/// 推荐在 unlock 时对比 token，确保只释放当前线程持有的锁
public final class LockContext {
    private static final ThreadLocal<Map<String, String>> TL = ThreadLocal.withInitial(HashMap::new);

    public static void setToken(String lockKey, String token) {
        TL.get().put(lockKey, token);
    }

    public static String getToken(String lockKey) {
        return TL.get().get(lockKey);
    }

    public static void clearToken(String lockKey) {
        TL.get().remove(lockKey);
    }

    public static void clearAll() {
        TL.remove();
    }
}

// 文件路径建议：src/main/java/com/yourorg/project/lock/RedisDistributedLock.java
package com.yourorg.project.lock;

import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.data.redis.core.script.DefaultRedisScript;
import org.springframework.stereotype.Component;

import javax.annotation.Resource;
import java.util.Collections;
import java.util.UUID;
import java.util.concurrent.TimeUnit;

/// 基于 Redis 的分布式锁实现（SET NX PX + Lua 验证持有者删除）
/// 锁值为随机 token，用于校验 unlock 的持有者身份
@Component
public class RedisDistributedLock implements MumbleDistributedLock {

    @Resource
    private StringRedisTemplate redisTemplate;

    /// 仅当值匹配当前持有者 token 时，执行 DEL，返回 1；否则返回 0
    private static final String LUA_UNLOCK =
            "local key = KEYS[1]\\n" +
            "local token = ARGV[1]\\n" +
            "if redis.call('get', key) == token then\\n" +
            "  return redis.call('del', key)\\n" +
            "else\\n" +
            "  return 0\\n" +
            "end\\n";

    private final DefaultRedisScript<Long> unlockScript;

    public RedisDistributedLock() {
        this.unlockScript = new DefaultRedisScript<>();
        this.unlockScript.setResultType(Long.class);
        this.unlockScript.setScriptText(LUA_UNLOCK);
    }

    @Override
    public boolean tryLock(String lockKey, long timeout, TimeUnit unit) {
        long leaseMillis = unit.toMillis(timeout);
        String token = UUID.randomUUID().toString();
        // 使用 SET NX PX 实现原子加锁与租约过期
        Boolean ok = redisTemplate.opsForValue().setIfAbsent(lockKey, token, leaseMillis, TimeUnit.MILLISECONDS);
        boolean acquired = Boolean.TRUE.equals(ok);
        if (acquired) {
            // 记录当前线程持有的 token
            LockContext.setToken(lockKey, token);
        }
        return acquired;
    }

    @Override
    public void unlock(String lockKey) {
        String token = LockContext.getToken(lockKey);
        try {
            if (token == null) {
                // 非当前线程持有或已释放
                return;
            }
            Long res = redisTemplate.execute(unlockScript, Collections.singletonList(lockKey), token);
            // 可选择记录日志：res == 1 表示成功释放；0 表示持有者不匹配（可能租约过期或被他人抢占）
        } finally {
            // 清理上下文中的 token
            LockContext.clearToken(lockKey);
        }
    }
}

// 文件路径建议：src/main/java/com/yourorg/project/service/AccountService.java
package com.yourorg.project.service;

import com.yourorg.project.lock.MumbleDistributedLock;
import org.springframework.stereotype.Service;

import javax.annotation.Resource;
import java.math.BigDecimal;
import java.util.concurrent.TimeUnit;

// ===== 以下为 MumbleSDK 相关类型，替换为你们项目中的实际包名 =====
// import com.yourorg.mumble.error.BusinessException;
// import com.yourorg.mumble.context.MumbleContextUtil;
// import com.yourorg.mumble.seq.MumbleSeqService;
// ===============================================================

@Service
public class AccountService {

    @Resource
    private MumbleDistributedLock distributedLock;

    public void transfer(String from, String to, BigDecimal amount) {
        String lockKey = "transfer:" + from + ":" + to;
        boolean acquired = distributedLock.tryLock(lockKey, 30, TimeUnit.SECONDS);
        if (!acquired) {
            throw new BusinessException("TRANSFER_LOCKED", "转账操作正在进行中，请稍后重试");
        }
        try {
            // 受锁保护的业务逻辑
            doTransfer(from, to, amount);
        } finally {
            // 确保释放锁（无论成功还是异常都释放）
            distributedLock.unlock(lockKey);
        }
    }

    private void doTransfer(String from, String to, BigDecimal amount) {
        // 实际的转账逻辑（校验余额、记账、落库等）
    }
}

// 使用注意事项（与 best-practices 对齐）：
// - [1] 锁粒度：优先使用业务主键或组合键（如 "transfer:{from}:{to}"），避免过宽导致大范围竞争。
// - [2] 持有时长：设置合理租约（PX 毫秒）；避免超长事务或远程调用导致持锁时间过长。
// - [3] finally unlock：必须在 finally 中释放；异常分支也要保证 unlock。
// - [4] 校验持有者：unlock 使用 Lua 校验当前 token，避免误删他人锁。
// - [5] 幂等与重试：对于失败的业务操作，结合锁使用幂等键设计与重试机制。
// - [6] 监控：记录锁获取失败次数、持锁时长分布，排查慢锁与竞争热点。

// 与 MumbleSDK 的集成要点：
// - 在服务层生成业务/交易流水（MumbleSeqService.nextValue(...)），并设置 MumbleContextUtil 的 bizSeqNo/txnSeqNo；在 finally 清理上下文。
// - 分布式锁不替代数据库唯一约束与事务控制；需综合设计以满足金融级一致性与可审计性。
// - 结合全局异常处理器（MumbleGlobalExceptionHandler），确保对外暴露统一的错误码与消息。

// 落地检查清单（对齐 integration-checklist.md 与 best-practices）：
// - [ ] 是否提供 MumbleDistributedLock 接口与 Redis 实现（SET NX PX + Lua 解锁）
// - [ ] tryLock 是否设置合理租约并返回布尔结果
// - [ ] unlock 是否校验持有者 token 并在 finally 中调用
// - [ ] 业务锁粒度是否合理（避免热点大锁）；是否避免持锁期间执行耗时 IO
// - [ ] 是否在服务层结合 MumbleSeqService 与 MumbleContextUtil 的上下文管理（生成流水 + finally 清理）
// - [ ] 是否有监控与日志：记录 lockKey、bizSeqNo/txnSeqNo、持锁时长、失败原因

---------------------------------------------------------------
【结束】
---------------------------------------------------------------
*/
