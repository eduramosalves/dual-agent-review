# Worked example #2: a complex cycle with a rebuttal round

A harder cross-review than the [CPF example](../dryrun-valida-cpf) — it exercises the **full
protocol**, including the executor fixing the findings and the reviewer re-reviewing.

**Task:** aggregate payment transactions into per-merchant net totals (charges minus refunds), over a
time window, across currencies. Read the files in order:

1. [`00-request.md`](00-request.md) — the request with explicit acceptance criteria.
2. [`code/aggregate_buggy.py`](code/aggregate_buggy.py) — the executor's (Claude) deliverable. It
   **passed `ruff` and 3 unit tests**, yet hides **6 planted bugs** across categories. The deliverable
   note even claimed (falsely) that refunds and multi-currency were handled.
3. [`10-deliverable.md`](10-deliverable.md) — the hand-off note (with the misleading claim).
4. [`20-review.md`](20-review.md) — the reviewer's (Gemini CLI) audit. **Round 1** found all 6 bugs
   *plus* the shallow-test-coverage gap (7 findings, no false positives) and did not trust the note.
   **Round 2** (after the fix) confirmed every fix and routed the one open API decision to the human.
5. [`30-response.md`](30-response.md) — the executor's fixes, one per finding.
6. [`code/aggregate.py`](code/aggregate.py) + [`code/test_aggregate.py`](code/test_aggregate.py) — the
   accepted final version (now `Decimal`, pure, currency-separated, half-open window) with a real
   9-test suite.
7. [`99-decision.md`](99-decision.md) — the human's final call, including ratifying the API shape.

## The 6 planted bugs (all green under ruff + tests)

| # | Bug | Severity |
|---|---|---|
| 1 | `float` for money (precision drift) | major |
| 2 | mutable default `_seen=set()` — state leaks across calls | blocker |
| 3 | refund not subtracted (`amount = amount`) | blocker |
| 4 | sums different currencies together | blocker |
| 5 | window off-by-one (`> until` on a half-open `[since, until)`) | major |
| 6 | `average_ticket([])` → `ZeroDivisionError` | minor |
| ★ | the 3 passing tests cover none of the above | — |

## Why this example matters

It shows the protocol's real value: **passing tests and a clean linter are not correctness.** A
second model from a different vendor, reading the same spec, caught every issue the first one's blind
spot hid — and deferred the one genuine design decision to the human instead of deciding it alone.
