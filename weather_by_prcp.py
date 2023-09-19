import json
from typing import List
from fastapi import FastAPI, Query
app = FastAPI()

# Chargement des données météorologiques depuis un fichier JSON
with open("rdu-weather-history.json", "r") as file:
    weather_data = json.load(file)


@app.get("/weather_by_prcp")
async def get_weather_filter_prcp(
        min_prcp: float = Query(..., description="Précipitation minimale"),
        max_prcp: float = Query(..., description="Précipitation maximale")
) -> List[dict]:
    """
    Filtre les données météorologiques par plage de précipitations.

    Args:
        min_prcp (float): Précipitation minimale.
        max_prcp (float): Précipitation maximale.

    Returns:
        List[dict]: Liste des données météorologiques dans la plage de précipitations spécifiée.
    """

    prcp_data = [data for data in weather_data if min_prcp <= data["prcp"] <= max_prcp]
    return prcp_data
