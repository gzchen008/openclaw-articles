---
name: mumblesdk
description: Use when implementing or reviewing Spring Boot services with MumbleSDK dependencies requiring enterprise compliance patterns in regulated/financial environments.
tools: Glob, Grep, Read, TodoWrite, BashOutput, Bash, Edit, Write
model: inherit
---

# MumbleSDK

## Overview

Enterprise framework skill for WeBank MumbleSDK integration. Provides templates, patterns, and validation for Spring Boot microservices following MumbleSDK conventions in regulated/financial environments.

## When to Use

**Use when:**
- Building a Spring Boot microservice that must comply with MumbleSDK standards
- Project has MumbleSDK dependencies (detect `mumble-sdk-*` in pom.xml/build.gradle)
- Using MumbleSDK classes (`MumbleAbstractBaseController`, `MumbleContextUtil`, `MumbleSeqService`, `RmbSAO`)
- Need compliance validation for controller/service/DAO/RMB patterns

**Do NOT use:**
- Project is NOT a MumbleSDK project → Use generic Java skills
- Writing tests only → Use `ease-testing`
- Writing architecture documentation → Use `ease-arch-documentation`

## Quick Reference

| You want to... | First step | Then go to... |
|----------------|-----------|---------------|
| Create a controller | Copy `templates/controller-template.java` | `references/quickstart.md` |
| Create a service | Copy `templates/service-template.java` | `references/integration-checklist.md` |
| Add MumbleSDK validation | Copy `templates/validation-template.java` | Templates/References |
| Set up RMB service | Copy `templates/rmb-service-template.java` | `references/mumble-sdk-rmb-sao-doc.md` |
| Configure properties | Copy `templates/application.properties.example` | Adjust for environment |
| Validate compliance | Run `scripts/quick_validate_mumblesdk.py` | See script output |
| Set up quality gates | Copy `assets/quality-gates.yml` to CI | `references/quality-gates.md` |

## Non-negotiables

### Configuration Format
- **Runtime configs MUST be `.properties`** - YAML is forbidden for application configuration
- CI config files (like `quality-gates.yml`) are exceptions - clearly marked as non-runtime

### Context Management
- `MumbleContextUtil` MUST be cleared in `finally` block
- Generate `bizSeqNo` and `txnSeqNo` before Business Logic, set in context
- Tests MUST verify context cleanup (no ThreadLocal leaks)

