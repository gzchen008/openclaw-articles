# SearXNG Podman 部署指南

🔍 **适用于 Podman 用户的 SearXNG 部署方案**

Podman 优势：
- ✅ 无需 root 权限（Rootless）
- ✅ 无守护进程（Daemonless）
- ✅ 与 Docker 兼容
- ✅ 更好的安全性

## 🚀 快速开始

### 方式 1: 使用管理脚本（推荐）

```bash
cd /Users/cgz/.openclaw/workspace/tools/searxng

# 启动服务
./searxng-podman.sh start

# 查看状态
./searxng-podman.sh status

# 查看日志
./searxng-podman.sh logs

# 停止服务
./searxng-podman.sh stop

# 重启服务
./searxng-podman.sh restart

# 更新镜像
./searxng-podman.sh update

# 进入容器
./searxng-podman.sh shell
```

### 方式 2: 使用独立脚本

```bash
cd /Users/cgz/.openclaw/workspace/tools/searxng

# 安装
./install-podman.sh

# 启动
cd ~/searxng-podman
./start-podman.sh

# 停止
./stop-podman.sh
```

### 方式 3: 使用 Podman Compose

如果你安装了 `podman-compose`：

```bash
cd /Users/cgz/.openclaw/workspace/tools/searxng
podman-compose -f docker-compose.yml up -d
```

### 方式 4: 使用 Systemd（高级）

使用 Podman Quadlet 集成到 systemd：

```bash
# 1. 复制 quadlet 文件
mkdir -p ~/.config/containers/systemd
cp searxng.container ~/.config/containers/systemd/

# 2. 生成 secret key
mkdir -p ~/searxng-podman/searxng
openssl rand -hex 32 > ~/searxng-podman/secret.key

# 3. 更新 quadlet 文件中的 SECRET_KEY
sed -i '' "s/{{SECRET_KEY}}/$(cat ~/searxng-podman/secret.key)/g" \
    ~/.config/containers/systemd/searxng.container

# 4. 重新加载 systemd
systemctl --user daemon-reload

# 5. 启动服务
systemctl --user start searxng

# 6. 设置开机自启
systemctl --user enable searxng
```

## 🌐 访问服务

| 方式 | URL | 说明 |
|------|-----|------|
| Web 界面 | http://localhost:8080 | 浏览器访问 |
| JSON API | http://localhost:8080/search?q=关键词＆format=json | API 调用 |
| 状态检查 | http://localhost:8080/status | 健康检查 |

## 🔧 常用 Podman 命令

```bash
# 查看运行中的容器
podman ps

# 查看所有容器（包括停止的）
podman ps -a

# 查看日志
podman logs searxng

# 实时查看日志
podman logs -f searxng

# 进入容器
podman exec -it searxng /bin/sh

# 重启容器
podman restart searxng

# 删除容器
podman rm -f searxng

# 查看镜像
podman images

# 删除镜像
podman rmi searxng/searxng:latest

# 拉取最新镜像
podman pull searxng/searxng:latest
```

## ⚙️ 配置文件

配置文件位置：`~/searxng-podman/searxng/settings.yml`

```bash
# 编辑配置
vim ~/searxng-podman/searxng/settings.yml

# 重启生效
./searxng-podman.sh restart
```

## 🔄 与 Python 版本对比

| 特性 | Podman 版本 | Python 版本 |
|------|-------------|-------------|
| 真实搜索 | ✅ 完整搜索引擎 | ⚠️ 模拟结果 |
| 资源占用 | 需要容器运行时 | 仅 Python |
| 配置灵活 | 高度可配置 | 基础功能 |
| 中文支持 | 完整 | 基础 |
| 引擎数量 | 100+ | 模拟 |

## 🐛 故障排除

### 端口被占用

```bash
# 查看占用 8080 的进程
lsof -i :8080

# 使用其他端口
./searxng-podman.sh stop
podman run -d --name searxng -p 8081:8080 ...
```

### 权限问题

```bash
# 修复卷权限
podman unshare chown -R $(id -u):$(id -g) ~/searxng-podman/searxng
```

### 镜像拉取失败

```bash
# 使用镜像代理
podman pull docker.io/searxng/searxng:latest

# 或使用其他镜像源
podman pull registry.cn-hangzhou.aliyuncs.com/searxng/searxng:latest
```

### 容器启动失败

```bash
# 查看详细日志
podman logs searxng

# 检查配置语法
podman run --rm -v ~/searxng-podman/searxng:/etc/searxng:ro searxng/searxng:latest cat /etc/searxng/settings.yml
```

## 📝 更新 SearXNG

```bash
./searxng-podman.sh update
```

或手动：

```bash
./searxng-podman.sh stop
podman pull searxng/searxng:latest
./searxng-podman.sh start
```

## 🗑️ 完全卸载

```bash
# 停止并删除容器
./searxng-podman.sh stop

# 删除镜像
podman rmi searxng/searxng:latest

# 删除数据
rm -rf ~/searxng-podman

# 如果使用 systemd
systemctl --user stop searxng
systemctl --user disable searxng
rm ~/.config/containers/systemd/searxng.container
systemctl --user daemon-reload
```

## 📚 相关链接

- [Podman 文档](https://docs.podman.io/)
- [SearXNG 文档](https://docs.searxng.org/)
- [Podman Compose](https://github.com/containers/podman-compose)
- [Podman Quadlet](https://docs.podman.io/en/latest/markdown/podman-systemd.unit.5.html)

---

💡 **提示**: Podman 版本提供完整的搜索引擎功能，包括 Google、Bing、百度等多引擎聚合。Python 版本是轻量级模拟，适合快速测试。
