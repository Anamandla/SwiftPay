"""
Tests for all 6 creational patterns
Run: pytest tests/test_creational_patterns.py -v
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
import threading
from decimal import Decimal
from src.models import (
    Wallet, NotificationType, NotificationStatus, TransactionType,
    TransactionStatus, OTPStatus, UserStatus, WalletStatus,
)


# ─────────────────────────────────────────
# 1. SIMPLE FACTORY
# ─────────────────────────────────────────

class TestSimpleFactory:
    def setup_method(self):
        from creational_patterns.simple_factory import NotificationFactory
        self.factory = NotificationFactory

    def test_creates_transfer_sent_notification(self):
        n = self.factory.create(
            NotificationType.TRANSFER_SENT,
            user_id="u1", fcm_token="tkn",
            amount=Decimal("100.00"), counterparty_name="Sipho"
        )
        assert n.status == NotificationStatus.QUEUED

    def test_creates_transfer_received_notification(self):
        n = self.factory.create(
            NotificationType.TRANSFER_RECEIVED,
            user_id="u1", fcm_token="tkn",
            amount=Decimal("50.00"), counterparty_name="Thabo"
        )
        assert n is not None

    def test_creates_account_suspended_notification(self):
        n = self.factory.create(
            NotificationType.ACCOUNT_SUSPENDED,
            user_id="u1", fcm_token="tkn"
        )
        assert n is not None

    def test_creates_top_up_notification(self):
        n = self.factory.create(
            NotificationType.TOP_UP_SUCCESS,
            user_id="u1", fcm_token="tkn",
            amount=Decimal("200.00")
        )
        assert n is not None

    def test_creates_bill_paid_notification(self):
        n = self.factory.create(
            NotificationType.BILL_PAID,
            user_id="u1", fcm_token="tkn",
            amount=Decimal("350.00")
        )
        assert n is not None

    def test_invalid_type_raises_value_error(self):
        with pytest.raises((ValueError, KeyError)):
            self.factory.create("INVALID_TYPE", user_id="u1", fcm_token="tkn")

    def test_each_call_returns_new_instance(self):
        n1 = self.factory.create(NotificationType.ACCOUNT_SUSPENDED, user_id="u1", fcm_token="t1")
        n2 = self.factory.create(NotificationType.ACCOUNT_SUSPENDED, user_id="u1", fcm_token="t1")
        assert n1 is not n2
        assert n1.notification_id != n2.notification_id


# ─────────────────────────────────────────
# 2. FACTORY METHOD
# ─────────────────────────────────────────

class TestFactoryMethod:
    def setup_method(self):
        from creational_patterns.factory_method import (
            TransferProcessor, TopUpProcessor, BillPaymentProcessor
        )
        from src.models import InsufficientFundsError
        self.TransferProcessor = TransferProcessor
        self.TopUpProcessor = TopUpProcessor
        self.BillPaymentProcessor = BillPaymentProcessor
        self.InsufficientFundsError = InsufficientFundsError

    def _funded_wallet(self, amount="500.00"):
        w = Wallet(user_id="test-user")
        w.credit(Decimal(amount))
        return w

    def test_transfer_processor_creates_transfer_transaction(self):
        wallet = self._funded_wallet()
        txn = self.TransferProcessor().process(
            wallet, Decimal("100.00"), recipient_wallet_id="wallet-b"
        )
        assert txn.transaction_type == TransactionType.TRANSFER
        assert txn.status == TransactionStatus.VALIDATING

    def test_transfer_processor_raises_on_insufficient_funds(self):
        wallet = self._funded_wallet("50.00")
        with pytest.raises(self.InsufficientFundsError):
            self.TransferProcessor().process(
                wallet, Decimal("100.00"), recipient_wallet_id="wallet-b"
            )

    def test_transfer_processor_raises_without_recipient(self):
        wallet = self._funded_wallet()
        with pytest.raises(ValueError):
            self.TransferProcessor().process(wallet, Decimal("100.00"))

    def test_topup_processor_creates_topup_transaction(self):
        wallet = self._funded_wallet("0.00")
        wallet2 = Wallet(user_id="t")
        txn = self.TopUpProcessor().process(wallet2, Decimal("200.00"))
        assert txn.transaction_type == TransactionType.TOP_UP

    def test_bill_processor_creates_bill_payment(self):
        wallet = self._funded_wallet()
        txn = self.BillPaymentProcessor().process(
            wallet, Decimal("150.00"),
            provider_id="eskom", reference="ACC-12345"
        )
        assert txn.transaction_type == TransactionType.BILL_PAYMENT

    def test_bill_processor_raises_without_provider(self):
        wallet = self._funded_wallet()
        with pytest.raises(ValueError):
            self.BillPaymentProcessor().process(wallet, Decimal("100.00"))

    def test_zero_amount_raises(self):
        wallet = self._funded_wallet()
        with pytest.raises(ValueError):
            self.TransferProcessor().process(
                wallet, Decimal("0.00"), recipient_wallet_id="wallet-b"
            )


# ─────────────────────────────────────────
# 3. ABSTRACT FACTORY
# ─────────────────────────────────────────

class TestAbstractFactory:
    def setup_method(self):
        from creational_patterns.abstract_factory import (
            TestingNotificationFactory, ProductionNotificationFactory,
            StubPushNotifier, StubEmailSender,
            FCMPushNotifier, SendGridEmailSender
        )
        self.TestingFactory = TestingNotificationFactory
        self.ProductionFactory = ProductionNotificationFactory
        self.StubPush = StubPushNotifier
        self.StubEmail = StubEmailSender
        self.FCMPush = FCMPushNotifier
        self.SendGridEmail = SendGridEmailSender

    def test_testing_factory_returns_stubs(self):
        factory = self.TestingFactory()
        assert isinstance(factory.create_push_notifier(), self.StubPush)
        assert isinstance(factory.create_email_sender(), self.StubEmail)

    def test_production_factory_returns_real_adapters(self):
        factory = self.ProductionFactory("fcm-key", "sg-key", "noreply@swiftpay.app")
        assert isinstance(factory.create_push_notifier(), self.FCMPush)
        assert isinstance(factory.create_email_sender(), self.SendGridEmail)

    def test_stub_push_records_sent_notifications(self):
        factory = self.TestingFactory()
        push = factory.create_push_notifier()
        push.send("token-123", "Test Title", "Test Body")
        assert len(push.sent_notifications) == 1
        assert push.sent_notifications[0]["title"] == "Test Title"

    def test_stub_email_records_sent_emails(self):
        factory = self.TestingFactory()
        email = factory.create_email_sender()
        email.send("user@test.com", "OTP Code", "Your OTP is 123456")
        assert len(email.sent_emails) == 1
        assert email.sent_emails[0]["to"] == "user@test.com"

    def test_stub_push_returns_true_on_send(self):
        factory = self.TestingFactory()
        push = factory.create_push_notifier()
        result = push.send("token", "Title", "Body")
        assert result is True

    def test_two_factories_produce_independent_stubs(self):
        factory1 = self.TestingFactory()
        factory2 = self.TestingFactory()
        p1 = factory1.create_push_notifier()
        p2 = factory2.create_push_notifier()
        p1.send("t", "T", "B")
        assert len(p1.sent_notifications) == 1
        assert len(p2.sent_notifications) == 0


# ─────────────────────────────────────────
# 4. BUILDER
# ─────────────────────────────────────────

class TestBuilder:
    def setup_method(self):
        from creational_patterns.builder import UserBuilder, UserDirector
        self.UserBuilder = UserBuilder
        self.UserDirector = UserDirector

    def _valid_builder(self):
        return (self.UserBuilder()
                .set_name("Test User")
                .set_email("test@swiftpay.app")
                .set_phone("+27821234567")
                .set_password("SecurePass99!"))

    def test_builds_valid_user(self):
        user = self._valid_builder().build()
        assert user.name == "Test User"
        assert user.email == "test@swiftpay.app"

    def test_auto_activate_sets_active_status(self):
        user = self._valid_builder().set_auto_activate(True).build()
        assert user.status == UserStatus.ACTIVE

    def test_without_auto_activate_status_is_unverified(self):
        user = self._valid_builder().build()
        assert user.status == UserStatus.UNVERIFIED

    def test_initial_credit_applied_to_wallet(self):
        user = (self._valid_builder()
                .set_auto_activate(True)
                .set_initial_credit(Decimal("500.00"))
                .build())
        assert user.wallet.balance == Decimal("500.00")

    def test_missing_email_raises(self):
        with pytest.raises(ValueError):
            (self.UserBuilder()
             .set_name("Test")
             .set_phone("+27821234567")
             .set_password("Pass1234!")
             .build())

    def test_invalid_email_raises(self):
        with pytest.raises(ValueError):
            self.UserBuilder().set_email("not-an-email")

    def test_short_password_raises(self):
        with pytest.raises(ValueError):
            self.UserBuilder().set_password("short")

    def test_short_name_raises(self):
        with pytest.raises(ValueError):
            self.UserBuilder().set_name("A")

    def test_invalid_phone_raises(self):
        with pytest.raises(ValueError):
            self.UserBuilder().set_phone("123")

    def test_negative_initial_credit_raises(self):
        with pytest.raises(ValueError):
            self.UserBuilder().set_initial_credit(Decimal("-50.00"))

    def test_director_builds_activated_test_user(self):
        user = self.UserDirector.build_activated_test_user(
            "Director User", "dir@test.com", "+27829876543"
        )
        assert user.status == UserStatus.ACTIVE
        assert user.wallet.balance == Decimal("1000.00")

    def test_builder_returns_self_for_chaining(self):
        b = self.UserBuilder()
        result = b.set_name("Chain Test")
        assert result is b


# ─────────────────────────────────────────
# 5. PROTOTYPE
# ─────────────────────────────────────────

class TestPrototype:
    def setup_method(self):
        from creational_patterns.prototype import TransactionPrototypeCache
        self.cache = TransactionPrototypeCache()

    def test_clone_has_correct_type(self):
        txn = self.cache.get("transfer", "wallet-a", Decimal("100.00"), "wallet-b")
        assert txn.transaction_type == TransactionType.TRANSFER

    def test_clone_has_correct_amount(self):
        txn = self.cache.get("top_up", "wallet-a", Decimal("250.00"))
        assert txn.amount == Decimal("250.00")

    def test_clones_are_independent_instances(self):
        t1 = self.cache.get("transfer", "w1", Decimal("100.00"), "w2")
        t2 = self.cache.get("transfer", "w3", Decimal("200.00"), "w4")
        assert t1 is not t2

    def test_clones_have_unique_ids(self):
        t1 = self.cache.get("bill_payment", "w1", Decimal("50.00"))
        t2 = self.cache.get("bill_payment", "w1", Decimal("50.00"))
        assert t1.transaction_id != t2.transaction_id

    def test_modifying_clone_does_not_affect_template(self):
        t1 = self.cache.get("transfer", "wallet-sender", Decimal("100.00"), "wallet-recv")
        t1.validate()
        t2 = self.cache.get("transfer", "wallet-sender", Decimal("100.00"), "wallet-recv")
        assert t2.status == TransactionStatus.INITIATED

    def test_invalid_key_raises_key_error(self):
        with pytest.raises(KeyError):
            self.cache.get("nonexistent", "w1", Decimal("100.00"))

    def test_topup_prototype_type(self):
        txn = self.cache.get("top_up", "wallet-1", Decimal("500.00"))
        assert txn.transaction_type == TransactionType.TOP_UP

    def test_bill_payment_prototype_type(self):
        txn = self.cache.get("bill_payment", "wallet-1", Decimal("300.00"))
        assert txn.transaction_type == TransactionType.BILL_PAYMENT

    def test_sender_wallet_id_set_correctly(self):
        txn = self.cache.get("top_up", "my-wallet-id", Decimal("100.00"))
        assert txn.sender_wallet_id == "my-wallet-id"

    def test_recipient_wallet_id_set_correctly(self):
        txn = self.cache.get("transfer", "sender-id", Decimal("100.00"), "recipient-id")
        assert txn.recipient_wallet_id == "recipient-id"


# ─────────────────────────────────────────
# 6. SINGLETON
# ─────────────────────────────────────────

class TestSingleton:
    def setup_method(self):
        from creational_patterns.singleton import DatabaseConnectionPool
        DatabaseConnectionPool.reset_instance()
        self.Pool = DatabaseConnectionPool

    def test_same_instance_returned(self):
        p1 = self.Pool(host="localhost", database="swiftpay")
        p2 = self.Pool(host="other-host", database="other_db")
        assert p1 is p2

    def test_second_init_does_not_override_first(self):
        p1 = self.Pool(host="primary-host", database="swiftpay")
        p2 = self.Pool(host="secondary-host", database="other")
        assert p2.host == "primary-host"
        assert p2.database == "swiftpay"

    def test_get_connection_increments_active_count(self):
        pool = self.Pool(host="localhost", database="swiftpay")
        conn = pool.get_connection()
        assert pool.active_connections == 1
        pool.release_connection(conn)

    def test_release_connection_decrements_active_count(self):
        pool = self.Pool(host="localhost", database="swiftpay")
        conn = pool.get_connection()
        pool.release_connection(conn)
        assert pool.active_connections == 0

    def test_pool_exhaustion_raises(self):
        pool = self.Pool(host="localhost", database="swiftpay", max_connections=2)
        conns = [pool.get_connection(), pool.get_connection()]
        with pytest.raises(RuntimeError):
            pool.get_connection()
        for c in conns:
            pool.release_connection(c)

    def test_execute_query_increments_count(self):
        pool = self.Pool(host="localhost", database="swiftpay")
        result = pool.execute_query("SELECT 1")
        assert pool.query_count >= 1

    def test_thread_safety(self):
        """Multiple threads must receive the same singleton instance."""
        instances = []
        def get_instance():
            instances.append(self.Pool(host="localhost", database="swiftpay"))

        threads = [threading.Thread(target=get_instance) for _ in range(20)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert all(inst is instances[0] for inst in instances), \
            "All threads must receive the same singleton instance"

    def test_reset_allows_new_instance(self):
        p1 = self.Pool(host="host-a", database="db-a")
        self.Pool.reset_instance()
        p2 = self.Pool(host="host-b", database="db-b")
        assert p2.host == "host-b"