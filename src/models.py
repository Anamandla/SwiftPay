"""
SwiftPay — Core Domain Models
Translated from CLASS_DIAGRAM.md (Assignment 9)
Language: Python 3.10+
"""

from __future__ import annotations
from datetime import datetime, timedelta
from decimal import Decimal
from enum import Enum
from typing import Optional
import uuid
import hashlib


# ── Enumerations ──────────────────────────────────────────────────────────────

class UserStatus(Enum):
    UNVERIFIED = "UNVERIFIED"
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    DELETED = "DELETED"

class WalletStatus(Enum):
    ACTIVE = "ACTIVE"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"

class TransactionType(Enum):
    TRANSFER = "TRANSFER"
    TOP_UP = "TOP_UP"
    BILL_PAYMENT = "BILL_PAYMENT"

class TransactionStatus(Enum):
    INITIATED = "INITIATED"
    VALIDATING = "VALIDATING"
    PROCESSING = "PROCESSING"
    PENDING_GATEWAY = "PENDING_GATEWAY"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    ROLLED_BACK = "ROLLED_BACK"
    DISPUTED = "DISPUTED"
    REFUNDED = "REFUNDED"

class NotificationStatus(Enum):
    QUEUED = "QUEUED"
    SENDING = "SENDING"
    DELIVERED = "DELIVERED"
    FAILED = "FAILED"
    READ = "READ"
    EXPIRED = "EXPIRED"

class NotificationType(Enum):
    TRANSFER_SENT = "TRANSFER_SENT"
    TRANSFER_RECEIVED = "TRANSFER_RECEIVED"
    BILL_PAID = "BILL_PAID"
    TOP_UP_SUCCESS = "TOP_UP_SUCCESS"
    ACCOUNT_SUSPENDED = "ACCOUNT_SUSPENDED"

class OTPStatus(Enum):
    GENERATED = "GENERATED"
    SENT = "SENT"
    PENDING = "PENDING"
    VERIFIED = "VERIFIED"
    EXPIRED = "EXPIRED"
    INVALIDATED = "INVALIDATED"

class SessionStatus(Enum):
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"

class AdminAction(Enum):
    SUSPEND = "SUSPEND"
    REACTIVATE = "REACTIVATE"
    DELETE = "DELETE"
    REFUND = "REFUND"
    ESCALATE = "ESCALATE"


# ── Exceptions ────────────────────────────────────────────────────────────────

class InsufficientFundsError(Exception):
    pass

class InvalidTransactionError(Exception):
    pass

class InvalidOTPError(Exception):
    pass

class WalletFrozenError(Exception):
    pass


# ── Wallet ────────────────────────────────────────────────────────────────────

class Wallet:
    """Digital ZAR wallet. BR-03: balance never below R0.00."""

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

    def validate_sufficient_funds(self, amount: Decimal) -> bool:
        return self._balance >= amount

    def credit(self, amount: Decimal) -> None:
        if self._status == WalletStatus.FROZEN:
            raise WalletFrozenError("Cannot credit a frozen wallet.")
        if self._status == WalletStatus.CLOSED:
            raise InvalidTransactionError("Cannot credit a closed wallet.")
        if amount <= Decimal("0.00"):
            raise InvalidTransactionError("Credit amount must be > R0.00.")
        self._balance += amount
        self._updated_at = datetime.utcnow()

    def debit(self, amount: Decimal) -> None:
        if self._status == WalletStatus.FROZEN:
            raise WalletFrozenError("Cannot debit a frozen wallet.")
        if self._status == WalletStatus.CLOSED:
            raise InvalidTransactionError("Cannot debit a closed wallet.")
        if amount <= Decimal("0.00"):
            raise InvalidTransactionError("Debit amount must be > R0.00.")
        if not self.validate_sufficient_funds(amount):
            raise InsufficientFundsError(
                f"Insufficient funds. Balance: R{self._balance}, Required: R{amount}"
            )
        self._balance -= amount
        self._updated_at = datetime.utcnow()

    def freeze(self) -> None:
        self._status = WalletStatus.FROZEN
        self._updated_at = datetime.utcnow()

    def unfreeze(self) -> None:
        self._status = WalletStatus.ACTIVE
        self._updated_at = datetime.utcnow()

    def close(self) -> None:
        self._status = WalletStatus.CLOSED
        self._updated_at = datetime.utcnow()

    def get_balance(self) -> Decimal:
        return self._balance

    def __repr__(self):
        return f"Wallet(id={self._wallet_id[:8]}, balance=R{self._balance}, status={self._status.value})"


