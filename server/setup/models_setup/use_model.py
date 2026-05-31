import pandas as pd
import tensorflow as tf
import json
from .util import prepare_features

def use_model(
    name: str,
    request_df: pd.DataFrame,
    stats_file: str,
    target: str = "t2m",
    extra_norm_cols: list[str] | None = None,
) -> list[float]:
    with open(stats_file) as f:
        stats = json.load(f)

    X, _ = prepare_features(request_df, stats, target, extra_norm_cols)

    model = tf.keras.models.load_model(f"models/{name}.keras")
    predictions = model.predict(X).flatten()

    t2m_min = stats[target]["min"]
    t2m_max = stats[target]["max"]
    result = predictions * (t2m_max - t2m_min) + t2m_min

    if target in ("t2m", "d2m"):
        result -= 273.15

    return result.tolist()