"""Tests for TransactionService — Assignment 12"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from decimal import Decimal
from src.models import TransactionStatus, TransactionType, InsufficientFundsError, InvalidTransactionError, UserNotFoundError
from repositories.inmemory.user_repository import InMemoryUserRepository
from repositories.inmemory.transaction_repository import InMemoryTransactionRepository
from services.user_service import UserService
from services.transaction_service import TransactionService

PASS = 0; FAIL = 0
def ok(n): global PASS; PASS+=1; print(f"  ✅ {n}")
def fail(n,e): global FAIL; FAIL+=1; print(f"  ❌ {n}: {e}")
def er(exc, fn):
    try: fn(); return False
    except exc: return True
    except: return False

def setup():
    ur = InMemoryUserRepository(); tr = InMemoryTransactionRepository()
    us = UserService(ur); ts = TransactionService(tr, ur)
    alice = us.register("Alice","alice@t.com","+27821111111","Password1!")
    bob   = us.register("Bob","bob@t.com","+27822222222","Password1!")
    ts.top_up(alice.user_id, Decimal("1000.00"))
    return us, ts, alice, bob

print("\n─── TransactionService Tests ───")
try:
    us, ts, alice, bob = setup()
    txn = ts.transfer(alice.user_id, bob.phone, Decimal("200.00"))
    assert txn.status == TransactionStatus.COMPLETED
    assert us.get_by_id(alice.user_id).wallet.balance == Decimal("800.00")
    assert us.get_by_id(bob.user_id).wallet.balance == Decimal("200.00")
    ok("transfer debits sender and credits recipient")
except Exception as e: fail("transfer", e)

try:
    us, ts, alice, bob = setup()
    assert er(InsufficientFundsError, lambda: ts.transfer(alice.user_id, bob.phone, Decimal("9999.00")))
    ok("transfer raises InsufficientFundsError")
except Exception as e: fail("transfer insufficient funds", e)

try:
    us, ts, alice, bob = setup()
    assert er(UserNotFoundError, lambda: ts.transfer(alice.user_id, "+27899999999", Decimal("50.00")))
    ok("transfer raises UserNotFoundError for unknown recipient")
except Exception as e: fail("transfer unknown recipient", e)

try:
    us, ts, alice, bob = setup()
    assert er(ValueError, lambda: ts.transfer(alice.user_id, bob.phone, Decimal("0.00")))
    ok("transfer raises ValueError for zero amount")
except Exception as e: fail("transfer zero amount", e)

try:
    us, ts, alice, bob = setup()
    txn = ts.top_up(alice.user_id, Decimal("500.00"))
    assert txn.status == TransactionStatus.COMPLETED
    assert txn.transaction_type == TransactionType.TOP_UP
    ok("top_up creates completed transaction")
except Exception as e: fail("top_up", e)

try:
    us, ts, alice, bob = setup()
    ts.transfer(alice.user_id, bob.phone, Decimal("100.00"))
    ts.transfer(alice.user_id, bob.phone, Decimal("200.00"))
    history = ts.get_history(alice.user_id)
    # 1 top_up + 2 transfers = 3
    assert len(history) == 3; ok("get_history returns all user transactions")
except Exception as e: fail("get_history", e)

try:
    us, ts, alice, bob = setup()
    us.suspend(alice.user_id, "admin", "test")
    assert er(InvalidTransactionError, lambda: ts.transfer(alice.user_id, bob.phone, Decimal("100.00")))
    ok("suspended sender cannot transfer")
except Exception as e: fail("suspended sender", e)

print(f"\n{'═'*50}\nTransactionService Tests: {PASS}/{PASS+FAIL} passed {'✅' if FAIL==0 else '❌'}\n{'═'*50}")
