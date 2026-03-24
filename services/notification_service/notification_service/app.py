"""API REST para envío de SMS (Twilio)."""

from __future__ import annotations

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.abspath(os.path.join(_ROOT, ".."))
if _PKG not in sys.path:
    sys.path.insert(0, _PKG)

from flask import Flask, jsonify, request

from notification_service.sender import NotificationPayload, TwilioNotificationService

app = Flask(__name__)
_sender = TwilioNotificationService()


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "notification-service"})


@app.post("/send")
def send():
    body = request.get_json(silent=True) or {}
    required = ("account_sid", "auth_token", "from_number", "to_number", "body")
    missing = [k for k in required if not body.get(k)]
    if missing:
        return jsonify({"error": f"Faltan campos: {missing}"}), 400
    payload = NotificationPayload(
        account_sid=body["account_sid"],
        auth_token=body["auth_token"],
        from_number=body["from_number"],
        to_number=body["to_number"],
        body=body["body"],
    )
    try:
        sid = _sender.send_sms(payload)
        return jsonify({"message_sid": sid})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 502


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8003"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
