"""
Pattern 2: Factory Method
─────────────────────────────────────────────────────────────────────────────
Use case: PaymentProcessor — abstract base class with factory method
`create_transaction()`. Concrete subclasses (TransferProcessor,
TopUpProcessor, BillPaymentProcessor) decide which Transaction variant to
instantiate and how to validate inputs.
Justification: Each payment type has different validation rules and required
fields. Delegating instantiation to subclasses keeps each processor focused
on its own domain logic without a monolithic if/else chain.
Linked to: FR-07, FR-06, FR-10, US-006, US-008, US-009
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from abc import ABC, abstractmethod
from decimal import Decimal
from src.models import Transaction, TransactionType, Wallet, InsufficientFundsError


class PaymentProcessor(ABC):
    """Abstract base — defines the factory method contract."""

    @abstractmethod
    def create_transaction(self, sender_wallet: Wallet, amount: Decimal, **kwargs) -> Transaction:
        """Factory method — subclasses instantiate the correct Transaction."""
        pass

    def process(self, sender_wallet: Wallet, amount: Decimal, **kwargs) -> Transaction:
        """Template method — validates then delegates to factory method."""
        if amount <= Decimal("0.00"):
            raise ValueError("Amount must be greater than R0.00.")
        txn = self.create_transaction(sender_wallet, amount, **kwargs)
        txn.validate()
        return txn


class TransferProcessor(PaymentProcessor):
    """Handles P2P transfers. Requires recipient_wallet_id."""

    def create_transaction(self, sender_wallet: Wallet, amount: Decimal, **kwargs) -> Transaction:
        recipient_wallet_id = kwargs.get("recipient_wallet_id")
        if not recipient_wallet_id:
            raise ValueError("TransferProcessor requires recipient_wallet_id.")
        if not sender_wallet.validate_sufficient_funds(amount):
            raise InsufficientFundsError(
                f"Insufficient funds. Balance: R{sender_wallet.balance}, Required: R{amount}"
            )
        return Transaction(
            sender_wallet_id=sender_wallet.wallet_id,
            amount=amount,
            transaction_type=TransactionType.TRANSFER,
            recipient_wallet_id=recipient_wallet_id,
        )


class TopUpProcessor(PaymentProcessor):
    """Handles wallet top-ups from external card payments."""

    def create_transaction(self, sender_wallet: Wallet, amount: Decimal, **kwargs) -> Transaction:
        # Top-ups credit the wallet — no balance check needed
        return Transaction(
            sender_wallet_id=sender_wallet.wallet_id,
            amount=amount,
            transaction_type=TransactionType.TOP_UP,
        )


class BillPaymentProcessor(PaymentProcessor):
    """Handles bill payments. Requires provider_id and reference."""

    def create_transaction(self, sender_wallet: Wallet, amount: Decimal, **kwargs) -> Transaction:
        provider_id = kwargs.get("provider_id")
        reference = kwargs.get("reference")
        if not provider_id or not reference:
            raise ValueError("BillPaymentProcessor requires provider_id and reference.")
        if not sender_wallet.validate_sufficient_funds(amount):
            raise InsufficientFundsError(
                f"Insufficient funds. Balance: R{sender_wallet.balance}, Required: R{amount}"
            )
        txn = Transaction(
            sender_wallet_id=sender_wallet.wallet_id,
            amount=amount,
            transaction_type=TransactionType.BILL_PAYMENT,
        )
        # Store provider metadata as a reference on the transaction
        txn._gateway_reference = f"{provider_id}:{reference}"
        return txn


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    from src.models import Wallet
    w = Wallet(user_id="user-1")
    w.credit(Decimal("500.00"))

    processor = TransferProcessor()
    txn = processor.process(w, Decimal("100.00"), recipient_wallet_id="wallet-recipient")
    print(txn)