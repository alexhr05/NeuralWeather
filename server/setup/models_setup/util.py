import pandas as pd
from utilities import add_cyclical

CYCLICAL_COLS = {
    "month": 12,
    "day":   30,
    "hour":  24,
}

FEATURE_COLS = [
    "latitude", "longitude", "year",
    "month_sin", "month_cos",
    "day_sin",   "day_cos",
    "hour_sin",  "hour_cos",
]

def minmax_normalize(series: pd.Series, col_min: float, col_max: float) -> pd.Series:
    return (series - col_min) / (col_max - col_min)

def prepare_features(df: pd.DataFrame, stats: dict,
                     target: str, extra_norm_cols: list[str] | None = None) -> tuple:
    df = df.copy()

    df["year"]  = df["time"].dt.year  if "time" in df.columns else df["year"]
    df["month"] = df["time"].dt.month if "time" in df.columns else df["month"]
    df["day"]   = df["time"].dt.day   if "time" in df.columns else df["day"]
    df["hour"]  = df["time"].dt.hour  if "time" in df.columns else df["hour"]

    for col, period in CYCLICAL_COLS.items():
        df = add_cyclical(df, col, period)

    norm_cols = ["latitude", "longitude", "year"] + (extra_norm_cols or [])
    for col in norm_cols:
        df[col] = minmax_normalize(df[col], stats[col]["min"], stats[col]["max"])

    feature_cols = FEATURE_COLS.copy()
    if target not in feature_cols:
        feature_cols_out = feature_cols
    else:
        feature_cols_out = feature_cols

    return df[feature_cols_out].values, df[target].values if target in df.columns else None