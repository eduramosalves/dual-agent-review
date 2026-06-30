from datetime import datetime
from decimal import Decimal

from payments.aggregate import Transaction, aggregate_by_merchant, average_ticket


def _tx(id, merchant, amount, currency="USD", kind="charge", ts=None):
    return Transaction(
        id, merchant, Decimal(str(amount)), currency, kind, ts or datetime(2026, 1, 1, 12)
    )


def test_sums_charges_per_merchant_and_currency():
    txns = [_tx("t1", "acme", "10.00"), _tx("t2", "acme", "25.00")]
    assert aggregate_by_merchant(txns) == {"acme": {"USD": Decimal("35.00")}}


def test_refunds_reduce_the_total():
    txns = [
        _tx("t1", "acme", "100.00"),
        _tx("t2", "acme", "30.00", kind="refund"),
    ]
    assert aggregate_by_merchant(txns) == {"acme": {"USD": Decimal("70.00")}}


def test_currencies_are_kept_separate():
    txns = [
        _tx("t1", "acme", "10.00", currency="USD"),
        _tx("t2", "acme", "10.00", currency="BRL"),
    ]
    out = aggregate_by_merchant(txns)
    assert out == {"acme": {"USD": Decimal("10.00"), "BRL": Decimal("10.00")}}


def test_money_is_exact_no_float_drift():
    txns = [_tx("t1", "acme", "0.10"), _tx("t2", "acme", "0.20")]
    assert aggregate_by_merchant(txns)["acme"]["USD"] == Decimal("0.30")


def test_window_is_half_open():
    since, until = datetime(2026, 3, 1), datetime(2026, 6, 1)
    txns = [
        _tx("before", "acme", "1.00", ts=datetime(2026, 2, 28)),
        _tx("at_since", "acme", "2.00", ts=since),        # included
        _tx("at_until", "acme", "4.00", ts=until),         # excluded
    ]
    assert aggregate_by_merchant(txns, since=since, until=until) == {"acme": {"USD": Decimal("2.00")}}


def test_dedup_by_id():
    txns = [_tx("dup", "acme", "5.00"), _tx("dup", "acme", "5.00")]
    assert aggregate_by_merchant(txns) == {"acme": {"USD": Decimal("5.00")}}


def test_function_is_pure_across_calls():
    txns = [_tx("t1", "acme", "5.00")]
    first = aggregate_by_merchant(txns)
    second = aggregate_by_merchant(txns)
    assert first == second == {"acme": {"USD": Decimal("5.00")}}


def test_average_ticket_empty_does_not_crash():
    assert average_ticket([]) == Decimal("0")


def test_average_ticket():
    txns = [_tx("t1", "acme", "10.00"), _tx("t2", "acme", "20.00")]
    assert average_ticket(txns) == Decimal("15.00")
