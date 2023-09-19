import json

from fastapi import FastAPI

app = FastAPI()


with open("rdu-weather-history.json", "r") as file:
    weather_data = json.load(file)


@app.get("/weather")
async def get_weather():
    data = [data for data in weather_data]
    return data
