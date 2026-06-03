"""InMemoryWalletRepository — Assignment 11"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from typing import Optional, List, Dict
from src.models import Wallet
from repositories.interfaces import WalletRepository


class InMemoryWalletRepository(WalletRepository):
    def __init__(self):
        self._storage: Dict[str, Wallet] = {}
        self._user_index: Dict[str, str] = {}  # user_id → wallet_id

    def save(self, wallet: Wallet) -> Wallet:
        self._storage[wallet.wallet_id] = wallet
        self._user_index[wallet.user_id] = wallet.wallet_id
        return wallet

    def find_by_id(self, wallet_id: str) -> Optional[Wallet]:
        return self._storage.get(wallet_id)

    def find_all(self) -> List[Wallet]:
        return list(self._storage.values())

    def delete(self, wallet_id: str) -> bool:
        wallet = self._storage.pop(wallet_id, None)
        if wallet:
            self._user_index.pop(wallet.user_id, None)
            return True
        return False

    def exists(self, wallet_id: str) -> bool:
        return wallet_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    def find_by_user_id(self, user_id: str) -> Optional[Wallet]:
        wallet_id = self._user_index.get(user_id)
        return self._storage.get(wallet_id) if wallet_id else None