# ── User ──────────────────────────────────────────────────────────────────────

class User:
    """Registered SwiftPay user. Owns exactly one Wallet (composition)."""

    def __init__(self, name: str, email: str, phone: str, password_hash: str):
        self._user_id = str(uuid.uuid4())
        self._name = name
        self._email = email
        self._phone = phone
        self._password_hash = password_hash
        self._status = UserStatus.UNVERIFIED
        self._wallet = Wallet(user_id=self._user_id)   # Composition
        self._created_at = datetime.utcnow()
        self._updated_at = datetime.utcnow()

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

    def activate(self) -> None:
        self._status = UserStatus.ACTIVE
        self._updated_at = datetime.utcnow()

    def suspend(self) -> None:
        self._status = UserStatus.SUSPENDED
        self._wallet.freeze()    # BR-05
        self._updated_at = datetime.utcnow()

    def reactivate(self) -> None:
        self._status = UserStatus.ACTIVE
        self._wallet.unfreeze()
        self._updated_at = datetime.utcnow()

    def delete(self) -> None:
        self._status = UserStatus.DELETED
        self._wallet.close()
        self._updated_at = datetime.utcnow()

    def can_transact(self) -> bool:
        return self._status == UserStatus.ACTIVE

    def update_profile(self, name: str = None, phone: str = None) -> None:
        if name: self._name = name
        if phone: self._phone = phone
        self._updated_at = datetime.utcnow()

    def get_wallet(self) -> Wallet:
        return self._wallet

    def __repr__(self):
        return f"User(id={self._user_id[:8]}, name={self._name}, status={self._status.value})"


# ── Transaction ───────────────────────────────────────────────────────────────

class Transaction:
    """
    Immutable financial event record.
    BR-07: COMPLETED transactions cannot be modified.
    BR-08: Rollback only valid from PROCESSING or PENDING_GATEWAY.
    """

    _TERMINAL_STATES = {
        TransactionStatus.COMPLETED, TransactionStatus.FAILED,
        TransactionStatus.ROLLED_BACK, TransactionStatus.REFUNDED,
    }

    def __init__(self, sender_wallet_id: str, amount: Decimal,
                 transaction_type: TransactionType,
                 recipient_wallet_id: Optional[str] = None, currency: str = "ZAR"):
        self._transaction_id = str(uuid.uuid4())
        self._sender_wallet_id = sender_wallet_id
        self._recipient_wallet_id = recipient_wallet_id
        self._type = transaction_type
        self._amount = amount
        self._currency = currency
        self._status = TransactionStatus.INITIATED
        self._gateway_reference: Optional[str] = None
        self._failure_reason: Optional[str] = None
        self._created_at = datetime.utcnow()
        self._completed_at: Optional[datetime] = None

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

    def _guard_not_terminal(self) -> None:
        if self._status in self._TERMINAL_STATES:
            raise InvalidTransactionError(
                f"Cannot modify terminal state: {self._status.value}")

    def validate(self) -> None:
        self._guard_not_terminal()
        self._status = TransactionStatus.VALIDATING

    def process(self) -> None:
        self._guard_not_terminal()
        self._status = TransactionStatus.PROCESSING

    def pending_gateway(self) -> None:
        self._guard_not_terminal()
        self._status = TransactionStatus.PENDING_GATEWAY

    def complete(self, gateway_reference: str) -> None:
        self._guard_not_terminal()
        self._gateway_reference = gateway_reference
        self._status = TransactionStatus.COMPLETED
        self._completed_at = datetime.utcnow()

    def fail(self, reason: str) -> None:
        self._guard_not_terminal()
        self._failure_reason = reason
        self._status = TransactionStatus.FAILED

    def rollback(self) -> None:
        if self._status not in {TransactionStatus.PROCESSING, TransactionStatus.PENDING_GATEWAY}:
            raise InvalidTransactionError(
                f"Cannot rollback from: {self._status.value}")
        self._status = TransactionStatus.ROLLED_BACK

    def dispute(self) -> None:
        if self._status != TransactionStatus.COMPLETED:
            raise InvalidTransactionError("Can only dispute COMPLETED transactions.")
        self._status = TransactionStatus.DISPUTED

    def refund(self) -> None:
        if self._status != TransactionStatus.DISPUTED:
            raise InvalidTransactionError("Can only refund DISPUTED transactions.")
        self._status = TransactionStatus.REFUNDED

    def get_status(self) -> TransactionStatus:
        return self._status

    def __repr__(self):
        return (f"Transaction(id={self._transaction_id[:8]}, "
                f"type={self._type.value}, amount=R{self._amount}, status={self._status.value})")


