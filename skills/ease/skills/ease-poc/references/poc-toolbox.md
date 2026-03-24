# POC 验证工具箱

本文档汇总 POC 验证中常用的工具，按语言和用途分类。

## 性能测试工具

| 工具 | 用途 | 适用语言 | 使用说明 |
|------|------|----------|----------|
| JMH (Java Microbenchmark Harness) | 微基准测试 | Java | Maven/Gradle 集成，运行 `mvn package -Pjmh` |
| wrk | HTTP 压测 | 通用 | 命令行：`wrk -t4 -c100 -d30s http://example.com` |
| k6 | 现代压测工具 | 通用 | 编写 JS 脚本，`k6 run script.js` |
 | Apache Bench (ab) | 简单压测 | 通用 | 命令行：`ab -n 1000 -c 10 http://example.com` |
| pytest-benchmark | 性能测试 | Python | 测试代码中添加 `@pytest.mark.benchmark` |
| go test -bench | 基准测试 | Go | 包含 `_test.go` 文件，运行 `go test -bench=. -benchmem` |

## 监控和诊断工具

| 工具 | 用途 | 适用语言 | 使用说明 |
|------|------|----------|----------|
| pprof | Go 性能分析 | Go | 运行时添加 `-cpuprofile`/`-memprofile` 参数 |
| arthas | Java 诊断 | Java | 下载 jar，`java -jar arthas-boot.jar` |
| py-spy | Python 性能分析 | Python | `py-spy top --pid <PID>` |
| VisualVM | Java 监控 | Java | JDK 内置，或下载独立版本 |
| tcpdump | 网络抓包 | 通用 | `tcpdump -i any -w capture.pcap` |

## 快速集成测试工具

| 工具 | 用途 | 适用场景 |
|------|------|----------|
| curl | 测试 HTTP API | REST API 调用 |
| jq | 处理 JSON | API 响应解析 |
| Docker Compose | 本地多容器验证 | 微服务集成 |
| Postman | API 测试 | HTTP/HTTPS 接口 |

## 数据库测试辅助

| 工具 | 用途 | 适用场景 |
|------|------|----------|
| docker | 快速启动数据库 | 临时数据库实例 |
| sqlcmd/mysql client | 直接 SQL 测试 | 数据库操作验证 |
| DBeaver | 数据库客户端 | 多数据库连接 |

## 常用命令示例

### Java 性能基准
```bash
# 安装 JMH
mvn archetype:generate -DinteractiveMode=false \
  -DarchetypeGroupId=org.openjdk.jmh \
  -DarchetypeArtifactId=jmh-java-benchmark-archetype \
  -DarchetypeVersion=1.37

# 运行基准
mvn clean install
java -jar target/benchmarks.jar
```

### Python 性能测试
```bash
# 安装 pytest-benchmark
pip install pytest-benchmark

# 运行测试
pytest test_perf.py --benchmark-only
```

### Go 基准测试
```bash
# 运行所有基准测试
go test -bench=. -benchmem

# 运行指定测试
go test -bench=TestFunction -benchmem

# 显示内存分配
go test -bench=. -benchmem -memprofile=mem.prof
```

### HTTP 压测
```bash
# wrk
wrk -t4 -c100 -d30s http://localhost:8080/api

# k6
k6 run --vus 100 --duration 30s script.js

# Apache Bench
ab -n 10000 -c 100 http://localhost:8080/api
```

## 工具选用建议

### 验证新库/框架可行性
- **目标**：验证核心功能和基本集成
- **推荐工具**：单元测试框架 + 集成测试
- **关注指标**：API 可用性、错误率

### 验证性能边界
- **目标**：获取性能基准和极限
- **推荐工具**：语言专用基准工具（JMH、go test、pytest-benchmark）
- **关注指标**：响应时间、吞吐量、资源占用

### 验证集成方案
- **目标**：验证两个系统/组件能否正确对接
- **推荐工具**：curl + jq、Docker Compose
- **关注指标**：接口调用成功率、数据格式兼容性