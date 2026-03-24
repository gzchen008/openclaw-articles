---
name: mx_data
description: 妙想金融数据skill，基于东方财富权威数据库及最新行情数据，支持查询行情、财务、关系与经营三类数据，避免模型基于过时知识回答金融问题。
required_env_vars:
  - MX_APIKEY
credentials:
  - type: api_key
    name: MX_APIKEY
    description: 从东方财富妙想Skills页面获取的 API Key
---

# 妙想金融数据skill (mx_data)

通过**自然语言**查询金融相关数据（股票、板块、指数等），获取权威及时的金融数据。

## API Key 配置

API Key 已配置在东方财富 vault 文件中：
```bash
~/.openclaw/workspace/vault/credentials/eastmoney.json
```

## 数据类型

### 1. 行情类数据
- 股票、行业、板块、指数、基金、债券的实时行情
- 主力资金流向、估值等数据

### 2. 财务类数据
- 上市公司与非上市公司的基本信息
- 财务指标、高管信息、主营业务
- 股东结构、融资情况等

### 3. 关系与经营类数据
- 股票、非上市公司、股东及高管之间的关联关系
- 企业经营相关数据

## API 调用

### 公共配置

```bash
API_KEY="mkt_Wdn2jqjmkucXQ5ElbXDoGQQKV7L3M_UohI65vryxVY8"
API_BASE="https://mkapi2.dfcfs.com"
```

### 数据查询接口

```bash
curl -X POST "${API_BASE}/finskillshub/api/claw/query" \
  -H "Content-Type: application/json" \
  -H "apikey: ${API_KEY}" \
  -d '{"toolQuery": "东方财富最新价"}'
```

**参数说明：**
- `toolQuery`: 自然语言查询（股票/板块/指数/财务指标）

## 返回字段说明

### 一级核心路径

| 字段 | 释义 |
|------|------|
| `data.questionId` | 查询请求唯一标识ID |
| `data.dataTableDTOList` | 标准化证券指标数据列表 |
| `data.entityTagDTOList` | 证券主体汇总信息 |

### 二级核心路径（dataTableDTOList[]）

| 字段 | 释义 |
|------|------|
| `code` | 证券完整代码（如 300059.SZ） |
| `entityName` | 证券全称（如东方财富(300059.SZ)） |
| `title` | 指标数据标题 |
| `table` | 标准化表格数据 |
| `nameMap` | 列名映射（编码→中文） |
| `indicatorOrder` | 指标列排序 |

### 三级核心路径（field/entityTagDTO）

| 字段 | 释义 |
|------|------|
| `field.returnName` | 指标业务中文名 |
| `field.startDate/endDate` | 查询时间范围 |
| `entityTagDTO.secuCode` | 证券纯代码 |
| `entityTagDTO.fullName` | 证券完整中文名 |

## 使用示例

**行情查询：**
```
用户：贵州茅台最新价
→ 调用 query 接口
→ toolQuery: "贵州茅台最新价"
→ 返回最新价、涨跌幅等行情数据
```

**财务查询：**
```
用户：比亚迪市盈率
→ 调用 query 接口
→ toolQuery: "比亚迪市盈率"
→ 返回PE、PB等估值数据
```

**资金流向：**
```
用户：宁德时代主力资金流向
→ 调用 query 接口
→ toolQuery: "宁德时代主力资金流向"
→ 返回主力净流入、大单、小单等数据
```

## 与其他 Skill 的区别

| Skill | 用途 |
|-------|------|
| **mx_data** | 查询数据（行情、财务、资金流向） |
| mx_search | 搜索资讯（新闻、研报、政策） |
| mx_select_stock | 条件选股（筛选符合条件股票） |
| mx_selfselect | 管理自选股（查询/添加/删除） |

## 注意事项

1. **避免大范围查询**：如某只股票3年的每日价格，可能导致上下文爆炸
2. **数据时效性**：行情数据为实时或近实时，财务数据为最新披露
3. **数据权威性**：基于东方财富权威数据库，避免模型幻觉
4. **结合使用**：可与 mx_search 结合，先查数据再搜资讯

## 错误处理

- `status = 0`：成功
- `status != 0`：失败，检查 API Key 或网络
- 数据为空：提示用户到东方财富妙想 AI 查询
