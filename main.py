import json
from typing import List

from fastapi import FastAPI, Query

app = FastAPI()


with open("rdu-weather-history.json", "r") as file:
    weather_data = json.load(file)


@app.get("/weather")
async def get_weather_filter_date(
    start_date: str = Query(..., description="Starting Date : "),
    end_date: str = Query(..., description="Ending Date : ")
) -> List[dict]:
    date_data = [data for data in weather_data if start_date <= data["date"] <= end_date]
    return date_data
