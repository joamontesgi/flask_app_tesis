"""Orquesta la inferencia de varios modelos sobre un CSV."""

from __future__ import annotations

import os
import tempfile
from pathlib import Path
from typing import BinaryIO

from werkzeug.datastructures import FileStorage

from ml_service.predictors import CNNPredictor, DNNPredictor
from ml_service.predictors.base import BaseTrafficPredictor
from shared.dto import CombinedPredictionResponse, ModelPredictionResult


def _default_model_paths() -> tuple[Path, Path]:
    root = Path(__file__).resolve().parents[3]
    base = Path(os.environ.get("MODEL_BASE_DIR", str(root / "models")))
    cnn = Path(os.environ.get("CNN_MODEL_PATH", str(base / "cnn.h5")))
    dnn = Path(os.environ.get("DNN_MODEL_PATH", str(base / "redneuronal4.h5")))
    return cnn, dnn


class TrafficInferenceService:
    def __init__(
        self,
        predictors: list[BaseTrafficPredictor] | None = None,
    ) -> None:
        if predictors is None:
            cnn_p, dnn_p = _default_model_paths()
            predictors = [CNNPredictor(cnn_p), DNNPredictor(dnn_p)]
        self._predictors = {p.name: p for p in predictors}

    def predict_upload(self, file_storage: FileStorage) -> CombinedPredictionResponse:
        suffix = Path(file_storage.filename or "upload.csv").suffix or ".csv"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(file_storage.read())
            tmp_path = Path(tmp.name)
        try:
            return self.predict_path(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)

    def predict_path(self, csv_path: Path | str) -> CombinedPredictionResponse:
        path = Path(csv_path)
        cnn_counts = self._predictors["cnn"].predict_counts(path)
        dnn_counts = self._predictors["dnn"].predict_counts(path)
        return CombinedPredictionResponse(
            cnn=ModelPredictionResult(model="cnn", counts=cnn_counts),
            dnn=ModelPredictionResult(model="dnn", counts=dnn_counts),
        )

    def predict_stream(self, stream: BinaryIO, filename: str = "upload.csv") -> CombinedPredictionResponse:
        storage = FileStorage(stream=stream, filename=filename)
        return self.predict_upload(storage)
