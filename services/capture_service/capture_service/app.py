"""API REST: interfaces, captura PCAP y conversión a CSV."""

from __future__ import annotations

import os
import sys

_ROOT = os.path.dirname(os.path.abspath(__file__))
_PKG = os.path.abspath(os.path.join(_ROOT, ".."))
if _PKG not in sys.path:
    sys.path.insert(0, _PKG)

from flask import Flask, jsonify, request, send_file

from capture_service.network import NetworkInterfaceLister
from capture_service.pipeline import TrafficCapturePipeline, resolve_workspace

app = Flask(__name__)


def get_pipeline() -> TrafficCapturePipeline:
    w, c = resolve_workspace()
    return TrafficCapturePipeline(w, c)


@app.get("/health")
def health():
    return jsonify({"status": "ok", "service": "capture-service"})


@app.get("/interfaces")
def interfaces():
    names = NetworkInterfaceLister().list_interfaces()
    return jsonify({"interfaces": names})


@app.post("/capture")
def capture():
    body = request.get_json(silent=True) or {}
    iface = body.get("interface") or request.form.get("interface")
    seconds = int(body.get("seconds", request.form.get("seconds", 30)))
    use_sudo = str(body.get("use_sudo", "true")).lower() in ("1", "true", "yes")
    if not iface:
        return jsonify({"error": "Parámetro 'interface' requerido."}), 400
    try:
        art = get_pipeline().capture_and_export_flows(iface, seconds, use_sudo=use_sudo)
        return jsonify(
            {
                "basename": art.basename,
                "pcap_path": art.pcap_path,
                "csv_path": art.csv_path,
            }
        )
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


@app.post("/convert")
def convert():
    if "file" not in request.files:
        return jsonify({"error": "Campo 'file' (pcap) requerido."}), 400
    f = request.files["file"]
    try:
        art = get_pipeline().convert_uploaded_pcap(f.stream, f.filename or "upload.pcap")
        return jsonify(
            {
                "basename": art.basename,
                "pcap_path": art.pcap_path,
                "csv_path": art.csv_path,
            }
        )
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


@app.get("/artifacts/<basename>/csv")
def download_csv(basename):
    p = get_pipeline()
    try:
        path = p.csv_path(basename)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    if not path.is_file():
        return jsonify({"error": "CSV no encontrado"}), 404
    return send_file(path, as_attachment=True, download_name=f"{basename}.csv")


@app.post("/archive")
def archive():
    body = request.get_json(silent=True) or {}
    basename = body.get("basename")
    if not basename:
        return jsonify({"error": "basename requerido"}), 400
    try:
        get_pipeline().archive_basename(basename)
        return jsonify({"ok": True})
    except Exception as ex:
        return jsonify({"error": str(ex)}), 400


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8002"))
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_DEBUG") == "1")
