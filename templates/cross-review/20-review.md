# Review (reviewer: <gemini|claude>)

**Verdict:** APPROVE | REQUEST-CHANGES | REJECT

## Review-contract checklist

- [ ] Correctness + edge cases
- [ ] Meets the request (`00-request.md`)
- [ ] Respects the project's conventions doc (if any)
- [ ] Tests green + linter clean
- [ ] No fabricated metrics

## Findings

1. **[blocker|major|minor|nit]** `file:line` — <problem>. Suggested fix: <...>
2. ...

> If APPROVE → `status: awaiting-user-decision`.
> If REQUEST-CHANGES/REJECT → bounce back to the executor (1 round, `status: awaiting-executor`) or
> send straight to the human to decide.
