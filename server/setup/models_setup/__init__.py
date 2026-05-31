import os
from .train_model import train_model

def setup_models():
    model_dir = "models"
    if not os.path.exists(model_dir):
        try:
            os.makedirs(model_dir)
            print(f"Dir '{model_dir}' created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return -1

    train_model(
        name="base_model",
        parquet_file="data/bulgaria/bulgaria_2m_temperature.parquet",
        stats_file="data/bulgaria/bulgaria_2m_temperature_stats.json",
        target="t2m",
        layers=[32, 32, 32],
    )
    train_model(
        name="solar_model",
        parquet_file="data/bulgaria/bulgaria_surface_solar_radiation_downwards.parquet",
        stats_file="data/bulgaria/bulgaria_surface_solar_radiation_downwards_stats.json",
        target="ssrd",
        non_negative=True,
        layers=[32, 32, 32],
    )
    print("model setup")