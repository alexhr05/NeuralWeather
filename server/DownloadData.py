import cdsapi

years = [f"{i}" for i in range(1940, 2026)]
months = [f"{i:02d}" for i in range(1, 13)]
days = [f"{i:02d}" for i in range(1,32,10)]
times = [f"{i:02d}:00" for i in range(0,24,1)]
area = [44.3, 22.0, 41.2, 28.7]

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

import os

nested_directory = "data/bulgaria"

try:
    os.makedirs(nested_directory)
    print(f"Nested directories '{nested_directory}' created successfully.")
except FileExistsError:
    print(f"One or more directories in '{nested_directory}' already exist.")
except PermissionError:
    print(f"Permission denied: Unable to create '{nested_directory}'.")
except Exception as e:
    print(f"An error occurred: {e}")

client = cdsapi.Client()
client.retrieve(dataset, request).download(f"{nested_directory}/data.grib")

