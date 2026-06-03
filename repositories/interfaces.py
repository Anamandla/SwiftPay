"""
Entity-Specific Repository Interfaces — Assignment 11
Each interface extends the generic Repository with domain-specific query methods.
"""
from abc import abstractmethod
from typing import Optional, List
from repositories.base import Repository
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.models import User, Wallet, Transaction, TransactionStatus, TransactionType


class UserRepository(Repository["User", str]):
    """User-specific repository — adds email/phone lookup."""

    @abstractmethod
    def find_by_email(self, email: str) -> Optional["User"]:
        pass

    @abstractmethod
    def find_by_phone(self, phone: str) -> Optional["User"]:
        pass

    @abstractmethod
    def find_by_status(self, status: str) -> List["User"]:
        pass


class WalletRepository(Repository["Wallet", str]):
    """Wallet-specific repository — adds user-based lookup."""

    @abstractmethod
    def find_by_user_id(self, user_id: str) -> Optional["Wallet"]:
        pass


class TransactionRepository(Repository["Transaction", str]):
    """Transaction-specific repository — adds rich query methods."""

    @abstractmethod
    def find_by_sender_wallet(self, wallet_id: str) -> List["Transaction"]:
        pass

    @abstractmethod
    def find_by_recipient_wallet(self, wallet_id: str) -> List["Transaction"]:
        pass

    @abstractmethod
    def find_by_status(self, status: "TransactionStatus") -> List["Transaction"]:
        pass

    @abstractmethod
    def find_by_type(self, txn_type: "TransactionType") -> List["Transaction"]:
        pass

    @abstractmethod
    def find_by_wallet(self, wallet_id: str) -> List["Transaction"]:
        """Return all transactions where wallet is sender OR recipient."""
        pass
