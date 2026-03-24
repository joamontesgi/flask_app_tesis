"""Preprocesado CSV compartido (mismo orden que el entrenamiento)."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn import preprocessing
from sklearn.preprocessing import normalize

from shared.constants import CLASS_LABELS, FEATURE_COLUMNS, LABEL_TO_JSON_KEY


def load_and_prepare_frame(csv_path: Path | str) -> tuple[pd.DataFrame, np.ndarray]:
    path = Path(csv_path)
    df = pd.read_csv(path)
    df = df.reindex(columns=FEATURE_COLUMNS)
    df = df.replace([np.inf, -np.inf], 0)
    values = df.values.astype(np.float64)
    normalized = normalize(values)
    return df, normalized


def counts_from_predictions(decoded_labels: np.ndarray) -> dict[str, int]:
    results_df = pd.DataFrame(decoded_labels, columns=["Label"])
    out = {LABEL_TO_JSON_KEY[label]: 0 for label in CLASS_LABELS}
    for label in CLASS_LABELS:
        key = LABEL_TO_JSON_KEY[label]
        out[key] = int(results_df[results_df["Label"] == label].shape[0])
    return out


def make_label_encoder():
    le = preprocessing.LabelEncoder()
    le.fit(CLASS_LABELS)
    return le
