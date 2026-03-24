"""Orquestación del modo monitoreo continuo (captura → ML → alerta)."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, Optional, Tuple

from gateway.clients import CaptureServiceClient, MlServiceClient, NotificationServiceClient
from gateway.threat import is_attack_prediction


@dataclass
class MonitorConfig:
    interface: str
    seconds_per_capture: int
    max_cycles: int
    use_sudo: bool
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_from: str
    twilio_to: str
    alert_message: str


class MonitorOrchestrator:
    def __init__(
        self,
        capture: CaptureServiceClient | None = None,
        ml: MlServiceClient | None = None,
        notify: NotificationServiceClient | None = None,
    ) -> None:
        self._capture = capture or CaptureServiceClient()
        self._ml = ml or MlServiceClient()
        self._notify = notify or NotificationServiceClient()

    def run_until_threat(
        self,
        cfg: MonitorConfig,
        on_cycle: Optional[Callable[[str], None]] = None,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        started = datetime.now().strftime("%Y-%m-%d")
        for i in range(cfg.max_cycles):
            if on_cycle:
                on_cycle(f"Ciclo {i + 1}/{cfg.max_cycles}: capturando...")
            cap, err = self._capture.capture(cfg.interface, cfg.seconds_per_capture, cfg.use_sudo)
            if err or not cap:
                return None, err or "Fallo en captura"
            basename = cap.get("basename")
            if not basename:
                return None, "Respuesta de captura sin basename"
            csv_bytes, err = self._capture.fetch_csv(basename)
            if err or csv_bytes is None:
                return None, err or "No se pudo leer el CSV"
            pred, err = self._ml.predict_csv_bytes(csv_bytes, f"{basename}.csv")
            if err or pred is None:
                return None, err or "Fallo en predicción"
            if is_attack_prediction(pred):
                payload = {
                    "account_sid": cfg.twilio_account_sid,
                    "auth_token": cfg.twilio_auth_token,
                    "from_number": cfg.twilio_from,
                    "to_number": cfg.twilio_to,
                    "body": cfg.alert_message,
                }
                _, nerr = self._notify.send_sms(payload)
                if nerr:
                    return None, nerr
                arc_err = self._capture.archive(basename)
                if arc_err:
                    return None, arc_err
                return {"fecha": started, "prediction": pred, "basename": basename}, None
            arc_err = self._capture.archive(basename)
            if arc_err:
                return None, arc_err
        return None, "Sin detección tras el número máximo de ciclos"
