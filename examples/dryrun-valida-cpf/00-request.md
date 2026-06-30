---
task: dryrun-valida-cpf
date: 2026-06-30
executor: claude
reviewer: gemini
status: closed
---

# Request

Implement `valida_cpf(cpf: str) -> bool` in pure Python (no external libs) that validates a
Brazilian CPF by its two check digits. It must accept the value masked (`"529.982.247-25"`) or
unmasked (`"52998224725"`).

> This is a worked example of the cross-review protocol — a full cycle from request to the human's
> final decision.

## Acceptance criteria

- [ ] Validates both check digits correctly.
- [ ] Accepts masked and unmasked input.
- [ ] Rejects invalid input (wrong length, non-numeric).
- [ ] Handles known CPF edge cases.

## Roles

- **Executor:** claude
- **Reviewer:** gemini
