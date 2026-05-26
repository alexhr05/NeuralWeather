import json
import numpy as np

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