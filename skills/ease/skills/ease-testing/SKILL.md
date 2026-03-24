---
name: ease-testing
description: Use when generating or improving tests for existing code with unclear behavior, missing coverage, or high regression risk.
tools: Glob, Grep, Read, TodoWrite, BashOutput, Bash, Edit, Write, NotebookEdit
model: inherit
---

# Ease Testing

## Overview

Test generation and quality improvement skill focused on TDD methodology and MC/DC (Modified Condition/Decision Coverage) principles. Generates high-quality unit and integration tests across languages (Java, Go, Python, TypeScript) with proper dependency handling.

## When to Use

**Use when:**
- User needs to generate or improve tests for existing code
- Code has unclear behavior or high regression risk
- Tests are missing, flaky, or have low coverage
- User wants to follow TDD methodology or MC/DC coverage
- Refactoring requires test verification
- Code has non-deterministic behavior (time, randomness, external dependencies)

**Do NOT use:**
- User wants to write implementation code → Use `ease-coding`
- User wants architecture design → Use `ease-architecture`
- User wants to analyze code structure → Use `ease-analysis`
- User wants code review → Use `code-review`

## Quick Reference

| You want to... | First step | Then go to... |
|----------------|-----------|---------------|
| Add unit tests for a single file | Detect language/framework | `flows/generate-test-code.md` + `references/testing-<lang>.md` |
| Improve coverage to target | Run baseline coverage first | `flows/generate-test-code.md` (round-based strategy) |
| Write integration tests | Verify local dependencies available | `commands/generate-tests.md` (--integration/--all) |
| Fix flaky tests | Identify non-determinism sources | `references/testing-<lang>.md` (deterministic section) |
| Standardize test structure | Use Mustache templates | `templates/README.md` + `templates/*` |

## Non-negotiables

### Test Type → Dependency Strategy (MUST Follow)

| Test Type | Purpose | Dependency Handling |
|-----------|---------|---------------------|
| **Unit Tests** | Verify pure business logic and branches (MC/DC) | **MUST isolate** I/O dependencies (DB/Redis/MQ/network/time) via Mock/Fake. Goal: fast, deterministic, repeatable. |
| **Integration Tests** | Verify real component interaction (database, HTTP, messaging) | **PREFER** reproducible local dependencies (TestContainers/embedded/docker-compose) with explicit fallback strategy when unavailable. |

**CRITICAL: Never say "resource layer should never be mocked outright"** - this misleads in unit test context. Instead:
- "Resource layer in integration tests: use real dependencies when possible"
- "Resource layer in unit tests: MUST isolate all I/O"

### Deterministic Requirements (FIRST)

**ALL unit tests MUST be:**
- **F**ast: milliseconds, run frequently
- **I**ndependent: no dependencies between tests, parallel-safe
- **R**epeatable: same result in any environment
- **S**elf-validating: clear pass/fail, no manual inspection
- **T**imely: written before or with production code

**FORBIDDEN in unit tests:**
- `sleep()` / `setTimeout()` - use injected clock
- `Math.random()` - use seeded generator
- Real network calls - Mock all I/O
- Global state - pass parameters

### Coverage Targets

**Default targets (when project has no config):**
- Line coverage: ≥ 80%
- Branch coverage: ≥ 70%
- Method coverage: ≥ 85%

**Priority: Read project config first** (jaCoCo/jest/pytest config). User-overridable.

**For unreachable code:** Either improve code testability OR allow documented exemption - never write fragile tests just for coverage.

### Project Type Detection (MUST Execute First)

| Language | Signature File | Reference |
|----------|----------------|-----------|
| Java | `pom.xml` or `build.gradle` | `references/testing-java.md` |
| Go | `go.mod` | `references/testing-go.md` |
| Python | `requirements.txt` or `pyproject.toml` | `references/testing-python.md` |
| TypeScript | `package.json` + `tsconfig.json` | `references/testing-typescript.md` |

**Detection priority:** User-specified file extension → Java → TypeScript → Go → Python

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Writing integration tests as unit tests | Slow, environment-dependent, flaky | Unit tests MUST isolate I/O; integration tests use reproducible dependencies (containers) |
| Chasing coverage over confidence | High coverage but regressions still happen | Prioritize critical business rules/branches; treat coverage as byproduct |
| Tests depend on execution order/time | Passes locally, fails in CI | No sleep/random; fixed clock/seeds; isolate external dependencies |
| Over-mocking | Tests drift from real behavior | Mock only boundaries (I/O, external services); core logic uses real objects |
| Weak assertions | Only assert not null | Add observable outputs, state changes, interaction verification; strong assertions for key rules |

## See Also

- `flows/generate-test-code.md` - Complete generation workflow
- `references/testing-java.md` - Java test patterns (JUnit 5 + Mockito + AssertJ)
- `references/testing-go.md` - Go test patterns (testing + testify)
- `references/testing-python.md` - Python test patterns (pytest + pytest-mock)
- `references/testing-typescript.md` - TypeScript test patterns (Jest)
- `templates/README.md` - Mustache templates for consistent test structure
- `commands/generate-tests.md` - Command interface with --unit/--integration/--all flags

## Testability Checklist

| Check | Requirement | Refactoring if not met |
|-------|-------------|------------------------|
| Single responsibility | Class/function does one thing | Extract methods/classes |
| Dependency injection | Dependencies via constructor | Use DI container |
| Interface segregation | Depend on interfaces not implementations | Extract interfaces |
| No global state | Avoid singletons/global variables | Pass parameters |
| Pure functions preferred | Same input → same output | Separate side effects |
