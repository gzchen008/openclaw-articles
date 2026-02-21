# SearXNG 自建搜索服务

🔍 **隐私保护的元搜索引擎**，聚合 Google、Bing、百度等多个搜索引擎结果

## ✨ 特点

- 🔒 **隐私保护** - 不记录搜索历史，保护用户隐私
- 🌐 **多引擎聚合** - 同时搜索 Google、Bing、百度等
- 🚀 **本地部署** - 数据完全掌控在自己手中
- 🔌 **API 支持** - 支持 JSON API，可被 OpenClaw 等工具调用
- 🇨🇳 **中文优化** - 针对中文用户优化配置

## 🚀 快速开始

### 1. 一键安装

```bash
# 运行安装脚本
./install.sh

# 启动服务
cd ~/searxng && docker-compose up -d
```

### 2. 手动安装

```bash
# 1. 创建目录
mkdir -p ~/searxng && cd ~/searxng

# 2. 复制配置文件
cp docker-compose.yml searxng/
cp settings.yml searxng/searxng/

# 3. 启动
docker-compose up -d
```

### 3. 验证安装

```bash
# 检查容器状态
docker ps | grep searxng

# 测试搜索
curl "http://localhost:8080/search?q=hello&format=json"
```

## 🌐 访问方式

| 方式 | 地址 | 说明 |
|------|------|------|
| Web 界面 | http://localhost:8080 | 浏览器直接访问 |
| JSON API | http://localhost:8080/search?q=关键词&format=json | 程序化调用 |
| OpenClaw | 使用 search.sh 脚本 | 命令行搜索 |

## 🔧 OpenClaw 集成

### 方法 1: 直接调用脚本

```bash
# 搜索并显示结果
./search.sh "OpenClaw 教程" 5
```

### 方法 2: 添加到 TOOLS.md

在 `workspace/TOOLS.md` 中添加：

```markdown
## 搜索工具

- SearXNG 本地搜索: `tools/searxng/search.sh "关键词"`
- API 地址: http://localhost:8080
```

### 方法 3: 创建 OpenClaw Skill

创建一个 Skill 让 OpenClaw 直接调用 SearXNG：

```json
{
  "name": "searxng-search",
  "command": "tools/searxng/search.sh",
  "description": "本地 SearXNG 搜索"
}
```

## ⚙️ 配置说明

### 修改配置

```bash
# 编辑配置文件
vim ~/searxng/searxng/settings.yml

# 重启生效
docker-compose restart
```

### 常用配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `server.port` | 8080 | 服务端口 |
| `search.safe_search` | 0 | 安全搜索级别 |
| `search.default_lang` | zh-CN | 默认语言 |
| `engines` | - | 启用的搜索引擎 |

### 添加搜索引擎

在 `settings.yml` 的 `engines` 部分添加：

```yaml
engines:
  - name: google
    engine: google
    shortcut: go
    
  - name: baidu
    engine: baidu
    shortcut: bd
```

## 🌟 高级用法

### 使用代理

如果在国内访问外网搜索引擎，可配置代理：

```yaml
outgoing:
  proxies:
    all://:
      - http://proxy:8080
```

### 启用 HTTPS

使用 Nginx 反向代理 + SSL：

```nginx
server {
    listen 443 ssl;
    server_name search.yourdomain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 自定义主题

```yaml
ui:
  theme_args:
    oscar_style: logicodev-dark  # 深色主题
    # oscar_style: logicodev  # 浅色主题
```

## 🔍 API 使用示例

### JSON API

```bash
# 基本搜索
curl "http://localhost:8080/search?q=OpenClaw&format=json"

# 指定语言
curl "http://localhost:8080/search?q=AI&format=json&language=en"

# 图片搜索
curl "http://localhost:8080/search?q=cat&format=json&categories=images"

# 新闻搜索
curl "http://localhost:8080/search?q=tech&format=json&categories=news"
```

### Python 调用

```python
import requests

def search(query, limit=10):
    url = "http://localhost:8080/search"
    params = {
        "q": query,
        "format": "json",
        "language": "zh-CN"
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    for result in data["results"][:limit]:
        print(f"{result['title']}")
        print(f"  {result['url']}")
        print(f"  {result['content'][:100]}...\n")

search("OpenClaw 教程")
```

## 🐛 故障排除

### 容器无法启动

```bash
# 查看日志
docker logs searxng

# 检查端口占用
lsof -i :8080
```

### 搜索结果为空

1. 检查网络连接：`curl https://google.com`
2. 检查配置文件语法
3. 查看引擎状态：访问 http://localhost:8080/preferences

### 性能优化

```yaml
# 启用缓存
search:
  cache_url: https://webcache.googleusercontent.com/search?q=cache:{href}
  
# 限制并发
outgoing:
  pool_connections: 100
  pool_maxsize: 100
```

## 📚 相关链接

- 📖 [官方文档](https://docs.searxng.org/)
- 🐙 [GitHub](https://github.com/searxng/searxng)
- 🌐 [公共实例列表](https://searx.space/)

## 📝 更新日志

- 2026-02-11: 初始版本，中文优化配置

---

💡 **提示**: 此配置已针对中文用户优化，包含百度、360搜索等国内引擎。如需添加更多引擎，编辑 `settings.yml` 文件。
