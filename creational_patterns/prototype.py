"""
Pattern 5: Prototype
─────────────────────────────────────────────────────────────────────────────
Use case: TransactionPrototypeCache — stores pre-configured Transaction
templates (transfer, top-up, bill payment) and clones them on demand.
Justification: Creating a Transaction with correct defaults (currency, type,
status) is repetitive. The prototype pattern stores validated template
instances and produces deep-copied clones, guaranteeing each transaction
starts from a known-good state without re-running validation logic.
Linked to: FR-07, FR-06, FR-10, US-006, US-008, US-009
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import copy
import uuid
from decimal import Decimal
from src.models import Transaction, TransactionType


class TransactionPrototype:
    """
    Wrapper that makes Transaction cloneable.
    Each clone gets a fresh transaction_id and reset timestamps.
    """

    def __init__(self, transaction: Transaction):
        self._template = transaction

    def clone(self, sender_wallet_id: str, amount: Decimal,
              recipient_wallet_id: str = None) -> Transaction:
        """
        Deep-clone the template and override identity fields.
        This ensures the new Transaction is independent of the template.
        """
        cloned = copy.deepcopy(self._template)
        # Override identity and variable fields
        cloned._transaction_id = str(uuid.uuid4())
        cloned._sender_wallet_id = sender_wallet_id
        cloned._amount = amount
        if recipient_wallet_id:
            cloned._recipient_wallet_id = recipient_wallet_id
        from datetime import datetime
        cloned._created_at = datetime.utcnow()
        cloned._completed_at = None
        cloned._gateway_reference = None
        cloned._failure_reason = None
        return cloned


class TransactionPrototypeCache:
    """
    Prototype cache — stores named Transaction templates.
    Cloning is O(1) lookup + deep copy vs full construction + validation.
    """

    def __init__(self):
        self._cache: dict[str, TransactionPrototype] = {}
        self._load_defaults()

    def _load_defaults(self) -> None:
        """Pre-load standard transaction templates."""
        transfer_template = Transaction(
            sender_wallet_id="template",
            amount=Decimal("0.00"),
            transaction_type=TransactionType.TRANSFER,
            recipient_wallet_id="template",
            currency="ZAR",
        )
        topup_template = Transaction(
            sender_wallet_id="template",
            amount=Decimal("0.00"),
            transaction_type=TransactionType.TOP_UP,
            currency="ZAR",
        )
        bill_template = Transaction(
            sender_wallet_id="template",
            amount=Decimal("0.00"),
            transaction_type=TransactionType.BILL_PAYMENT,
            currency="ZAR",
        )
        self._cache["transfer"] = TransactionPrototype(transfer_template)
        self._cache["top_up"] = TransactionPrototype(topup_template)
        self._cache["bill_payment"] = TransactionPrototype(bill_template)

    def get(self, key: str, sender_wallet_id: str, amount: Decimal,
            recipient_wallet_id: str = None) -> Transaction:
        """Retrieve and clone a template by key."""
        if key not in self._cache:
            raise KeyError(f"No transaction prototype found for key: '{key}'")
        return self._cache[key].clone(
            sender_wallet_id=sender_wallet_id,
            amount=amount,
            recipient_wallet_id=recipient_wallet_id,
        )

    def register(self, key: str, transaction: Transaction) -> None:
        """Register a custom template."""
        self._cache[key] = TransactionPrototype(transaction)


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    cache = TransactionPrototypeCache()
    t1 = cache.get("transfer", sender_wallet_id="wallet-a", amount=Decimal("250.00"),
                   recipient_wallet_id="wallet-b")
    t2 = cache.get("transfer", sender_wallet_id="wallet-c", amount=Decimal("75.00"),
                   recipient_wallet_id="wallet-d")
    print(t1)
    print(t2)
    print("Same instance?", t1 is t2)             # False
    print("Same type?", t1.transaction_type == t2.transaction_type)  # True