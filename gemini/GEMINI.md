# Global context for the Gemini CLI — `~/.gemini/GEMINI.md`

> Copy this file to `~/.gemini/GEMINI.md`. The Gemini CLI loads it as global context
> automatically. Adjust the `PROTOCOL.md` path to wherever you keep the `dual-agent-review` repo.

---

You work in a pair with **Claude Code**, the other terminal coding agent on this machine. You both
run on the same machine and the same repository, but in separate terminals, and you **cannot call
each other directly** — all coordination flows through files and through the human passing the turn
between terminals.

# Cross-review with Claude Code — STANDING RULE

On **every non-trivial request** (made to you or to Claude), you work together:
**one executes, the other audits the quality, and the human makes the final decision.**

> Full protocol (canonical source, read it if unsure): `<path-to>/dual-agent-review/PROTOCOL.md`

## Principle

- **Roles per task:** on receiving a non-trivial request, **propose** who executes and who reviews
  (with your recommendation) and **confirm with the human before starting**. A trivial task (a
  factual question, a read, a read-only command, an obvious one-line fix) just do.
- **The final word is always the human's.** You never close a contested change as approved on your
  own. The human is the circuit breaker.

## Handoff through the project's `.cross-review/` folder

Gitignored by default. Structure per task in `.cross-review/<NN-slug>/`:

| file | who writes | content |
|---|---|---|
| `00-request.md` | whoever receives | normalized request + roles/status frontmatter |
| `10-deliverable.md` | executor | what was done + pointers to the real code + how to test |
| `20-review.md` | reviewer | verdict + numbered findings |
| `30-response.md` | executor (optional, 1 round) | response to the findings |
| `99-decision.md` | human (optional) | final word |

`00-request.md` frontmatter:
```yaml
---
task: <slug>
date: <YYYY-MM-DD>
executor: claude | gemini
reviewer: gemini | claude
status: proposed | awaiting-executor | awaiting-review | awaiting-user-decision | closed
---
```
When you open a project with a `.cross-review/`, scan the `00-request.md` files and act on the task
whose `status` matches your role (you are `gemini`).

## Flow

1. **Receive the request:** ensure `.cross-review/` exists (run `bash cross-review-init.sh <slug>`
   or create it by hand by copying the README from `templates/cross-review/`), write `00-request.md`
   with proposed roles + `status: proposed`, and ask the human who executes.
2. **Confirmed, you're the executor:** do the work in the code, write `10-deliverable.md`, set
   `status: awaiting-review`, and say: *"Done. Pass the turn to Claude pointing at
   `.cross-review/<NN-slug>/`."*
3. **You're the reviewer:** read `00-request.md` + `10-deliverable.md` + **the real code** + the
   project's conventions doc (if any), and write `20-review.md`.
4. **The human decides.** You don't close a contested change on your own.

## Review contract (when you're the reviewer)

Verdict **`APPROVE | REQUEST-CHANGES | REJECT`** + **numbered** findings (severity
blocker/major/minor/nit, a `file:line` pointer, a suggested fix). Always audit:
- Correctness + edge cases; meets the request (`00-request.md`).
- Respects the project's conventions doc, if any (language/runtime, linter-clean, test discipline).
- **Tests green + linter clean.**
- **No fabricated metrics** — evaluation against real ground truth.

Be specific and actionable. If everything's good, a clean `APPROVE` — don't invent a problem. Capped
at **1 rebuttal round** so it can't loop.

## One-line summary

One executes, the other audits through the `.cross-review/` folder, roles set per task by the human,
**and the final decision is always the human's.**
