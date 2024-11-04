import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from model.execute_model import execute_model
app = FastAPI()

@app.get('/get_predictions/')
def get_predictions(image_url: str = "https://github.com/pytorch/hub/raw/master/images/dog.jpg"):
    return execute_model(image_url)