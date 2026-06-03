"""Integration tests for REST API — Assignment 12"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
import json, threading
from http.server import HTTPServer
from urllib.request import urlopen, Request
from urllib.error import HTTPError
from urllib.parse import urlencode
from decimal import Decimal

# Reset repos for test isolation
from repositories.inmemory.user_repository import InMemoryUserRepository
from repositories.inmemory.transaction_repository import InMemoryTransactionRepository
from repositories.inmemory.wallet_repository import InMemoryWalletRepository
import api.app as app_module

app_module.user_repo     = InMemoryUserRepository()
app_module.wallet_repo   = InMemoryWalletRepository()
app_module.txn_repo      = InMemoryTransactionRepository()
from services.user_service import UserService
from services.transaction_service import TransactionService
from services.wallet_service import WalletService
app_module.user_service   = UserService(app_module.user_repo)
app_module.txn_service    = TransactionService(app_module.txn_repo, app_module.user_repo)
app_module.wallet_service = WalletService(app_module.wallet_repo, app_module.user_repo)

PORT = 18765
server = HTTPServer(("127.0.0.1", PORT), app_module.SwiftPayHandler)
t = threading.Thread(target=server.serve_forever); t.daemon = True; t.start()

BASE = f"http://127.0.0.1:{PORT}"
PASS = 0; FAIL = 0

def ok(n): global PASS; PASS+=1; print(f"  ✅ {n}")
def fail(n,e): global FAIL; FAIL+=1; print(f"  ❌ {n}: {e}")

def post(path, data):
    req = Request(BASE+path, json.dumps(data).encode(), {"Content-Type":"application/json"})
    try:
        r = urlopen(req); return json.loads(r.read()), r.status
    except HTTPError as e: return json.loads(e.read()), e.code

def get(path):
    try:
        r = urlopen(BASE+path); return json.loads(r.read()), r.status
    except HTTPError as e: return json.loads(e.read()), e.code

print("\n─── API Integration Tests ───")
try:
    data, code = get("/api/health")
    assert code == 200 and data["status"] == "ok"; ok("GET /api/health returns 200")
except Exception as e: fail("health check", e)

try:
    data, code = post("/api/users", {"name":"Alice","email":"alice@api.com","phone":"+27821111111","password":"Password1!"})
    assert code == 201 and "user" in data; ok("POST /api/users creates user (201)")
except Exception as e: fail("POST /api/users", e)

try:
    data, code = post("/api/users", {"name":"A","email":"bad-email","phone":"+27821111112","password":"Password1!"})
    assert code == 422; ok("POST /api/users returns 422 for invalid email")
except Exception as e: fail("POST /api/users invalid email", e)

try:
    r1, _ = post("/api/users", {"name":"Bob","email":"bob@api.com","phone":"+27822222222","password":"Password1!"})
    user_id = r1["user"]["user_id"]
    data, code = get(f"/api/users/{user_id}")
    assert code == 200 and data["user_id"] == user_id; ok("GET /api/users/{id} returns user")
except Exception as e: fail("GET /api/users/{id}", e)

try:
    data, code = get("/api/users/nonexistent-id")
    assert code == 404; ok("GET /api/users/{id} returns 404 for missing user")
except Exception as e: fail("GET /api/users/{id} 404", e)

try:
    r1, _ = post("/api/users", {"name":"Carol","email":"carol@api.com","phone":"+27823333333","password":"Password1!"})
    uid = r1["user"]["user_id"]
    post("/api/transactions/topup", {"user_id": uid, "amount": 500})
    data, code = get(f"/api/users/{uid}/balance")
    assert code == 200 and data["balance"] == "500.00"; ok("GET /api/users/{id}/balance returns balance")
except Exception as e: fail("GET balance", e)

try:
    r1,_ = post("/api/users", {"name":"Dave","email":"dave@api.com","phone":"+27824444444","password":"Password1!"})
    r2,_ = post("/api/users", {"name":"Eve","email":"eve@api.com","phone":"+27825555555","password":"Password1!"})
    did = r1["user"]["user_id"]
    post("/api/transactions/topup", {"user_id": did, "amount": 300})
    data, code = post("/api/transactions/transfer", {"sender_id": did, "recipient_phone": "+27825555555", "amount": 100})
    assert code == 201 and data["transaction"]["status"] == "COMPLETED"
    bal, _ = get(f"/api/users/{did}/balance")
    assert bal["balance"] == "200.00"; ok("POST /api/transactions/transfer completes successfully")
except Exception as e: fail("POST transfer", e)

try:
    data, code = post("/api/auth/login", {"email":"alice@api.com","password":"Password1!"})
    assert code == 200 and "user_id" in data; ok("POST /api/auth/login returns 200")
except Exception as e: fail("POST /api/auth/login", e)

try:
    data, code = post("/api/auth/login", {"email":"alice@api.com","password":"WrongPass"})
    assert code == 401; ok("POST /api/auth/login returns 401 for wrong password")
except Exception as e: fail("POST /api/auth/login 401", e)

try:
    data, code = get("/api/docs")
    assert code == 200 and "openapi" in data; ok("GET /api/docs returns OpenAPI spec")
except Exception as e: fail("GET /api/docs", e)

server.shutdown()
print(f"\n{'═'*50}\nAPI Tests: {PASS}/{PASS+FAIL} passed {'✅' if FAIL==0 else '❌'}\n{'═'*50}")
