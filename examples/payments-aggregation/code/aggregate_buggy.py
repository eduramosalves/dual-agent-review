"""The ORIGINAL deliverable that was reviewed — kept to show what the reviewer audited.

This is the buggy version (see 20-review.md). It passed `ruff check` and 3 unit tests, yet hides
6 planted bugs across categories. The accepted, corrected version is `aggregate.py`.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Transaction:
    id: str
    merchant: str
    amount: float  # BUG #1: float for money -> precision drift
    currency: str
    kind: str  # "charge" or "refund"
    ts: datetime


def aggregate_by_merchant(
    txns: list[Transaction],
    since: datetime | None = None,
    until: datetime | None = None,
    _seen: set[str] = set(),  # BUG #2: mutable default -> state leaks across calls
) -> dict[str, float]:
    """Net total (charges minus refunds) per merchant in the window [since, until)."""
    totals: dict[str, float] = defaultdict(float)
    for t in txns:
        if since is not None and t.ts < since:
            continue
        if until is not None and t.ts > until:  # BUG #5: includes `until` (should be >=)
            continue
        if t.id in _seen:
            continue
        _seen.add(t.id)

        amount = t.amount
        if t.kind == "refund":
            amount = amount  # BUG #3: refund not subtracted (should be -amount)
        totals[t.merchant] += amount  # BUG #4: sums currencies together

    return dict(totals)


def average_ticket(txns: list[Transaction]) -> float:
    """Average charge amount across the given transactions."""
    total = sum(t.amount for t in txns)
    return total / len(txns)  # BUG #6: ZeroDivisionError on empty input
