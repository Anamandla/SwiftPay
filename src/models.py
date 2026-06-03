"""SwiftPay Core Domain Models — Assignment 9/10"""
from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional
import uuid, hashlib

class UserStatus(Enum):
    UNVERIFIED="UNVERIFIED"; ACTIVE="ACTIVE"; SUSPENDED="SUSPENDED"; DELETED="DELETED"

class WalletStatus(Enum):
    ACTIVE="ACTIVE"; FROZEN="FROZEN"; CLOSED="CLOSED"

class TransactionType(Enum):
    TRANSFER="TRANSFER"; TOP_UP="TOP_UP"; BILL_PAYMENT="BILL_PAYMENT"

class TransactionStatus(Enum):
    INITIATED="INITIATED"; VALIDATING="VALIDATING"; PROCESSING="PROCESSING"
    PENDING_GATEWAY="PENDING_GATEWAY"; COMPLETED="COMPLETED"; FAILED="FAILED"
    ROLLED_BACK="ROLLED_BACK"; DISPUTED="DISPUTED"; REFUNDED="REFUNDED"

class NotificationType(Enum):
    TRANSFER_SENT="TRANSFER_SENT"; TRANSFER_RECEIVED="TRANSFER_RECEIVED"
    BILL_PAID="BILL_PAID"; TOP_UP_SUCCESS="TOP_UP_SUCCESS"; ACCOUNT_SUSPENDED="ACCOUNT_SUSPENDED"

class NotificationStatus(Enum):
    QUEUED="QUEUED"; SENDING="SENDING"; DELIVERED="DELIVERED"
    FAILED="FAILED"; READ="READ"; EXPIRED="EXPIRED"

class OTPStatus(Enum):
    GENERATED="GENERATED"; SENT="SENT"; PENDING="PENDING"
    VERIFIED="VERIFIED"; EXPIRED="EXPIRED"; INVALIDATED="INVALIDATED"

class AdminAction(Enum):
    SUSPEND="SUSPEND"; REACTIVATE="REACTIVATE"; DELETE="DELETE"; REFUND="REFUND"

class InsufficientFundsError(Exception): pass
class InvalidTransactionError(Exception): pass
class InvalidOTPError(Exception): pass
class WalletFrozenError(Exception): pass
class UserNotFoundError(Exception): pass
class DuplicateUserError(Exception): pass

class Wallet:
    def __init__(self, user_id: str, currency: str = "ZAR"):
        self._wallet_id = str(uuid.uuid4())
        self._user_id = user_id
        self._balance = Decimal("0.00")
        self._currency = currency
        self._status = WalletStatus.ACTIVE
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()

    @property
    def wallet_id(self): return self._wallet_id
    @property
    def user_id(self): return self._user_id
    @property
    def balance(self): return self._balance
    @property
    def currency(self): return self._currency
    @property
    def status(self): return self._status
    @property
    def created_at(self): return self._created_at

    def validate_sufficient_funds(self, amount: Decimal) -> bool:
        return self._balance >= amount

    def credit(self, amount: Decimal) -> None:
        if self._status == WalletStatus.FROZEN: raise WalletFrozenError("Wallet is frozen.")
        if self._status == WalletStatus.CLOSED: raise InvalidTransactionError("Wallet is closed.")
        if amount <= Decimal("0.00"): raise InvalidTransactionError("Amount must be > R0.00.")
        self._balance += amount; self._updated_at = datetime.utcnow()

    def debit(self, amount: Decimal) -> None:
        if self._status == WalletStatus.FROZEN: raise WalletFrozenError("Wallet is frozen.")
        if self._status == WalletStatus.CLOSED: raise InvalidTransactionError("Wallet is closed.")
        if amount <= Decimal("0.00"): raise InvalidTransactionError("Amount must be > R0.00.")
        if not self.validate_sufficient_funds(amount):
            raise InsufficientFundsError(f"Insufficient funds. Balance: R{self._balance}, Required: R{amount}")
        self._balance -= amount; self._updated_at = datetime.utcnow()

    def freeze(self): self._status = WalletStatus.FROZEN; self._updated_at = datetime.utcnow()
    def unfreeze(self): self._status = WalletStatus.ACTIVE; self._updated_at = datetime.utcnow()
    def close(self): self._status = WalletStatus.CLOSED; self._updated_at = datetime.utcnow()
    def get_balance(self): return self._balance

    def to_dict(self):
        return {"wallet_id": self._wallet_id, "user_id": self._user_id,
                "balance": str(self._balance), "currency": self._currency,
                "status": self._status.value, "created_at": self._created_at.isoformat()}

    def __repr__(self): return f"Wallet(id={self._wallet_id[:8]}, balance=R{self._balance}, status={self._status.value})"


