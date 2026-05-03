"""
Tests for core domain models (src/models.py)
Run: pytest tests/test_models.py -v
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from decimal import Decimal
from src.models import (
    User, Wallet, Transaction, Notification, OTP, Session, AuditLog,
    UserStatus, WalletStatus, TransactionType, TransactionStatus,
    NotificationType, NotificationStatus, OTPStatus, SessionStatus, AdminAction,
    InsufficientFundsError, InvalidTransactionError, InvalidOTPError, WalletFrozenError,
)


# ─────────────────────────────────────────
# WALLET TESTS
# ─────────────────────────────────────────

class TestWallet:
    def setup_method(self):
        self.wallet = Wallet(user_id="user-1")

    def test_initial_balance_is_zero(self):
        assert self.wallet.balance == Decimal("0.00")

    def test_initial_status_is_active(self):
        assert self.wallet.status == WalletStatus.ACTIVE

    def test_credit_increases_balance(self):
        self.wallet.credit(Decimal("500.00"))
        assert self.wallet.balance == Decimal("500.00")

    def test_debit_decreases_balance(self):
        self.wallet.credit(Decimal("300.00"))
        self.wallet.debit(Decimal("100.00"))
        assert self.wallet.balance == Decimal("200.00")

    def test_debit_raises_on_insufficient_funds(self):
        self.wallet.credit(Decimal("50.00"))
        with pytest.raises(InsufficientFundsError):
            self.wallet.debit(Decimal("100.00"))

    def test_debit_raises_on_zero_amount(self):
        with pytest.raises(InvalidTransactionError):
            self.wallet.debit(Decimal("0.00"))

    def test_credit_raises_on_zero_amount(self):
        with pytest.raises(InvalidTransactionError):
            self.wallet.credit(Decimal("0.00"))

    def test_freeze_prevents_debit(self):
        self.wallet.credit(Decimal("200.00"))
        self.wallet.freeze()
        with pytest.raises(WalletFrozenError):
            self.wallet.debit(Decimal("50.00"))

    def test_freeze_prevents_credit(self):
        self.wallet.freeze()
        with pytest.raises(WalletFrozenError):
            self.wallet.credit(Decimal("100.00"))

    def test_unfreeze_restores_active_status(self):
        self.wallet.freeze()
        self.wallet.unfreeze()
        assert self.wallet.status == WalletStatus.ACTIVE

    def test_validate_sufficient_funds_true(self):
        self.wallet.credit(Decimal("200.00"))
        assert self.wallet.validate_sufficient_funds(Decimal("200.00")) is True

    def test_validate_sufficient_funds_false(self):
        self.wallet.credit(Decimal("50.00"))
        assert self.wallet.validate_sufficient_funds(Decimal("100.00")) is False

    def test_balance_never_goes_negative(self):
        self.wallet.credit(Decimal("100.00"))
        self.wallet.debit(Decimal("100.00"))
        assert self.wallet.balance == Decimal("0.00")


# ─────────────────────────────────────────
# USER TESTS
# ─────────────────────────────────────────

class TestUser:
    def setup_method(self):
        self.user = User("Amandla", "a@test.com", "+27821234567", "hash123")

    def test_initial_status_is_unverified(self):
        assert self.user.status == UserStatus.UNVERIFIED

    def test_activate_sets_active_status(self):
        self.user.activate()
        assert self.user.status == UserStatus.ACTIVE

    def test_wallet_created_on_init(self):
        assert self.user.wallet is not None
        assert isinstance(self.user.wallet, Wallet)

    def test_wallet_initial_balance_zero(self):
        assert self.user.wallet.balance == Decimal("0.00")

    def test_suspend_freezes_wallet(self):
        self.user.activate()
        self.user.suspend()
        assert self.user.status == UserStatus.SUSPENDED
        assert self.user.wallet.status == WalletStatus.FROZEN

    def test_reactivate_unfreezes_wallet(self):
        self.user.activate()
        self.user.suspend()
        self.user.reactivate()
        assert self.user.status == UserStatus.ACTIVE
        assert self.user.wallet.status == WalletStatus.ACTIVE

    def test_delete_closes_wallet(self):
        self.user.delete()
        assert self.user.status == UserStatus.DELETED
        assert self.user.wallet.status == WalletStatus.CLOSED

    def test_can_transact_only_when_active(self):
        assert self.user.can_transact() is False
        self.user.activate()
        assert self.user.can_transact() is True
        self.user.suspend()
        assert self.user.can_transact() is False

    def test_update_profile(self):
        self.user.update_profile(name="New Name", phone="+27829999999")
        assert self.user.name == "New Name"
        assert self.user.phone == "+27829999999"


# ─────────────────────────────────────────
# TRANSACTION TESTS
# ─────────────────────────────────────────

class TestTransaction:
    def setup_method(self):
        self.txn = Transaction(
            sender_wallet_id="wallet-1",
            amount=Decimal("200.00"),
            transaction_type=TransactionType.TRANSFER,
            recipient_wallet_id="wallet-2",
        )

    def test_initial_status_is_initiated(self):
        assert self.txn.status == TransactionStatus.INITIATED

    def test_state_progression(self):
        self.txn.validate()
        assert self.txn.status == TransactionStatus.VALIDATING
        self.txn.process()
        assert self.txn.status == TransactionStatus.PROCESSING
        self.txn.pending_gateway()
        assert self.txn.status == TransactionStatus.PENDING_GATEWAY
        self.txn.complete("GW-REF-001")
        assert self.txn.status == TransactionStatus.COMPLETED
        assert self.txn.gateway_reference == "GW-REF-001"

    def test_rollback_from_processing(self):
        self.txn.validate()
        self.txn.process()
        self.txn.rollback()
        assert self.txn.status == TransactionStatus.ROLLED_BACK

    def test_rollback_from_pending_gateway(self):
        self.txn.validate()
        self.txn.process()
        self.txn.pending_gateway()
        self.txn.rollback()
        assert self.txn.status == TransactionStatus.ROLLED_BACK

    def test_rollback_invalid_from_initiated(self):
        with pytest.raises(InvalidTransactionError):
            self.txn.rollback()

    def test_cannot_modify_completed_transaction(self):
        self.txn.validate()
        self.txn.process()
        self.txn.pending_gateway()
        self.txn.complete("GW-REF-002")
        with pytest.raises(InvalidTransactionError):
            self.txn.validate()

    def test_fail_sets_reason(self):
        self.txn.validate()
        self.txn.fail("Insufficient funds")
        assert self.txn.status == TransactionStatus.FAILED
        assert self.txn.failure_reason == "Insufficient funds"

    def test_dispute_only_from_completed(self):
        with pytest.raises(InvalidTransactionError):
            self.txn.dispute()

    def test_dispute_to_refund_flow(self):
        self.txn.validate()
        self.txn.process()
        self.txn.pending_gateway()
        self.txn.complete("GW-REF-003")
        self.txn.dispute()
        assert self.txn.status == TransactionStatus.DISPUTED
        self.txn.refund()
        assert self.txn.status == TransactionStatus.REFUNDED


# ─────────────────────────────────────────
# OTP TESTS
# ─────────────────────────────────────────

class TestOTP:
    def test_correct_code_verifies(self):
        otp = OTP(user_id="user-1", code="123456")
        assert otp.verify("123456") is True
        assert otp.status == OTPStatus.VERIFIED

    def test_wrong_code_returns_false(self):
        otp = OTP(user_id="user-1", code="123456")
        assert otp.verify("999999") is False

    def test_three_wrong_attempts_invalidate(self):
        otp = OTP(user_id="user-1", code="123456")
        for _ in range(3):
            otp.verify("000000")
        assert otp.status == OTPStatus.INVALIDATED

    def test_invalidated_otp_raises_on_verify(self):
        otp = OTP(user_id="user-1", code="123456")
        for _ in range(3):
            otp.verify("000000")
        with pytest.raises(InvalidOTPError):
            otp.verify("123456")

    def test_expired_otp_raises_on_verify(self):
        otp = OTP(user_id="user-1", code="123456")
        otp.expire()
        with pytest.raises(InvalidOTPError):
            otp.verify("123456")

    def test_attempt_counter_increments(self):
        otp = OTP(user_id="user-1", code="123456")
        otp.verify("000000")
        assert otp.attempt_count == 1

    def test_verified_otp_cannot_be_reverified(self):
        otp = OTP(user_id="user-1", code="123456")
        otp.verify("123456")
        with pytest.raises(InvalidOTPError):
            otp.verify("123456")


# ─────────────────────────────────────────
# NOTIFICATION TESTS
# ─────────────────────────────────────────

class TestNotification:
    def setup_method(self):
        self.notif = Notification(
            user_id="user-1",
            notification_type=NotificationType.TRANSFER_SENT,
            title="Transfer Sent",
            body="R100 sent",
            fcm_token="fcm-token-abc",
            transaction_id="txn-001",
        )

    def test_initial_status_queued(self):
        assert self.notif.status == NotificationStatus.QUEUED

    def test_send_transitions_to_sending(self):
        self.notif.send()
        assert self.notif.status == NotificationStatus.SENDING

    def test_mark_delivered(self):
        self.notif.send()
        self.notif.mark_delivered()
        assert self.notif.status == NotificationStatus.DELIVERED

    def test_retry_increments_count(self):
        self.notif.retry()
        assert self.notif.retry_count == 1

    def test_max_retries_sets_failed(self):
        for _ in range(Notification.MAX_RETRIES):
            self.notif.retry()
        result = self.notif.retry()
        assert result is False
        assert self.notif.status == NotificationStatus.FAILED

    def test_mark_read_from_delivered(self):
        self.notif.send()
        self.notif.mark_delivered()
        self.notif.mark_read()
        assert self.notif.status == NotificationStatus.READ

    def test_expire(self):
        self.notif.expire()
        assert self.notif.status == NotificationStatus.EXPIRED


# ─────────────────────────────────────────
# SESSION TESTS
# ─────────────────────────────────────────

class TestSession:
    def setup_method(self):
        self.session = Session(
            user_id="user-1",
            access_token_hash="hash-access-abc",
            refresh_token_hash="hash-refresh-xyz",
        )

    def test_initial_status_active(self):
        assert self.session.status == SessionStatus.ACTIVE

    def test_validate_correct_token(self):
        assert self.session.validate("hash-access-abc") is True

    def test_validate_wrong_token(self):
        assert self.session.validate("wrong-hash") is False

    def test_revoke_sets_revoked_status(self):
        self.session.revoke()
        assert self.session.status == SessionStatus.REVOKED

    def test_validate_fails_after_revoke(self):
        self.session.revoke()
        assert self.session.validate("hash-access-abc") is False

    def test_refresh_updates_token_hash(self):
        self.session.refresh("new-access-hash", "new-refresh-hash")
        assert self.session.validate("new-access-hash") is True
        assert self.session.validate("hash-access-abc") is False


# ─────────────────────────────────────────
# AUDIT LOG TESTS
# ─────────────────────────────────────────

class TestAuditLog:
    def test_creation(self):
        log = AuditLog(
            admin_id="admin-1",
            target_user_id="user-2",
            action=AdminAction.SUSPEND,
            reason="Fraud suspected",
            previous_status="ACTIVE",
            new_status="SUSPENDED",
        )
        assert log.action == AdminAction.SUSPEND
        assert log.reason == "Fraud suspected"

    def test_to_dict_contains_required_keys(self):
        log = AuditLog(
            admin_id="admin-1",
            target_user_id="user-2",
            action=AdminAction.REACTIVATE,
            reason="Appeal approved",
            previous_status="SUSPENDED",
            new_status="ACTIVE",
        )
        d = log.to_dict()
        for key in ["log_id", "admin_id", "target_user_id", "action", "reason", "created_at"]:
            assert key in d

    def test_archive(self):
        log = AuditLog("a", "b", AdminAction.DELETE, "Test", "ACTIVE", "DELETED")
        log.archive()
        assert log._archived is True