from fastapi import FastAPI
from setup import setup
from os import listdir
from os.path import isfile, join
setup()
app = FastAPI()


@app.get("/models")
def get_models():
    models_dir = "models"
    print("test")
    return [f for f in listdir(models_dir) if isfile(join(models_dir, f))]


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}