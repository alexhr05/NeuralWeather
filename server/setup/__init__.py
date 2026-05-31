import os
from .data import download_data_bulgaria, download_data_europe
from .models_setup import setup_models


def setup():
    setup_data()
    setup_models()

def setup_data():
    download_data_europe()
    download_data_bulgaria()
    
