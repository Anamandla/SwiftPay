"""
SwiftPay REST API — Assignment 12
Built with Python's built-in http.server — no external framework required.
Implements full CRUD + business endpoints for User, Transaction, Wallet.
Auto-generates OpenAPI documentation.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import json
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from decimal import Decimal, InvalidOperation

from repositories.factory import RepositoryFactory
from services.user_service import UserService
from services.transaction_service import TransactionService
from services.wallet_service import WalletService
from src.models import DuplicateUserError, UserNotFoundError, InsufficientFundsError, InvalidTransactionError


# ── Dependency Injection via Factory ─────────────────────────────────────────
STORAGE = os.getenv("SWIFTPAY_STORAGE", "MEMORY")

user_repo     = RepositoryFactory.get_user_repository(STORAGE)
wallet_repo   = RepositoryFactory.get_wallet_repository(STORAGE)
txn_repo      = RepositoryFactory.get_transaction_repository(STORAGE)

user_service  = UserService(user_repo)
txn_service   = TransactionService(txn_repo, user_repo)
wallet_service= WalletService(wallet_repo, user_repo)


def json_response(data, status=200):
    return json.dumps(data, default=str), status


class SwiftPayHandler(BaseHTTPRequestHandler):

    def log_message(self, format, *args):
        pass  # suppress default access log

    def _send(self, body: str, status: int = 200):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", len(encoded))
        self.end_headers()
        self.wfile.write(encoded)

    def _read_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def do_GET(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")
        parts  = path.split("/")  # ['', 'api', 'users', ...]

        try:
            # GET /api/users
            if path == "/api/users":
                users = [u.to_dict() for u in user_service.get_all()]
                body, code = json_response({"users": users, "count": len(users)})

            # GET /api/users/{id}
            elif len(parts) == 4 and parts[2] == "users":
                user = user_service.get_by_id(parts[3])
                body, code = json_response(user.to_dict())

            # GET /api/users/{id}/balance
            elif len(parts) == 5 and parts[2] == "users" and parts[4] == "balance":
                balance = wallet_service.get_balance(parts[3])
                body, code = json_response({"user_id": parts[3], "balance": str(balance), "currency": "ZAR"})

            # GET /api/users/{id}/transactions
            elif len(parts) == 5 and parts[2] == "users" and parts[4] == "transactions":
                txns = [t.to_dict() for t in txn_service.get_history(parts[3])]
                body, code = json_response({"transactions": txns, "count": len(txns)})

            # GET /api/transactions
            elif path == "/api/transactions":
                txns = [t.to_dict() for t in txn_service.get_all()]
                body, code = json_response({"transactions": txns, "count": len(txns)})

            # GET /api/transactions/{id}
            elif len(parts) == 4 and parts[2] == "transactions":
                txn = txn_service.get_by_id(parts[3])
                body, code = json_response(txn.to_dict())

            # GET /api/health
            elif path == "/api/health":
                body, code = json_response({
                    "status": "ok", "service": "SwiftPay API",
                    "users": user_service.count(), "transactions": txn_service.count()
                })

            # GET /api/docs
            elif path == "/api/docs":
                body, code = json_response(_openapi_spec())

            else:
                body, code = json_response({"error": "Not found"}, 404)

        except UserNotFoundError as e:
            body, code = json_response({"error": str(e)}, 404)
        except Exception as e:
            body, code = json_response({"error": str(e)}, 500)

        self._send(body, code)

    def do_POST(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")
        parts  = path.split("/")

        try:
            data = self._read_body()

            # POST /api/users  — Register
            if path == "/api/users":
                user = user_service.register(
                    name=data["name"], email=data["email"],
                    phone=data["phone"], password=data["password"]
                )
                body, code = json_response({"message": "User registered.", "user": user.to_dict()}, 201)

            # POST /api/auth/login
            elif path == "/api/auth/login":
                user = user_service.authenticate(data.get("email",""), data.get("password",""))
                if not user:
                    body, code = json_response({"error": "Invalid credentials."}, 401)
                else:
                    body, code = json_response({"message": "Login successful.", "user_id": user.user_id, "name": user.name})

            # POST /api/transactions/transfer
            elif path == "/api/transactions/transfer":
                try:
                    amount = Decimal(str(data["amount"]))
                except (InvalidOperation, KeyError):
                    body, code = json_response({"error": "Invalid amount."}, 422)
                    self._send(body, code); return
                txn = txn_service.transfer(
                    sender_id=data["sender_id"],
                    recipient_phone=data["recipient_phone"],
                    amount=amount
                )
                body, code = json_response({"message": "Transfer successful.", "transaction": txn.to_dict()}, 201)

            # POST /api/transactions/topup
            elif path == "/api/transactions/topup":
                try:
                    amount = Decimal(str(data["amount"]))
                except (InvalidOperation, KeyError):
                    body, code = json_response({"error": "Invalid amount."}, 422)
                    self._send(body, code); return
                txn = txn_service.top_up(user_id=data["user_id"], amount=amount)
                body, code = json_response({"message": "Wallet topped up.", "transaction": txn.to_dict()}, 201)

            # POST /api/users/{id}/suspend
            elif len(parts) == 5 and parts[2] == "users" and parts[4] == "suspend":
                user = user_service.suspend(parts[3], data.get("admin_id","admin"), data.get("reason",""))
                body, code = json_response({"message": "User suspended.", "user": user.to_dict()})

            # POST /api/users/{id}/reactivate
            elif len(parts) == 5 and parts[2] == "users" and parts[4] == "reactivate":
                user = user_service.reactivate(parts[3], data.get("admin_id","admin"), data.get("reason",""))
                body, code = json_response({"message": "User reactivated.", "user": user.to_dict()})

            else:
                body, code = json_response({"error": "Not found"}, 404)

        except (DuplicateUserError, ValueError) as e:
            body, code = json_response({"error": str(e)}, 422)
        except UserNotFoundError as e:
            body, code = json_response({"error": str(e)}, 404)
        except InsufficientFundsError as e:
            body, code = json_response({"error": str(e)}, 422)
        except InvalidTransactionError as e:
            body, code = json_response({"error": str(e)}, 422)
        except KeyError as e:
            body, code = json_response({"error": f"Missing field: {e}"}, 400)
        except Exception as e:
            body, code = json_response({"error": str(e)}, 500)

        self._send(body, code)

    def do_PUT(self):
        parsed = urlparse(self.path)
        path   = parsed.path.rstrip("/")
        parts  = path.split("/")
        try:
            data = self._read_body()
            # PUT /api/users/{id}
            if len(parts) == 4 and parts[2] == "users":
                user = user_service.update_profile(parts[3], name=data.get("name"), phone=data.get("phone"))
                body, code = json_response({"message": "Profile updated.", "user": user.to_dict()})
            else:
                body, code = json_response({"error": "Not found"}, 404)
        except UserNotFoundError as e:
            body, code = json_response({"error": str(e)}, 404)
        except Exception as e:
            body, code = json_response({"error": str(e)}, 500)
        self._send(body, code)


def _openapi_spec() -> dict:
    return {
        "openapi": "3.0.0",
        "info": {"title": "SwiftPay API", "version": "1.0.0",
                 "description": "Mobile payment platform REST API"},
        "servers": [{"url": "http://localhost:8000"}],
        "paths": {
            "/api/health": {"get": {"summary": "Health check", "tags": ["System"],
                "responses": {"200": {"description": "Service healthy"}}}},
            "/api/users": {
                "get":  {"summary": "List all users", "tags": ["Users"],
                    "responses": {"200": {"description": "List of users"}}},
                "post": {"summary": "Register a new user", "tags": ["Users"],
                    "requestBody": {"required": True, "content": {"application/json": {
                        "schema": {"type": "object", "required": ["name","email","phone","password"],
                            "properties": {"name": {"type":"string"}, "email": {"type":"string"},
                                           "phone": {"type":"string"}, "password": {"type":"string"}}}}}},
                    "responses": {"201": {"description": "User created"}, "422": {"description": "Validation error"}}}},
            "/api/users/{id}": {
                "get": {"summary": "Get user by ID", "tags": ["Users"],
                    "responses": {"200": {"description": "User object"}, "404": {"description": "Not found"}}},
                "put": {"summary": "Update user profile", "tags": ["Users"],
                    "responses": {"200": {"description": "Updated"}}}},
            "/api/users/{id}/balance": {"get": {"summary": "Get wallet balance", "tags": ["Wallet"],
                "responses": {"200": {"description": "Balance object"}}}},
            "/api/users/{id}/transactions": {"get": {"summary": "Get transaction history", "tags": ["Transactions"],
                "responses": {"200": {"description": "Transaction list"}}}},
            "/api/auth/login": {"post": {"summary": "Authenticate user", "tags": ["Auth"],
                "responses": {"200": {"description": "Login success"}, "401": {"description": "Invalid credentials"}}}},
            "/api/transactions/transfer": {"post": {"summary": "P2P money transfer", "tags": ["Transactions"],
                "responses": {"201": {"description": "Transfer complete"}, "422": {"description": "Failed"}}}},
            "/api/transactions/topup": {"post": {"summary": "Top up wallet", "tags": ["Transactions"],
                "responses": {"201": {"description": "Top-up complete"}}}},
            "/api/transactions": {"get": {"summary": "List all transactions (admin)", "tags": ["Transactions"],
                "responses": {"200": {"description": "Transaction list"}}}},
        }
    }


def create_app():
    return SwiftPayHandler


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    server = HTTPServer(("0.0.0.0", port), SwiftPayHandler)
    print(f"SwiftPay API running on http://localhost:{port}")
    print(f"OpenAPI docs: http://localhost:{port}/api/docs")
    server.serve_forever()
