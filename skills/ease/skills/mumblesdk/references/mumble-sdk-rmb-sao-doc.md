# RmbPojoSAO 使用指南

## 概述

`RmbPojoSAO` 是 Mumble SDK 中用于发送 RMB（Realizable Message Bus）请求的核心工具类，实现了 `RmbSAO` 接口。它提供了同步/异步消息发送、消息发布、订阅者管理等核心能力。

## 依赖配置

### Gradle 依赖
```groovy
dependencies {
    implementation project(':mumble-sdk-rmb')
    implementation project(':mumble-sdk-common')
}
```

### 配置参数（application.properties）
```properties
# 启用 RMB 模块（默认 true）
mumble.rmb.enabled=true

# Masa 降级到 RMB 开关（默认 false）
mumble.masa.degrade.to.rmb=false

# 是否需要更多返回列表（默认 false）
mumble.masa.need.more.retList=false

# 是否设置消息语言环境（默认 false）
mumble.send.message.need.locale=false

# 是否开启 RMB 报文监控（默认 false）
# 开启后将请求、接收和返回内容进行 MD5，截取前6位打印日志
mumble.rmb.content.monitor.enable=false
```

## Bean 注入

```java
@Autowired
@Qualifier("cn.webank.mumble.framework.module.rmb.integration.RmbSAO")
private RmbSAO rmbSAO;
```

## 核心功能

### 1. 同步消息发送

#### 基础用法（send）
```java
// 创建同步消息对象
SyncRMBMessage<UserRequest, UserResponse> message = new SyncRMBMessage<UserRequest, UserResponse>() {};

// 设置消息属性
message.setServiceId("user-service");        // 服务ID
message.setTxnSeqNo("txn123");               // 交易流水号
message.setConsumerSeqNo("consumer456");     // 消费者流水号
message.setDcnNo("dcn001");                  // DCN编号
message.setOrgSysId("system001");            // 系统ID
message.setScenario("01");                   // 场景
message.setVersion("1.0.0");                 // 版本
message.setUserLang(Locale.CHINESE.toString());

// 设置请求对象
UserRequest request = new UserRequest();
request.setUserId("U123");
message.setRequestObject(request);

// 发送请求（超时 5 秒，异常时抛出）
SyncRMBMessage<UserRequest, UserResponse> response =
    rmbSAO.send(message, 5, TimeUnit.SECONDS, true);

// 处理响应
if (response.isSuccess()) {
    UserResponse result = response.getResponseObject();
} else {
    List<Ret> retList = response.getRetList();
    // 处理错误信息
}
```

#### Masa 模式发送（sendWithMasa）
```java
// 使用 Masa 模式发送（云原生服务调用）
SyncRMBMessage<UserRequest, UserResponse> response =
    rmbSAO.sendWithMasa(message, 5, TimeUnit.SECONDS, true);

// 当 mumble.masa.degrade.to.rmb=true 时，会自动降级到普通 RMB 发送
```

### 2. 异步消息发送

#### CompletableFuture 方式
```java
// 异步发送，返回 CompletableFuture
CompletableFuture<SyncRMBMessage<UserRequest, UserResponse>> future =
    rmbSAO.asyncSend(message, 5, TimeUnit.SECONDS, true);

// 处理异步结果
future.thenAccept(response -> {
    if (response.isSuccess()) {
        UserResponse result = response.getResponseObject();
        // 处理成功响应
    } else {
        // 处理错误
    }
});

// 或使用 Masa 模式
CompletableFuture<SyncRMBMessage<UserRequest, UserResponse>> masaFuture =
    rmbSAO.asyncSendWithMasa(message, 5, TimeUnit.SECONDS, true);
```

#### Callback 方式
```java
// 使用 Consumer 回调处理异步响应
rmbSAO.asyncSend(message, response -> {
    // 处理响应
    if (response.isSuccess()) {
        UserResponse result = response.getResponseObject();
    }
}, 5, TimeUnit.SECONDS, true);
```

### 3. 异步消息发布

```java
// 创建异步消息对象（PUBSUB 模式）
AsyncRMBMessage<OrderEvent> message = new AsyncRMBMessage<>(AsyncRMBMessage.MessageMode.PUBSUB);

// 设置消息属性
message.setEventId("order-created");          // 事件ID
message.setTxnSeqNo("txn123");
message.setConsumerSeqNo("consumer456");
message.setDcnNo("dcn001");
message.setOrgSysId("system001");

// 设置消息内容
OrderEvent event = new OrderEvent();
event.setOrderId("O123");
event.setOrderStatus("CREATED");
message.setRequestObject(event);

// 发布消息
rmbSAO.publish(message, true);

// 或使用 Masa 模式发布
rmbSAO.publishWithMasa(message, true);
```

