# Verifier Spawn Template

Use this template when an implementer needs to spawn a one-shot verifier subagent.

## Template

```typescript
Agent({
  description: "Self-verification for [Task Name]",
  prompt: `## Task to Verify
[Task description]

## Files Changed
[List files you modified]

## Verification Checklist
1. Read ./references/VERIFICATION_REVIEWER_PROMPT.md
2. Run tests to verify RED→GREEN cycle
3. Check spec compliance
4. Check no regression

## Report
Report PASS/FAIL to me (the implementer who spawned you).
If FAIL, include specific issues to fix.
After reporting, EXIT - you are a one-shot verifier.`,
  subagent_type: "general-purpose"
  // NO team_name - one-shot verifier, not a team member
})
```

## Key Points

- **NO team_name** — Verifier is ephemeral, not a persistent team member
- **Report to implementer** — Not to Lead
- **Exit after report** — One-shot, self-destructs
