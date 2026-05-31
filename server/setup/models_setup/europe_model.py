import pandas as pd
import tensorflow as tf
import json
import numpy as np
from sklearn.model_selection import train_test_split
from utilities import minmax_normalize, add_cyclical

def train_base_model(parquet_file, model_file):

    df = pd.read_parquet(parquet_file)

    feature_cols = ["latitude", "longitude", "year",
                    "month_sin", "month_cos",
                    "day_sin", "day_cos",
                    "hour_sin", "hour_cos"]


    X = df[feature_cols].values
    y = df["t2m"].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.05, random_state=42)

    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=(len(feature_cols),)),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(32, activation="relu"),
        
        tf.keras.layers.Dense(1)
    ])

    model.compile(optimizer="adam", loss="mse", metrics=["mae"])
    # model.summary()

    model.fit(
        X_train, y_train,
        validation_split=0.1,
        epochs=2,
        batch_size=1024,
        callbacks=[
            tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True)
        ]
    )

    # loss, mae = model.evaluate(X_test, y_test)
    # print(f"Test MAE (normalized): {mae:.4f}")
    # min_t2m=stats["t2m"]["min"]
    # max_t2m=stats["t2m"]["max"]
    # print(f"Test MAE: {(max_t2m-min_t2m)*mae:.4f}")

    model.save(model_file)



def use_base_model(responseBody):
    df = pd.DataFrame([coord.dict() for coord in responseBody.coordinate])
    df["year"] = responseBody.year
    df["month"] = responseBody.month
    df["day"] = responseBody.day
    df["hour"] = responseBody.hour 

    print(df)

    add_cyclical(df, "month", 12)
    add_cyclical(df, "day", 31)
    add_cyclical(df, "hour", 24)

    df = minmax_normalize(df, ["latitude", "longitude", "year"])

    feature_cols = ["latitude", "longitude", "year",
                    "month_sin", "month_cos",
                    "day_sin", "day_cos",
                    "hour_sin", "hour_cos"]

    model = tf.keras.models.load_model("models/base_model.keras")   

    with open("data/bulgaria/stats.json") as f:
        stats = json.load(f)

    X = df[feature_cols].values
    predictions = model.predict(X).flatten()

    t2m_min = stats["t2m"]["min"]
    t2m_max = stats["t2m"]["max"]
    temps_celsius = predictions * (t2m_max - t2m_min) + t2m_min - 273.15

    return temps_celsius.tolist()