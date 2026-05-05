import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import cartopy.crs as ccrs
import cartopy.feature as cfeature

ds = xr.open_dataset("data/bulgaria/data.grib", engine="cfgrib")

year = 2000 # 1940 - 2025
month = 1
day = 3 # 1
hour = 12

target_time = ds["valid_time"].values[24*2]

slice_data = ds["t2m"].sel(
    valid_time=target_time,
)

t2m_c = slice_data - 273.15

lats = t2m_c["latitude"].values
lons = t2m_c["longitude"].values
Z = t2m_c.values


fig = plt.figure(figsize=(10, 6))
ax = plt.axes(projection=ccrs.PlateCarree())

ax.add_feature(cfeature.BORDERS, linewidth=2)
ax.add_feature(cfeature.COASTLINE, linewidth=2)

# ax.add_feature(cfeature.LAND, alpha=0.5)

cf = ax.contourf(
    lons,
    lats,
    Z,
    levels=20,
    cmap="coolwarm",
    transform=ccrs.PlateCarree()
)

cs = ax.contour(
    lons,
    lats,
    Z,
    levels=10,
    colors="black",
    linewidths=0.5,
    transform=ccrs.PlateCarree()
)

ax.clabel(cs, fontsize=8)

plt.colorbar(cf, ax=ax, label="°C")

plt.title(f"Temps for \n{str(target_time)}")

plt.tight_layout()
plt.show()