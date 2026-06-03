"""WalletService — Assignment 12"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from decimal import Decimal
from src.models import Wallet, UserNotFoundError
from repositories.interfaces import WalletRepository, UserRepository


class WalletService:
    def __init__(self, wallet_repo: WalletRepository, user_repo: UserRepository):
        self._wallet_repo = wallet_repo
        self._user_repo = user_repo

    def get_balance(self, user_id: str) -> Decimal:
        user = self._user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")
        return user.wallet.get_balance()

    def get_wallet(self, user_id: str) -> Wallet:
        user = self._user_repo.find_by_id(user_id)
        if not user:
            raise UserNotFoundError(f"User not found: {user_id}")
        return user.wallet
