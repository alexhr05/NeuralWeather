import cdsapi
import os
import xarray as xr
import pandas as pd
import numpy as np
import json

def download_data(file, area, years, months, days,times):

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
        "area": area
    }


    client = cdsapi.Client()
    client.retrieve(dataset, request).download(file)

def download_data_bulgaria():
    years = [f"{i}" for i in range(1940, 2026)]
    months = [f"{i:02d}" for i in range(1, 13)]
    days = [f"{i:02d}" for i in range(1,32,10)]
    times = [f"{i:02d}:00" for i in range(0,24,1)]
    area = [44.3, 22.0, 41.2, 28.7]
    data_dir = "data/bulgaria"
    grib_file = f"{data_dir}/data.grib"
    stats_file = f"{data_dir}/stats.json"
    parquet_file = f"{data_dir}/data.parquet"
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
            print(f"Dirs '{data_dir}' created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return -1
    
    if not os.path.exists(grib_file):
        print("data dont exist")
        download_data(file=grib_file, years=years,months=months, days=days, times=times,area=area)
    if not os.path.exists(stats_file) or not os.path.exists(grib_file):
        print("formatted data does not exist")
        format_data(original_file=grib_file, stats_file=stats_file, new_file=parquet_file)
    

def download_data_europe():
    years = [f"{i}" for i in range(1940, 2026)]
    months = [f"{i:02d}" for i in range(1, 13)]
    days = [f"{i:02d}" for i in range(1,32,10)]
    times = [f"{i:02d}:00" for i in range(0,24,1)]
    area = [71.0, -25.0, 34.0, 60.0]

    data_dir = "data/europe"
    grib_file = f"{data_dir}/data.grib"
    stats_file = f"{data_dir}/stats.json"
    parquet_file = f"{data_dir}/data.parquet"
    if not os.path.exists(data_dir):
        try:
            os.makedirs(data_dir)
            print(f"Dirs '{data_dir}' created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return -1
    
    if not os.path.exists(grib_file):
        print("data dont exist")
        download_data(file=grib_file, years=years,months=months, days=days, times=times,area=area)
    if not os.path.exists(stats_file) or not os.path.exists(grib_file):
        print("formatted data does not exist")
        format_data(original_file=grib_file, stats_file=stats_file, new_file=parquet_file)
    
    
    
    

def format_data(original_file, stats_file, new_file):

    ds = xr.open_dataset(original_file, engine="cfgrib")
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
    with open(stats_file, "w") as f:
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
    df.to_parquet(new_file, index=False)