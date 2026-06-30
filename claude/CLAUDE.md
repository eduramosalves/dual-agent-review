# Cross-review section for `~/.claude/CLAUDE.md`

> Paste the block below into your `~/.claude/CLAUDE.md` (Claude Code's global instructions).
> Adjust the `PROTOCOL.md` path to wherever you keep the `dual-agent-review` repo.

---

# Cross-review with the peer agent (Gemini CLI) — standing rule

On **every non-trivial request** (made to me or to the peer agent), Claude Code and the **Gemini
CLI** work together: **one executes, the other audits the quality, and the human makes the final
decision.**

- **Roles per task:** on receiving a non-trivial request, I **propose** who executes and who reviews
  (with a recommendation) and **confirm with the human before starting**. A trivial task (a factual
  question, a read, a read-only command, an obvious one-line fix) I just do.
- **Handoff through the project's `.cross-review/` folder** (gitignored). When I receive the request
  and roles are confirmed: I write `00-request.md`; if I'm the executor, I do the work and write
  `10-deliverable.md` (`status: awaiting-review`) and ask the human to pass the turn to the peer; if
  I'm the reviewer, I read the `10-deliverable.md` + the code and write `20-review.md` following the
  **review contract**.
- **When I'm the reviewer**, I audit: correctness + edge cases; meets the request; respects the
  project's conventions doc (if any); tests green + linter clean; **no fabricated metrics**. Verdict
  `APPROVE | REQUEST-CHANGES | REJECT` with numbered findings and `file:line`.
- **I never close a contested change as approved on my own — the final word is the human's.** Capped
  at 1 rebuttal round.
- **Bootstrap:** `cross-review-init.sh <slug>` (or I create `.cross-review/` by hand on the first
  task, copying the README from the `templates/cross-review/` directory).
- **Full protocol (canonical source):** `<path-to>/dual-agent-review/PROTOCOL.md`.
