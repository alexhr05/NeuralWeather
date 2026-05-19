from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from setup import setup
from os import listdir
from os.path import isfile, join
from pydantic import BaseModel
from typing import List
from utilities import use_data

setup()
app = FastAPI()

origins = ["http://localhost:5174"]

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

@app.post("/use")
def use_model(responseBody: ResponseBody):    
    return use_data(responseBody)
