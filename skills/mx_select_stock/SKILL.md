---
name: mx_select_stock
description: 妙想智能选股skill，支持基于行情指标、财务指标筛选股票，查询指定行业/板块成分股，股票推荐等任务。
required_env_vars:
  - MX_APIKEY
credentials:
  - type: api_key
    name: MX_APIKEY
    description: 从东方财富妙想Skills页面获取的 API Key
---

# 妙想智能选股skill (mx_select_stock)

通过**自然语言查询**进行选股，支持 **A股、港股、美股**，返回符合条件的股票列表。

## API Key 配置

API Key 已配置在东方财富 vault 文件中：
```bash
~/.openclaw/workspace/vault/credentials/eastmoney.json
```

## 功能列表

| 功能 | 示例查询 |
|------|---------|
| 条件选股 | "今日涨幅2%的股票"、"市盈率低于10的银行股" |
| 板块成分股 | "半导体板块的成分股"、"新能源汽车概念股" |
| 行业查询 | "白酒行业的上市公司"、"芯片行业龙头" |
| 股票推荐 | "低估值高分红的股票推荐"、"业绩增长的科技股" |

## API 调用

### 公共配置

```bash
API_KEY="mkt_Wdn2jqjmkucXQ5ElbXDoGQQKV7L3M_UohI65vryxVY8"
API_BASE="https://mkapi2.dfcfs.com"
```

### 选股接口

```bash
curl -X POST "${API_BASE}/finskillshub/api/claw/stock-screen" \
  -H "Content-Type: application/json" \
  -H "apikey: ${API_KEY}" \
  -d '{"keyword": "今日涨幅2%的股票", "pageNo": 1, "pageSize": 20}'
```

**参数说明：**
- `keyword`: 自然语言选股条件
- `pageNo`: 页码（从1开始）
- `pageSize`: 每页数量（默认20，最大100）

## 返回字段说明

### 顶层状态字段

| 字段 | 含义 |
|------|------|
| `status` | 0 = 成功 |
| `data.code` | 100 = 解析成功 |
| `data.data.result.total` | 符合条件的股票总数 |

### 列定义 (columns)

| 字段 | 含义 |
|------|------|
| `title` | 列标题（如"最新价(元)"） |
| `key` | 数据键（如 NEWEST_PRICE） |
| `sortable` | 是否可排序 |
| `redGreenAble` | 是否红绿涨跌着色 |
| `unit` | 单位（元、%、倍） |

### 行数据 (dataList)

| 核心键 | 含义 |
|--------|------|
| `SECURITY_CODE` | 股票代码 |
| `SECURITY_SHORT_NAME` | 股票简称 |
| `MARKET_SHORT_NAME` | 市场（SH上交所/SZ深交所） |
| `NEWEST_PRICE` | 最新价（元） |
| `CHG` | 涨跌幅（%） |
| `PCHG` | 涨跌额（元） |

### 选股条件字段

| 字段 | 含义 |
|------|------|
| `responseConditionList` | 单条筛选条件统计 |
| `totalCondition` | 组合条件总统计 |
| `parserText` | 选股条件解析文本 |

## 输出格式

将返回的 `dataList` 按 `columns` 把英文列名替换为中文后，输出 CSV 格式数据。

**示例输出：**
```
| 代码 | 名称 | 市场 | 最新价 | 涨跌幅 |
|------|------|------|--------|--------|
| 603866 | 桃李面包 | SH | 12.50 | +2.35% |
| 300991 | 创益通 | SZ | 28.80 | +1.85% |
```

## 错误处理

- `status = 0`：成功
- `status != 0`：失败，检查 API Key 或网络
- 数据为空：提示用户到东方财富妙想 AI 进行选股

## 使用示例

**条件选股：**
```
用户：今日涨幅2%的股票
→ 调用 stock-screen 接口
→ keyword: "今日涨幅2%的股票"
→ 返回符合条件的股票列表
```

**板块成分股：**
```
用户：半导体板块的成分股
→ 调用 stock-screen 接口
→ keyword: "半导体板块的成分股"
→ 返回半导体板块所有股票
```

**财务筛选：**
```
用户：市盈率低于10的银行股
→ 调用 stock-screen 接口
→ keyword: "市盈率低于10的银行股"
→ 返回低估值银行股
```

## 注意事项

1. 支持的股票类型：A股、港股、美股
2. 分页查询：大量结果时使用 pageNo/pageSize 分页
3. 实时数据：行情数据为实时或近实时
4. 条件组合：支持多条件组合筛选（用"且"、"和"连接）
