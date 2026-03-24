"""Clientes HTTP hacia microservicios downstream."""

from __future__ import annotations

import os
from typing import Any, Dict, Optional, Tuple

import requests


class MlServiceClient:
    def __init__(self, base_url: str | None = None) -> None:
        self._base = (base_url or os.environ.get("ML_SERVICE_URL", "http://127.0.0.1:8001")).rstrip("/")

    def predict_csv_bytes(self, content: bytes, filename: str = "flows.csv") -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        url = f"{self._base}/predict"
        try:
            r = requests.post(url, files={"file": (filename, content)}, timeout=600)
        except requests.RequestException as ex:
            return None, str(ex)
        if r.status_code >= 400:
            return None, r.text or r.reason
        return r.json(), None


class CaptureServiceClient:
    def __init__(self, base_url: str | None = None) -> None:
        self._base = (base_url or os.environ.get("CAPTURE_SERVICE_URL", "http://127.0.0.1:8002")).rstrip("/")

    def list_interfaces(self) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            r = requests.get(f"{self._base}/interfaces", timeout=60)
        except requests.RequestException as ex:
            return None, str(ex)
        if r.status_code >= 400:
            return None, r.text
        return r.json(), None

    def capture(self, interface: str, seconds: int, use_sudo: bool = True) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            r = requests.post(
                f"{self._base}/capture",
                json={"interface": interface, "seconds": seconds, "use_sudo": use_sudo},
                timeout=seconds + 120,
            )
        except requests.RequestException as ex:
            return None, str(ex)
        if r.status_code >= 400:
            try:
                return None, r.json().get("error", r.text)
            except Exception:
                return None, r.text
        return r.json(), None

    def convert_pcap(self, content: bytes, filename: str) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        try:
            r = requests.post(
                f"{self._base}/convert",
                files={"file": (filename, content)},
                timeout=600,
            )
        except requests.RequestException as ex:
            return None, str(ex)
        if r.status_code >= 400:
            try:
                return None, r.json().get("error", r.text)
            except Exception:
                return None, r.text
        return r.json(), None

    def fetch_csv(self, basename: str) -> Tuple[Optional[bytes], Optional[str]]:
        try:
            r = requests.get(f"{self._base}/artifacts/{basename}/csv", timeout=120)
        except requests.RequestException as ex:
            return None, str(ex)
        if r.status_code >= 400:
            return None, r.text
        return r.content, None

    def archive(self, basename: str) -> Optional[str]:
        try:
            r = requests.post(f"{self._base}/archive", json={"basename": basename}, timeout=60)
        except requests.RequestException as ex:
            return str(ex)
        if r.status_code >= 400:
            try:
                return r.json().get("error", r.text)
            except Exception:
                return r.text
        return None


class NotificationServiceClient:
    def __init__(self, base_url: str | None = None) -> None:
        self._base = (base_url or os.environ.get("NOTIFICATION_SERVICE_URL", "http://127.0.0.1:8003")).rstrip("/")

    def send_sms(self, payload: Dict[str, str]) -> Tuple[Optional[str], Optional[str]]:
        try:
            r = requests.post(f"{self._base}/send", json=payload, timeout=60)
        except requests.RequestException as ex:
            return None, str(ex)
        if r.status_code >= 400:
            try:
                return None, r.json().get("error", r.text)
            except Exception:
                return None, r.text
        return r.json().get("message_sid"), None
