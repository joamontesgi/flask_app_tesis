from __future__ import annotations

from pathlib import Path

import keras
import numpy as np

from ml_service.predictors._dataframe import counts_from_predictions, load_and_prepare_frame, make_label_encoder
from ml_service.predictors.base import BaseTrafficPredictor


class CNNPredictor(BaseTrafficPredictor):
    name = "cnn"

    def __init__(self, model_path: Path | str) -> None:
        self._model = keras.models.load_model(str(model_path))
        self._label_encoder = make_label_encoder()

    def predict_counts(self, csv_path: Path | str) -> dict[str, int]:
        _, normalized = load_and_prepare_frame(csv_path)
        n_samples, n_features = normalized.shape
        x = normalized.reshape((n_samples, 1, n_features, 1))
        preds = np.argmax(self._model.predict(x, verbose=0), axis=1)
        decoded = self._label_encoder.inverse_transform(preds)
        return counts_from_predictions(decoded)
