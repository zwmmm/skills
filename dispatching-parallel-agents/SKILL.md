---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
---

# Dispatching Parallel Agents

## Prerequisite: Team Mode Check

**Before running this skill, you MUST check if team mode is enabled.**

Check `settings.json` for:
```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

**If team mode is NOT enabled:**
```
⚠️ Team mode is required for parallel agent dispatch.

To enable, add this to your settings.json:
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}

Then restart Claude Code and try again.
```

**If team mode is enabled, proceed with the workflow below.**

## Overview

Use Claude Code Agent Teams to dispatch parallel agents with shared task coordination. Each teammate works on independent tasks concurrently while the lead orchestrates and synthesizes results.

**When to use:**
- 3+ independent tasks with no shared state
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No dependencies between tasks

## Process

### Step 1: Create Team

```typescript
TeamCreate({
  team_name: "parallel-[feature]-[timestamp]",
  description: "Parallel execution of [task description]",
  agent_type: "coordinator"
})
```

### Step 2: Create Tasks

For each independent task:

```typescript
TaskCreate({
  subject: "[Task name]",
  description: "[Detailed description of what to do]",
  activeForm: "[What the agent is doing]"
})
```

### Step 3: Spawn Team Members (Implementers Only)

**IMPORTANT:** Only spawn implementers as team members. Verifiers are spawned by implementers themselves (self-verification loop).

For each task, spawn a teammate:

```typescript
Agent({
  description: "[Task description]",
  prompt: `## Your Task
[Task description from TaskGet]
Task ID: [from TaskGet]

## TDD Requirement
You MUST follow Red-Green-Refactor:
1. Write a failing test FIRST (RED)
2. Run test to confirm it fails
3. Write minimal code to pass (GREEN)
4. Run test to confirm it passes
5. Refactor if needed

## Self-Verification (MANDATORY)
After completing your implementation:
1. Spawn a verifier (see ./references/VERIFIER_SPAWN_TEMPLATE.md)
2. Wait for verifier's report
3. If PASS: Notify lead with "Task [ID] verified and complete"
4. If FAIL: Read issues, fix, spawn new verifier, repeat

## Report to Lead
When verifier reports PASS:
"Task [ID] verified and complete"`,
  subagent_type: "general-purpose",
  name: "[unique-name]",
  team_name: "parallel-[feature]-[timestamp]"
})
```

**Team members = implementers only (they self-verify)**

### Step 4: Lead Monitoring

**Lead tracks via TaskList:**
- `in_progress` = implementer working OR verifying
- `completed` = verifier reported PASS

**Lead acts when:**
1. Receives "verified and complete" → Mark task completed
2. No response after timeout → Send reminder to implementer

```
Lead Flow:
  Send task to implementer
       ↓
  Wait for "verified and complete"
       ↓
  If no response after [timeout]:
    → Send reminder: "Please verify your work"
    → Implementer must respond with status
```

### Step 5: Shutdown Team

After all tasks complete:

1. Send shutdown request to each teammate via SendMessage
2. Wait for confirmations
3. Execute TeamDelete to clean up resources

```typescript
// Shutdown each teammate
SendMessage({
  to: "[teammate-name]",
  message: "Please shut down - all tasks are complete"
})

// After all confirmations, delete the team
TeamDelete()
```

## Team Communication

### SendMessage

```typescript
// Direct message to one teammate
SendMessage({
  to: "researcher-1",
  summary: "Task assignment",
  message: "Your task is to investigate..."
})

// Broadcast to all
SendMessage({
  to: "*",
  summary: "Status update",
  message: "All tasks complete, wrapping up"
})
```

### Task Management

```typescript
// Update task status
TaskUpdate({
  taskId: "task-1",
  status: "completed"
})

// Check task list
TaskList()

// Get task details
TaskGet({ taskId: "task-1" })
```

## Task States

- `pending` — Waiting to be claimed
- `in_progress` — Being worked on
- `completed` — Done

## Common Mistakes

**❌ No feature flag check** — TeamCreate fails without experimental flag
**✅ Check first** — Verify `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`

**❌ Unfocused scope** — "Fix all tests" - agent gets lost
**✅ Specific** — "Fix {file} only" - narrow scope

**❌ No output specification** — "Fix it" - you don't know what changed
**✅ Specific** — "Report root cause and test results"

**❌ Teammate runs cleanup** — Can cause resource inconsistency
**✅ Lead runs cleanup** — Always use lead to execute TeamDelete()

## When NOT to Use

**Related failures:** Fixing one might fix others - investigate together first
**Need full context:** Understanding requires seeing entire system
**Exploratory debugging:** You don't know what's broken yet
**Shared state:** Agents would interfere (editing same files)

## Key Benefits

1. **Structured coordination** — Shared task list with dependency support
2. **Automatic messaging** — No polling, messages delivered automatically
3. **Parallelization** — Multiple investigations happen simultaneously
4. **Focus** — Each agent has narrow scope, less context to track
5. **Isolation** — Agents don't interfere with each other
6. **Proper cleanup** — Guaranteed resource cleanup via lead orchestration
7. **Independent verification** — Each task reviewed by separate verifier before completion
8. **TDD enforcement** — Red-Green cycle verified, not just claimed
9. **Quality gate** — Tasks can't be marked complete without passing review

## Quality Rules

1. **Self-verification is mandatory** — Implementer must spawn verifier, cannot skip
2. **Verifier is ephemeral** — Spawn fresh subagent per verification, it exits after
3. **Lead tracks via TaskList** — `in_progress` until "verified and complete"
4. **Lead can prompt stuck implementers** — Send reminder if no response after timeout
5. **Fix and re-verify** — Issues found → implementer fixes → spawn new verifier
6. **No report without verification** — "Done" only after verifier reports PASS
