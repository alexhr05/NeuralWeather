import cdsapi
import os
import xarray as xr
import pandas as pd
import numpy as np
import json
import dask.dataframe as dd
from pathlib import Path


REGIONS = {
    "bulgaria": [44.3, 22.0, 41.2, 28.7],
    "europe":   [71.0, -25.0, 34.0, 60.0],
}

YEARS  = [f"{i}" for i in range(1940, 2026)]
MONTHS = [f"{i:02d}" for i in range(1, 13)]
DAYS   = [f"{i:02d}" for i in [1, 11, 21]]
TIMES  = [f"{i:02d}:00" for i in range(0, 24)]

TIME_CHUNK_SIZE = 100


def download_data(file: str, area: list, years: list, months: list, days: list, times: list) -> None:
    dataset = "reanalysis-era5-single-levels"
    request = {
        "product_type": ["reanalysis"],
        "variable": ["2m_temperature"],
        "year": years,
        "month": months,
        "day": days,
        "time": times,
        "data_format": "grib",
        "download_format": "unarchived",
        "area": area,
    }
    client = cdsapi.Client()
    client.retrieve(dataset, request).download(file)


def add_cyclical(df: pd.DataFrame, col: str, period: float) -> pd.DataFrame:
    df[f"{col}_sin"] = np.sin(2 * np.pi * df[col] / period)
    df[f"{col}_cos"] = np.cos(2 * np.pi * df[col] / period)
    return df


def compute_stats(ds: xr.Dataset, lat_min: float, lat_max: float,
                  lon_min: float, lon_max: float) -> dict:
    t2m = ds["t2m"]

    t2m_min = float(t2m.min().compute())
    t2m_max = float(t2m.max().compute())

    return {
        "latitude":  {"min": lat_min,  "max": lat_max},
        "longitude": {"min": lon_min,  "max": lon_max},
        "year":      {"min": 1940,     "max": 2025},
        "t2m":       {"min": t2m_min,  "max": t2m_max},
    }


def normalize(series: pd.Series, col_min: float, col_max: float) -> pd.Series:
    return (series - col_min) / (col_max - col_min)


def process_chunk(chunk_ds: xr.Dataset, stats: dict) -> pd.DataFrame:
    df = chunk_ds["t2m"].to_dataframe().reset_index()

    df["year"]  = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["day"]   = df["time"].dt.day
    df["hour"]  = df["time"].dt.hour

    df = add_cyclical(df, "month", 12)
    df = add_cyclical(df, "day",   30)
    df = add_cyclical(df, "hour",  24)

    for col in ["latitude", "longitude", "year", "t2m"]:
        df[col] = normalize(df[col], stats[col]["min"], stats[col]["max"])

    feature_cols = [
        "latitude", "longitude", "year",
        "month_sin", "month_cos",
        "day_sin",   "day_cos",
        "hour_sin",  "hour_cos",
        "t2m",
    ]
    return df[feature_cols]


def format_data(original_file: str, stats_file: str, new_file: str, area: list) -> None:
    parts_dir = Path(new_file).parent / "parts"
    parts_dir.mkdir(exist_ok=True)

    print("Opening dataset with dask chunks...")
    ds = xr.open_dataset(original_file, engine="cfgrib", chunks={"time": TIME_CHUNK_SIZE})

    lat_min, lon_min = area[2], area[1]
    lat_max, lon_max = area[0], area[3]

    print("Computing normalization stats...")
    stats = compute_stats(ds, lat_min, lat_max, lon_min, lon_max)
    with open(stats_file, "w") as f:
        json.dump(stats, f, indent=2)
    print(f"Stats saved to {stats_file}")

    n_times = len(ds.time)
    n_chunks = (n_times + TIME_CHUNK_SIZE - 1) // TIME_CHUNK_SIZE
    print(f"Processing {n_times} timesteps in {n_chunks} chunks...")

    part_files = []
    for i in range(n_chunks):
        part_file = parts_dir / f"part_{i:05d}.parquet"
        if part_file.exists():
            print(f"  Chunk {i+1}/{n_chunks} already exists, skipping.")
            part_files.append(str(part_file))
            continue

        start = i * TIME_CHUNK_SIZE
        end   = min(start + TIME_CHUNK_SIZE, n_times)
        chunk_ds = ds.isel(time=slice(start, end))

        chunk_df = process_chunk(chunk_ds, stats)
        chunk_df.to_parquet(str(part_file), index=False)
        part_files.append(str(part_file))
        print(f"  Chunk {i+1}/{n_chunks} written.")

    print("Combining chunks into final parquet...")
    combined = dd.read_parquet(part_files)
    combined.to_parquet(new_file, write_index=False)
    print(f"Final parquet saved to {new_file}")


def download_data_region(region_name: str) -> int:
    if region_name not in REGIONS:
        print(f"Unknown region '{region_name}'. Available: {list(REGIONS.keys())}")
        return -1

    area     = REGIONS[region_name]
    data_dir = Path("data") / region_name
    grib_file    = data_dir / "data.grib"
    stats_file   = data_dir / "stats.json"
    parquet_file = data_dir / "data.parquet"

    try:
        data_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Failed to create directory '{data_dir}': {e}")
        return -1

    if not grib_file.exists():
        print(f"[{region_name}] Downloading data...")
        download_data(
            file=str(grib_file),
            area=area,
            years=YEARS,
            months=MONTHS,
            days=DAYS,
            times=TIMES,
        )

    if not stats_file.exists() or not parquet_file.exists():
        print(f"[{region_name}] Formatting data...")
        format_data(
            original_file=str(grib_file),
            stats_file=str(stats_file),
            new_file=str(parquet_file),
            area=area,
        )

    print(f"[{region_name}] Done.")
    return 0