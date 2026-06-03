"""
TransactionService — Assignment 12
Orchestrates P2P transfers, top-ups, bill payments.
Enforces business rules: balance checks, atomicity, rollback.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from decimal import Decimal
from typing import List, Optional
from src.models import (
    Transaction, TransactionType, TransactionStatus,
    InsufficientFundsError, InvalidTransactionError, UserNotFoundError
)
from repositories.interfaces import TransactionRepository, UserRepository


class TransactionService:
    def __init__(self, txn_repo: TransactionRepository, user_repo: UserRepository):
        self._txn_repo = txn_repo
        self._user_repo = user_repo

    def _get_user_or_raise(self, user_id: str):
        user = self._user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")
        return user

    def transfer(self, sender_id: str, recipient_phone: str, amount: Decimal) -> Transaction:
        if amount <= Decimal("0.00"):
            raise ValueError("Transfer amount must be > R0.00.")

        sender = self._get_user_or_raise(sender_id)
        if not sender.can_transact():
            raise InvalidTransactionError("Sender account is not active.")

        recipient = self._user_repo.find_by_phone(recipient_phone)
        if not recipient:
            raise UserNotFoundError(f"No SwiftPay account for phone: {recipient_phone}")
        if not recipient.can_transact():
            raise InvalidTransactionError("Recipient account is not active.")

        if not sender.wallet.validate_sufficient_funds(amount):
            raise InsufficientFundsError(
                f"Insufficient funds. Balance: R{sender.wallet.balance}, Required: R{amount}")

        txn = Transaction(
            sender_wallet_id=sender.wallet.wallet_id,
            amount=amount,
            transaction_type=TransactionType.TRANSFER,
            recipient_wallet_id=recipient.wallet.wallet_id,
        )
        txn.validate(); txn.process(); txn.pending_gateway()

        try:
            # Atomic debit + credit
            sender.wallet.debit(amount)
            recipient.wallet.credit(amount)
            self._user_repo.save(sender)
            self._user_repo.save(recipient)
            txn.complete(f"GW-{txn.transaction_id[:8].upper()}")
        except Exception as e:
            txn.rollback()
            self._txn_repo.save(txn)
            raise InvalidTransactionError(f"Transfer failed and was rolled back: {e}")

        return self._txn_repo.save(txn)

    def top_up(self, user_id: str, amount: Decimal) -> Transaction:
        if amount <= Decimal("0.00"):
            raise ValueError("Top-up amount must be > R0.00.")
        user = self._get_user_or_raise(user_id)
        if not user.can_transact():
            raise InvalidTransactionError("Account is not active.")

        txn = Transaction(
            sender_wallet_id=user.wallet.wallet_id,
            amount=amount,
            transaction_type=TransactionType.TOP_UP,
        )
        txn.validate(); txn.process(); txn.pending_gateway()
        user.wallet.credit(amount)
        self._user_repo.save(user)
        txn.complete(f"GW-TOPUP-{txn.transaction_id[:6].upper()}")
        return self._txn_repo.save(txn)

    def get_history(self, user_id: str) -> List[Transaction]:
        user = self._get_user_or_raise(user_id)
        return self._txn_repo.find_by_wallet(user.wallet.wallet_id)

    def get_by_id(self, txn_id: str) -> Transaction:
        txn = self._txn_repo.find_by_id(txn_id)
        if not txn:
            raise InvalidTransactionError(f"Transaction not found: {txn_id}")
        return txn

    def get_all(self) -> List[Transaction]:
        return self._txn_repo.find_all()

    def count(self) -> int:
        return self._txn_repo.count()
