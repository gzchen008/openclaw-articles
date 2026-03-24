# 文档同步规则

## 核心原则

1. **代码是真相**: 文档必须反映代码实际状态
2. **最小同步**: 只更新受影响的部分
3. **自动化优先**: 尽可能通过工具/脚本完成

## 文档类型与同步触发

### 领域模型文档

**位置**: `docs/domain/`

**同步触发条件**:
- 新增/删除/重命名实体
- 新增/删除/修改属性
- 新增/删除/修改枚举值
- 实体关系变更

**不触发条件**:
- 纯内部实现变更
- 方法签名不变的重构
- 注释修改

**同步示例**:

代码变更:
```java
public enum OrderStatus {
    CREATED, PAID, SHIPPED, COMPLETED,
    PARTIAL_REFUNDED  // 新增
}
```

文档更新:
```markdown
### OrderStatus 订单状态

| 值 | 含义 | 流转 |
|---|------|-----|
| CREATED | 已创建 | → PAID, CANCELLED |
| PAID | 已支付 | → SHIPPED, REFUNDING |
| SHIPPED | 已发货 | → COMPLETED |
| COMPLETED | 已完成 | - |
| **PARTIAL_REFUNDED** | **部分退款** | **← REFUNDING** | ← 新增
```

### UseCase 文档

**位置**: `docs/usecase/`

**同步触发条件**:
- 业务流程步骤变更
- 前置/后置条件变更
- 异常处理逻辑变更
- 参与者变更

**不触发条件**:
- 不影响业务流程的内部实现
- 性能优化
- 代码重构

**同步示例**:

代码变更:
```java
// 原: 全额退款
// 现: 支持部分退款
public void refund(Order order, BigDecimal amount) {
    if (amount.compareTo(order.getTotalAmount()) < 0) {
        order.setStatus(OrderStatus.PARTIAL_REFUNDED);
    } else {
        order.setStatus(OrderStatus.REFUNDED);
    }
}
```

文档更新:
```markdown
## UC-ORDER-005: 订单退款

### 主流程
1. 用户发起退款申请
2. 系统校验退款条件
3. **系统判断退款类型**: ← 新增
   - 部分退款: 退款金额 < 订单金额
   - 全额退款: 退款金额 = 订单金额
4. 执行退款操作
5. 更新订单状态
   - **部分退款 → PARTIAL_REFUNDED** ← 新增
   - 全额退款 → REFUNDED
```

### API 文档

**位置**: `docs/api/` 或代码中的 OpenAPI 注解

**同步触发条件**:
- 接口 URL 变更
- 请求/响应参数变更
- HTTP 方法变更
- 错误码变更

**不触发条件**:
- 不影响契约的内部实现
- 日志、监控等非功能变更

## 代码-文档关联标记

### 标记格式

在代码中添加文档引用注释:

```java
/**
 * 订单状态枚举
 * 
 * @domain-model docs/domain/order-aggregate.md#OrderStatus
 */
public enum OrderStatus { ... }

/**
 * 订单退款服务
 * 
 * @usecase docs/usecase/UC-ORDER-005-refund.md
 * @api docs/api/order-api.md#refund
 */
public class RefundService { ... }
```

### 标记规范

| 标记 | 用途 | 示例 |
|-----|------|------|
| `@domain-model` | 关联领域模型 | `docs/domain/xxx.md#EntityName` |
| `@usecase` | 关联用例文档 | `docs/usecase/UC-XXX.md` |
| `@api` | 关联 API 文档 | `docs/api/xxx.md#endpoint` |
| `@trd` | 关联技术需求 | `docs/trd/TRD-XXX.md` |

## 同步检查清单

在代码变更完成后，逐项确认:

```markdown
## 文档同步检查

### 领域模型
- [ ] 实体定义是否有变更？
- [ ] 属性是否有增删改？
- [ ] 枚举值是否有变更？
- [ ] 实体关系是否有变更？

### UseCase
- [ ] 业务流程是否有变更？
- [ ] 前置/后置条件是否有变更？
- [ ] 异常处理是否有变更？

### API
- [ ] 接口定义是否有变更？
- [ ] 请求/响应是否有变更？
- [ ] 错误码是否有变更？

### 结论
- [ ] 无需更新文档
- [ ] 需要更新: [文档列表]
```

## 自动化工具支持

### 1. 文档引用扫描

扫描代码中的文档引用标记:

```bash
# 查找所有文档引用
grep -r "@domain-model\|@usecase\|@api" src/

# 输出格式
# src/Order.java:@domain-model docs/domain/order-aggregate.md#Order
```

### 2. 一致性检查

检查文档引用路径是否有效（可执行脚本）:

```bash
#!/bin/bash
# doc-sync-check.sh - 文档引用一致性检查脚本

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔍 检查文档引用一致性..."
echo ""

# 查找所有文档引用
find src -name "*.java" -type f | while read -r file; do
  # 提取 @domain-model 引用
  grep -h "@domain-model" "$file" 2>/dev/null | sed -E 's/.*@domain-model\s+//' | while read -r ref; do
    path="${ref%#*}"
    anchor="${ref#*#}"

    if [ ! -f "$path" ]; then
      echo -e "${RED}❌ 文档不存在: $path${NC} (在 $file 中引用)"
    elif [ "$anchor" != "$ref" ] && ! grep -q "# $anchor" "$path" 2>/dev/null && ! grep -q "## $anchor" "$path" 2>/dev/null; then
      echo -e "${YELLOW}⚠️  锚点可能不存在: $anchor${NC} (在 $path 中)"
    fi
  done

  # 提取 @usecase 引用
  grep -h "@usecase" "$file" 2>/dev/null | sed -E 's/.*@usecase\s+//' | while read -r ref; do
    if [ ! -f "$ref" ]; then
      echo -e "${RED}❌ 用例文档不存在: $ref${NC} (在 $file 中引用)"
    fi
  done

  # 提取 @api 引用
  grep -h "@api" "$file" 2>/dev/null | sed -E 's/.*@api\s+//' | while read -r ref; do
    if [ ! -f "$ref" ]; then
      echo -e "${RED}❌ API 文档不存在: $ref${NC} (在 $file 中引用)"
    fi
  done
done

echo ""
echo -e "${GREEN}✅ 检查完成${NC}"
```

**使用方法**:
```bash
# 赋予执行权限
chmod +x doc-sync-check.sh

# 执行检查
./doc-sync-check.sh
```

### 3. 变更影响分析

基于 Git diff 识别需要同步的文档:

```bash
#!/bin/bash
# doc-impact-analyzer.sh - 分析代码变更对文档的影响

# 获取变更文件
changed_files=$(git diff --name-only HEAD~1 2>/dev/null || git diff --name-only)

echo "📊 分析代码变更对文档的影响..."
echo ""

# 提取文档引用
for file in $changed_files; do
  if [ -f "$file" ]; then
    echo "📄 $file:"

    # 提取并显示所有文档引用
    grep -h "@domain-model\|@usecase\|@api" "$file" 2>/dev/null | while read -r line; do
      ref=$(echo "$line" | sed -E 's/.*@(@domain-model|@usecase|@api)\s+//')
      echo "  → $ref"
    done
  fi
done
```

**使用方法**:
```bash
# 分析最近一次提交的影响
./doc-impact-analyzer.sh

# 分析当前未提交变更的影响
git diff --name-only | ./doc-impact-analyzer.sh
```

