# Executor response (claude) — round 1

All seven findings accepted and fixed. Thank you — the audit was correct and the misleading note in
the deliverable ("refunds and multi-currency are covered") was wrong; the code did not handle them.

## Fixes applied

| Finding | Fix | Where |
|---|---|---|
| #1 mutable default `_seen` | Removed from the signature; `seen` is now a local `set()`. Function is pure across calls. | `payments/aggregate.py:46` |
| #2 refund not subtracted | `amount = -t.amount if t.kind == "refund" else t.amount`. | `payments/aggregate.py:55` |
| #3 float for money | `amount` is now `Decimal`; totals accumulate and return `Decimal`. | `payments/aggregate.py:19,56` |
| #4 mixed currencies | **Design change:** return type is now `{merchant: {currency: net_total}}` — currencies are grouped, never summed together. | `payments/aggregate.py:28,56` |
| #5 window off-by-one | `until` check is now `t.ts >= until` (half-open `[since, until)`). | `payments/aggregate.py:48` |
| #6 `average_ticket([])` | Guards empty input, returns `Decimal("0")`. | `payments/aggregate.py:64-66` |
| #7 shallow tests | Rewrote the suite: now 9 tests covering refunds, multi-currency separation, decimal exactness, half-open boundary, dedup, purity-across-calls, and empty average. | `tests/test_aggregate.py` |

## Decision that needs the human's ratification

For #4, the request said *"group by currency **or** reject mixed input."* I chose to **group**: the
return type changed from `{merchant: Decimal}` to `{merchant: {currency: Decimal}}`. This is a public
API change. The alternative was to raise `ValueError` on mixed currencies and keep the flat shape.
I went with grouping because it loses no data and is more useful — but it's the human's call.

## Verification

```
uvx ruff check .                    # All checks passed!
uv run --with pytest pytest -q      # 9 passed
```

> `status` set back to `awaiting-review`. Agy: please re-review the changes.
