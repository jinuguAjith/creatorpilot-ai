import pytest

from app.services.credit_service import CreditService, InsufficientCreditsError


def test_reserve_deducts_balance():
    svc = CreditService()
    svc.set_balance("u1", 100)
    svc.reserve("u1", "res1", 30)
    assert svc.get_balance("u1") == 70


def test_reserve_insufficient_credits_raises():
    svc = CreditService()
    svc.set_balance("u1", 10)
    with pytest.raises(InsufficientCreditsError):
        svc.reserve("u1", "res1", 30)


def test_refund_restores_balance():
    svc = CreditService()
    svc.set_balance("u1", 100)
    svc.reserve("u1", "res1", 30)
    svc.refund("res1")
    assert svc.get_balance("u1") == 100


def test_finalize_then_refund_does_not_double_refund():
    svc = CreditService()
    svc.set_balance("u1", 100)
    svc.reserve("u1", "res1", 30)
    svc.finalize("res1")
    svc.refund("res1")  # must be a no-op — already finalized
    assert svc.get_balance("u1") == 70


def test_double_refund_is_a_noop():
    svc = CreditService()
    svc.set_balance("u1", 100)
    svc.reserve("u1", "res1", 30)
    svc.refund("res1")
    svc.refund("res1")  # second refund must not double-credit
    assert svc.get_balance("u1") == 100
