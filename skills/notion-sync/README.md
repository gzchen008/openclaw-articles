# Notion 同步技能

将 Markdown 文章自动同步到 Notion 数据库。

## 🚀 快速开始

### 1. 配置 Notion Integration

```bash
python skills/notion-sync/scripts/setup_notion.py
```

按提示完成配置。

### 2. 同步文章

```bash
python skills/notion-sync/scripts/notion_sync.py sync \
  --title "OpenClaw 入门指南" \
  --content articles/openclaw-guide.md \
  --tags "OpenClaw,教程" \
  --status "已发布"
```

### 3. 查询数据库

```bash
python skills/notion-sync/scripts/notion_sync.py list --limit 10
```

## 📚 功能

- ✅ 创建 Notion 页面
- ✅ 更新页面属性
- ✅ 查询数据库内容
- ✅ Markdown 转 Notion Block

## 🔧 命令详解

### sync - 同步文章

```bash
python scripts/notion_sync.py sync \
  --title "标题" \          # 必填
  --content article.md \    # 必填：Markdown 文件路径
  --tags "标签1,标签2" \    # 可选：逗号分隔
  --status "已发布" \       # 可选：草稿/已发布（默认：草稿）
  --url "https://..."       # 可选：原文链接
```

### list - 查询数据库

```bash
python scripts/notion_sync.py list --limit 20
```

### update - 更新页面

```bash
python scripts/notion_sync.py update \
  --page-id "page_id" \
  --status "已发布" \
  --tags "新标签"
```

## 📝 Notion 数据库结构

推荐创建以下列：

| 列名 | 类型 | 说明 |
|------|------|------|
| 标题 | Title | 文章标题（默认列） |
| 状态 | Select | 草稿 / 已发布 |
| 标签 | Multi-select | 文章标签 |
| 发布日期 | Date | 发布时间 |
| 链接 | URL | 原文链接 |

## ⚠️ 注意事项

- Notion API 限制：3 requests/second（免费版）
- 单段落最多 2000 字符
- 复杂 Markdown 格式可能不完全支持

## 🔗 集成到公众号发布流程

在发布公众号文章后自动同步：

```python
# 在 wechat-mp-publish 技能中添加
import subprocess

subprocess.run([
    'python', 'skills/notion-sync/scripts/notion_sync.py', 'sync',
    '--title', article_title,
    '--content', article_path,
    '--tags', '公众号,OpenClaw',
    '--status', '已发布',
    '--url', f'https://mp.weixin.qq.com/s/{media_id}'
])
```

## 📚 参考文档

- [Notion API 文档](https://developers.notion.com/)
- [Python SDK](https://github.com/ramnes/notion-sdk-py)

---

**创建时间**：2026-02-19
**作者**：小J
