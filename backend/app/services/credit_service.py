"""Implements the mandatory credit flow from the product spec:
  1. Check available credits
  2. Reserve credits
  3. Run generation
  4. On success: finalize usage
  5. On failure: refund reserved credits

Backed by an in-memory store here (Phase 3). Phase 10 replaces this with
Firestore `credit_transactions` + `users.credits_balance`, using a
Firestore transaction to make reserve/finalize/refund atomic and prevent
double-charging under concurrent requests.
"""
from dataclasses import dataclass, field
from enum import Enum

from app.core.credit_config import get_credit_config
from app.core.logging import get_logger

logger = get_logger(__name__)


class InsufficientCreditsError(Exception):
    pass


class ReservationState(str, Enum):
    reserved = "reserved"
    finalized = "finalized"
    refunded = "refunded"


@dataclass
class Reservation:
    reservation_id: str
    user_id: str
    amount: int
    state: ReservationState = ReservationState.reserved


class CreditService:
    def __init__(self):
        # Phase 10: replace with Firestore-backed balances.
        self._balances: dict[str, int] = {}
        self._reservations: dict[str, Reservation] = {}

    def set_balance(self, user_id: str, amount: int) -> None:
        self._balances[user_id] = amount

    def get_balance(self, user_id: str) -> int:
        return self._balances.get(user_id, 0)

    def cost_for_outputs(self, outputs: list[str]) -> int:
        cfg = get_credit_config()
        total = 0
        if "poster" in outputs:
            total += cfg.poster
        if "video" in outputs:
            total += cfg.video_30_sec
        if "voiceover" in outputs:
            total += cfg.voiceover
        return total

    def reserve(self, user_id: str, reservation_id: str, amount: int) -> Reservation:
        balance = self.get_balance(user_id)
        if balance < amount:
            logger.warning("credit_reservation_denied", user_id=user_id, requested=amount, balance=balance)
            raise InsufficientCreditsError(f"Need {amount} credits, have {balance}")
        self._balances[user_id] = balance - amount
        reservation = Reservation(reservation_id=reservation_id, user_id=user_id, amount=amount)
        self._reservations[reservation_id] = reservation
        logger.info("credit_reserved", user_id=user_id, amount=amount, reservation_id=reservation_id)
        return reservation

    def finalize(self, reservation_id: str) -> None:
        res = self._reservations.get(reservation_id)
        if not res or res.state != ReservationState.reserved:
            return
        res.state = ReservationState.finalized
        logger.info("credit_finalized", reservation_id=reservation_id, amount=res.amount)

    def refund(self, reservation_id: str) -> None:
        res = self._reservations.get(reservation_id)
        if not res or res.state != ReservationState.reserved:
            return  # already finalized or refunded — never double-refund
        self._balances[res.user_id] = self.get_balance(res.user_id) + res.amount
        res.state = ReservationState.refunded
        logger.info("credit_refunded", reservation_id=reservation_id, amount=res.amount)


_credit_service_singleton = CreditService()


def get_credit_service() -> CreditService:
    return _credit_service_singleton
