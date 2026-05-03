"""
Pattern 1: Simple Factory
─────────────────────────────────────────────────────────────────────────────
Use case: NotificationFactory centralises creation of all Notification types.
Justification: The system creates 5 different notification types (TRANSFER_SENT,
TRANSFER_RECEIVED, BILL_PAID, TOP_UP_SUCCESS, ACCOUNT_SUSPENDED). Rather than
scattering constructor calls with repeated title/body templates throughout the
codebase, a single factory method encapsulates the creation logic.
Linked to: FR-09, US-007
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models import Notification, NotificationType
from decimal import Decimal


class NotificationFactory:
    """
    Simple Factory — centralised Notification object creation.
    Encapsulates all title/body templates for each notification type.
    """

    @staticmethod
    def create(
        notification_type: NotificationType,
        user_id: str,
        fcm_token: str,
        transaction_id: str = None,
        amount: Decimal = None,
        counterparty_name: str = None,
    ) -> Notification:
        """
        Factory method — returns the correct Notification based on type.
        Raises ValueError for unsupported types.
        """
        templates = {
            NotificationType.TRANSFER_SENT: (
                "Transfer Sent",
                f"R{amount} sent to {counterparty_name}. Your new balance has been updated."
            ),
            NotificationType.TRANSFER_RECEIVED: (
                "Money Received",
                f"R{amount} received from {counterparty_name}. Check your balance."
            ),
            NotificationType.BILL_PAID: (
                "Bill Payment Successful",
                f"Your bill payment of R{amount} was processed successfully."
            ),
            NotificationType.TOP_UP_SUCCESS: (
                "Wallet Topped Up",
                f"R{amount} has been added to your SwiftPay wallet."
            ),
            NotificationType.ACCOUNT_SUSPENDED: (
                "Account Suspended",
                "Your SwiftPay account has been suspended. Contact support for assistance."
            ),
        }

        if notification_type not in templates:
            raise ValueError(f"Unsupported notification type: {notification_type}")

        title, body = templates[notification_type]
        return Notification(
            user_id=user_id,
            notification_type=notification_type,
            title=title,
            body=body,
            fcm_token=fcm_token,
            transaction_id=transaction_id,
        )


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    n = NotificationFactory.create(
        NotificationType.TRANSFER_SENT,
        user_id="user-abc",
        fcm_token="fcm-token-xyz",
        transaction_id="txn-001",
        amount=Decimal("150.00"),
        counterparty_name="Sipho Dlamini",
    )
    print(n)