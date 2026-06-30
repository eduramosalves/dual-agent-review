# Worked example: a full cross-review cycle

This folder is a **real, completed cycle** of the protocol — the dry-run that first validated the
Claude Code ⇄ Gemini CLI integration. Read the files in order:

1. [`00-request.md`](00-request.md) — the human's request (implement `valida_cpf`), roles agreed.
2. [`valida_cpf.py`](valida_cpf.py) — the executor's (Claude) deliverable. It has a **subtle planted
   bug**: it accepts CPFs whose 11 digits are all identical (e.g. `111.111.111-11`), which pass the
   checksum but are invalid CPFs. Kept uncorrected on purpose.
3. [`10-deliverable.md`](10-deliverable.md) — the executor's hand-off note.
4. [`20-review.md`](20-review.md) — the reviewer's (Gemini CLI) audit. It caught the planted bug as
   a **Blocker** — *and* found a second genuine bug nobody planted (permissive non-numeric input).
5. [`99-decision.md`](99-decision.md) — the human's final verdict.

**The takeaway:** the second agent saw what the first one's blind spot hid. That's the entire point
of the protocol — and the reviewer followed the format on its own, just from reading the global
`GEMINI.md`.
