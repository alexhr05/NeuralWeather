import os
from .data_setup import download_data_region
from .models_setup import setup_models


def setup():
    setup_data()
    setup_models()

def setup_data():
    download_data_region("bulgaria")
    download_data_region("bulgaria", variables=["surface_solar_radiation_downwards"])
    # download_data_region("europe")
    
