import json
from fastapi import FastAPI

app = FastAPI()

# Chargement des données météorologiques depuis un fichier JSON
with open("rdu-weather-history.json", "r") as file:
    weather_data = json.load(file)

# Endpoint pour obtenir toutes les données météorologiques
@app.get("/all-weather-data")
async def get_all_weather_data():
    return weather_data
