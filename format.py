import xarray as xr
import pandas as pd
import numpy as np
import json

ds = xr.open_dataset("data/bulgaria/data.grib", engine="cfgrib")
df = ds["t2m"].to_dataframe().reset_index()

df["year"]  = df["time"].dt.year
df["month"] = df["time"].dt.month
df["day"]   = df["time"].dt.day
df["hour"]  = df["time"].dt.hour

def add_cyclical(df, col, period):
    df[f"{col}_sin"] = np.sin(2 * np.pi * df[col] / period)
    df[f"{col}_cos"] = np.cos(2 * np.pi * df[col] / period)
    return df

df = add_cyclical(df, "month", 12)
df = add_cyclical(df, "day", 31)
df = add_cyclical(df, "hour", 24)

def minmax_normalize(df, cols):
    stats = {}
    for col in cols:
        col_min = df[col].min()
        col_max = df[col].max()
        df[col] = (df[col] - col_min) / (col_max - col_min)
        stats[col] = {"min": col_min, "max": col_max}
    return df, stats

df, stats = minmax_normalize(df, ["latitude", "longitude", "year", "t2m"])
with open("data/bulgaria/stats.json", "w") as f:
    json.dump({col: {"min": float(v["min"]), "max": float(v["max"])} for col, v in stats.items()}, f)

# How to inverse normalization:
# def inverse_normalize(value, col, stats):
#     return value * (stats[col]["max"] - stats[col]["min"]) + stats[col]["min"]

# real_temp = inverse_normalize(predicted, "t2m", stats)

feature_cols = ["latitude", "longitude", "year",
                "month_sin", "month_cos",
                "day_sin", "day_cos",
                "hour_sin", "hour_cos"]

df = df[feature_cols + ["t2m"]]
df.to_parquet("data/bulgaria/data.parquet", index=False)