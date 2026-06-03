"""InMemoryTransactionRepository — Assignment 11"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))
from typing import Optional, List, Dict
from src.models import Transaction, TransactionStatus, TransactionType
from repositories.interfaces import TransactionRepository


class InMemoryTransactionRepository(TransactionRepository):
    def __init__(self):
        self._storage: Dict[str, Transaction] = {}

    def save(self, txn: Transaction) -> Transaction:
        self._storage[txn.transaction_id] = txn
        return txn

    def find_by_id(self, txn_id: str) -> Optional[Transaction]:
        return self._storage.get(txn_id)

    def find_all(self) -> List[Transaction]:
        return list(self._storage.values())

    def delete(self, txn_id: str) -> bool:
        return self._storage.pop(txn_id, None) is not None

    def exists(self, txn_id: str) -> bool:
        return txn_id in self._storage

    def count(self) -> int:
        return len(self._storage)

    def find_by_sender_wallet(self, wallet_id: str) -> List[Transaction]:
        return [t for t in self._storage.values() if t.sender_wallet_id == wallet_id]

    def find_by_recipient_wallet(self, wallet_id: str) -> List[Transaction]:
        return [t for t in self._storage.values() if t.recipient_wallet_id == wallet_id]

    def find_by_status(self, status: TransactionStatus) -> List[Transaction]:
        return [t for t in self._storage.values() if t.status == status]

    def find_by_type(self, txn_type: TransactionType) -> List[Transaction]:
        return [t for t in self._storage.values() if t.transaction_type == txn_type]

    def find_by_wallet(self, wallet_id: str) -> List[Transaction]:
        return [t for t in self._storage.values()
                if t.sender_wallet_id == wallet_id or t.recipient_wallet_id == wallet_id]
