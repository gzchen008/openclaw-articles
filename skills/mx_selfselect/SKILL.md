---
name: mx_selfselect
description: 妙想自选股管理skill，基于东方财富通行证账户数据，支持通过自然语言查询/添加/删除自选股。
required_env_vars:
  - MX_APIKEY
credentials:
  - type: api_key
    name: MX_APIKEY
    description: 从东方财富妙想Skills页面获取的 API Key
---

# 妙想自选股管理skill (mx_selfselect)

通过**自然语言**查询或操作我在东方财富通行证账户下的自选股数据。

## API Key 配置

API Key 已配置在东方财富 vault 文件中：
```bash
~/.openclaw/workspace/vault/credentials/eastmoney.json
```

## 功能列表

| 功能 | 关键词示例 |
|------|-----------|
| 查询自选股 | "查询我的自选股列表"、"我的自选" |
| 添加自选股 | "把贵州茅台添加到我的自选股列表"、"加东方财富到自选" |
| 删除自选股 | "把贵州茅台从我的自选股列表删除"、"删除茅台自选" |

## API 调用

### 公共配置

```bash
API_KEY="mkt_Wdn2jqjmkucXQ5ElbXDoGQQKV7L3M_UohI65vryxVY8"
API_BASE="https://mkapi2.dfcfs.com"
```

### 1. 查询自选股列表

```bash
curl -X POST "${API_BASE}/finskillshub/api/claw/self-select/get" \
  -H "Content-Type: application/json" \
  -H "apikey: ${API_KEY}"
```

**返回字段说明：**

| 字段 | 含义 |
|------|------|
| `SECURITY_CODE` | 股票代码 |
| `SECURITY_SHORT_NAME` | 股票简称 |
| `MARKET_SHORT_NAME` | 所在市场（SZ:深交所, SH:上交所） |
| `NEWEST_PRICE` | 最新价（元） |
| `CHG` | 涨跌幅（%） |
| `PCHG` | 涨跌额（元） |
| `010000_TURNOVER_RATE...` | 换手率（%） |
| `010000_PE_D...` | 动态市盈率（倍） |
| `010000_PB...` | 市净率（倍） |
| `010000_TOAL_MARKET_VALUE...` | 总市值（元） |

### 2. 添加/删除自选股

```bash
curl -X POST "${API_BASE}/finskillshub/api/claw/self-select/manage" \
  -H "Content-Type: application/json" \
  -H "apikey: ${API_KEY}" \
  -d '{"query": "把贵州茅台加入自选"}'
```

**支持的查询语句：**
- `"把贵州茅台添加到我的自选股列表"`
- `"把贵州茅台从我的自选股列表删除"`
- `"加比亚迪到自选"`
- `"删除茅台自选"`

## 错误处理

- `status = 0`：成功
- `status != 0`：失败，检查 API Key 或网络
- 数据为空：提示用户到东方财富 App 查询

## 使用示例

**查询自选股：**
```
用户：查询我的自选股
→ 调用 self-select/get 接口
→ 返回自选股列表（股票代码、名称、最新价、涨跌幅等）
```

**添加自选股：**
```
用户：把比亚迪加到自选
→ 调用 self-select/manage 接口
→ query: "把比亚迪加入自选"
→ 返回操作结果
```

**删除自选股：**
```
用户：把茅台从自选删掉
→ 调用 self-select/manage 接口
→ query: "把贵州茅台从我的自选股列表删除"
→ 返回操作结果
```
