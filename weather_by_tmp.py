import json
from typing import List
from fastapi import FastAPI, Query
app = FastAPI()

# Chargement des données météorologiques depuis un fichier JSON
with open("rdu-weather-history.json", "r") as file:
    weather_data = json.load(file)


@app.get("/weather_by_temperature")
async def filter_by_temperature(
        min_tmp: float = Query(..., description="Température minimale"),
        max_tmp: float = Query(..., description="Température maximale")
) -> List[dict]:
    """
    Filtre les données météorologiques par plage de températures.

    Args:
        min_tmp (float): Température minimale.
        max_tmp (float): Température maximale.

    Returns:
        List[dict]: Liste des données météorologiques dans la plage de températures spécifiée.
    """
    filtered_data = [data for data in weather_data if min_tmp <= data["tmin"] <= max_tmp]
    return filtered_data