### 4. 订阅者管理

#### 注册/注销订阅者
```java
// 注册单个订阅者
ISubscriber subscriber = new MySubscriber();
rmbSAO.registerSubscriber(subscriber, true);

// 批量注册订阅者
List<ISubscriber> subscribers = Arrays.asList(sub1, sub2);
rmbSAO.registerSubscribers(subscribers, true);

// 注销订阅者
rmbSAO.deregisterSubscriber(subscriber, true);
rmbSAO.deregisterSubscribers(subscribers, true);
```

#### Reactor 订阅者
```java
// 注册 Reactor 订阅者（响应式，适合高并发场景）
List<ReactorSubscriber> reactorSubscribers = Arrays.asList(reactor1, reactor2);
rmbSAO.registerReactorSubscribers(reactorSubscribers, true);

// 注销 Reactor 订阅者
rmbSAO.deregisterReactorSubscribers(reactorSubscribers, true);
```

#### Pipe 订阅者
```java
// 注册 Pipe 订阅者（Merge queue 模式）
List<PipeSubscriber> pipeSubscribers = Arrays.asList(pipe1, pipe2);
rmbSAO.registerPipeSubscribers(pipeSubscribers, true);

// 注销 Pipe 订阅者
rmbSAO.deregisterPipeSubscribers(pipeSubscribers, true);
```

### 5. 资源清理

```java
// 清理 RMB 资源
rmbSAO.destroy(true);
```

## 响应处理

### 统一响应处理工具方法
```java
// 使用 SyncRMBMessage 提供的静态方法处理响应
if (SyncRMBMessage.handleRmbMessageResponse(response, bizErrors)) {
    // 调用成功
    UserResponse result = response.getResponseObject();
} else {
    // 调用失败，错误信息已填充到 bizErrors 中
}
```

### 自定义响应处理
```java
private <E, T> void handleResponse(SyncRMBMessage<E, T> response, BizErrors bizErrors) {
    if (response == null) {
        bizErrors.reject("SYSTEM_ERROR", null, "RMB response is null");
        return;
    }

    if (!response.isSuccess()) {
        List<Ret> retList = response.getRetList();
        if (retList != null && !retList.isEmpty()) {
            Ret ret = retList.get(0);
            bizErrors.reject(ret.getCode(), null, ret.getMsg());
        } else {
            bizErrors.reject("SYSTEM_ERROR", null, "Unknown error");
        }
    }
}
```

## 超时限制

- **同步调用最大超时时间**: 100 秒（100,000 毫秒）
- 超过此限制将抛出 `IllegalArgumentException`

## 错误码

| 错误码 | 说明 |
|--------|------|
| 9001   | RMB 超时错误 |

## 最佳实践

1. **超时设置**: 根据业务场景合理设置超时时间，建议 3-10 秒
2. **异常处理**: 在生产环境建议 `isThrowWhenException=true`，便于问题定位
3. **消息监控**: 生产环境可开启 `mumble.rmb.content.monitor.enable` 进行报文监控
4. **异步处理**: 高并发场景优先使用异步方式
5. **资源清理**: 应用关闭时调用 `destroy()` 方法释放 RMB 资源

## 完整示例

```java
@Service
public class UserService {

    @Autowired
    @Qualifier("cn.webank.mumble.framework.module.rmb.integration.RmbSAO")
    private RmbSAO rmbSAO;

    public UserDTO getUserById(String userId, BizErrors bizErrors) {
        // 创建消息
        SyncRMBMessage<UserRequest, UserDTO> message =
            new SyncRMBMessage<UserRequest, UserDTO>() {};

        // 设置消息属性
        message.setServiceId("user-query-service");
        message.setTxnSeqNo(MumbleContextUtil.getTxnSeqNo());
        message.setConsumerSeqNo(MumbleContextUtil.getConsumerSeqNo());
        message.setScenario("01");
        message.setVersion("1.0.0");
        message.setUserLang(Locale.CHINESE.toString());

        // 设置请求
        UserRequest request = new UserRequest();
        request.setUserId(userId);
        message.setRequestObject(request);

        // 发送请求
        SyncRMBMessage<UserRequest, UserDTO> response =
            rmbSAO.sendWithMasa(message, 5000, TimeUnit.MILLISECONDS, true);

        // 处理响应
        if (SyncRMBMessage.handleRmbMessageResponse(response, bizErrors)) {
            return response.getResponseObject();
        }
        return null;
    }
}
```
