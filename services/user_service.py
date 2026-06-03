"""
UserService — Assignment 12
Business logic for user registration, authentication, and account management.
Uses UserRepository for persistence (Dependency Injection).
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import hashlib
import re
from typing import Optional, List
from src.models import User, UserStatus, DuplicateUserError, UserNotFoundError
from repositories.interfaces import UserRepository


class UserService:
    def __init__(self, user_repo: UserRepository):
        self._repo = user_repo  # DI — any UserRepository implementation

    def register(self, name: str, email: str, phone: str, password: str) -> User:
        email = email.strip().lower()
        if not re.match(r"^[\w\.\+\-]+@[\w\-]+\.[a-z]{2,}$", email):
            raise ValueError(f"Invalid email: {email}")
        if not re.match(r"^\+?[0-9]{10,13}$", re.sub(r"\s+", "", phone)):
            raise ValueError(f"Invalid phone: {phone}")
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters.")
        if len(name.strip()) < 2:
            raise ValueError("Name must be at least 2 characters.")
        if self._repo.find_by_email(email):
            raise DuplicateUserError(f"Email already registered: {email}")
        if self._repo.find_by_phone(phone):
            raise DuplicateUserError(f"Phone already registered: {phone}")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User(name=name.strip(), email=email, phone=phone, password_hash=password_hash)
        user.activate()   # auto-activate for MVP (email verify = future sprint)
        return self._repo.save(user)

    def get_by_id(self, user_id: str) -> User:
        user = self._repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")
        return user

    def get_by_email(self, email: str) -> Optional[User]:
        return self._repo.find_by_email(email.lower())

    def get_all(self) -> List[User]:
        return self._repo.find_all()

    def suspend(self, user_id: str, admin_id: str, reason: str) -> User:
        user = self.get_by_id(user_id)
        if user.status == UserStatus.SUSPENDED:
            raise ValueError("User is already suspended.")
        user.suspend()
        return self._repo.save(user)

    def reactivate(self, user_id: str, admin_id: str, reason: str) -> User:
        user = self.get_by_id(user_id)
        if user.status != UserStatus.SUSPENDED:
            raise ValueError("User is not suspended.")
        user.reactivate()
        return self._repo.save(user)

    def update_profile(self, user_id: str, name: str = None, phone: str = None) -> User:
        user = self.get_by_id(user_id)
        user.update_profile(name=name, phone=phone)
        return self._repo.save(user)

    def authenticate(self, email: str, password: str) -> Optional[User]:
        user = self._repo.find_by_email(email.lower())
        if not user:
            return None
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        if user.password_hash != password_hash:
            return None
        if user.status != UserStatus.ACTIVE:
            return None
        return user

    def count(self) -> int:
        return self._repo.count()
