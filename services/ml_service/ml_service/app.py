"""API REST del microservicio ML (CNN + DNN)."""

from __future__ import annotations

import os
import sys

# Permite `python ml_service/app.py` desde services/ml_service con shared en path
_SERVICE_ROOT = os.path.dirname(os.path.abspath(__file__))
_ML_ROOT = os.path.abspath(os.path.join(_SERVICE_ROOT, ".."))
_SERVICES_ROOT = os.path.abspath(os.path.join(_SERVICE_ROOT, "..", ".."))
for p in (_SERVICES_ROOT, _ML_ROOT):
    if p not in sys.path:
        sys.path.insert(0, p)

from flask import Flask, jsonify, request

from ml_service.inference_service import TrafficInferenceService

app = Flask(__name__)
_inference: TrafficInferenceService | None = None


def get_inference() -> TrafficInferenceService:
    global _inference
    if _inference is None:
        _inference = TrafficInferenceService()
    return _inference


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "ml-service"})


@app.post("/predict")
def predict():
    if "file" not in request.files:
        return jsonify({"error": "Campo multipart 'file' requerido (CSV)."}), 400
    f = request.files["file"]
    if not f.filename:
        return jsonify({"error": "Nombre de archivo vacío."}), 400
    result = get_inference().predict_upload(f)
    return jsonify(result.to_dict())


def create_app() -> Flask:
    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8001"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
