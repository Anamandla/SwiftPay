"""
InMemoryUserRepository — Assignment 11
HashMap-backed User storage implementing UserRepository interface.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from typing import Optional, List, Dict
from src.models import User, UserStatus, DuplicateUserError
from repositories.interfaces import UserRepository


class InMemoryUserRepository(UserRepository):
    """
    In-memory HashMap implementation of UserRepository.
    Primary key: user_id (UUID string).
    Secondary indexes: email → user_id, phone → user_id.
    """

    def __init__(self):
        self._storage: Dict[str, User] = {}
        self._email_index: Dict[str, str] = {}   # email → user_id
        self._phone_index: Dict[str, str] = {}   # phone → user_id

    def save(self, user: User) -> User:
        """
        Create or update a User.
        Raises DuplicateUserError if email/phone belongs to a DIFFERENT user.
        """
        existing_by_email = self._email_index.get(user.email)
        if existing_by_email and existing_by_email != user.user_id:
            raise DuplicateUserError(f"Email already registered: {user.email}")

        existing_by_phone = self._phone_index.get(user.phone)
        if existing_by_phone and existing_by_phone != user.user_id:
            raise DuplicateUserError(f"Phone already registered: {user.phone}")

        # Remove old index entries if updating
        if user.user_id in self._storage:
            old = self._storage[user.user_id]
            self._email_index.pop(old.email, None)
            self._phone_index.pop(old.phone, None)

        self._storage[user.user_id] = user
        self._email_index[user.email] = user.user_id
        self._phone_index[user.phone] = user.user_id
        return user

    def find_by_id(self, user_id: str) -> Optional[User]:
        return self._storage.get(user_id)

    def find_all(self) -> List[User]:
        return list(self._storage.values())

    def delete(self, user_id: str) -> bool:
        user = self._storage.pop(user_id, None)
        if user:
            self._email_index.pop(user.email, None)
            self._phone_index.pop(user.phone, None)
            return True
        return False

    def exists(self, user_id: str) -> bool:
        return user_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    def find_by_email(self, email: str) -> Optional[User]:
        user_id = self._email_index.get(email.lower())
        return self._storage.get(user_id) if user_id else None

    def find_by_phone(self, phone: str) -> Optional[User]:
        user_id = self._phone_index.get(phone)
        return self._storage.get(user_id) if user_id else None

    def find_by_status(self, status: str) -> List[User]:
        return [u for u in self._storage.values() if u.status.value == status]
