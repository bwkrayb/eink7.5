import os
from typing import Union
from fastapi import FastAPI
from datetime import datetime

app = FastAPI()

@app.get("/weather_refresh")
def weather_refresh():
    os.system("sh bin/start.sh")
    return {"Refresh time":datetime.now()}

@app.get("/refresh_weather")
def not_what_you_wanted():
    return {"Do you mean ": "weather_refresh?"}
