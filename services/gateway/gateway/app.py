"""Gateway HTTP: CORS, agregación y orquestación para el SPA."""

from __future__ import annotations

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.abspath(os.path.join(_ROOT, ".."))
if _PKG not in sys.path:
    sys.path.insert(0, _PKG)

from flask import Flask, jsonify, request
from flask_cors import CORS

from gateway.clients import CaptureServiceClient, MlServiceClient, NotificationServiceClient
from gateway.monitor import MonitorConfig, MonitorOrchestrator

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": os.environ.get("CORS_ORIGINS", "*")}})

_ml = MlServiceClient()
_capture = CaptureServiceClient()


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "gateway"})


@app.get("/api/v1/interfaces")
def interfaces():
    data, err = _capture.list_interfaces()
    if err:
        return jsonify({"error": err}), 502
    return jsonify(data)


@app.post("/api/v1/predict")
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Sube un CSV en el campo 'file'."}), 400
    f = request.files["file"]
    content = f.read()
    pred, err = _ml.predict_csv_bytes(content, f.filename or "upload.csv")
    if err:
        return jsonify({"error": err}), 502
    return jsonify(pred)


@app.post("/api/v1/capture")
def capture():
    body = request.get_json(silent=True) or {}
    iface = body.get("interface")
    seconds = int(body.get("seconds", 30))
    use_sudo = bool(body.get("use_sudo", True))
    if not iface:
        return jsonify({"error": "interface requerido"}), 400
    data, err = _capture.capture(iface, seconds, use_sudo)
    if err:
        return jsonify({"error": err}), 502
    return jsonify(data)


@app.post("/api/v1/convert")
def convert():
    if "file" not in request.files:
        return jsonify({"error": "Campo 'file' (pcap) requerido."}), 400
    f = request.files["file"]
    data, err = _capture.convert_pcap(f.read(), f.filename or "upload.pcap")
    if err:
        return jsonify({"error": err}), 502
    return jsonify(data)


@app.post("/api/v1/monitor/run")
def monitor_run():
    body = request.get_json(silent=True) or {}
    try:
        cfg = MonitorConfig(
            interface=body["interface"],
            seconds_per_capture=int(body.get("seconds_per_capture", 30)),
            max_cycles=int(body.get("max_cycles", 500)),
            use_sudo=bool(body.get("use_sudo", True)),
            twilio_account_sid=body["twilio_account_sid"],
            twilio_auth_token=body["twilio_auth_token"],
            twilio_from=body["twilio_from"],
            twilio_to=body["twilio_to"],
            alert_message=body.get("alert_message", "Posible ataque DDoS detectado."),
        )
    except KeyError as e:
        return jsonify({"error": f"Falta el campo {e}"}), 400
    orch = MonitorOrchestrator()
    result, err = orch.run_until_threat(cfg)
    if err:
        return jsonify({"error": err}), 502
    return jsonify(result)


def create_app() -> Flask:
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
