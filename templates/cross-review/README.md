# `.cross-review/` — handoff between two terminal agents

Coordination folder for two terminal coding agents (reference: Claude Code ⇄ Gemini CLI).
**Gitignored by default.**

**Golden rule:** one agent executes, the other audits the quality, and **the human makes the final
decision**. Roles are decided per task (the agent that receives the request proposes; the human
confirms).

## Per-task structure (`<NN-slug>/`)

| file | who writes | content |
|---|---|---|
| `00-request.md` | whoever receives | normalized request + roles/status frontmatter |
| `10-deliverable.md` | executor | what was done + pointers to the code + how to test |
| `20-review.md` | reviewer | verdict (`APPROVE`/`REQUEST-CHANGES`/`REJECT`) + numbered findings |
| `30-response.md` | executor (optional, 1 round) | response to the findings |
| `99-decision.md` | human (optional) | final word |

`status` in `00-request.md`: `proposed → awaiting-executor → awaiting-review →
awaiting-user-decision → closed`. Each agent acts on the task whose `status` matches its role.

**Full protocol:** see `PROTOCOL.md` in the `dual-agent-review` repo.
