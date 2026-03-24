---
name: mx_search
description: 妙想资讯搜索skill，基于东方财富妙想搜索能力，获取金融资讯（新闻、公告、研报、政策等），避免AI参考非权威或过时信息。
required_env_vars:
  - MX_APIKEY
credentials:
  - type: api_key
    name: MX_APIKEY
    description: 从东方财富妙想Skills页面获取的 API Key
---

# 妙想资讯搜索skill (mx_search)

根据**用户问句**搜索相关**金融资讯**，获取研报、新闻、解读等时效性信息。

## API Key 配置

API Key 已配置在东方财富 vault 文件中：
```bash
~/.openclaw/workspace/vault/credentials/eastmoney.json
```

## 适用场景

| 场景 | 示例问句 |
|------|---------|
| 个股资讯 | 「格力电器最新研报」「贵州茅台机构观点」 |
| 板块/主题 | 「商业航天板块近期新闻」「新能源政策解读」 |
| 宏观/风险 | 「美联储加息对A股影响」「汇率风险分析」 |
| 综合解读 | 「今日大盘异动原因」「北向资金流向解读」 |

**何时使用此 Skill：**
- 需要获取时效性信息（新闻、公告、研报）
- 查询特定事件或政策解读
- 需要检索外部数据的非常识信息
- 避免参考非权威或过时的信息

## API 调用

### 公共配置

```bash
API_KEY="mkt_Wdn2jqjmkucXQ5ElbXDoGQQKV7L3M_UohI65vryxVY8"
API_BASE="https://mkapi2.dfcfs.com"
```

### 资讯搜索接口

```bash
curl -X POST "${API_BASE}/finskillshub/api/claw/news-search" \
  -H "Content-Type: application/json" \
  -H "apikey: ${API_KEY}" \
  -d '{"query": "立讯精密的资讯"}'
```

**参数说明：**
- `query`: 自然语言查询（个股/板块/宏观/事件）

## 返回字段说明

| 字段路径 | 释义 |
|----------|------|
| `title` | 信息标题，高度概括核心内容 |
| `secuList` | 关联证券列表 |
| `secuList[].secuCode` | 证券代码（如 002475） |
| `secuList[].secuName` | 证券名称（如立讯精密） |
| `secuList[].secuType` | 证券类型（股票/债券等） |
| `trunk` | 信息核心正文/结构化数据块 |

## 使用示例

**个股资讯：**
```
用户：格力电器最新研报
→ 调用 news-search 接口
→ query: "格力电器最新研报"
→ 返回研报摘要和机构观点
```

**板块新闻：**
```
用户：商业航天板块近期新闻
→ 调用 news-search 接口
→ query: "商业航天板块近期新闻"
→ 返回板块相关新闻列表
```

**宏观分析：**
```
用户：美联储加息对A股影响
→ 调用 news-search 接口
→ query: "美联储加息对A股影响"
→ 返回政策解读和市场分析
```

## 与其他 Skill 的区别

| Skill | 用途 |
|-------|------|
| **mx_search** | 搜索资讯（新闻、研报、政策） |
| mx_select_stock | 条件选股（行情、财务指标筛选） |
| mx_selfselect | 管理自选股（查询/添加/删除） |
| eastmoney-tools | 数据查询（行情、财务、资金流向） |

## 注意事项

1. **时效性优先**：资讯信息具有时效性，注意发布时间
2. **信源权威**：东方财富妙想已做信源筛选，信息相对权威
3. **结合数据**：资讯搜索结果可与 eastmoney-tools 数据结合分析
4. **避免幻觉**：对于不确定的事件，优先使用此 Skill 搜索确认
