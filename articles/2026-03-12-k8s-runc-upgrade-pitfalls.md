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

**原理**：
- runc 在执行 `exec` 时会打开 `/proc/self/exe`
- 攻击者可以在容器内替换 `/proc/self/exe` 指向的文件
- 当宿主机执行 `kubectl exec` 时，会运行攻击者的恶意代码

**修复版本**：runc >= 1.0-rc6

### 2. CVE-2021-30465 - Symlink Exchange Attack

**严重程度**：CVSS 8.2 (High)

**影响**：攻击者可以通过符号链接交换获取宿主机文件系统访问权限。

**原理**：
- runc 在处理文件系统时存在竞态条件
- 攻击者可以通过符号链接交换绕过安全检查

**修复版本**：runc >= 1.0.0-rc95

### 3. CVE-2024-21626 - File Descriptor Leak

**严重程度**：CVSS 8.6 (High)

**影响**：攻击者可以通过泄漏的文件描述符访问宿主机文件系统。

**原理**：
- runc 在 `exec` 时泄漏了 `/sys/fs/cgroup` 的文件描述符
- 攻击者可以通过 `/proc/self/fd/` 访问宿主机目录

**修复版本**：runc >= 1.1.12

### 4. CVE-2024-3154 - Container Escape via Hooks

**严重程度**：CVSS 8.6 (High)

**影响**：攻击者可以通过容器生命周期钩子执行任意代码。

**原理**：
- runc 在处理 prestart/poststop hooks 时存在安全漏洞
- 攻击者可以注入恶意钩子代码

**修复版本**：runc >= 1.1.13

---

## 🕳️ 升级过程中的坑

### 坑 1：K8s 版本兼容性

**问题**：不同版本的 K8s 对 runc 有不同的版本要求。

**示例**：
| K8s 版本 | runc 版本要求 |
|----------|---------------|
| 1.24.x | >= 1.0.2 |
| 1.25.x | >= 1.1.0 |
| 1.26.x | >= 1.1.0 |
| 1.27.x | >= 1.1.1 |
| 1.28.x | >= 1.1.2 |

**解决**：升级前检查 K8s 官方文档的版本兼容性矩阵。

### 坑 2：containerd 版本依赖

**问题**：containerd 和 runc 有版本依赖关系。

**示例**：
| containerd 版本 | runc 版本要求 |
|-----------------|---------------|
| 1.6.x | >= 1.1.0 |
| 1.7.x | >= 1.1.2 |
| 2.0.x | >= 1.2.0 |

**解决**：升级 runc 前先确认 containerd 版本。

### 坑 3：操作系统包管理器冲突

**问题**：系统自带的 runc 包和手动安装的版本冲突。

**示例**：
```bash
# Ubuntu/Debian
apt install runc  # 可能安装旧版本

# CentOS/RHEL
yum install runc  # 可能安装旧版本
```

**解决**：
```bash
# 手动安装最新版本
wget https://github.com/opencontainers/runc/releases/download/v1.1.13/runc.amd64
chmod +x runc.amd64
mv runc.amd64 /usr/local/sbin/runc
```

### 坑 4：节点重启导致 Pod 重建

**问题**：升级 runc 后需要重启 containerd/kubelet，会导致所有 Pod 重建。

**影响**：
- 所有 Pod 重新调度
- 服务中断（取决于 PDB 配置）
- 存储卷可能被重新挂载

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

**错误示例**：
```
Error: failed to create containerd task: OCI runtime create failed:
container with id exists: <container-id>
```

**解决**：
```bash
# 清理旧的 Pod Sandbox
crictl rm -a
crictl rmp -a
```

### 坑 6：CNI 插件兼容性

**问题**：升级后 CNI 插件可能无法正常工作。

**错误示例**：
```
NetworkPlugin cni failed to set up pod network: failed to allocate for range
```

**解决**：
```bash
# 重启 CNI 插件
kubectl rollout restart daemonset <cni-daemonset> -n kube-system
```

### 坑 7：安全策略冲突

**问题**：升级后 Pod Security Policy (PSP) 或 Pod Security Standards (PSS) 可能阻止 Pod 启动。

**错误示例**：
```
Error: container has runAsNonRoot and image will run as root
```

**解决**：
```yaml
# 检查 Pod 安全上下文
securityContext:
  runAsNonRoot: true
  runAsUser: 1000
```

---

## 🛠️ 最佳实践

### 1. 滚动升级策略

```bash
# 逐个节点升级
for node in $(kubectl get nodes -o name); do
  # 驱逐节点
  kubectl drain $node --ignore-daemonsets --delete-emptydir-data
  
  # SSH 到节点升级 runc
  ssh $node "systemctl stop containerd && \
             cp /path/to/new/runc /usr/local/sbin/runc && \
             chmod +x /usr/local/sbin/runc && \
             systemctl start containerd && \
             systemctl restart kubelet"
  
  # 恢复节点
  kubectl uncordon $node
  
  # 等待节点就绪
  kubectl wait --for=condition=Ready $node --timeout=300s
done
```

### 2. 版本验证

```bash
# 检查 runc 版本
runc --version

# 检查 containerd 版本
containerd --version

# 检查 kubelet 版本
kubelet --version
```

### 3. 回滚计划

```bash
# 升级前备份
cp /usr/local/sbin/runc /usr/local/sbin/runc.bak

# 升级失败时回滚
systemctl stop containerd
mv /usr/local/sbin/runc.bak /usr/local/sbin/runc
systemctl start containerd
systemctl restart kubelet
```

### 4. 监控和告警

```yaml
# Prometheus 告警规则
groups:
- name: runc
  rules:
  - alert: RuncVersionOutdated
    expr: runc_version < 1.1.13
    for: 1h
    labels:
      severity: critical
    annotations:
      summary: "runc version is outdated"
      description: "Node {{ $labels.node }} is running runc {{ $labels.version }}"
```

### 5. 安全扫描

```bash
# 使用 Trivy 扫描
trivy fs /usr/local/sbin/runc

# 使用 Grype 扫描
grype /usr/local/sbin/runc
```

---

## 📊 升级检查清单

- [ ] 确认当前 runc 版本
- [ ] 确认目标 runc 版本
- [ ] 检查 K8s 版本兼容性
- [ ] 检查 containerd 版本兼容性
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

**记住**：runc 是 K8s 的核心组件，升级必须谨慎。

---

如果觉得有用，点个"在看"吧 👇
