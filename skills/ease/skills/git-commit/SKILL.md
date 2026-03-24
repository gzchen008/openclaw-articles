---
name: git-commit
description: Use when creating a Git commit and needing Conventional Commits format with safety checks, especially when unsure what type/scope/subject to use.
tools: Glob, Grep, Read, BashOutput, Bash
model: inherit
---

# Git Commit

## Overview

Intelligent Git commit assistant that automatically gathers all current branch changes, analyzes git diff to generate Conventional Commits-style messages, then performs commit and push in one automated flow.

## When to Use

**Use when:**
- User has current branch changes and wants one-shot automated commit and push
- User wants Conventional Commits format (type/scope:subject)
- User needs commit message quality check and auto-generated summary
- User wants the tool to collect all changes automatically

**Do NOT use:**
- User wants Git branching strategy → Use `gitflow-worktree`
- User wants code review → Use `code-review`
- User wants to merge/rebase/cherry-pick → Use appropriate Git commands directly
- User wants to undo changes → Use `git restore`/`git checkout` directly

## Quick Reference

| You want to... | First step | Then go to... |
|----------------|-----------|---------------|
| Commit current branch changes | Check full working tree diff | Generate message → auto stage → commit → push |
| Commit all changes | Collect staged + unstaged changes automatically | See automated workflow |
| Split changes into atomic commits | Not the default mode of this skill | Use manual Git commands separately |
| Mark breaking change | Use `feat!:` type or `BREAKING CHANGE:` footer | Breaking Change section |
| Revert a commit | Use `revert:` type | Revert section |
| Add co-author | Add `Co-authored-by:` trailer | Trailers section |

## Non-negotiables

### Automation Rules (MUST Follow)

**Auto-collect full branch changes:**
- Default to collecting staged and unstaged changes together
- Automatically include the current branch working tree in one commit
- Execute `git add -A` as the default staging strategy

**Sensitive file red lines:**
- If changed files match `.env*`, `credentials*`, `id_rsa*`, `*.key`, `*.pem`, etc. MUST stop and warn user
- If `.gitignore` would match but file is already tracked or included in this commit, warn user explicitly

**Forbidden operations:**
- NEVER use `--no-verify` or `--no-gpg-sign` (unless user explicitly requests)
- NEVER use `git commit --amend` automatically
- NEVER use `push --force` automatically

**Pre-commit hook failure:**
- Hook failed → fix the issue → create NEW commit
- Hook auto-format changed working tree → re-stage all affected files and continue automated flow

### Conventional Commits Format

First line MUST be: `<type>(<scope>): <subject>`

**Types:** `feat`(new feature) | `fix`(bug fix) | `docs`(documentation) | `style`(formatting) | `refactor`(change without behavior) | `perf`(performance) | `test`(tests) | `chore`(maintenance) | `ci`(CI/CD) | `build`(build system) | `revert`(revert a previous commit)

**Body guidelines:**
- Subject: WHAT changed (verb-first, no trailing period, Chinese unless project uses English)
- Body: WHY changed / impact / risk / migration steps (only when needed)
- Use bullet points (-) for multi-line body

**When body is needed:**
- Multi-module changes
- Behavior changes / fixing production issues
- Migration steps or breaking changes
- Complex refactoring

### Breaking Change

When compatibility is broken:

1. **Preferred (if project supports):** Use `!` after type
   ```
   feat!: remove deprecated user endpoints
   ```

2. **Or use footer:**
   ```
   feat(api): add rate limiting

   BREAKING CHANGE: API endpoints now require authentication header
   ```

### Revert Commits

Format: `revert: <subject of original commit>`

Body must explain WHY reverting:
```
revert: add user login via OAuth

Causing session conflicts with local auth flow. Need redesign.
```

### Trailers

Supported trailers (optional):
- `Co-authored-by:` - multiple authors
- `Refs:` - references issues / PRs
- `Closes:` - closes an issue
- `Reviewed-by:` - code review credit

