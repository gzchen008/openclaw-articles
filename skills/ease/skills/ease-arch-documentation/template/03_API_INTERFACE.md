# API接口

## 1. 接口分类说明

### 1.1 RMB接口说明
RMB (Remote Message Bus) 接口是ECIF-Core系统内部服务间通信的主要方式，基于Webank的Mumble框架实现。这是系统最主要的对外服务能力。

**关键技术特征**:
- 使用@MumbleMessageService注解标识RMB服务
- serviceId作为RMB接口的唯一标识
- 支持同步和异步调用模式
- 集成服务治理和监控能力
- 自动化的服务注册与发现

### 1.2 HTTP接口说明
HTTP接口主要用于系统管理、文件上传、健康检查等场景，基于Spring Web框架实现。主要用于运维和维护功能。

**关键技术特征**:
- RESTful API设计风格
- 支持文件上传下载
- 集成Spring Boot Actuator监控
- 提供系统维护接口
- 支持认证授权机制

## 2. RMB接口详情列表

### 2.1 客户信息查询服务

#### QueryClientInfoService
- **serviceId**: 120001
- **归属模块**: 个人客户管理模块
- **功能描述**: 查询个人客户完整信息
- **请求参数**: 
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | ecifNo | String | 是 | 客户号 |
  | productCode | String | 否 | 产品代码 |
- **响应示例**:
```json
{
  "ecifNo": "1000000000000001",
  "personalName": "张三",
  "personalIdentificationNumber": "110101199001011234",
  "telephone": "13800138000",
  "updatedDate": "2025-11-03 20:00:00"
}
```

#### QueryClientInfoByCertService
- **serviceId**: 120002
- **归属模块**: 个人客户管理模块
- **功能描述**: 根据证件信息查询客户
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | personalIdentificationNumber | String | 是 | 证件号码 |
  | personalIdentificationType | String | 是 | 证件类型 |
- **响应示例**:
```json
{
  "ecifNo": "1000000000000001",
  "personalName": "张三",
  "matchResult": "MATCH"
}
```

#### QueryClientInfoByMobileService
- **serviceId**: 120003
- **归属模块**: 个人客户管理模块
- **功能描述**: 根据手机号查询客户
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | mobile | String | 是 | 手机号码 |
- **响应示例**:
```json
{
  "ecifNo": "1000000000000001",
  "personalName": "张三",
  "mobile": "13800138000"
}
```

### 2.2 客户信息修改服务

#### ModifyInfoService
- **serviceId**: 120011
- **归属模块**: 个人客户管理模块
- **功能描述**: 修改客户基本信息
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | ecifNo | String | 是 | 客户号 |
  | personalClient | PersonalClient | 是 | 客户信息对象 |
- **响应示例**:
```json
{
  "resultCode": "0000",
  "resultMsg": "成功"
}
```

#### ModifyNameService
- **serviceId**: 120012
- **归属模块**: 个人客户管理模块
- **功能描述**: 修改客户姓名
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | ecifNo | String | 是 | 客户号 |
  | personalName | String | 是 | 新姓名 |
- **响应示例**:
```json
{
  "resultCode": "0000",
  "resultMsg": "姓名修改成功"
}
```

### 2.3 文件处理服务

#### UploadFileService
- **serviceId**: 120021
- **归属模块**: 批量处理模块
- **功能描述**: 上传文件到FPS服务
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | fileName | String | 是 | 文件名 |
  | fileContent | byte[] | 是 | 文件内容 |
  | fileType | String | 否 | 文件类型 |
- **响应示例**:
```json
{
  "fileId": "F123456789",
  "fileHash": "abc123def456",
  "uploadTime": "2025-11-03 20:00:00"
}
```

#### DownloadFileService
- **serviceId**: 120022
- **归属模块**: 批量处理模块
- **功能描述**: 从FPS服务下载文件
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | fileId | String | 是 | 文件ID |
  | fileHash | String | 是 | 文件哈希值 |
- **响应示例**:
```json
{
  "fileName": "customer_data.xlsx",
  "fileContent": "base64_encoded_content",
  "downloadTime": "2025-11-03 20:00:00"
}
```

### 2.4 产品权限服务

#### ProductPermissionService
- **serviceId**: 120031
- **归属模块**: 个人客户管理模块
- **功能描述**: 管理客户产品权限
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | ecifNo | String | 是 | 客户号 |
  | productCode | String | 是 | 产品代码 |
  | permission | String | 是 | 权限设置 |
- **响应示例**:
```json
{
  "resultCode": "0000",
  "resultMsg": "权限设置成功"
}
```

### 2.5 批量处理服务

