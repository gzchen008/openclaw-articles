# OpenClaw v2026.3.7 版本更新

> 发布时间：2026-03-08

## 📦 更新总览

OpenClaw 发布了最新版本 **v2026.3.7**，带来了多项重要功能和改进。以下是本次更新的详细内容。

---

## 🚀 新功能

1. Agents/context engine plugin interface: add `ContextEngine` plugin slot with full lifecycle hooks (`bootstrap`, `ingest`, `assemble`, `compact`, `afterTurn`, `prepareSubagentSpawn`, `onSubagentEnded`), slot-based registry with config-driven resolution, `LegacyContextEngine` wrapper preserving existing compaction behavior, scoped subagent runtime for plugin runtimes via `AsyncLocalStorage`, and `sessions.get` gateway method. Enables plugins like `lossless-claw` to provide alternative context management strategies without modifying core compaction logic. Zero behavior change when no context engine plugin is configured. (#22201) thanks @jalehman.

2. ACP/persistent channel bindings: add durable Discord channel and Telegram topic binding storage, routing resolution, and CLI/docs support so ACP thread targets survive restarts and can be managed consistently. (#34873) Thanks @dutifulbob.

3. Telegram/ACP topic bindings: accept Telegram Mac Unicode dash option prefixes in `/acp spawn`, support Telegram topic thread binding (`--thread here|auto`), route bound-topic follow-ups to ACP sessions, add actionable Telegram approval buttons with prefixed approval-id resolution, and pin successful bind confirmations in-topic. (#36683) Thanks @huntharo.

4. Telegram/topic agent routing: support per-topic `agentId` overrides in forum groups and DM topics so topics can route to dedicated agents with isolated sessions. (#33647; based on #31513) Thanks @kesor and @Sid-Qin.

5. Web UI/i18n: add Spanish (`es`) locale support in the Control UI, including locale detection, lazy loading, and language picker labels across supported locales. (#35038) Thanks @DaoPromociones.


*注：本次更新共 27 项新功能，以上为部分精选。*

---
## ⚠️ 破坏性变更

- **BREAKING:** Gateway auth now requires explicit `gateway.auth.mode` when both `gateway.auth.token` and `gateway.auth.password` are configured (including SecretRefs). Set `gateway.auth.mode` to `token` or `password` before upgrade to avoid startup/pairing/TUI failures. (#35094) Thanks @joshavant.

---
## 🐛 Bug 修复

1. Models/MiniMax: stop advertising removed `MiniMax-M2.5-Lightning` in built-in provider catalogs, onboarding metadata, and docs; keep the supported fast-tier model as `MiniMax-M2.5-highspeed`.

2. Security/Config: fail closed when `loadConfig()` hits validation or read errors so invalid configs cannot silently fall back to permissive runtime defaults. (#9040) Thanks @joetomasone.

3. Memory/Hybrid search: preserve negative FTS5 BM25 relevance ordering in `bm25RankToScore()` so stronger keyword matches rank above weaker ones instead of collapsing or reversing scores. (#33757) Thanks @lsdcc01.

4. LINE/`requireMention` group gating: align inbound and reply-stage LINE group policy resolution across raw, `group:`, and `room:` keys (including account-scoped group config), preserve plugin-backed reply-stage fallback behavior, and add regression coverage for prefixed-only group/room config plus reply-stage policy resolution. (#35847) Thanks @kirisame-wang.

5. Onboarding/local setup: default unset local `tools.profile` to `coding` instead of `messaging`, restoring file/runtime tools for fresh local installs while preserving explicit user-set profiles. (from #38241, overlap with #34958) Thanks @cgdusek.

---

## 📝 升级指南

### 升级命令

\`\`\`bash
# 使用 npm 升级
npm update -g openclaw

# 或使用 homebrew
brew upgrade openclaw
\`\`\`

### 检查版本

\`\`\`bash
openclaw --version
\`\`\`

### 查看完整更新日志

完整更新日志和详细说明请访问：

🔗 [OpenClaw Releases](https://github.com/openclaw/openclaw/releases/tag/v2026.3.7)

---

## 💡 相关资源

- 📚 [OpenClaw 文档](https://docs.openclaw.ai)
- 💬 [Discord 社区](https://discord.gg/clawd)
- 🌟 [GitHub 仓库](https://github.com/openclaw/openclaw)

---

*本文由 OpenClaw 自动生成*

---

**关注我们，第一时间获取 OpenClaw 最新动态！**

