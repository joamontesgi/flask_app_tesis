"""Cliente Twilio encapsulado."""

from __future__ import annotations

from dataclasses import dataclass

from twilio.rest import Client


@dataclass
class NotificationPayload:
    account_sid: str
    auth_token: str
    from_number: str
    to_number: str
    body: str


class TwilioNotificationService:
    def send_sms(self, payload: NotificationPayload) -> str:
        client = Client(payload.account_sid, payload.auth_token)
        msg = client.messages.create(
            body=payload.body,
            from_=payload.from_number,
            to=payload.to_number,
        )
        return str(msg.sid)