#### BatchProcessService
- **serviceId**: 120041
- **归属模块**: 批量处理模块
- **功能描述**: 执行批量数据处理任务
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | taskId | String | 是 | 任务ID |
  | batchData | List<String> | 是 | 批量数据 |
  | processType | String | 是 | 处理类型 |
- **响应示例**:
```json
{
  "taskId": "T123456789",
  "processCount": 1000,
  "successCount": 998,
  "failCount": 2
}
```

## 3. HTTP接口详情列表

### 3.1 系统管理接口

#### 文件上传接口
- **URL路径**: /ecif-core/file/upload
- **HTTP方法**: POST
- **归属模块**: Web接口模块
- **功能描述**: 上传文件到系统
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | file | MultipartFile | 是 | 上传的文件 |
  | fileType | String | 否 | 文件类型 |
- **响应示例**:
```json
{
  "fileId": "F123456789",
  "fileName": "customer_data.xlsx",
  "uploadTime": "2025-11-03 20:00:00"
}
```

#### 系统健康检查
- **URL路径**: /ecif-core/health
- **HTTP方法**: GET
- **归属模块**: Web接口模块
- **功能描述**: 检查系统健康状态
- **请求参数**: 无
- **响应示例**:
```json
{
  "status": "UP",
  "timestamp": "2025-11-03T20:00:00Z",
  "components": {
    "db": {"status": "UP"},
    "redis": {"status": "UP"}
  }
}
```

#### 系统信息查询
- **URL路径**: /ecif-core/info
- **HTTP方法**: GET
- **归属模块**: Web接口模块
- **功能描述**: 获取系统基本信息
- **请求参数**: 无
- **响应示例**:
```json
{
  "appName": "ecif-core",
  "version": "3.12.0",
  "buildTime": "2025-11-03 20:00:00",
  "environment": "prd"
}
```

### 3.2 数据修补接口

#### 数据修补执行接口
- **URL路径**: /ecif-core/patch/execute
- **HTTP方法**: POST
- **归属模块**: 批量处理模块
- **功能描述**: 执行数据修补任务
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | patchType | String | 是 | 修补类型 |
  | startTime | String | 否 | 开始时间 |
  | endTime | String | 否 | 结束时间 |
- **响应示例**:
```json
{
  "patchId": "P123456789",
  "totalCount": 1000,
  "successCount": 995,
  "failCount": 5
}
```

#### 修补任务查询接口
- **URL路径**: /ecif-core/patch/query
- **HTTP方法**: GET
- **归属模块**: 批量处理模块
- **功能描述**: 查询修补任务执行结果
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | patchId | String | 是 | 修补任务ID |
- **响应示例**:
```json
{
  "patchId": "P123456789",
  "status": "COMPLETED",
  "details": [
    {"ecifNo": "1000000000000001", "status": "SUCCESS"},
    {"ecifNo": "1000000000000002", "status": "FAILED", "errorMsg": "数据不存在"}
  ]
}
```

### 3.3 配置管理接口

#### 配置刷新接口
- **URL路径**: /ecif-core/config/refresh
- **HTTP方法**: POST
- **归属模块**: Web接口模块
- **功能描述**: 刷新系统配置
- **请求参数**: 无
- **响应示例**:
```json
{
  "resultCode": "0000",
  "resultMsg": "配置刷新成功"
}
```

#### 缓存清理接口
- **URL路径**: /ecif-core/cache/clear
- **HTTP方法**: POST
- **归属模块**: Web接口模块
- **功能描述**: 清理系统缓存
- **请求参数**:
  | 参数名 | 类型 | 必填 | 说明 |
  |--------|------|------|------|
  | cacheKey | String | 否 | 缓存键名 |
- **响应示例**:
```json
{
  "resultCode": "0000",
  "resultMsg": "缓存清理成功",
  "clearedKeys": 150
}
```

## 4. 接口调用规范

### 4.1 RMB调用规范
- 所有RMB服务必须实现对应的Service接口
- 服务ID必须在系统内唯一
- 请求和响应对象必须实现Serializable接口
- 异常处理必须遵循统一的错误码规范

### 4.2 HTTP调用规范
- RESTful API设计，遵循资源导向原则
- HTTP状态码使用标准语义
- 请求和响应数据格式统一使用JSON
- 接口安全性通过认证授权机制保障

### 4.3 性能要求
- RMB接口响应时间不超过3秒
- HTTP接口响应时间不超过5秒
- 大数据量接口支持分页和流式处理
- 接口调用频率限制和熔断机制

### 4.4 监控要求
- 所有接口调用必须记录日志
- 接口性能指标需要监控
- 异常调用需要告警
- 接口调用链路需要追踪
