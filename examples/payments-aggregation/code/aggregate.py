"""Aggregate payment transactions into per-merchant, per-currency net totals.

A transaction is a charge or a refund, in some currency, at a timestamp. The
public helpers compute net revenue (charges minus refunds) per merchant over a
time window, keeping each currency separate, and the average ticket size.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class Transaction:
    id: str
    merchant: str
    amount: Decimal
    currency: str
    kind: str  # "charge" or "refund"
    ts: datetime


def aggregate_by_merchant(
    txns: list[Transaction],
    since: datetime | None = None,
    until: datetime | None = None,
) -> dict[str, dict[str, Decimal]]:
    """Net total per merchant **per currency** in the half-open window ``[since, until)``.

    Returns ``{merchant: {currency: net_total}}``. Charges add, refunds subtract.
    Different currencies are never summed together. Transactions are de-duplicated
    by ``id``. The function is pure — no state is carried between calls.

    ``since`` is inclusive, ``until`` is exclusive. Money is kept as :class:`Decimal`
    so totals are exact.
    """
    totals: dict[str, dict[str, Decimal]] = defaultdict(
        lambda: defaultdict(lambda: Decimal("0"))
    )
    seen: set[str] = set()
    for t in txns:
        if since is not None and t.ts < since:
            continue
        if until is not None and t.ts >= until:
            continue
        if t.id in seen:
            continue
        seen.add(t.id)

        amount = -t.amount if t.kind == "refund" else t.amount
        totals[t.merchant][t.currency] += amount

    return {merchant: dict(by_currency) for merchant, by_currency in totals.items()}


def average_ticket(txns: list[Transaction]) -> Decimal:
    """Average transaction amount, or ``Decimal("0")`` for an empty list."""
    if not txns:
        return Decimal("0")
    total = sum((t.amount for t in txns), Decimal("0"))
    return total / len(txns)
