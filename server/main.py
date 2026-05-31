from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from setup import setup
from os import listdir
from os.path import isfile, join
from pydantic import BaseModel
from typing import List
from setup.models_setup.use_model import use_model
# from server.setup.models_setup.train_model import use_base_model

setup()
app = FastAPI()

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Coordinate(BaseModel):
    longitude: float
    latitude: float

class ResponseBody(BaseModel):
    year: int
    month: int
    day: int
    hour: int
    coordinate: List[Coordinate]
    model: str



@app.get("/models")
def get_models():
    models_dir = "models"
    print("test")
    return [f for f in listdir(models_dir) if isfile(join(models_dir, f))]

@app.post("/test")
def test_data(year:int):
    return year

MODEL_REGISTRY = {
    "base_model": {
        "stats_file": "data/bulgaria/bulgaria_2m_temperature_stats.json",
        "target": "t2m",
    },
    "solar_model": {
        "stats_file": "data/bulgaria/bulgaria_surface_solar_radiation_downwards_stats.json",
        "target": "ssrd",
    },
}

@app.post("/use")
def use_default_model(responseBody: ResponseBody):  
    name = "base_model"
    entry = MODEL_REGISTRY[name]
    df = pd.DataFrame([coord.dict() for coord in responseBody.coordinate])
    df["year"]  = responseBody.year
    df["month"] = responseBody.month
    df["day"]   = responseBody.day
    df["hour"]  = responseBody.hour  
    return use_model(
            name=name,
            request_df=df,
            stats_file=entry["stats_file"],
            target=entry["target"],
        )

@app.post("/use/{model}")
def use_model_by_name(model: str, responseBody: ResponseBody):
    name = model.removesuffix(".keras")

    if name not in MODEL_REGISTRY:
        raise HTTPException(status_code=404, detail=f"Model '{model}' not found.")

    entry = MODEL_REGISTRY[name]

    df = pd.DataFrame([coord.dict() for coord in responseBody.coordinate])
    df["year"]  = responseBody.year
    df["month"] = responseBody.month
    df["day"]   = responseBody.day
    df["hour"]  = responseBody.hour

    try:
        return use_model(
            name=name,
            request_df=df,
            stats_file=entry["stats_file"],
            target=entry["target"],
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail=f"Model '{model}' not found.")