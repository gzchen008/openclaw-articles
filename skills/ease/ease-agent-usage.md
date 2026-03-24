# ease-agent 使用指南

ease-agent 是一款面向专业开发者的结对编程助手，聚焦代码实现、重构、调试与架构设计，提供可信赖的专家级指导。

## 调用方式

### 方案 1：使用 Slash Command（推荐）

用户可在命令行直接调用：

```bash
/ease:ease-agent 帮我重构这个函数，提高可读性
```

或：

```bash
/ease:ease-agent 分析 src/main/java/com/example/UserService.java 中的代码质量问题
```

优点：

- 上手成本低、语法直观
- 无需了解底层实现细节
- 适合快速、一次性任务

### 方案 2：使用 Task 工具（程序化/脚本化集成）

在 Claude Code 内部或自动化脚本中以编程方式调用：

```
Task(
  subagent_type: "ease:ease-agent",
  prompt: "Review the authentication logic in auth.ts and suggest improvements",
  description: "Code review assistance"
)
```

优点：

- 可被其他 agent 或 command 复用
- 便于在复杂工作流中集成
- 支持传递额外参数与上下文

## 专长领域

1. 编写新代码：提供实现思路与最佳实践
2. 重构现有代码：提出改进方向与重构策略
3. 调试问题：系统化定位与解决故障
4. 架构设计：给出技术选型与架构模式建议
5. 学习新技术：协作探索新框架、库与方法论
6. 代码审查：评估质量、可维护性与规范遵循

## 使用示例

### 示例 1：代码审查

```bash
/ease:ease-agent 审查 src/utils/calculator.ts，关注边界条件和错误处理
```

### 示例 2：架构设计

```bash
/ease:ease-agent 我需要设计一个用户认证系统，支持 JWT 和 OAuth2，请提供架构建议
```

### 示例 3：调试协助

```bash
/ease:ease-agent 我的 React 组件在更新状态时出现无限循环，帮我找出原因
```

### 示例 4：重构建议

```bash
/ease:ease-agent 重构 src/services/payment.ts，提高代码的可测试性
```

## 配置文件位置

- Slash Command：`plugins/ease/commands/ease-agent.md`
- Agent 定义：`plugins/ease/agents/ease-agent.md`
- 插件配置：`plugins/ease/.claude-plugin/plugin.json`

## 技术细节

ease-agent 具备以下工具访问权限：

- Glob、Grep、Read：代码检索与静态分析
- Edit、Write：代码修改与写入
- Bash、BashOutput：命令执行与结果输出
- WebFetch、WebSearch：在线资料抓取与搜索
- TodoWrite：任务分解与进度跟踪
- mcp__ide__getDiagnostics：IDE 诊断信息读取

## 自动加载的 Skills

启动时自动加载以下 skills：

- ease-analysis：领域分析
- ease-architecture：架构设计
- ease-coding：编码最佳实践
- ease-arch-documentation：文档编写
- ease-testing：测试策略
- springboot-docs：Spring Boot 文档
- fps-docs：FPS 框架文档
- git-docs：Git 工作流文档
