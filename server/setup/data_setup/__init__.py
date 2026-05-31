from setup.data_setup.formatter import format_data
import pandas as pd
from pathlib import Path
from utilities import download_data

REGIONS = {
    "bulgaria": [44.3, 22.0, 41.2, 28.7],
    "europe":   [71.0, -25.0, 34.0, 60.0],
}

def download_data_region(
    region_name: str,
    year_range: tuple[int, int] = (1940, 2025),
    months: list[int] | None = None,
    days: list[int] | None = None,
    hours: list[int] | None = None,
    variables: list[str] | None = None,
) -> int:
    if region_name not in REGIONS:
        print(f"Unknown region '{region_name}'. Available: {list(REGIONS.keys())}")
        return -1

    # --- resolve defaults ---
    months    = months    if months    is not None else list(range(1, 13))
    days      = days      if days      is not None else [1, 11, 21]
    hours     = hours     if hours     is not None else list(range(0, 24))
    variables = variables if variables is not None else ["2m_temperature"]

    # --- validate ---
    if not (1940 <= year_range[0] <= year_range[1] <= 2025):
        print(f"Invalid year_range {year_range}. Must be within 1940–2025.")
        return -1
    if not all(1 <= m <= 12 for m in months):
        print(f"Invalid months {months}. Must be 1–12.")
        return -1
    if not all(1 <= d <= 31 for d in days):
        print(f"Invalid days {days}. Must be 1–31.")
        return -1
    if not all(0 <= h <= 23 for h in hours):
        print(f"Invalid hours {hours}. Must be 0–23.")
        return -1

    # --- format for ERA5 API ---
    years      = [f"{y}"      for y in range(year_range[0], year_range[1] + 1)]
    months_fmt = [f"{m:02d}"  for m in months]
    days_fmt   = [f"{d:02d}"  for d in days]
    times_fmt  = [f"{h:02d}:00" for h in hours]

    area     = REGIONS[region_name]
    var_suffix = "_".join(sorted(variables))
    slug = f"{region_name}_{var_suffix}"

    data_dir     = Path("data") / region_name
    grib_file    = data_dir / f"{slug}.grib"
    stats_file   = data_dir / f"{slug}_stats.json"
    parquet_file = data_dir / f"{slug}.parquet"

    try:
        data_dir.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Failed to create directory '{data_dir}': {e}")
        return -1

    if not grib_file.exists():
        print(f"[{slug}] Downloading data...")
        download_data(
            file=str(grib_file),
            area=area,
            years=years,
            months=months_fmt,
            days=days_fmt,
            times=times_fmt,
            variables=variables,
        )

    if not stats_file.exists() or not parquet_file.exists():
        print(f"[{slug}] Formatting data...")
        format_data(
            original_file=str(grib_file),
            stats_file=str(stats_file),
            new_file=str(parquet_file),
            area=area,
            variables=variables,
        )

    print(f"[{slug}] Done.")
    return 0