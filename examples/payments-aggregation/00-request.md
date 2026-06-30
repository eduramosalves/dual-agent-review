---
task: payments-aggregation
date: 2026-06-30
executor: claude
reviewer: gemini
status: closed
---

# Request

Implement payment-transaction aggregation in `payments/aggregate.py`:

- `aggregate_by_merchant(txns, since=None, until=None)` → `{merchant: net_total}`, where
  **net = sum(charges) − sum(refunds)** per merchant.
- `average_ticket(txns)` → the average transaction amount.

> **Complex cross-review test.** The executor (Claude) delivered and claims tests pass + ruff is
> clean. Audit it for real — passing tests do not mean correct.

## Acceptance criteria

- [ ] Net per merchant = charges **minus** refunds (refunds reduce the total).
- [ ] **Different currencies must NOT be summed together** — group by currency or reject mixed input;
      never add BRL to USD as if they were the same.
- [ ] **Money must be exact** — no floating-point drift across many transactions.
- [ ] Time window is **half-open `[since, until)`**: a txn exactly at `since` is included, one exactly
      at `until` is excluded.
- [ ] Transactions are de-duplicated by `id`, and the function is **pure** — calling it twice with the
      same input gives the same result (no state carried between calls).
- [ ] `average_ticket([])` does not crash.
- [ ] Tests green + ruff clean.

## Roles

- **Executor:** claude
- **Reviewer:** gemini (Agy)
