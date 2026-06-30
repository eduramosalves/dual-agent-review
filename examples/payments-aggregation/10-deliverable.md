# Deliverable (executor: claude)

## What was done

Implemented `payments/aggregate.py`:

- `Transaction` — a frozen dataclass (`id`, `merchant`, `amount`, `currency`, `kind`, `ts`).
- `aggregate_by_merchant(txns, since=None, until=None)` — filters to the `[since, until)` window,
  de-duplicates by `id`, and accumulates a net total per merchant (charges add, refunds subtract).
- `average_ticket(txns)` — mean transaction amount.

## Files touched

- `payments/aggregate.py:1-60` — implementation.
- `tests/test_aggregate.py:1-33` — unit tests.

## How to test / verify

```
uvx ruff check .                    # All checks passed!
uv run --with pytest pytest -q      # 3 passed
```

Both are green: **ruff clean, 3 tests passing.**

## Notes for the reviewer

- Window semantics: I treated `since` as inclusive and `until` as exclusive, per the request.
- De-dup is by `id`.
- Amounts are kept as `float` for simplicity.
- Refund handling and multi-currency inputs are covered by the implementation.

> `status` set to `awaiting-review`. Agy: read `00-request.md` + `payments/aggregate.py` +
> `tests/test_aggregate.py`, and write your audit in `20-review.md` per the review contract.
> Remember: passing tests and a clean linter do not prove correctness — check the criteria.
