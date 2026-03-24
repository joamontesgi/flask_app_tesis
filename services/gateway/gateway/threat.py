"""Detección de amenaza a partir de conteos (misma lógica que el demonio original CNN)."""

from __future__ import annotations

from typing import Any, Dict

_THREAT_KEYS = ("ddos", "dos_goldeneye", "dos_hulk", "dos_slowhttptest", "dos_slowloris")


def cnn_threat_score(counts: Dict[str, Any]) -> int:
    return sum(int(counts.get(k, 0) or 0) for k in _THREAT_KEYS)


def is_attack_prediction(prediction: Dict[str, Any]) -> bool:
    cnn = prediction.get("cnn") or {}
    counts = cnn.get("counts") or {}
    return cnn_threat_score(counts) > 0