# ── Notification ──────────────────────────────────────────────────────────────

class Notification:
    """Push notification via FCM. BR-15: Max 3 retries."""

    MAX_RETRIES = 3

    def __init__(self, user_id: str, notification_type: NotificationType,
                 title: str, body: str, fcm_token: str,
                 transaction_id: Optional[str] = None):
        self._notification_id = str(uuid.uuid4())
        self._user_id = user_id
        self._transaction_id = transaction_id
        self._type = notification_type
        self._title = title
        self._body = body
        self._fcm_token = fcm_token
        self._status = NotificationStatus.QUEUED
        self._retry_count = 0
        self._created_at = datetime.utcnow()
        self._delivered_at: Optional[datetime] = None

    @property
    def notification_id(self): return self._notification_id
    @property
    def status(self): return self._status
    @property
    def retry_count(self): return self._retry_count

    def send(self) -> None:
        self._status = NotificationStatus.SENDING

    def mark_delivered(self) -> None:
        self._status = NotificationStatus.DELIVERED
        self._delivered_at = datetime.utcnow()

    def retry(self) -> bool:
        if self._retry_count >= self.MAX_RETRIES:
            self._status = NotificationStatus.FAILED
            return False
        self._retry_count += 1
        self._status = NotificationStatus.SENDING
        return True

    def mark_read(self) -> None:
        if self._status == NotificationStatus.DELIVERED:
            self._status = NotificationStatus.READ

    def expire(self) -> None:
        self._status = NotificationStatus.EXPIRED

    def get_status(self) -> NotificationStatus:
        return self._status

    def __repr__(self):
        return f"Notification(id={self._notification_id[:8]}, type={self._type.value}, status={self._status.value})"


# ── OTP ───────────────────────────────────────────────────────────────────────

class OTP:
    """
    6-digit one-time password for password reset.
    BR-09: Expires 10 min; invalidated after 3 failed attempts.
    """

    MAX_ATTEMPTS = 3
    TTL_MINUTES = 10

    def __init__(self, user_id: str, code: str):
        self._otp_id = str(uuid.uuid4())
        self._user_id = user_id
        self._code_hash = hashlib.sha256(code.encode()).hexdigest()
        self._attempt_count = 0
        self._status = OTPStatus.GENERATED
        self._expires_at = datetime.utcnow() + timedelta(minutes=self.TTL_MINUTES)
        self._created_at = datetime.utcnow()

    @property
    def otp_id(self): return self._otp_id
    @property
    def status(self): return self._status
    @property
    def attempt_count(self): return self._attempt_count
    @property
    def expires_at(self): return self._expires_at

    def is_expired(self) -> bool:
        return datetime.utcnow() > self._expires_at

    def mark_sent(self) -> None:
        self._status = OTPStatus.SENT

    def verify(self, input_code: str) -> bool:
        if self._status in {OTPStatus.EXPIRED, OTPStatus.INVALIDATED, OTPStatus.VERIFIED}:
            raise InvalidOTPError(f"OTP is {self._status.value}.")
        if self.is_expired():
            self.expire()
            raise InvalidOTPError("OTP has expired.")
        self._attempt_count += 1
        input_hash = hashlib.sha256(input_code.encode()).hexdigest()
        if input_hash == self._code_hash:
            self._status = OTPStatus.VERIFIED
            return True
        if self._attempt_count >= self.MAX_ATTEMPTS:
            self.invalidate()
        return False

    def expire(self) -> None:
        self._status = OTPStatus.EXPIRED

    def invalidate(self) -> None:
        self._status = OTPStatus.INVALIDATED

    def __repr__(self):
        return f"OTP(id={self._otp_id[:8]}, status={self._status.value}, attempts={self._attempt_count})"


