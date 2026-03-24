---
description: Create a structured diary entry from the current session transcript
---

# Create Project Diary Entry from Current Session

You are going to create a structured diary entry that documents what happened in the current Claude Code session **specifically related to this project**. This entry will be saved in the project's `.claude/memory/diary` directory and used later for reflection and pattern identification within this project context.

## Important: Project-Only Focus

**Only include content directly related to the current project:**
- Files within the project directory structure
- Project-specific commands and configurations
- Code changes, implementations, and refactoring
- Project documentation and tests
- Project-specific design decisions and patterns
- Build and deployment processes for this project

**Exclude:**
- General Claude Code usage outside this project
- Personal or unrelated tasks
- Global configurations not project-specific
- Example code not used in this project

## Approach: Context-First Strategy

**Primary Method (use this first):**
Reflect on the conversation history loaded in this session. You have access to:
- All user messages and requests
- Your responses and tool invocations
- Files you read, edited, or wrote
- Errors encountered and solutions applied
- Design decisions discussed
- User preferences expressed

**When to use JSONL fallback (rare):**
- Session was compacted and context is incomplete
- You need precise statistics (exact tool counts, timestamps)
- User specifically requests detailed session analysis

## Steps to Follow

### 1. Create Diary Entry from Context (Primary Method)

Review the current conversation and create a diary entry based on what happened. No tool invocations needed for typical sessions.

Skip to Step 4 to write the diary entry.

### 2. Fallback: Locate Session Transcript (Only if context insufficient)

If you determine context is insufficient, run the appropriate command for your operating system to find the transcript:

#### For Unix/Linux/macOS:

```bash
# Find the most recent session file for this project
# NOTE: Path format includes leading dash: -Users-name-Code-app
SESSION_FILE=$(ls -t ~/.claude/projects/-$(echo "{{ cwd }}" | sed 's/\//‐/g')/*.jsonl 2>/dev/null | head -1) && \
if [ -z "$SESSION_FILE" ]; then \
  echo "ERROR: No session file found" && \
  echo "Looking in: ~/.claude/projects/-$(echo "{{ cwd }}" | sed 's/\//‐/g')/" && \
  ls -la ~/.claude/projects/ | head -20; \
else \
  echo "FOUND: $SESSION_FILE" && \
  ls -lh "$SESSION_FILE"; \
fi
```

#### For Windows (PowerShell):

```powershell
# Convert current directory to project hash format
$projectPath = "{{ cwd }}"
$projectHash = "-$($projectPath.Replace('/', '-'))"
$projectsPath = "$env:USERPROFILE\.claude\projects\$projectHash"

# Find the most recent session file
$sessionFile = Get-ChildItem -Path "$projectsPath\*.jsonl" -ErrorAction SilentlyContinue |
    Sort-Object LastWriteTime -Descending |
    Select-Object -First 1

if ($sessionFile) {
    Write-Output "FOUND: $($sessionFile.FullName)"
    Write-Output "Size: $([math]::Round($sessionFile.Length / 1KB, 2)) KB"
    Write-Output "Modified: $($sessionFile.LastWriteTime)"
} else {
    Write-Output "ERROR: No session file found"
    Write-Output "Looking in: $projectsPath"
    if (Test-Path "$env:USERPROFILE\.claude\projects") {
        Get-ChildItem "$env:USERPROFILE\.claude\projects" | Head -20
    }
}
```

#### For Windows (Command Prompt):

```cmd
@echo off
REM This requires PowerShell for path conversion
powershell -Command "
$projectPath = '{{ cwd }}'
$projectHash = \"-$($projectPath.Replace('/', '-'))\"
$projectsPath = \"$env:USERPROFILE\.claude\projects\$projectHash\"
$sessionFile = Get-ChildItem -Path \"$projectsPath*.jsonl\" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
if ($sessionFile) {
    Write-Output \"FOUND: $($sessionFile.FullName)\"
    Write-Output \"Size: $([math]::Round($sessionFile.Length / 1KB, 2)) KB\"
} else {
    Write-Output \"ERROR: No session file found\"
    Write-Output \"Looking in: $projectsPath\"
}
"
```

**What this does:**
- Converts current directory to project hash format (e.g., `/Users/name/Code/app` → `-Users-name-Code-app`)
- Note the LEADING DASH in the path format
- Finds the most recent `.jsonl` file in that project's directory

### 3. Fallback: Extract Key Metadata (Only if needed)

Only run this if you need precise statistics for **project-related work**:

#### For Unix/Linux/macOS:

```bash
SESSION_FILE="[path-from-step-2]" && \
PROJECT_ROOT="{{ cwd }}" && \
echo "=== SESSION METADATA ===" && \
echo "File: $SESSION_FILE" && \
echo "Project: $PROJECT_ROOT" && \
echo "Size: $(ls -lh "$SESSION_FILE" | awk '{print $5}')" && \
echo "" && \
echo "=== PROJECT-RELATED TOOL COUNTS ===" && \
jq -r "select(.message.content[]?.name) | .message.content[].name" "$SESSION_FILE" | sort | uniq -c && \
echo "" && \
echo "=== PROJECT FILES MODIFIED ===" && \
grep -o '"filePath":"[^"]*"' "$SESSION_FILE" | grep "^$PROJECT_ROOT" | sort -u
```

