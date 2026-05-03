"""
Pattern 3: Abstract Factory
─────────────────────────────────────────────────────────────────────────────
Use case: NotificationServiceFactory — creates families of related objects
(push notifier + email sender) for different environments: Production
(Firebase FCM + SendGrid) and Testing (in-memory stubs).
Justification: The system needs to swap out the entire notification stack
between environments without changing domain code. The Abstract Factory
ensures that when a TestingFactory is used, ALL notification objects are
test stubs — preventing accidental real FCM/email calls in unit tests.
Linked to: FR-09, NFR-03 (deployability), US-007
"""

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from abc import ABC, abstractmethod
from typing import List


# ── Abstract Products ─────────────────────────────────────────────────────────

class PushNotifier(ABC):
    """Abstract product A — sends push notifications."""
    @abstractmethod
    def send(self, fcm_token: str, title: str, body: str) -> bool:
        pass

class EmailSender(ABC):
    """Abstract product B — sends transactional emails."""
    @abstractmethod
    def send(self, to_email: str, subject: str, body: str) -> bool:
        pass


# ── Concrete Products — Production ────────────────────────────────────────────

class FCMPushNotifier(PushNotifier):
    """Production: sends via Firebase Cloud Messaging."""

    def __init__(self, api_key: str):
        self._api_key = api_key

    def send(self, fcm_token: str, title: str, body: str) -> bool:
        # In production this would call the FCM HTTP v1 API
        print(f"[FCM] Sending to token={fcm_token[:8]}...: '{title}'")
        return True


class SendGridEmailSender(EmailSender):
    """Production: sends via SendGrid SMTP API."""

    def __init__(self, api_key: str, from_address: str):
        self._api_key = api_key
        self._from_address = from_address

    def send(self, to_email: str, subject: str, body: str) -> bool:
        print(f"[SendGrid] Email to {to_email}: '{subject}'")
        return True


# ── Concrete Products — Testing ───────────────────────────────────────────────

class StubPushNotifier(PushNotifier):
    """Test stub — records calls instead of sending real notifications."""

    def __init__(self):
        self.sent_notifications: List[dict] = []

    def send(self, fcm_token: str, title: str, body: str) -> bool:
        self.sent_notifications.append({"token": fcm_token, "title": title, "body": body})
        return True


class StubEmailSender(EmailSender):
    """Test stub — records emails instead of sending them."""

    def __init__(self):
        self.sent_emails: List[dict] = []

    def send(self, to_email: str, subject: str, body: str) -> bool:
        self.sent_emails.append({"to": to_email, "subject": subject, "body": body})
        return True


# ── Abstract Factory ──────────────────────────────────────────────────────────

class NotificationServiceFactory(ABC):
    """Abstract factory — creates a family of notification-related objects."""

    @abstractmethod
    def create_push_notifier(self) -> PushNotifier:
        pass

    @abstractmethod
    def create_email_sender(self) -> EmailSender:
        pass


# ── Concrete Factories ────────────────────────────────────────────────────────

class ProductionNotificationFactory(NotificationServiceFactory):
    """Creates real FCM + SendGrid instances for production."""

    def __init__(self, fcm_api_key: str, sendgrid_api_key: str, from_email: str):
        self._fcm_key = fcm_api_key
        self._sg_key = sendgrid_api_key
        self._from_email = from_email

    def create_push_notifier(self) -> PushNotifier:
        return FCMPushNotifier(api_key=self._fcm_key)

    def create_email_sender(self) -> EmailSender:
        return SendGridEmailSender(api_key=self._sg_key, from_address=self._from_email)


class TestingNotificationFactory(NotificationServiceFactory):
    """Creates in-memory stubs for unit/integration tests."""

    def create_push_notifier(self) -> StubPushNotifier:
        return StubPushNotifier()

    def create_email_sender(self) -> StubEmailSender:
        return StubEmailSender()


# ── Demo ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    factory = TestingNotificationFactory()
    push = factory.create_push_notifier()
    email = factory.create_email_sender()
    push.send("token-abc", "Transfer Sent", "R150 sent to Sipho")
    email.send("user@example.com", "Transfer Alert", "R150 was debited from your wallet")
    print("Push calls:", push.sent_notifications)
    print("Email calls:", email.sent_emails)