# ── Session ───────────────────────────────────────────────────────────────────

class Session:
    """JWT session. BR-11: access=24hr, refresh=30days. BR-12: revoked on suspension."""

    def __init__(self, user_id: str, access_token_hash: str,
                 refresh_token_hash: str, device_info: str = "", ip_address: str = ""):
        self._session_id = str(uuid.uuid4())
        self._user_id = user_id
        self._access_token_hash = access_token_hash
        self._refresh_token_hash = refresh_token_hash
        self._device_info = device_info
        self._ip_address = ip_address
        self._status = SessionStatus.ACTIVE
        self._issued_at = datetime.utcnow()
        self._access_expires_at = datetime.utcnow() + timedelta(hours=24)
        self._refresh_expires_at = datetime.utcnow() + timedelta(days=30)

    @property
    def session_id(self): return self._session_id
    @property
    def status(self): return self._status
    @property
    def access_expires_at(self): return self._access_expires_at
    @property
    def refresh_expires_at(self): return self._refresh_expires_at

    def is_expired(self) -> bool:
        if datetime.utcnow() > self._access_expires_at:
            self._status = SessionStatus.EXPIRED
            return True
        return False

    def validate(self, token_hash: str) -> bool:
        if self._status != SessionStatus.ACTIVE:
            return False
        if self.is_expired():
            return False
        return self._access_token_hash == token_hash

    def revoke(self) -> None:
        self._status = SessionStatus.REVOKED

    def refresh(self, new_access_hash: str, new_refresh_hash: str) -> None:
        if datetime.utcnow() > self._refresh_expires_at:
            self._status = SessionStatus.EXPIRED
            raise InvalidTransactionError("Refresh token expired.")
        self._access_token_hash = new_access_hash
        self._refresh_token_hash = new_refresh_hash
        self._access_expires_at = datetime.utcnow() + timedelta(hours=24)

    def __repr__(self):
        return f"Session(id={self._session_id[:8]}, user={self._user_id[:8]}, status={self._status.value})"


# ── AuditLog ──────────────────────────────────────────────────────────────────

class AuditLog:
    """
    Immutable admin action record.
    BR-13: Every admin action produces an entry atomically.
    BR-14: No update/delete — retained >= 12 months.
    """

    def __init__(self, admin_id: str, target_user_id: str, action: AdminAction,
                 reason: str, previous_status: str, new_status: str,
                 ip_address: str = "", transaction_id: Optional[str] = None):
        self._log_id = str(uuid.uuid4())
        self._admin_id = admin_id
        self._target_user_id = target_user_id
        self._transaction_id = transaction_id
        self._action = action
        self._reason = reason
        self._previous_status = previous_status
        self._new_status = new_status
        self._ip_address = ip_address
        self._created_at = datetime.utcnow()
        self._archived = False

    @property
    def log_id(self): return self._log_id
    @property
    def action(self): return self._action
    @property
    def reason(self): return self._reason
    @property
    def admin_id(self): return self._admin_id
    @property
    def target_user_id(self): return self._target_user_id
    @property
    def created_at(self): return self._created_at

    def archive(self) -> None:
        self._archived = True

    def to_dict(self) -> dict:
        return {
            "log_id": self._log_id,
            "admin_id": self._admin_id,
            "target_user_id": self._target_user_id,
            "action": self._action.value,
            "reason": self._reason,
            "previous_status": self._previous_status,
            "new_status": self._new_status,
            "created_at": self._created_at.isoformat(),
        }

    def __repr__(self):
        return (f"AuditLog(id={self._log_id[:8]}, action={self._action.value}, "
                f"admin={self._admin_id[:8]}, target={self._target_user_id[:8]})")