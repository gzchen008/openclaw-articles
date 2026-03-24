## Minimal End-to-End Example

本示例用于说明“首次生成 vs 增量更新”的最小闭环（不依赖真实仓库）。

### First run（首次全量生成）

1. **构建索引**：生成 `metadata.json.indexes`（至少 module/api/schema/config/utils）。
2. **生成文档**：按顺序产出 01-06 六份文档。
3. **质量门禁**：运行 `references/quality-gates.md` 中的 Fail/Warning 规则。
4. **落盘记忆**：写入 `metadata.json.last_generation.commit_id` + `generation_trace`（如实现）。

### Incremental run（增量更新）

输入：`metadata.json.last_generation.commit_id` 到 `HEAD` 的 diff。

1. diff 只包含 `controller` 相关文件 → **只更新 api_index**。
2. 依据新 api_index → **只更新 `03_API_INTERFACE.md`**。
3. 质量门禁：执行 API 索引对齐 + 随机反向验证。

### Failure fallback（失败回退）

当无法可靠收敛更新范围（例如大规模重构/目录迁移）时：

- 退化为“全量重建索引 + 受影响文档全量更新”。