class User:
    def __init__(self, name: str, email: str, phone: str, password_hash: str):
        self._user_id = str(uuid.uuid4())
        self._name = name; self._email = email; self._phone = phone
        self._password_hash = password_hash
        self._status = UserStatus.UNVERIFIED
        self._wallet = Wallet(user_id=self._user_id)
        self._created_at = datetime.utcnow(); self._updated_at = datetime.utcnow()

    @property
    def user_id(self): return self._user_id
    @property
    def name(self): return self._name
    @property
    def email(self): return self._email
    @property
    def phone(self): return self._phone
    @property
    def status(self): return self._status
    @property
    def wallet(self): return self._wallet
    @property
    def password_hash(self): return self._password_hash
    @property
    def created_at(self): return self._created_at

    def activate(self): self._status = UserStatus.ACTIVE; self._updated_at = datetime.utcnow()
    def suspend(self): self._status = UserStatus.SUSPENDED; self._wallet.freeze(); self._updated_at = datetime.utcnow()
    def reactivate(self): self._status = UserStatus.ACTIVE; self._wallet.unfreeze(); self._updated_at = datetime.utcnow()
    def delete(self): self._status = UserStatus.DELETED; self._wallet.close(); self._updated_at = datetime.utcnow()
    def can_transact(self): return self._status == UserStatus.ACTIVE
    def update_profile(self, name=None, phone=None):
        if name: self._name = name
        if phone: self._phone = phone
        self._updated_at = datetime.utcnow()
    def get_wallet(self): return self._wallet

    def to_dict(self):
        return {"user_id": self._user_id, "name": self._name, "email": self._email,
                "phone": self._phone, "status": self._status.value,
                "wallet": self._wallet.to_dict(), "created_at": self._created_at.isoformat()}

    def __repr__(self): return f"User(id={self._user_id[:8]}, name={self._name}, status={self._status.value})"


class Transaction:
    _TERMINAL = {TransactionStatus.COMPLETED, TransactionStatus.FAILED,
                 TransactionStatus.ROLLED_BACK, TransactionStatus.REFUNDED}

    def __init__(self, sender_wallet_id: str, amount: Decimal,
                 transaction_type: TransactionType,
                 recipient_wallet_id: Optional[str] = None, currency: str = "ZAR"):
        self._transaction_id = str(uuid.uuid4())
        self._sender_wallet_id = sender_wallet_id
        self._recipient_wallet_id = recipient_wallet_id
        self._type = transaction_type; self._amount = amount; self._currency = currency
        self._status = TransactionStatus.INITIATED
        self._gateway_reference: Optional[str] = None
        self._failure_reason: Optional[str] = None
        self._created_at = datetime.utcnow(); self._completed_at: Optional[datetime] = None

    @property
    def transaction_id(self): return self._transaction_id
    @property
    def amount(self): return self._amount
    @property
    def status(self): return self._status
    @property
    def transaction_type(self): return self._type
    @property
    def gateway_reference(self): return self._gateway_reference
    @property
    def failure_reason(self): return self._failure_reason
    @property
    def sender_wallet_id(self): return self._sender_wallet_id
    @property
    def recipient_wallet_id(self): return self._recipient_wallet_id
    @property
    def created_at(self): return self._created_at

    def _guard(self):
        if self._status in self._TERMINAL:
            raise InvalidTransactionError(f"Cannot modify terminal state: {self._status.value}")

    def validate(self): self._guard(); self._status = TransactionStatus.VALIDATING
    def process(self): self._guard(); self._status = TransactionStatus.PROCESSING
    def pending_gateway(self): self._guard(); self._status = TransactionStatus.PENDING_GATEWAY
    def complete(self, ref: str): self._guard(); self._gateway_reference = ref; self._status = TransactionStatus.COMPLETED; self._completed_at = datetime.utcnow()
    def fail(self, reason: str): self._guard(); self._failure_reason = reason; self._status = TransactionStatus.FAILED
    def rollback(self):
        if self._status not in {TransactionStatus.PROCESSING, TransactionStatus.PENDING_GATEWAY}:
            raise InvalidTransactionError(f"Cannot rollback from: {self._status.value}")
        self._status = TransactionStatus.ROLLED_BACK
    def dispute(self):
        if self._status != TransactionStatus.COMPLETED: raise InvalidTransactionError("Only COMPLETED can be disputed.")
        self._status = TransactionStatus.DISPUTED
    def refund(self):
        if self._status != TransactionStatus.DISPUTED: raise InvalidTransactionError("Only DISPUTED can be refunded.")
        self._status = TransactionStatus.REFUNDED
    def get_status(self): return self._status

    def to_dict(self):
        return {"transaction_id": self._transaction_id, "sender_wallet_id": self._sender_wallet_id,
                "recipient_wallet_id": self._recipient_wallet_id, "type": self._type.value,
                "amount": str(self._amount), "currency": self._currency,
                "status": self._status.value, "gateway_reference": self._gateway_reference,
                "failure_reason": self._failure_reason, "created_at": self._created_at.isoformat()}

    def __repr__(self): return f"Transaction(id={self._transaction_id[:8]}, type={self._type.value}, amount=R{self._amount}, status={self._status.value})"
