import os
from .data import download_data, format_data
from .models import train_model

def setup():
    setup_data()
    setup_models()

def setup_data():
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
        # download_data(grib_file)
    if not os.path.exists(stats_file) or not os.path.exists(grib_file):
        print("formatted data does not exist")
        # format_data(grib_file, stats_file, parquet_file)
    
    
def setup_models():
    data_dir = "data/bulgaria"
    model_dir = "models"
    if not os.path.exists(model_dir):
        try:
            os.makedirs(model_dir)
            print(f"Dir '{model_dir}' created successfully.")
        except Exception as e:
            print(f"An error occurred: {e}")
            return -1
    
    parquet_file = f"{data_dir}/data.parquet"
    model_file = f"{model_dir}/model.keras"
    # train_model(parquet_file, model_file)
    print("model setup")