#### For Windows (PowerShell):

```powershell
$sessionFile = "[path-from-step-2]"
$projectRoot = "{{ cwd }}"

Write-Output "=== SESSION METADATA ==="
Write-Output "File: $sessionFile"
Write-Output "Project: $projectRoot"

if (Test-Path $sessionFile) {
    $fileInfo = Get-Item $sessionFile
    Write-Output "Size: $([math]::Round($fileInfo.Length / 1KB, 2)) KB"
    Write-Output "Modified: $($fileInfo.LastWriteTime)"

    Write-Output ""
    Write-Output "=== PROJECT-RELATED TOOL COUNTS ==="

    # Parse JSONL and count tools
    try {
        $content = Get-Content $sessionFile
        $toolCounts = @{}
        foreach ($line in $content) {
            if ($line.Trim()) {
                try {
                    $json = $line | ConvertFrom-Json
                    if ($json.message.content) {
                        foreach ($item in $json.message.content) {
                            if ($item.name) {
                                $toolCounts[$item.name] = $toolCounts[$item.name] + 1
                            }
                        }
                    }
                } catch {
                    # Skip malformed JSON lines
                }
            }
        }

        $toolCounts.GetEnumerator() | Sort-Object Name | ForEach-Object {
            Write-Output "$($_.Value) $($_.Key)"
        }
    } catch {
        Write-Output "Error parsing file for tool counts"
    }

    Write-Output ""
    Write-Output "=== PROJECT FILES MODIFIED ==="

    # Extract file paths from JSONL, filtering to project directory only
    try {
        $content = Get-Content $sessionFile -Raw
        $pattern = '"filePath":"([^"]*)"'
        $matches = [regex]::Matches($content, $pattern)
        $filePaths = $matches | ForEach-Object { $_.Groups[1].Value } |
            Where-Object { $_ -like "*$projectRoot*" } |
            Sort-Object -Unique
        $filePaths | ForEach-Object { Write-Output $_ }
    } catch {
        Write-Output "Error extracting file paths"
    }
} else {
    Write-Output "ERROR: File not found"
}
```

#### For Windows (Command Prompt - requires jq for JSON parsing):

```cmd
@echo off
set SESSION_FILE="[path-from-step-2]"
set PROJECT_ROOT="{{ cwd }}"

echo === SESSION METADATA ===
echo File: %SESSION_FILE%
echo Project: %PROJECT_ROOT%

if exist "%SESSION_FILE%" (
    for %%F in ("%SESSION_FILE%") do (
        echo Size: %%~zF bytes
    )

    echo.
    echo === PROJECT-RELATED TOOL COUNTS ===
    REM This requires jq to be installed and in PATH
    jq -r "select(.message.content[]?.name) | .message.content[].name" "%SESSION_FILE%" 2>nul | sort | uniq -c

    echo.
    echo === PROJECT FILES MODIFIED ===
    REM This filters for files within the project directory
    jq -r 'select(.message.content[]?.input?.filePath) | .message.content[].input.filePath' "%SESSION_FILE%" 2>nul | findstr "%PROJECT_ROOT%" | sort /M
) else (
    echo ERROR: File not found
)
```

This extracts only project-related metadata, filtering files to those within the project directory.

### 4. Create the Diary Entry

Based on the conversation context (and optional metadata from Step 3), create a structured markdown diary entry focusing **only on project-related work** with these sections:

```markdown
# Project Diary Entry

**Date**: [YYYY-MM-DD from timestamp]
**Time**: [HH:MM:SS from timestamp]
**Session ID**: [uuid from filename]
**Project**: [project path]
**Git Branch**: [branch name if available]

## Project Task Summary
[2-3 sentences: What project-specific work was the user trying to accomplish? Focus on the project goals.]

## Project Work Summary
[Bullet list of project accomplishments ONLY:]
- Features implemented in the project
- Project bugs fixed
- Project documentation added/updated
- Tests written for the project
- Build/CI/CD improvements
- Dependencies updated for the project

## Project Design Decisions
[IMPORTANT: Document project-specific technical decisions and WHY:]
- Project architecture choices
- Framework/library selections for this project
- API design decisions for the project
- Code organization patterns
- Project-specific trade-offs

## Project Files & Actions
[Based on tool usage and file operations within the project:]
- Project files edited: [list only project files]
- Project-specific commands executed
- Project tools used (build tools, linters, etc.)
- Project dependencies modified

## Project Code Review Feedback
[CRITICAL: Capture project-specific code quality feedback:]
- Code review comments for project changes
- Project-specific quality standards
- Linting issues fixed in the project
- Style preferences for this project

## Project Challenges
[Based on project-specific errors and solutions:]
- Project build issues encountered
- Project runtime errors
- Integration challenges
- Debugging steps within the project

## Project Solutions
[How project-specific problems were resolved]

## Project Preferences & Standards
[Document project-specific conventions observed:]

### Development Workflow:
- Branching strategy used
- Commit message patterns for this project
- PR review process

### Code Quality Standards:
- Testing requirements for this project
- Linting rules/configurations
- Code formatting preferences

### Technical Stack Preferences:
- Frameworks preferred for this project
- Build tools used
- Deployment approaches

## Project Patterns
[Reusable patterns established for this project]

## Project Context
- Project type: [web app, CLI tool, library, etc.]
- Primary languages: [Python, JavaScript, etc.]
- Key frameworks/libraries in use
- Project status: [new, maintenance, refactor, etc.]

## Project Notes
[Any project-specific observations or future considerations]
```

