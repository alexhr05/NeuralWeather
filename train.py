import pandas as pd
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import json
import matplotlib.pyplot as plt

with open("data/bulgaria/stats.json") as f:
    stats = json.load(f)
df = pd.read_parquet("data/bulgaria/data.parquet")


# feature_cols = ["latitude", "longitude", "year",
#                 "month_sin", "month_cos",
#                 "day_sin", "day_cos",
#                 "hour_sin", "hour_cos"]


feature_cols = ["latitude", "longitude", "year",
                "month_sin", "month_cos",
                "day_sin", "day_cos",
                "hour_sin", "hour_cos"]


X = df[feature_cols].values
y = df["t2m"].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=42)

model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(len(feature_cols),)),
    tf.keras.layers.Dense(64, activation="relu"),
    tf.keras.layers.Dense(64, activation="relu"),
    
    tf.keras.layers.Dense(1)
])

model.compile(optimizer="adam", loss="mse", metrics=["mae"])
# model.summary()

history = model.fit(
    X_train, y_train,
    validation_split=0.1,
    epochs=2,
    batch_size=4096,
    callbacks=[
        tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
    ]
)

loss, mae = model.evaluate(X_test, y_test)
print(f"Test MAE (normalized): {mae:.4f}")
min_t2m=stats["t2m"]["min"]
max_t2m=stats["t2m"]["max"]
print(f"Test MAE: {(max_t2m-min_t2m)*mae:.4f}")

model.save("data/bulgaria/model.keras")