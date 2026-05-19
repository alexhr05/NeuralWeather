import pandas as pd
import tensorflow as tf
import json
import numpy as np
def use_data(responseBody):
    longs = [coord.longitude for coord in responseBody.coordinate]
    lats  = [coord.latitude  for coord in responseBody.coordinate]
    year = responseBody.year
    month = responseBody.month
    day = responseBody.day
    hour = responseBody.hour

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

    model = tf.keras.models.load_model("models/model.keras")   
    

    X = df[feature_cols].values
    predictions = model.predict(X) # returns numpy 2d array

    return predictions.flatten().tolist() # plain list
    
def minmax_normalize(df, cols):


    stats_file = "data/bulgaria/stats.json"

    with open(stats_file) as f:
        stats = json.load(f)



    for col in cols:
        col_min = stats[col]["min"]
        col_max = stats[col]["max"]
        df[col] = (df[col] - col_min) / (col_max - col_min)
        stats[col] = {"min": col_min, "max": col_max}
    
    
    return df



def add_cyclical(df, col, period):
        df[f"{col}_sin"] = np.sin(2 * np.pi * df[col] / period)
        df[f"{col}_cos"] = np.cos(2 * np.pi * df[col] / period)
        return df