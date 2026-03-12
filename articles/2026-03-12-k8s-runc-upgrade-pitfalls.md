# K8s 场景下 runc 安全漏洞升级的坑

> runc 是 Kubernetes 的核心组件，每次安全漏洞升级都是一场"惊心动魄"的冒险。

---

## 🔍 runc 是什么？

**runc** 是 OCI (Open Container Initiative) 容器运行时的参考实现，是 Kubernetes 中最常用的容器运行时。

**层级关系**：
```
Kubernetes → containerd/CRI-O → runc → Linux Kernel
```

**简单说**：K8s 创建的每个 Pod，最终都由 runc 负责启动和管理。

---

## 🚨 历史上的重大 runc 漏洞

### 1. CVE-2019-5736 - 容器逃逸

**严重程度**：CVSS 9.8 (Critical)

**影响**：攻击者可以通过恶意容器获取宿主机 root 权限。

**修复版本**：runc >= 1.0-rc6

### 2. CVE-2024-21626 - File Descriptor Leak

**严重程度**：CVSS 8.6 (High)

**影响**：攻击者可以通过泄漏的文件描述符访问宿主机文件系统。

**修复版本**：runc >= 1.1.12

### 3. CVE-2024-3154 - Container Escape via Hooks

**严重程度**：CVSS 8.6 (High)

**影响**：攻击者可以通过容器生命周期钩子执行任意代码。

**修复版本**：runc >= 1.1.13

---

## 🕳️ 升级过程中的坑

### 坑 1：K8s 版本兼容性

**问题**：不同版本的 K8s 对 runc 有不同的版本要求。

**解决**：升级前检查 K8s 官方文档的版本兼容性矩阵。

### 坑 2：containerd 版本依赖

**问题**：containerd 和 runc 有版本依赖关系。

**示例**：
| containerd 版本 | runc 版本要求 |
|-----------------|---------------|
| 1.6.x | >= 1.1.0 |
| 1.7.x | >= 1.1.2 |
| 2.0.x | >= 1.2.0 |

### 坑 3：cgroup 版本兼容性（重要！）

**问题**：runc 需要正确识别系统的 cgroup 版本。

**关键点**：
- **runc 1.2.x 同时支持 cgroup v1 和 v2**
- 并没有废弃 cgroup v1！
- runc 会自动检测系统使用的 cgroup 版本

**正确的兼容性矩阵**：

| runc 版本 | cgroup v1 | cgroup v2 | 备注 |
|-----------|-----------|-----------|------|
| 1.0.x | ✅ | ❌ | 只支持 v1 |
| 1.1.x | ✅ | ✅ | 同时支持 |
| 1.2.x | ✅ | ✅ | 同时支持 |

**检查 cgroup 版本**：
```bash
# 查看当前 cgroup 版本
mount | grep cgroup

# cgroup v1 输出示例：
# cgroup on /sys/fs/cgroup/systemd type cgroup

# cgroup v2 输出示例：
# cgroup2 on /sys/fs/cgroup type cgroup2

# 或者用更简单的方法
stat -fc %T /sys/fs/cgroup/
# 输出 "cgroup2fs" 表示 v2
# 输出 "tmpfs" 表示 v1
```

**CentOS 7 的真实限制**：

| 限制因素 | 说明 |
|----------|------|
| **内核版本** | 3.10.x，缺少某些新特性 |
| **cgroup** | 只支持 v1 |
| **runc** | 可以用 1.2.x（使用 v1 模式） |

**真正的坑**：
1. **containerd 2.0.x 要求 runc >= 1.2.0**，但 CentOS 7 的 systemd 版本太老（219），可能有兼容性问题
2. **建议**：CentOS 7 用 containerd 1.7.x + runc 1.1.13 最稳定

### 坑 4：节点重启导致 Pod 重建

**问题**：升级 runc 后需要重启 containerd/kubelet，会导致所有 Pod 重建。

**解决**：
```bash
# 1. 驱逐节点
kubectl drain <node-name> --ignore-daemonsets --delete-emptydir-data

# 2. 升级 runc
systemctl stop containerd
mv /usr/local/sbin/runc /usr/local/sbin/runc.bak
cp runc.amd64 /usr/local/sbin/runc
chmod +x /usr/local/sbin/runc

# 3. 重启服务
systemctl start containerd
systemctl restart kubelet

# 4. 恢复节点
kubectl uncordon <node-name>
```

### 坑 5：Pod Sandbox 不兼容

**问题**：升级 runc 后，旧的 Pod Sandbox 可能无法正常工作。

**解决**：
```bash
# 清理旧的 Pod Sandbox
crictl rm -a
crictl rmp -a
```

---

## 🛠️ 最佳实践

### 1. 版本验证

```bash
# 检查 runc 版本
runc --version

# 检查 containerd 版本
containerd --version

# 检查 cgroup 版本
stat -fc %T /sys/fs/cgroup/
```

### 2. 回滚计划

```bash
# 升级前备份
cp /usr/local/sbin/runc /usr/local/sbin/runc.bak

# 升级失败时回滚
systemctl stop containerd
mv /usr/local/sbin/runc.bak /usr/local/sbin/runc
systemctl start containerd
systemctl restart kubelet
```

---

## 📊 升级检查清单

- [ ] 确认当前 runc 版本
- [ ] 确认目标 runc 版本
- [ ] 检查 K8s 版本兼容性
- [ ] 检查 containerd 版本兼容性
- [ ] **检查 cgroup 版本（确定用 v1 还是 v2）**
- [ ] 备份当前 runc 二进制文件
- [ ] 准备回滚脚本
- [ ] 设置 PDB (Pod Disruption Budget)
- [ ] 通知相关团队
- [ ] 选择低峰期执行
- [ ] 逐节点滚动升级
- [ ] 验证升级结果
- [ ] 监控集群状态

---

## 🎯 总结

**升级 runc 的核心原则**：

1. **先测试后生产** — 在测试环境验证升级流程
2. **逐节点滚动** — 不要一次性升级所有节点
3. **备份和回滚** — 永远要有回滚方案
4. **监控和告警** — 实时监控升级过程
5. **选择低峰期** — 减少对业务的影响

**CentOS 7 建议**：
- containerd 1.7.x + runc 1.1.13（最稳定）
- 或 containerd 1.7.x + runc 1.2.x（可用，但需测试）

---

如果觉得有用，点个"在看"吧 👇