### 4. Save the Diary Entry

Run the appropriate command for your operating system to save the entry in the **project's** directory: `<project-root>/.claude/memory/diary`

#### For Unix/Linux/macOS:

``` bash
# Create project diary directory if needed
PROJECT_ROOT="{{ cwd }}" && \
mkdir -p "$PROJECT_ROOT/.claude/memory/diary" && \
# Determine filename
TODAY=$(date +%Y-%m-%d) && \
N=1 && \
while [ -f "$PROJECT_ROOT/.claude/memory/diary/${TODAY}-session-${N}.md" ]; do N=$((N+1)); done && \
DIARY_FILE="$PROJECT_ROOT/.claude/memory/diary/${TODAY}-session-${N}.md" && \
# Output the file path for use with Write tool
echo "Diary file path: $DIARY_FILE"
```

#### For Windows (PowerShell):

```powershell
# Create project diary directory if needed
$projectRoot = "{{ cwd }}"
$memoryDir = Join-Path $projectRoot ".claude\memory"
New-Item -ItemType Directory -Force -Path $memoryDir | Out-Null

# Determine filename
$today = Get-Date -Format "yyyy-MM-dd"
$n = 1
$diaryFile = Join-Path $memoryDir "${today}-session-${n}.md"

# Find next available session number
while (Test-Path $diaryFile) {
    $n++
    $diaryFile = Join-Path $memoryDir "${today}-session-${n}.md"
}

# Output the file path for use with Write tool
Write-Output "Diary file path: $diaryFile"
```

#### For Windows (Command Prompt):

```cmd
@echo off
REM Create project diary directory if needed
set PROJECT_ROOT={{ cwd }}
set MEMORY_DIR=%PROJECT_ROOT%\.claude\memory
if not exist "%MEMORY_DIR%" mkdir "%MEMORY_DIR%"

REM Determine filename using PowerShell for date formatting
for /f "tokens=*" %%i in ('powershell -Command "Get-Date -Format ''yyyy-MM-dd''"') do set TODAY=%%i

REM Find next available session number
set N=1
:check_file
if exist "%MEMORY_DIR%\%TODAY%-session-%N%.md" (
    set /a N+=1
    goto check_file
)

REM Set the diary file path
set DIARY_FILE=%MEMORY_DIR%\%TODAY%-session-%N%.md

REM Output the file path
echo Diary file path: %DIARY_FILE%
```

Use the Write tool to actually write the diary content to the determined file path. The script will output the exact file path you should use.

### 5. Confirm Completion

Display:
- Path where diary was saved
- Brief summary of what was captured

## Important Guidelines

- **Be factual and specific**: Include concrete details (file paths, error messages)
- **Capture the 'why'**: Explain reasoning behind decisions
- **Document ALL user preferences**: Especially around commits, PRs, linting, testing
- **Include failures**: What didn't work is valuable learning
- **Keep it structured**: Follow the template consistently
- **Use context first**: Only parse JSONL files when truly necessary
- **Stay project-focused**: Exclude non-project activities and global configurations

## Decision Guide: When to Use Each Approach

| Situation | Approach | Reasoning |
|-----------|----------|-----------|
| During active session | **Context only** | All information available, 0 tool calls |
| PreCompact hook trigger | **Context only** | Session still in memory |
| Post-session analysis | **JSONL fallback** | Context no longer available |
| Need exact statistics | **JSONL metadata** | Precise counts unavailable from context |
| User says "create diary" | **Context first** | Assume current session unless specified |

## Error Handling

**Context-based errors:**
- If context seems incomplete, mention what's missing and offer to use JSONL fallback
- If uncertain about details, document with "approximately" or "unclear from context"

**JSONL-based errors:**
- If session file not found, show where you looked (remember: `-Users-...` format with leading dash)
- Check projects directory to help diagnose path issues:
  - **Unix/Linux/macOS**: `ls -la ~/.claude/projects/`
  - **Windows (PowerShell)**: `Get-ChildItem "$env:USERPROFILE\.claude\projects"`
  - **Windows (CMD)**: `dir "%USERPROFILE%\.claude\projects"`
- If transcript is malformed, document what you could parse and fall back to context

## Git Integration

**Important**: The `.claude/memory` directory should be added to your project's `.gitignore` file to avoid committing session-specific diary entries. Add this line to your `.gitignore`:

```
.claude/memory/
```

This ensures that:
- Project-specific diary entries remain local to each developer
- Sensitive project information discussed in sessions isn't accidentally committed
- The diary serves as personal memory for each developer's work on the project
