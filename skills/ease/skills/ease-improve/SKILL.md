---
name: ease-improve
description: Use when analyzing Claude session files to identify skill improvement opportunities and generate structured optimization proposals.
tools: Glob, Grep, Read, Write, Bash, Edit
---

# Ease Improve

## Overview

**Ease Improve analyzes Claude session transcripts to identify improvement opportunities for ease skills and generate structured optimization proposals.**

This skill bridges the gap between skill usage patterns and skill evolution by:
1. Extracting skill-related content from Claude session JSONL files
2. Analyzing patterns, issues, and improvement opportunities
3. Generating structured optimization proposals in BRD format

## When to Use

**Triggering symptoms:**
- You need to understand how ease skills perform in real sessions
- You want to identify patterns from skill usage (failures, successes, edge cases)
- You need to generate optimization requirements for skill improvements
- You want to track skill evolution based on actual usage data

**Input sources:**
- Claude session JSONL files (`~/.claude/projects/*/session-*.jsonl`)
- Project-specific session transcripts

**Do NOT use when:**
- Analyzing general project patterns → `reflect` command
- Creating skills from scratch → `writing-skills`
- Code quality review → `ease:code-review`

## Quick Reference

| Task | Method | Output |
|---|---|---|
| Analyze single session | Parse JSONL, extract ease skill content | Console summary |
| Generate BRD proposal | Synthesize patterns into structured doc | `docs/brd/###-skill-name-optimization.md` |
| Token analysis | Use `analyze-token-usage.py` script | Token usage report |

## Decision Flowchart

```dot
digraph ease_improve_decision {
    "Have session file?" [shape=diamond];
    "Single session" [shape=box, label="Parse JSONL\n→ Extract ease skill content\n→ Generate summary"];
    "Multiple sessions" [shape=box, label="Analyze patterns\n→ Identify issues\n→ Generate BRD"];
    "ease-improve" [shape=ellipse, style=filled, fillcolor=lightblue];

    "Have session file?" -> "Single session" [label="Yes, one file"];
    "Have session file?" -> "Multiple sessions" [label="Yes, multiple files"];
    "Single session" -> ease-improve;
    "Multiple sessions" -> ease-improve;
}
```

## Non-negotiables

### Output structure
- BRD files saved to: `docs/brd/[###]-[skill-name]-optimization.md`
- Follow existing BRD format (see `docs/brd/001-ease-analysis-skill-optimization.md`)
- Use incrementing three-digit numbers (001, 002, 003...)

### Analysis requirements
- Extract content related to ease skills only
- Identify patterns: successful usage, failures, edge cases, user corrections
- Focus on actionable improvements (not general observations)
- Include specific examples from session transcripts

### Quality standards
- Each optimization proposal must include:
  - **问题类别**: CSO / 结构 / 一致性 / Token效率 / 可发现性
  - **严重程度**: 高 / 中 / 低
  - **问题描述**: Clear, specific description
  - **建议**: Actionable improvement steps

## Implementation

### 1. Locate Session Files

Find Claude session JSONL files:

```bash
# For Unix/Linux/macOS
SESSION_FILE=$(ls -t ~/.claude/projects/-*/session-*.jsonl 2>/dev/null | head -1)
echo "Session: $SESSION_FILE"

# For Windows (PowerShell)
$sessionFile = Get-ChildItem -Path "$env:USERPROFILE\.claude\projects\*\session-*.jsonl" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1
Write-Output "Session: $($sessionFile.FullName)"
```

### 2. Extract Ease Skill Content

Parse JSONL and filter for ease skill related content:

```python
# Key patterns to extract:
- Skill invocations (ease:* commands)
- Skill file reads (plugins/ease/skills/*/SKILL.md)
- Ease-related tool usage
- User feedback about ease skills
- Errors/issues with ease skills
```

### 3. Analyze Patterns

Look for:
- **Successful patterns**: What worked well?
- **Failures**: Where did the skill not help?
- **User corrections**: What did users override?
- **Token efficiency**: Is the skill consuming excessive context?
- **CSO issues**: Can the skill be found/discovered?
- **Structure issues**: Is documentation clear?

### 4. Generate BRD Proposal

Use this template for `docs/brd/###-[skill-name]-optimization.md`:

```markdown
# [Skill Name] 优化建议

## 概述

本文档基于 Claude session 分析，对 `[skill-name]` 进行审查，并提供结构化优化建议。

- **审查日期**: [YYYY-MM-DD]
- **数据来源**: [Session file(s) analyzed]
- **目标技能**: [skill-name]
- **状态**: [待实现/进行中/已完成]

---

## 关键问题概览

| 类别 | 严重程度 | 问题描述 |
|---|---:|---|
| [类别] | [严重程度] | [问题描述] |
...

---

## 详细分析

### 1) [问题类别标题]

### 当前状态

[Describe current state with specific examples from session]

### 主要问题

[List specific issues identified]

### 建议

[Provide actionable improvement recommendations]

---

## 优化优先级

### P0（立刻做）
1. [Critical issue]
2. [Critical issue]

### P1（重要）
1. [Important issue]

### P2（增强）
1. [Enhancement]
```

### 5. Token Analysis (Optional)

Use the `analyze-token-usage.py` script:

```bash
# Analyze token usage for a session
python3 /path/to/analyze-token-usage.py <session-file.jsonl>
```

## Common Mistakes

| 错误 | 症状 | 修复 |
|---|---|---|
| 分析非 ease 相关内容 | BRD 包含无关信息 | 仅提取 ease skill 相关内容 |
| 缺少具体示例 | 问题描述抽象 | 引用 session 中的具体对话 |
| 建议不可操作 | 描述问题但不给方案 | 每个问题必须包含可执行的改进建议 |
| 格式不一致 | BRD 结构混乱 | 严格遵循现有 BRD 模板 |

## Session Analysis Patterns

### What to Extract

**Ease skill invocations:**
```jsonl
{"type": "user", "content": [{"type": "toolUse", "name": "Skill", "input": {"skill": "ease:analyze-brd", ...}}]}
```

**Ease skill file reads:**
```jsonl
{"type": "assistant", "message": {"content": [{"type": "toolResult", "toolName": "Read", "input": {"filePath": "plugins/ease/skills/..."}}]}}
```

**User feedback patterns:**
- "No, don't use that skill"
- "This skill is not helping"
- "Let me try a different approach"
- Corrections after skill invocation

**Error patterns:**
- Skill not found errors
- Tool usage failures
- Context window issues
- Malformed skill content

## See Also

- `diary.md` - Project diary entry creation
- `reflect.md` - Diary analysis for CLAUDE.md updates
- `tests/claude-code/analyze-token-usage.py` - Token usage analysis script
- `docs/brd/` - Existing optimization proposals (reference format)
- `writing-skills/SKILL.md` - Skill writing best practices