Example:
```
feat(auth): add OAuth2 login

Co-authored-by: Alice <alice@example.com>
Refs: #123
Closes: #456
```

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Sensitive files included by automation | Secrets enter commit or remote history | Stop immediately and warn user |
| Weak messages | "fix bug", "update files" | Describe WHAT + WHY + scope |
| Missing body when needed | Multi-module change in one line | Add body explaining impact/risk |
| Overly long subject | Subject spans multiple lines | Keep subject ≤72 chars, use body for details |
| Forgetting breaking change | Changelogs don't show breaking change | Use `feat!:` or `BREAKING CHANGE:` footer |
| Oversized automated commit | One commit does 5 different things | Allow automation but summarize all key changes accurately |

## Workflow

1. **Check workspace status** - `git status --porcelain`
2. **Get full diff** - Read both `git diff` and `git diff --cached`
3. **Analyze changes** - Files modified, type/rule determination
4. **Generate message** - Conventional Commits format with type/scope/subject
5. **Stage all changes** - Execute `git add -A`
6. **Execute commit** - Run `git commit -m`
7. **Push automatically** - Run `git push`

## Type Detection Rules

| Change characteristic | Type |
|---------------------|------|
| New file/function/class | `feat` |
| Bug fix / error handling | `fix` |
| Only .md files | `docs` |
| Only whitespace/format | `style` |
| Code restructure, same behavior | `refactor` |
| Performance optimization | `perf` |
| Add/modify tests | `test` |
| package.json / dependencies | `chore` |
| CI/CD config | `ci` |
| Build scripts (webpack/vite) | `build` |

## Multi-type Changes

When commit has multiple change types:

1. Priority: `fix` > `feat` > `refactor` > others
2. Choose highest impact type as primary
3. Describe other types in body

### Dependency Lock Files

| File | Type | Reason |
|------|------|--------|
| `package-lock.json` | `chore` | Dependency lock, not functional change |
| `yarn.lock` | `chore` | Dependency lock, not functional change |
| `pnpm-lock.yaml` | `chore` | Dependency lock, not functional change |
| `go.sum` | `chore` | Go module checksums |
| `Cargo.lock` | `chore` | Rust dependency lock |
| `poetry.lock` | `chore` | Python dependency lock |
| `Gemfile.lock` | `chore` | Ruby dependency lock |

## Post-Commit Verification

提交后必须验证：

- [ ] **提交成功**: `git log -1 --pretty=format:%s` 显示正确的提交信息
- [ ] **推送成功**: 远程分支已包含最新提交
- [ ] **格式合规**: 提交信息符合 `<type>(<scope>): <subject>` 格式
- [ ] **无敏感文件**: 再次检查未提交 `.env`, `credentials`, `*.key` 等敏感文件
- [ ] **Hook 通过**: 如果项目有 pre-commit hooks，确认它们已执行通过

## Edge Cases

| 场景 | 处理策略 |
|------|----------|
| **空提交** (无变更) | 拒绝提交，提示用户 `git status` 检查变更 |
| **合并冲突** | 暂停提交流程，提示用户先解决冲突 (`git status` 查看冲突文件) |
| **子模块变更** | 识别子模块路径，建议分别提交主项目和子模块 |
| **Hook 失败** | 显示 hook 错误信息，要求修复后重新提交（不自动 amend） |
| **已推送的提交需要修改** | 拒绝 amend，建议用 `git revert` + 新提交 |
| **超大提交** (>50 文件) | 建议拆分为多个原子提交，使用 `git add -p` 分批处理 |

## See Also

### Upstream (Related Skills)
- `ease-coding/SKILL.md` - Code implementation that leads to commits
- `ease-testing/SKILL.md` - Test changes that need committing

### Downstream (Next Steps)
- `gitflow-worktree/SKILL.md` - Git branching and pushing strategy
- Remote branch follow-up or PR creation after auto push

### Alternatives
- `git/SKILL.md` - Git branch management entry point
- Manual Git commands for complex scenarios

### References
- `commands/git-commit.md` - Command interface with detailed workflow
- `https://www.conventionalcommits.org/` - Conventional Commits specification
