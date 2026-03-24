# Web Search Tool - 免费多源网络搜索

> 位置：`tools/web-search/`
> 创建时间：2026-03-21

## 功能

- ✅ **多源搜索**：自动尝试多个免费搜索 API
- ✅ **自动降级**：一个源失败自动切换到下一个
- ✅ **多语言支持**：自动检测中英日韩文
- ✅ **完全免费**：无需 API key

## 支持的搜索源

| 源 | 特点 | 限制 |
|---|---|---|
| **Wikipedia** | 知识、定义、百科 | 仅限 Wikipedia 文章 |
| **DuckDuckGo** | 即时答案、相关主题 | 部分网络可能不可用 |
| **SearXNG** | 聚合搜索（Google+Bing+更多） | 公共实例可能不稳定 |

## 使用方法

### 基础搜索

```bash
# 英文搜索
web-search "OpenAI" 5

# 中文搜索
web-search "人工智能" 3

# 日文搜索
web-search "人工知能" 3
```

### 指定搜索源

```bash
# 只用 Wikipedia
python3 tools/web-search/search.py "人工智能" -s wikipedia

# 只用 DuckDuckGo
python3 tools/web-search/search.py "AI" -s duckduckgo

# 多源搜索（默认）
python3 tools/web-search/search.py "AI" -s all
```

### JSON 输出

```bash
# JSON 格式（方便程序处理）
python3 tools/web-search/search.py "AI" -f json
```

## 示例输出

### 文本格式

```
🔍 尝试 Wikipedia (zh)...

1. 人工智能
   URL: https://zh.wikipedia.org/wiki/人工智能
   摘要: 人工智能，是指计算机系统执行通常与人类智慧相关的任务的能力...
   来源: Wikipedia (zh)
```

### JSON 格式

```json
[
  {
    "title": "人工智能",
    "url": "https://zh.wikipedia.org/wiki/人工智能",
    "snippet": "人工智能，是指计算机系统执行通常与人类智慧相关的任务的能力...",
    "source": "Wikipedia (zh)"
  }
]
```

## 技术细节

### API 调用

- **Wikipedia API**: `https://{lang}.wikipedia.org/w/api.php`
- **DuckDuckGo API**: `https://api.duckduckgo.com/`
- **SearXNG**: `https://searx.be/search`

### 语言检测

自动检测查询语言：
- 中文 → `zh.wikipedia.org`
- 日文 → `ja.wikipedia.org`
- 韩文 → `ko.wikipedia.org`
- 其他 → `en.wikipedia.org`

### 超时设置

- DuckDuckGo: 10 秒
- Wikipedia: 10 秒
- SearXNG: 15 秒

## 限制

1. **Wikipedia**: 只能搜索 Wikipedia 文章，不是全网搜索
2. **DuckDuckGo**: 主要返回即时答案，不是完整搜索结果
3. **SearXNG**: 公共实例可能被封锁或限流
4. **网络依赖**: 需要能访问 Wikipedia（zh.wikipedia.org）

## 未来改进

- [ ] 添加 Google Custom Search（免费额度 100 次/天）
- [ ] 添加 Bing Web Search（免费额度 1000 次/月）
- [ ] 添加本地缓存（避免重复查询）
- [ ] 添加代理支持（绕过网络限制）

## 故障排查

### 问题：所有搜索源都失败

**原因**：网络访问问题

**解决**：
1. 检查网络连接
2. 尝试访问 https://zh.wikipedia.org
3. 如果 Wikipedia 可访问，说明工具正常，只是其他源被封锁

### 问题：中文搜索无结果

**原因**：Wikipedia 中文版没有对应文章

**解决**：
1. 尝试英文搜索（更全面）
2. 使用更通用的关键词

---

*创建时间：2026-03-21*
