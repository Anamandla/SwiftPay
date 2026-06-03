"""Tests for UserService — Assignment 12"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from decimal import Decimal
from src.models import DuplicateUserError, UserNotFoundError, UserStatus
from repositories.inmemory.user_repository import InMemoryUserRepository
from services.user_service import UserService

PASS = 0; FAIL = 0
def ok(n): global PASS; PASS+=1; print(f"  ✅ {n}")
def fail(n,e): global FAIL; FAIL+=1; print(f"  ❌ {n}: {e}")
def er(exc, fn):
    try: fn(); return False
    except exc: return True
    except: return False

def fresh(): return UserService(InMemoryUserRepository())

print("\n─── UserService Tests ───")
try:
    svc = fresh()
    u = svc.register("Amandla", "amandla@test.com", "+27821234567", "Password123!")
    assert u.name == "Amandla" and u.status == UserStatus.ACTIVE; ok("register creates active user")
except Exception as e: fail("register creates active user", e)

try:
    svc = fresh(); svc.register("Alice","a@t.com","+27821111111","Password1!")
    assert er(DuplicateUserError, lambda: svc.register("Bob","a@t.com","+27829999999","Password1!"))
    ok("duplicate email raises DuplicateUserError")
except Exception as e: fail("duplicate email", e)

try:
    svc = fresh()
    assert er(ValueError, lambda: svc.register("Alice","bad","0827654321","Password1!"))
    ok("invalid email raises ValueError")
except Exception as e: fail("invalid email", e)

try:
    svc = fresh()
    assert er(ValueError, lambda: svc.register("Alice","a@t.com","0827654321","short"))
    ok("short password raises ValueError")
except Exception as e: fail("short password", e)

try:
    svc = fresh(); u = svc.register("Alice","a@t.com","+27821234567","Password1!")
    found = svc.get_by_id(u.user_id)
    assert found.user_id == u.user_id; ok("get_by_id returns user")
except Exception as e: fail("get_by_id", e)

try:
    svc = fresh()
    assert er(UserNotFoundError, lambda: svc.get_by_id("nonexistent"))
    ok("get_by_id raises UserNotFoundError for missing user")
except Exception as e: fail("get_by_id missing", e)

try:
    svc = fresh(); u = svc.register("Alice","a@t.com","+27821234567","Password1!")
    svc.suspend(u.user_id,"admin-1","fraud")
    assert svc.get_by_id(u.user_id).status == UserStatus.SUSPENDED; ok("suspend sets SUSPENDED")
except Exception as e: fail("suspend", e)

try:
    svc = fresh(); u = svc.register("Alice","a@t.com","+27821234567","Password1!")
    svc.suspend(u.user_id,"admin-1","fraud")
    svc.reactivate(u.user_id,"admin-1","cleared")
    assert svc.get_by_id(u.user_id).status == UserStatus.ACTIVE; ok("reactivate sets ACTIVE")
except Exception as e: fail("reactivate", e)

try:
    svc = fresh(); u = svc.register("Old Name","a@t.com","+27821234567","Password1!")
    svc.update_profile(u.user_id, name="New Name")
    assert svc.get_by_id(u.user_id).name == "New Name"; ok("update_profile changes name")
except Exception as e: fail("update_profile", e)

try:
    svc = fresh(); svc.register("Alice","a@t.com","+27821234567","Password1!")
    user = svc.authenticate("a@t.com","Password1!")
    assert user is not None; ok("authenticate returns user on valid credentials")
except Exception as e: fail("authenticate valid", e)

try:
    svc = fresh(); svc.register("Alice","a@t.com","+27821234567","Password1!")
    assert svc.authenticate("a@t.com","WrongPass") is None; ok("authenticate returns None on wrong password")
except Exception as e: fail("authenticate invalid", e)

print(f"\n{'═'*50}\nUserService Tests: {PASS}/{PASS+FAIL} passed {'✅' if FAIL==0 else '❌'}\n{'═'*50}")
