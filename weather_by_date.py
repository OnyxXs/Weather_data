import json
from typing import List
from fastapi import FastAPI, Query
app = FastAPI()

# Chargement des données météorologiques depuis un fichier JSON
with open("rdu-weather-history.json", "r") as file:
    weather_data = json.load(file)


@app.get("/weather_by_date")
async def get_weather_filter_date(
    start_date: str = Query(..., description="Date de début : "),
    end_date: str = Query(..., description="Date de fin : ")
) -> List[dict]:
    """
       Obtenez des données météorologiques filtrées en fonction des dates spécifiées.

       Args:
           start_date (str): Date de début pour la filtration.
           end_date (str): Date de fin pour la filtration.

       Returns:
           List[dict]: Liste des données météorologiques correspondant à la plage de dates spécifiée.
    """
    # Filtrer les données en fonction des dates spécifiées
    date_data = [data for data in weather_data if start_date <= data["date"] <= end_date]
    return date_data