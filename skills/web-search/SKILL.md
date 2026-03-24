# Web Search Skill - 免费网络搜索

## 描述
多源网络搜索工具，支持自动降级和多语言。

## 使用场景
当用户要求搜索网络、查询信息、了解某个话题时使用。

## 触发条件
- "搜索..."
- "查一下..."
- "帮我找..."
- "了解一下..."
- "网上说..."
- "Search for..."
- "Look up..."

## 使用方法

### 在对话中使用

用户：搜索一下 AI Agent
助手：[自动调用搜索工具，返回结果]

### 命令行使用

```bash
# 基础搜索
web-search "关键词" -n 5

# JSON 输出
web-search "关键词" -n 5 -f json

# 指定搜索源
web-search "关键词" -n 5 -s wikipedia
```

## 搜索源

1. **Wikipedia**（优先）
   - 适合：知识、定义、百科
   - 语言：自动检测（中英日韩）
   - 特点：完全免费，稳定

2. **DuckDuckGo**（英文优先）
   - 适合：即时答案、相关主题
   - 特点：无需 API key

3. **SearXNG**（备用）
   - 适合：全网搜索
   - 特点：聚合多个搜索引擎

## 输出格式

### 文本格式（默认）
```
1. 标题
   URL: https://...
   摘要: ...
   来源: Wikipedia (zh)
```

### JSON 格式
```json
[
  {
    "title": "...",
    "url": "...",
    "snippet": "...",
    "source": "..."
  }
]
```

## 示例

### 中文搜索
```
用户：搜索人工智能
助手：
找到了 3 条结果：

1. 人工智能
   Wikipedia: 计算机系统执行通常与人类智慧相关的任务的能力...

2. 人工智能应用
   Wikipedia: 利用模拟人类智能的计算技术...
```

### 英文搜索
```
用户：Search for AI Agent
助手：
Found 3 results:

1. AI agent
   Wikipedia: A class of intelligent agents distinguished by their ability...
```

## 限制

- **Wikipedia**: 只能搜索 Wikipedia 文章
- **DuckDuckGo**: 部分网络可能不可用
- **SearXNG**: 公共实例可能不稳定

## 技术细节

- 工具位置：`tools/web-search/search.py`
- 快捷命令：`~/.local/bin/web-search`
- API 调用：Wikipedia API + DuckDuckGo API + SearXNG
- 超时设置：10-15 秒

## 故障排查

### 问题：所有搜索源都失败

**解决**：
1. 检查网络连接
2. 确认能访问 zh.wikipedia.org
3. 尝试使用英文关键词

### 问题：中文搜索无结果

**解决**：
1. 使用更通用的关键词
2. 尝试英文搜索（更全面）

---

*创建时间：2026-03-21*
*版本：1.0*
