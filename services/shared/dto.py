"""DTOs simples (dict-friendly) para respuestas entre servicios."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict

from shared.constants import LABEL_ORDER


def _empty_counts() -> Dict[str, int]:
    return {k: 0 for k in LABEL_ORDER}


@dataclass
class ModelPredictionResult:
    model: str
    counts: Dict[str, int] = field(default_factory=_empty_counts)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class CombinedPredictionResponse:
    cnn: ModelPredictionResult
    dnn: ModelPredictionResult

    def to_dict(self) -> Dict[str, Any]:
        return {"cnn": self.cnn.to_dict(), "dnn": self.dnn.to_dict()}
