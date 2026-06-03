"""Tests for repository layer — Assignment 11"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from decimal import Decimal
from src.models import User, Wallet, Transaction, TransactionType, TransactionStatus, DuplicateUserError
from repositories.inmemory.user_repository import InMemoryUserRepository
from repositories.inmemory.wallet_repository import InMemoryWalletRepository
from repositories.inmemory.transaction_repository import InMemoryTransactionRepository
from repositories.factory import RepositoryFactory

PASS = 0; FAIL = 0

def ok(n): global PASS; PASS+=1; print(f"  ✅ {n}")
def fail(n,e): global FAIL; FAIL+=1; print(f"  ❌ {n}: {e}")
def section(t): print(f"\n{'─'*50}\n{t}\n{'─'*50}")

def make_user(name="Alice", email="alice@test.com", phone="+27821000001"):
    u = User(name, email, phone, "hash"); u.activate(); return u

section("UserRepository CRUD")
try:
    repo = InMemoryUserRepository()
    u = make_user(); repo.save(u)
    assert repo.find_by_id(u.user_id) is u; ok("save and find_by_id")
except Exception as e: fail("save and find_by_id", e)

try:
    repo = InMemoryUserRepository()
    u = make_user(); repo.save(u)
    assert repo.count() == 1; repo.delete(u.user_id)
    assert repo.count() == 0; ok("delete removes user")
except Exception as e: fail("delete removes user", e)

try:
    repo = InMemoryUserRepository()
    u = make_user(); repo.save(u)
    found = repo.find_by_email("alice@test.com")
    assert found is u; ok("find_by_email")
except Exception as e: fail("find_by_email", e)

try:
    repo = InMemoryUserRepository()
    u = make_user(); repo.save(u)
    found = repo.find_by_phone("+27821000001")
    assert found is u; ok("find_by_phone")
except Exception as e: fail("find_by_phone", e)

try:
    repo = InMemoryUserRepository()
    u1 = make_user(); repo.save(u1)
    u2 = User("Bob","alice@test.com","+27821000002","h")
    raised = False
    try: repo.save(u2)
    except DuplicateUserError: raised = True
    assert raised; ok("duplicate email raises DuplicateUserError")
except Exception as e: fail("duplicate email raises DuplicateUserError", e)

try:
    repo = InMemoryUserRepository()
    assert repo.find_by_id("nonexistent") is None; ok("find_by_id returns None for missing")
except Exception as e: fail("find_by_id returns None for missing", e)

try:
    repo = InMemoryUserRepository()
    for i in range(3): repo.save(make_user(f"U{i}", f"u{i}@t.com", f"+2782100000{i}"))
    assert len(repo.find_all()) == 3; ok("find_all returns all users")
except Exception as e: fail("find_all returns all users", e)

section("TransactionRepository CRUD")
try:
    repo = InMemoryTransactionRepository()
    t = Transaction("w1", Decimal("100"), TransactionType.TRANSFER, "w2")
    repo.save(t)
    assert repo.find_by_id(t.transaction_id) is t; ok("save and find_by_id")
except Exception as e: fail("save and find_by_id", e)

try:
    repo = InMemoryTransactionRepository()
    t1 = Transaction("w1", Decimal("50"), TransactionType.TRANSFER, "w2")
    t2 = Transaction("w1", Decimal("75"), TransactionType.TOP_UP)
    repo.save(t1); repo.save(t2)
    results = repo.find_by_sender_wallet("w1")
    assert len(results) == 2; ok("find_by_sender_wallet")
except Exception as e: fail("find_by_sender_wallet", e)

try:
    repo = InMemoryTransactionRepository()
    t = Transaction("w1", Decimal("100"), TransactionType.TRANSFER, "w2")
    t.validate(); t.process(); t.pending_gateway(); t.complete("GW-001")
    repo.save(t)
    results = repo.find_by_status(TransactionStatus.COMPLETED)
    assert len(results) == 1; ok("find_by_status")
except Exception as e: fail("find_by_status", e)

try:
    repo = InMemoryTransactionRepository()
    t = Transaction("w-alice", Decimal("100"), TransactionType.TRANSFER, "w-bob")
    repo.save(t)
    assert len(repo.find_by_wallet("w-alice")) == 1
    assert len(repo.find_by_wallet("w-bob")) == 1; ok("find_by_wallet (sender and recipient)")
except Exception as e: fail("find_by_wallet (sender and recipient)", e)

section("RepositoryFactory")
try:
    r = RepositoryFactory.get_user_repository("MEMORY")
    assert isinstance(r, InMemoryUserRepository); ok("factory returns InMemoryUserRepository for MEMORY")
except Exception as e: fail("factory returns correct type", e)

try:
    raised = False
    try: RepositoryFactory.get_user_repository("INVALID")
    except ValueError: raised = True
    assert raised; ok("factory raises ValueError for unknown storage type")
except Exception as e: fail("factory raises ValueError", e)

try:
    r1 = RepositoryFactory.get_user_repository("FILE")
    assert r1 is not None; ok("factory returns FILE stub")
except Exception as e: fail("factory returns FILE stub", e)

print(f"\n{'═'*50}\nRepository Tests: {PASS}/{PASS+FAIL} passed {'✅' if FAIL==0 else '❌'}\n{'═'*50}")
