import numpy as np

from utilities import add_cyclical
import xarray as xr
import pandas as pd
import json
import dask.dataframe as dd
from pathlib import Path


# TIME_CHUNK_SIZE = 10
# SHORT_NAMES = {
#     "2m_temperature":"t2m",
#     "surface_solar_radiation_downwards":"ssrd",
# }

# def normalize(series: pd.Series, col_min: float, col_max: float) -> pd.Series:
#     return (series - col_min) / (col_max - col_min)

# def compute_stats(ds: xr.Dataset, lat_min: float, lat_max: float,
#                   lon_min: float, lon_max: float, variables: list[str]) -> dict:
#     import gc

#     stats = {
#         "latitude":  {"min": lat_min, "max": lat_max},
#         "longitude": {"min": lon_min, "max": lon_max},
#         "year":      {"min": 1940,    "max": 2025},
#     }

#     short_names = [SHORT_NAMES[v] for v in variables]
#     running = {s: {"min": float("inf"), "max": float("-inf")} for s in short_names}

#     n_times = len(ds.time)
#     n_chunks = (n_times + TIME_CHUNK_SIZE - 1) // TIME_CHUNK_SIZE
#     print(f"  Computing stats over {n_chunks} chunks...")

#     for i in range(n_chunks):
#         start = i * TIME_CHUNK_SIZE
#         end   = min(start + TIME_CHUNK_SIZE, n_times)
#         chunk = ds.isel(time=slice(start, end))

#         for short in short_names:
#             arr = chunk[short].values  # numpy, one small chunk
#             running[short]["min"] = min(running[short]["min"], float(arr.min()))
#             running[short]["max"] = max(running[short]["max"], float(arr.max()))

#         del chunk, arr
#         gc.collect()

#         if i % 10 == 0:
#             print(f"  Stats chunk {i+1}/{n_chunks}...")

#     for short in short_names:
#         stats[short] = running[short]

#     return stats

# def format_data(original_file: str, stats_file: str, new_file: str, area: list, variables: list) -> None:
#     parts_dir = Path(new_file).parent / "parts"
#     parts_dir.mkdir(exist_ok=True)

#     print("Opening dataset with dask chunks...")
#     ds = xr.open_dataset(original_file, engine="cfgrib", chunks={"time": TIME_CHUNK_SIZE})

#     lat_min, lon_min = area[2], area[1]
#     lat_max, lon_max = area[0], area[3]

#     print("Computing normalization stats...")
#     stats = compute_stats(ds, lat_min, lat_max, lon_min, lon_max, variables)
#     with open(stats_file, "w") as f:
#         json.dump(stats, f, indent=2)
#     print(f"Stats saved to {stats_file}")

#     n_times = len(ds.time)
#     n_chunks = (n_times + TIME_CHUNK_SIZE - 1) // TIME_CHUNK_SIZE
#     print(f"Processing {n_times} timesteps in {n_chunks} chunks...")

#     part_files = []
#     for i in range(n_chunks):
#         part_file = parts_dir / f"part_{i:05d}.parquet"
#         if part_file.exists():
#             print(f"  Chunk {i+1}/{n_chunks} already exists, skipping.")
#             part_files.append(str(part_file))
#             continue

#         start = i * TIME_CHUNK_SIZE
#         end   = min(start + TIME_CHUNK_SIZE, n_times)
#         chunk_ds = ds.isel(time=slice(start, end))

#         chunk_df = process_chunk(chunk_ds, stats, variables)
#         chunk_df.to_parquet(str(part_file), index=False)
#         part_files.append(str(part_file))
#         print(f"  Chunk {i+1}/{n_chunks} written.")

#     print("Combining chunks into final parquet...")
#     combined = dd.read_parquet(part_files)
#     combined.to_parquet(new_file, write_index=False)
#     print(f"Final parquet saved to {new_file}")


# def process_chunk(chunk_ds: xr.Dataset, stats: dict, variables: list) -> pd.DataFrame:
#     short_names = [SHORT_NAMES[v] for v in variables]

#     # merge all variable arrays into one dataframe
#     frames = [chunk_ds[s].to_dataframe().reset_index() for s in short_names]
#     df = frames[0]
#     for frame, short in zip(frames[1:], short_names[1:]):
#         df[short] = frame[short]

#     df["year"]  = df["time"].dt.year
#     df["month"] = df["time"].dt.month
#     df["day"]   = df["time"].dt.day
#     df["hour"]  = df["time"].dt.hour

#     df = add_cyclical(df, "month", 12)
#     df = add_cyclical(df, "day",   30)
#     df = add_cyclical(df, "hour",  24)

#     for col in ["latitude", "longitude", "year"] + short_names:
#         df[col] = normalize(df[col], stats[col]["min"], stats[col]["max"])

#     feature_cols = [
#         "latitude", "longitude", "year",
#         "month_sin", "month_cos",
#         "day_sin",   "day_cos",
#         "hour_sin",  "hour_cos",
#     ] + short_names

#     return df[feature_cols]

ACCUMULATED_VARS = {"ssrd"}

SHORT_NAMES = {
    "2m_temperature":                      "t2m",
    "surface_solar_radiation_downwards":   "ssrd",
}

def format_data(original_file: str, stats_file: str, new_file: str, area: list, variables: list[str] | None = None) -> None:
    variables = variables if variables is not None else ["2m_temperature"]
    short_names = [SHORT_NAMES[v] for v in variables]

    ds = xr.open_dataset(original_file, engine="cfgrib")

    frames = [ds[s].to_dataframe().reset_index() for s in short_names]
    df = frames[0]
    for frame, short in zip(frames[1:], short_names[1:]):
        df[short] = frame[short]

    df["year"]  = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["day"]   = df["time"].dt.day
    df["hour"]  = df["time"].dt.hour

    df = add_cyclical(df, "month", 12)
    df = add_cyclical(df, "day",   30)
    df = add_cyclical(df, "hour",  24)

    for short in short_names:
        if short in ACCUMULATED_VARS:
            df[short] = df[short].clip(lower=0)

    def minmax_normalize(df, cols):
        stats = {}
        for col in cols:
            col_min = df[col].min()
            col_max = df[col].max()
            df[col] = (df[col] - col_min) / (col_max - col_min)
            stats[col] = {"min": col_min, "max": col_max}
        return df, stats

    df, stats = minmax_normalize(df, ["latitude", "longitude", "year"] + short_names)

    with open(stats_file, "w") as f:
        json.dump({col: {"min": float(v["min"]), "max": float(v["max"])} for col, v in stats.items()}, f)

    feature_cols = [
        "latitude", "longitude", "year",
        "month_sin", "month_cos",
        "day_sin",   "day_cos",
        "hour_sin",  "hour_cos",
    ]
    df = df[feature_cols + short_names]
    df.to_parquet(new_file, index=False)