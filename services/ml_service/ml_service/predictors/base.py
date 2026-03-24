from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict


class BaseTrafficPredictor(ABC):
    """Contrato común para modelos de clasificación de tráfico."""

    name: str

    @abstractmethod
    def predict_counts(self, csv_path: Path | str) -> Dict[str, int]:
        """Devuelve conteos por clase (claves LABEL_ORDER / JSON)."""
