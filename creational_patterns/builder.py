"""
Pattern 4: Builder
─────────────────────────────────────────────────────────────────────────────
Use case: UserBuilder — constructs User objects step-by-step.
Justification: User creation has many optional fields (device_info, referral
code, initial top-up amount, admin-set status) plus mandatory validation
across multiple fields. A builder enforces the construction sequence,
validates each step, and prevents partially-constructed User objects from
being used before they are ready.
Linked to: FR-01, UC-01, US-001
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import hashlib
import re
from src.models import User, UserStatus
from decimal import Decimal


class UserBuilder:
    """
    Builder for User objects.
    Enforces mandatory fields and validates format before build().
    """

    def __init__(self):
        self._name: str = None
        self._email: str = None
        self._phone: str = None
        self._password: str = None
        self._auto_activate: bool = False
        self._initial_credit: Decimal = Decimal("0.00")

    def set_name(self, name: str) -> "UserBuilder":
        name = name.strip()
        if len(name) < 2:
            raise ValueError("Name must be at least 2 characters.")
        self._name = name
        return self

    def set_email(self, email: str) -> "UserBuilder":
        email = email.strip().lower()
        if not re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$", email):
            raise ValueError(f"Invalid email format: {email}")
        self._email = email
        return self

    def set_phone(self, phone: str) -> "UserBuilder":
        phone = re.sub(r"\s+", "", phone)
        if not re.match(r"^\+?[0-9]{10,13}$", phone):
            raise ValueError(f"Invalid phone format: {phone}")
        self._phone = phone
        return self

    def set_password(self, password: str) -> "UserBuilder":
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")
        self._password = password
        return self

    def set_auto_activate(self, activate: bool = True) -> "UserBuilder":
        """If True, user is activated immediately (e.g. for tests/admin creation)."""
        self._auto_activate = activate
        return self

    def set_initial_credit(self, amount: Decimal) -> "UserBuilder":
        """Optional initial wallet credit (e.g. welcome bonus)."""
        if amount < Decimal("0.00"):
            raise ValueError("Initial credit cannot be negative.")
        self._initial_credit = amount
        return self

    def build(self) -> User:
        """Validates all mandatory fields then constructs the User."""
        missing = [f for f, v in [
            ("name", self._name),
            ("email", self._email),
            ("phone", self._phone),
            ("password", self._password),
        ] if v is None]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        password_hash = hashlib.sha256(self._password.encode()).hexdigest()
        user = User(
            name=self._name,
            email=self._email,
            phone=self._phone,
            password_hash=password_hash,
        )
        if self._auto_activate:
            user.activate()
        if self._initial_credit > Decimal("0.00"):
            user.get_wallet().credit(self._initial_credit)
        return user


# ── Director (optional convenience wrapper) ───────────────────────────────────

class UserDirector:
    """Director — constructs common User configurations."""

    @staticmethod
    def build_standard_user(name: str, email: str, phone: str, password: str) -> User:
        return (UserBuilder()
                .set_name(name)
                .set_email(email)
                .set_phone(phone)
                .set_password(password)
                .build())

    @staticmethod
    def build_activated_test_user(name: str, email: str, phone: str) -> User:
        """Pre-activated user with R1000 wallet credit for testing."""
        return (UserBuilder()
                .set_name(name)
                .set_email(email)
                .set_phone(phone)
                .set_password("TestPass123!")
                .set_auto_activate(True)
                .set_initial_credit(Decimal("1000.00"))
                .build())


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    user = (UserBuilder()
            .set_name("Amandla Dlamini")
            .set_email("amandla@example.com")
            .set_phone("+27821234567")
            .set_password("SecurePass99!")
            .set_auto_activate(True)
            .set_initial_credit(Decimal("500.00"))
            .build())
    print(user)
    print(f"Wallet balance: R{user.wallet.balance}")