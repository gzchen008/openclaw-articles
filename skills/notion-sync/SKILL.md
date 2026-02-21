# Notion 同步技能

## 功能说明

将 Markdown 文章自动同步到 Notion 数据库，支持：
- ✅ 创建新页面
- ✅ 更新已有页面
- ✅ 查询数据库内容
- ✅ Markdown 转 Notion Block

## 前置要求

### 1. 创建 Notion Integration

1. 访问 https://www.notion.so/my-integrations
2. 点击 "New integration"
3. 填写名称（如 "OpenClaw Sync"）
4. 复制 **Internal Integration Token**（以 `secret_` 开头）

### 2. 创建 Notion 数据库

1. 在 Notion 中创建新页面
2. 添加数据库（表格视图）
3. 添加以下列：
   - **标题**（Title）- 默认列
   - **状态**（Select）：草稿 / 已发布
   - **标签**（Multi-select）
   - **发布日期**（Date）
   - **链接**（URL）

4. 复制数据库 ID：
   - 打开数据库页面
   - URL 格式：`https://www.notion.so/workspace/[DATABASE_ID]?v=...`
   - 复制 `[DATABASE_ID]` 部分（32 位字符串）

5. **重要**：分享数据库给 Integration
   - 点击数据库右上角 "..." → "Add connections"
   - 选择你创建的 Integration

### 3. 配置到 OpenClaw

```bash
# 使用 gateway config.patch
openclaw gateway config.patch
```

添加以下配置：

```json
{
  "env": {
    "NOTION_TOKEN": "secret_your_token_here",
    "NOTION_DATABASE_ID": "your_database_id_here"
  }
}
```

## 使用方式

### 基础命令

```bash
# 同步文章
python skills/notion-sync/scripts/notion_sync.py sync \
  --title "文章标题" \
  --content articles/article.md \
  --tags "OpenClaw,教程" \
  --status "已发布"

# 查询数据库
python skills/notion-sync/scripts/notion_sync.py list --limit 10

# 更新页面
python skills/notion-sync/scripts/notion_sync.py update \
  --page-id "page_id" \
  --status "草稿"
```

### 集成到公众号发布流程

在 `wechat-mp-publish` 技能中添加自动同步：

```python
# 发布公众号后自动同步到 Notion
subprocess.run([
    'python', 'skills/notion-sync/scripts/notion_sync.py', 'sync',
    '--title', title,
    '--content', content_path,
    '--tags', '公众号,OpenClaw',
    '--status', '已发布'
])
```

## API 参考

- 官方文档：https://developers.notion.com/
- Python SDK：https://github.com/ramnes/notion-sdk-py

## 示例：Notion 数据库结构

| 标题 | 状态 | 标签 | 发布日期 | 链接 |
|------|------|------|----------|------|
| OpenClaw 入门指南 | 已发布 | OpenClaw,教程 | 2026-02-19 | https://... |
| MCP 协议研究 | 草稿 | MCP,AI | - | - |

## 注意事项

⚠️ **Notion API 限制**
- 3 requests/second（免费版）
- 单个页面最多 100 个 blocks

⚠️ **Markdown 转 Notion Block**
- 支持：标题、段落、列表、代码块、引用
- 不支持：部分复杂格式、表格（需要特殊处理）

## 扩展功能（可选）

- [ ] 自动上传图片到 Notion
- [ ] 双向同步（Notion → 本地）
- [ ] 定时同步任务
- [ ] 多数据库支持

---

**创建时间**：2026-02-19
**作者**：小J
