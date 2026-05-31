import pandas as pd
import tensorflow as tf
import json
from pathlib import Path
from sklearn.model_selection import train_test_split
from .util import FEATURE_COLS

def build_model(n_features: int, layers: list[int]) -> tf.keras.Model:
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(n_features,)),
        *[tf.keras.layers.Dense(size, activation="relu") for size in layers],
        tf.keras.layers.Dense(1),
    ])
    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    return model


def train_model(
    name: str,
    parquet_file: str,
    stats_file: str,
    target: str = "t2m",
    layers: list[int] = [32, 32, 32],
    test_size: float = 0.05,
    epochs: int = 20,
    batch_size: int = 1024,
    extra_norm_cols: list[str] | None = None,
) -> None:
    model_file = f"models/{name}.keras"
    if Path(model_file).exists():
        print(f"[{name}] Model already exists, skipping training.")
        return

    print(f"[{name}] Loading data from {parquet_file}...")
    df = pd.read_parquet(parquet_file)
    df = df.replace([float("inf"), float("-inf")], float("nan")).dropna()

    with open(stats_file) as f:
        stats = json.load(f)

    X, y = df[FEATURE_COLS].values, df[target].values

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    print(f"[{name}] Training on {len(X_train)} samples...")
    model = build_model(n_features=X.shape[1], layers=layers)
    model.fit(
        X_train, y_train,
        validation_split=0.1,
        epochs=epochs,
        batch_size=batch_size,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
        ]
    )

    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"[{name}] Test MAE (normalized): {mae:.4f}")

    model.save(model_file)
    print(f"[{name}] Saved to {model_file}")