### Distributed Locks
- Lock MUST be released in `finally` block
- Handle lock acquisition failure explicitly (don't proceed without lock)
- Combine lock scope with transaction boundaries carefully

### RMB Messaging
- Use `@MumbleRmbService` and `@MumbleServiceMethod` annotations (new projects)
- All exceptions MUST convert to standard `ResponseMessage` error format
- Log with business sequence numbers for audit trace

### Validation
- Use `@Webank*` annotations for financial-grade validation
- Custom validators MUST implement `WebankConstraintValidator`

## Common Mistakes

| Mistake | Symptom | Fix |
|---------|---------|-----|
| Applying MumbleSDK to non-MumbleSDK project | Missing base classes/annotations | Detect dependencies first, fall back to generic skills |
| Missing `MumbleContextUtil.clear()` | ThreadLocal leaks under load/concurrency | Force `finally` clear; tests must cover this |
| Lock not released in all branches | Production deadlock/long unavailability | Force `finally` unlock; clarify timeout/retry strategy |
| Using YAML for runtime config | Config not applied / compliance violation | Runtime config MUST be `.properties` only |
| Mixing old RMB annotations | serviceId/methodName inconsistency | New projects: use recommended annotations; old: compatibility layer only |
| No sequence in business logic | Missing audit trail, traceability issues | MUST generate `bizSeqNo` and `txnSeqNo` in service layer |

## Content Structure

```
mumblesdk/
├── SKILL.md                          # This file
├── templates/                        # Copyable code & config templates
│   ├── controller-template.java      # MumbleAbstractBaseController pattern
│   ├── service-template.java         # Transaction + Context + Sequence pattern
│   ├── validation-template.java      # MumbleSDK validation annotations
│   ├── rmb-service-template.java     # RMB messaging with unified response
│   ├── distributed-lock-template.java # Distributed lock pattern
│   ├── rate-limiter-template.java    # Rate limiting template
│   ├── MumbleGlobalExceptionHandler.java # Global exception handler
│   ├── application.properties.example # Configuration template
│   └── mybatis/                      # MyBatis DAO patterns
├── references/                       # Readable documentation
│   ├── quickstart.md                 # Quick start & integration steps
│   ├── integration-checklist.md      # Controller/service/DAO/config/checklist
│   ├── quality-gates.md              # Quality gates & metrics
│   └── mumble-sdk-rmb-sao-doc.md     # RMB SAO specification
├── scripts/
│   └── quick_validate_mumblesdk.py   # Static compliance validation script
└── assets/
    └── quality-gates.yml              # CI/CD quality gate example
```

## Directory

All authoritative sources are in `mumblesdk/references/*`. External/historical docs are background reference only.

## Key Patterns

### Controller (Async + Unified Response)

See `templates/controller-template.java`:
- Extend `MumbleAbstractBaseController`
- Implement `getFrontTaskExecutor()` and `getBizSeqNo()`
- Use `execute(...)` with `DeferredResult` for async processing
- Return `ResponseMessage<T>` for unified response

### Service (Transaction + Context + Sequence)

See `templates/service-template.java`:
- `@Transactional(rollbackFor = Exception.class)`
- Generate `bizSeqNo` and `txnSeqNo` with `MumbleSeqService.nextValue(...)`
- Set/clear `MumbleContextUtil` in try/finally
- Handle BusinessException/SystemException separately

### Validation

See `templates/validation-template.java`:
- Use `@WebankIdNo`, `@WebankMobilePhone`, `@WebankCardNo`, etc.
- Custom validators: implement `WebankConstraintValidator`
- Support i18n error messages

### RMB Service

See `templates/rmb-service-template.java` and `references/mumble-sdk-rmb-sao-doc.md`:
- `@MumbleRmbService(serviceId = "...")` - service identifier
- `@MumbleServiceMethod(methodName = "...")` - method identifier
- Convert all exceptions to `ResponseMessage.error(code, msg)`
- Log with sequence numbers

### Distributed Lock

See `templates/distributed-lock-template.java`:
- `MumbleDistributedLock.tryLock(key, timeout, unit)`
- Release in `finally` block regardless of outcome
- Handle lock acquisition failure with BusinessException

## Configuration

Copy `templates/application.properties.example`:
- Required sections:
  - `mumble.system.*` - System identification
  - `mumble.env` - Environment (dev/test/prod)
  - DataSource (HikariCP) and connection pool
  - MyBatis mapping and performance settings
  - Thread pools, HTTP client, distributed lock, sequence service
  - Logging with MDC fields (`bizSeqNo`, `txnSeqNo`)

## Quality Gates & Testing

- CI quality gates: See `assets/quality-gates.yml` and `references/quality-gates.md`
- Test practices:
  - Static mock: `MumbleContextUtil`, `MumbleSeqService`
  - Verify context cleanup and sequence generation calls
  - Controller isolation: `@WebMvcTest` + `MockMvc`
  - DAO/Service integration: Transaction rollback, data setup/cleanup

## Decision Tree

| Question | Action |
|----------|--------|
| Web controller? | Extend `MumbleAbstractBaseController`, use `execute`, unified response |
| Core service? | `@Transactional` + `MumbleSeqService` + `MumbleContextUtil` set/clear |
| Financial validation? | Use `@Webank*` annotations; write custom validator if needed |
| Distributed concurrency? | Use `MumbleDistributedLock` with `finally` unlock |
| RMB integration? | `@MumbleRmbService` + `@MumbleServiceMethod` + unified error response |
| Quality gates/testing? | Enable CI gates, write standard tests, run validation script |

## Compliance Validation Script

```bash
python scripts/quick_validate_mumblesdk.py /path/to/project-root [--json]
```

Scans for:
- Controller inheritance (`MumbleAbstractBaseController`)
- Service context + transaction patterns
- DAO patterns and exception declarations
- Properties file existence
- Static mocks in tests

Outputs compliance report with fix suggestions.

## See Also

- `references/quickstart.md` - Quick start and integration steps
- `references/integration-checklist.md` - Complete integration checklist
- `references/quality-gates.md` - Quality gates and metrics
- `references/mumble-sdk-rmb-sao-doc.md` - RMB SAO specification
- `examples/compliance-demo/` - Compliant example project
