"""
Standalone test runner — no pytest dependency required.
Run: python3 tests/run_tests.py
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import unittest
from decimal import Decimal
from src.models import (
    User, Wallet, Transaction, Notification, OTP, Session, AuditLog,
    UserStatus, WalletStatus, TransactionType, TransactionStatus,
    NotificationType, NotificationStatus, OTPStatus, SessionStatus, AdminAction,
    InsufficientFundsError, InvalidTransactionError, InvalidOTPError, WalletFrozenError,
)

PASS = 0; FAIL = 0

def ok(name):
    global PASS; PASS += 1; print(f"  ✅ {name}")

def fail(name, e):
    global FAIL; FAIL += 1; print(f"  ❌ {name}: {e}")

def section(title):
    print(f"\n{'─'*55}\n{title}\n{'─'*55}")

def expect_raises(exc_class, fn):
    try:
        fn()
        return False
    except exc_class:
        return True
    except Exception:
        return False

# ── Wallet ────────────────────────────────────────────────────────────────────
section("Wallet Tests")
try:
    w = Wallet("u1")
    assert w.balance == Decimal("0.00"); ok("initial balance is zero")
except Exception as e: fail("initial balance is zero", e)

try:
    w = Wallet("u1"); w.credit(Decimal("500.00"))
    assert w.balance == Decimal("500.00"); ok("credit increases balance")
except Exception as e: fail("credit increases balance", e)

try:
    w = Wallet("u1"); w.credit(Decimal("300.00")); w.debit(Decimal("100.00"))
    assert w.balance == Decimal("200.00"); ok("debit decreases balance")
except Exception as e: fail("debit decreases balance", e)

try:
    w = Wallet("u1"); w.credit(Decimal("50.00"))
    assert expect_raises(InsufficientFundsError, lambda: w.debit(Decimal("100.00")))
    ok("debit raises on insufficient funds")
except Exception as e: fail("debit raises on insufficient funds", e)

try:
    w = Wallet("u1"); w.credit(Decimal("200.00")); w.freeze()
    assert expect_raises(WalletFrozenError, lambda: w.debit(Decimal("50.00")))
    ok("freeze prevents debit")
except Exception as e: fail("freeze prevents debit", e)

try:
    w = Wallet("u1"); w.freeze(); w.unfreeze()
    assert w.status == WalletStatus.ACTIVE; ok("unfreeze restores active status")
except Exception as e: fail("unfreeze restores active status", e)

try:
    w = Wallet("u1")
    assert expect_raises(InvalidTransactionError, lambda: w.credit(Decimal("0.00")))
    ok("credit raises on zero amount")
except Exception as e: fail("credit raises on zero amount", e)

# ── User ──────────────────────────────────────────────────────────────────────
section("User Tests")
try:
    u = User("Amandla", "a@t.com", "+27821234567", "hash")
    assert u.status == UserStatus.UNVERIFIED; ok("initial status is UNVERIFIED")
except Exception as e: fail("initial status is UNVERIFIED", e)

try:
    u = User("A", "a@t.com", "+27821234567", "hash"); u.activate()
    assert u.status == UserStatus.ACTIVE; ok("activate sets ACTIVE")
except Exception as e: fail("activate sets ACTIVE", e)

try:
    u = User("A", "a@t.com", "+27821234567", "hash"); u.activate(); u.suspend()
    assert u.status == UserStatus.SUSPENDED
    assert u.wallet.status == WalletStatus.FROZEN; ok("suspend freezes wallet")
except Exception as e: fail("suspend freezes wallet", e)

try:
    u = User("A", "a@t.com", "+27821234567", "hash"); u.activate(); u.suspend(); u.reactivate()
    assert u.status == UserStatus.ACTIVE
    assert u.wallet.status == WalletStatus.ACTIVE; ok("reactivate unfreezes wallet")
except Exception as e: fail("reactivate unfreezes wallet", e)

try:
    u = User("A", "a@t.com", "+27821234567", "hash")
    assert u.can_transact() is False; u.activate()
    assert u.can_transact() is True; ok("can_transact only when ACTIVE")
except Exception as e: fail("can_transact only when ACTIVE", e)

# ── Transaction ───────────────────────────────────────────────────────────────
section("Transaction Tests")
try:
    t = Transaction("w1", Decimal("100.00"), TransactionType.TRANSFER, "w2")
    assert t.status == TransactionStatus.INITIATED; ok("initial status INITIATED")
except Exception as e: fail("initial status INITIATED", e)

try:
    t = Transaction("w1", Decimal("100.00"), TransactionType.TRANSFER, "w2")
    t.validate(); t.process(); t.pending_gateway(); t.complete("GW-001")
    assert t.status == TransactionStatus.COMPLETED
    assert t.gateway_reference == "GW-001"; ok("full completion flow")
except Exception as e: fail("full completion flow", e)

try:
    t = Transaction("w1", Decimal("100.00"), TransactionType.TRANSFER, "w2")
    t.validate(); t.process(); t.rollback()
    assert t.status == TransactionStatus.ROLLED_BACK; ok("rollback from PROCESSING")
except Exception as e: fail("rollback from PROCESSING", e)

try:
    t = Transaction("w1", Decimal("100.00"), TransactionType.TRANSFER, "w2")
    assert expect_raises(InvalidTransactionError, lambda: t.rollback())
    ok("rollback raises from INITIATED")
except Exception as e: fail("rollback raises from INITIATED", e)

try:
    t = Transaction("w1", Decimal("100.00"), TransactionType.TRANSFER, "w2")
    t.validate(); t.process(); t.pending_gateway(); t.complete("GW-X")
    assert expect_raises(InvalidTransactionError, lambda: t.validate())
    ok("cannot modify COMPLETED transaction")
except Exception as e: fail("cannot modify COMPLETED transaction", e)

try:
    t = Transaction("w1", Decimal("100.00"), TransactionType.TRANSFER, "w2")
    t.validate(); t.process(); t.pending_gateway(); t.complete("GW-Y")
    t.dispute(); t.refund()
    assert t.status == TransactionStatus.REFUNDED; ok("dispute to refund flow")
except Exception as e: fail("dispute to refund flow", e)

# ── OTP ───────────────────────────────────────────────────────────────────────
section("OTP Tests")
try:
    otp = OTP("u1", "123456")
    assert otp.verify("123456") is True
    assert otp.status == OTPStatus.VERIFIED; ok("correct code verifies")
except Exception as e: fail("correct code verifies", e)

try:
    otp = OTP("u1", "123456")
    assert otp.verify("999999") is False; ok("wrong code returns False")
except Exception as e: fail("wrong code returns False", e)

try:
    otp = OTP("u1", "123456")
    for _ in range(3): otp.verify("000000")
    assert otp.status == OTPStatus.INVALIDATED; ok("3 wrong attempts invalidates OTP")
except Exception as e: fail("3 wrong attempts invalidates OTP", e)

try:
    otp = OTP("u1", "123456"); otp.expire()
    assert expect_raises(InvalidOTPError, lambda: otp.verify("123456"))
    ok("expired OTP raises InvalidOTPError")
except Exception as e: fail("expired OTP raises InvalidOTPError", e)

try:
    otp = OTP("u1", "123456"); otp.verify("123456")
    assert expect_raises(InvalidOTPError, lambda: otp.verify("123456"))
    ok("verified OTP cannot be re-verified")
except Exception as e: fail("verified OTP cannot be re-verified", e)

# ── Notification ──────────────────────────────────────────────────────────────
section("Notification Tests")
try:
    n = Notification("u1", NotificationType.TRANSFER_SENT, "T", "B", "fcm")
    assert n.status == NotificationStatus.QUEUED; ok("initial status QUEUED")
except Exception as e: fail("initial status QUEUED", e)

try:
    n = Notification("u1", NotificationType.TRANSFER_SENT, "T", "B", "fcm")
    for _ in range(Notification.MAX_RETRIES): n.retry()
    result = n.retry()
    assert result is False and n.status == NotificationStatus.FAILED
    ok("max retries sets FAILED")
except Exception as e: fail("max retries sets FAILED", e)

# ── Creational Patterns ───────────────────────────────────────────────────────
section("Simple Factory Tests")
from creational_patterns.simple_factory import NotificationFactory
try:
    n = NotificationFactory.create(NotificationType.TRANSFER_SENT, user_id="u1",
        fcm_token="t", amount=Decimal("100"), counterparty_name="Sipho")
    assert n.status == NotificationStatus.QUEUED; ok("factory creates TRANSFER_SENT")
except Exception as e: fail("factory creates TRANSFER_SENT", e)

try:
    assert expect_raises((ValueError, KeyError),
        lambda: NotificationFactory.create("BAD_TYPE", user_id="u1", fcm_token="t"))
    ok("invalid type raises ValueError")
except Exception as e: fail("invalid type raises ValueError", e)

try:
    n1 = NotificationFactory.create(NotificationType.ACCOUNT_SUSPENDED, user_id="u1", fcm_token="t")
    n2 = NotificationFactory.create(NotificationType.ACCOUNT_SUSPENDED, user_id="u1", fcm_token="t")
    assert n1 is not n2; ok("each call returns new instance")
except Exception as e: fail("each call returns new instance", e)

section("Factory Method Tests")
from creational_patterns.factory_method import TransferProcessor, TopUpProcessor, BillPaymentProcessor
try:
    w = Wallet("u1"); w.credit(Decimal("500.00"))
    txn = TransferProcessor().process(w, Decimal("100.00"), recipient_wallet_id="w2")
    assert txn.transaction_type == TransactionType.TRANSFER; ok("TransferProcessor creates TRANSFER")
except Exception as e: fail("TransferProcessor creates TRANSFER", e)

try:
    w = Wallet("u1"); w.credit(Decimal("50.00"))
    assert expect_raises(InsufficientFundsError,
        lambda: TransferProcessor().process(w, Decimal("100.00"), recipient_wallet_id="w2"))
    ok("TransferProcessor raises on insufficient funds")
except Exception as e: fail("TransferProcessor raises on insufficient funds", e)

try:
    w = Wallet("u1")
    txn = TopUpProcessor().process(w, Decimal("200.00"))
    assert txn.transaction_type == TransactionType.TOP_UP; ok("TopUpProcessor creates TOP_UP")
except Exception as e: fail("TopUpProcessor creates TOP_UP", e)

try:
    w = Wallet("u1"); w.credit(Decimal("500.00"))
    txn = BillPaymentProcessor().process(w, Decimal("150.00"), provider_id="eskom", reference="ACC-001")
    assert txn.transaction_type == TransactionType.BILL_PAYMENT; ok("BillPaymentProcessor creates BILL_PAYMENT")
except Exception as e: fail("BillPaymentProcessor creates BILL_PAYMENT", e)

section("Abstract Factory Tests")
from creational_patterns.abstract_factory import TestingNotificationFactory, ProductionNotificationFactory, StubPushNotifier, StubEmailSender
try:
    f = TestingNotificationFactory()
    assert isinstance(f.create_push_notifier(), StubPushNotifier); ok("testing factory returns StubPushNotifier")
except Exception as e: fail("testing factory returns StubPushNotifier", e)

try:
    f = TestingNotificationFactory()
    push = f.create_push_notifier()
    push.send("token", "Title", "Body")
    assert len(push.sent_notifications) == 1; ok("stub records sent notifications")
except Exception as e: fail("stub records sent notifications", e)

try:
    f1 = TestingNotificationFactory(); f2 = TestingNotificationFactory()
    p1 = f1.create_push_notifier(); p2 = f2.create_push_notifier()
    p1.send("t", "T", "B")
    assert len(p2.sent_notifications) == 0; ok("two factories produce independent stubs")
except Exception as e: fail("two factories produce independent stubs", e)

section("Builder Tests")
from creational_patterns.builder import UserBuilder, UserDirector
def vb():
    return (UserBuilder().set_name("Test User").set_email("test@swiftpay.app")
            .set_phone("+27821234567").set_password("SecurePass99!"))

try:
    u = vb().build(); assert u.name == "Test User"; ok("builds valid user")
except Exception as e: fail("builds valid user", e)

try:
    u = vb().set_auto_activate(True).build()
    assert u.status == UserStatus.ACTIVE; ok("auto_activate sets ACTIVE")
except Exception as e: fail("auto_activate sets ACTIVE", e)

try:
    u = vb().set_auto_activate(True).set_initial_credit(Decimal("500.00")).build()
    assert u.wallet.balance == Decimal("500.00"); ok("initial credit applied to wallet")
except Exception as e: fail("initial credit applied to wallet", e)

try:
    assert expect_raises(ValueError, lambda: UserBuilder().set_email("bad-email"))
    ok("invalid email raises ValueError")
except Exception as e: fail("invalid email raises ValueError", e)

try:
    assert expect_raises(ValueError, lambda: UserBuilder().set_password("short"))
    ok("short password raises ValueError")
except Exception as e: fail("short password raises ValueError", e)

try:
    u = UserDirector.build_activated_test_user("Dir", "dir@t.com", "+27829876543")
    assert u.status == UserStatus.ACTIVE
    assert u.wallet.balance == Decimal("1000.00"); ok("director builds test user with R1000")
except Exception as e: fail("director builds test user with R1000", e)

section("Prototype Tests")
from creational_patterns.prototype import TransactionPrototypeCache
try:
    cache = TransactionPrototypeCache()
    t = cache.get("transfer", "w1", Decimal("100.00"), "w2")
    assert t.transaction_type == TransactionType.TRANSFER; ok("clone has correct type")
except Exception as e: fail("clone has correct type", e)

try:
    cache = TransactionPrototypeCache()
    t1 = cache.get("transfer", "w1", Decimal("100.00"), "w2")
    t2 = cache.get("transfer", "w3", Decimal("200.00"), "w4")
    assert t1 is not t2; ok("clones are independent instances")
except Exception as e: fail("clones are independent instances", e)

try:
    cache = TransactionPrototypeCache()
    t1 = cache.get("transfer", "w1", Decimal("50.00"), "w2")
    t2 = cache.get("transfer", "w1", Decimal("50.00"), "w2")
    assert t1.transaction_id != t2.transaction_id; ok("clones have unique IDs")
except Exception as e: fail("clones have unique IDs", e)

try:
    cache = TransactionPrototypeCache()
    t1 = cache.get("transfer", "w1", Decimal("100.00"), "w2"); t1.validate()
    t2 = cache.get("transfer", "w1", Decimal("100.00"), "w2")
    assert t2.status == TransactionStatus.INITIATED; ok("modifying clone does not affect template")
except Exception as e: fail("modifying clone does not affect template", e)

try:
    cache = TransactionPrototypeCache()
    assert expect_raises(KeyError, lambda: cache.get("nonexistent", "w1", Decimal("1.00")))
    ok("invalid key raises KeyError")
except Exception as e: fail("invalid key raises KeyError", e)

section("Singleton Tests")
import threading
from creational_patterns.singleton import DatabaseConnectionPool
try:
    DatabaseConnectionPool.reset_instance()
    p1 = DatabaseConnectionPool(host="h1", database="db1")
    p2 = DatabaseConnectionPool(host="h2", database="db2")
    assert p1 is p2; ok("same instance returned")
except Exception as e: fail("same instance returned", e)

try:
    DatabaseConnectionPool.reset_instance()
    p1 = DatabaseConnectionPool(host="primary", database="swiftpay")
    p2 = DatabaseConnectionPool(host="other", database="other")
    assert p2.host == "primary"; ok("second init does not override first")
except Exception as e: fail("second init does not override first", e)

try:
    DatabaseConnectionPool.reset_instance()
    pool = DatabaseConnectionPool(host="h", database="d", max_connections=2)
    c1 = pool.get_connection(); c2 = pool.get_connection()
    assert expect_raises(RuntimeError, lambda: pool.get_connection())
    pool.release_connection(c1); pool.release_connection(c2)
    ok("pool exhaustion raises RuntimeError")
except Exception as e: fail("pool exhaustion raises RuntimeError", e)

try:
    DatabaseConnectionPool.reset_instance()
    instances = []
    def get_inst(): instances.append(DatabaseConnectionPool(host="h", database="d"))
    threads = [threading.Thread(target=get_inst) for _ in range(20)]
    for t in threads: t.start()
    for t in threads: t.join()
    assert all(i is instances[0] for i in instances); ok("thread safety — 20 threads get same instance")
except Exception as e: fail("thread safety — 20 threads get same instance", e)

# ── Summary ───────────────────────────────────────────────────────────────────
total = PASS + FAIL
print(f"\n{'═'*55}")
print(f"RESULTS: {PASS}/{total} passed", "✅" if FAIL == 0 else "❌")
if FAIL > 0:
    print(f"  {FAIL} test(s) FAILED")
print(f"{'═'*55}")
sys.exit(0 if FAIL == 0 else 1)