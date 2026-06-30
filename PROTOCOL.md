# Cross-review protocol (canonical spec)

The single source of truth for the dual-agent cross-review workflow. Both agents reference this.
The reference implementation pairs **Claude Code** and the **Gemini CLI**, but any two terminal
agents that share a filesystem work.

> Both sides point here:
> - Claude Code: `~/.claude/CLAUDE.md` → "Cross-review" section.
> - Gemini CLI: `~/.gemini/GEMINI.md`.
> If you edit this file, reflect the change on both.

---

## Roles

- **Executor** — the agent that does the work for a given task.
- **Reviewer** — the other agent, which audits the executor's output.
- **Human** — the operator. **Always has the final decision.** Acts as the circuit breaker and
  passes the turn between the two terminals.

The two agents run on the **same machine and repo**, but in **separate terminals**, and **cannot
call each other directly**. All coordination flows through files in the project's `.cross-review/`
folder plus the human passing the turn.

## Core principle

On every non-trivial request, **one agent executes and the other audits the quality**. Who executes
and who reviews is decided **per task**: the agent that receives the request **proposes** the roles
and the **human confirms before work starts**. Delivery is only considered good after the other
agent's audit — and **the final word is always the human's**. No agent merges a contested change on
its own.

A **trivial** task (a factual question, a read, a read-only command, an obvious one-line fix) does
not need the flow — just do it. When in doubt, propose the flow.

---

## The handoff folder `.cross-review/`

At the project root. **Gitignored by default** (scratch between agents; version a specific task
deliberately if you want to keep an audit trail). Structure per task:

```
.cross-review/
  README.md                 # protocol cheat-sheet (copied from the template on bootstrap)
  <NN-slug>/                # NN = 01, 02, ... ; short kebab-case slug
    00-request.md           # normalized request + roles/status frontmatter
    10-deliverable.md       # what the executor did + pointers to the real code
    20-review.md            # the reviewer's audit: verdict + numbered findings
    30-response.md          # (optional, 1 round) executor's response to the findings
    99-decision.md          # (optional) the human's final word
```

### `00-request.md` frontmatter

```yaml
---
task: <slug>
date: <YYYY-MM-DD>
executor: claude | gemini
reviewer: gemini | claude
status: proposed | awaiting-executor | awaiting-review | awaiting-user-decision | closed
---
```

`status` is the synchronization point: when an agent is opened in a project that has a
`.cross-review/`, it scans the `00-request.md` files and acts on the task whose `status` matches its
role.

---

## State machine (the flow, step by step)

1. **Receive the request** (either agent):
   - Create/ensure `.cross-review/` (run `cross-review-init.sh <slug>` or create it by hand).
   - Write `00-request.md`: normalized request, acceptance criteria, **proposed** roles,
     `status: proposed`.
   - **Ask the human**: "I execute and the other reviews, or the reverse?" + a recommendation.

2. **Human confirms the roles** → the executor sets `status: awaiting-executor`, does the real work
   in the code, and writes `10-deliverable.md` (summary + files/lines touched + how to test). Sets
   `status: awaiting-review`. Tells the human:
   *"Done. Pass the turn to the `<reviewer>` pointing at `.cross-review/<NN-slug>/`."*

3. **Reviewer** (in the other terminal, opened by the human) reads `00-request.md` +
   `10-deliverable.md` + **the real code** + the project's conventions doc (if any), and writes
   `20-review.md` with:
   - **Verdict**: `APPROVE` | `REQUEST-CHANGES` | `REJECT`.
   - **Numbered** findings, each with a severity (blocker/major/minor/nit) and a `file:line` pointer.
   - If `APPROVE` → `status: awaiting-user-decision`.
   - If `REQUEST-CHANGES`/`REJECT` → it may bounce back to the executor for **1 round**
     (`status: awaiting-executor`); the executor responds in `30-response.md` and/or fixes, and
     returns to review. After 1 round it goes to `awaiting-user-decision` regardless.

4. **Human decides** — reads both sides and gives the final verdict. Optionally records it in
   `99-decision.md`. Sets `status: closed`. **Only the human closes a contested change as approved.**

> Capped at **1 rebuttal round** so it can't loop. The human can end it at any time.

---

## Review contract

When you are the **reviewer**, always audit:

- **Correctness + edge cases** — does the code do what it says and survive bad input?
- **Meets the request** — does it match `00-request.md` and the acceptance criteria?
- **Respects project conventions** — your project's fixed-decisions / style doc, if you keep one
  (e.g. language/runtime choices, linter-clean as a commit condition, "baseline before a big model").
- **Objective quality** — tests green, linter clean, no dead code.
- **Honesty** — **no fabricated metrics**; evaluation against real ground truth.

Be specific and actionable: point at `file:line` and propose the fix. No empty praise, no vague
rejection. If everything's good, a clean `APPROVE` — don't invent a problem to look useful.

---

## Bootstrap

- Script: `cross-review-init.sh <slug>` — creates `.cross-review/`, copies the `README.md`, ensures
  `/.cross-review/` is in the project's `.gitignore`, and creates `<NN-slug>/`.
- If the script hasn't run, **create the folder yourself** on the first task (copy the `README.md`
  from the `templates/cross-review/` directory).

## One-line summary

One executes, the other audits through the `.cross-review/` folder, roles set per task by the human,
**and the final decision is always the human's.**
