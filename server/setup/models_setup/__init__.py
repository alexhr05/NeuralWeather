import os
from .base_model import train_base_model

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
    model_file = f"{model_dir}/base_model.keras"
    if not os.path.exists(model_file):
        train_base_model(parquet_file, model_file)
    print("model setup")