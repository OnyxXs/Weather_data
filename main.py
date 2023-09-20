import json
from typing import List
from fastapi import FastAPI, Query, HTTPException, Body

app = FastAPI()

@app.post("/weather")
async def create_weather_entry(
    weather_entry: dict = Body(
        ...,
        description="Nouvelle entrée de données météorologiques au format JSON.",
        example={
            "date": "2017-01-01",
            "tmin": 41,
            "tmax": 50,
            "prcp": 0.54,
            "snow": 0.0,
            "snwd": 0.0,
            "awnd": 6.49
        }
    )
):
    # Ajoutez la nouvelle entrée de données météorologiques à la liste existante
    weather_data.append(weather_entry)
    
    # Vous pouvez également enregistrer ces modifications dans le fichier JSON si nécessaire
    with open("rdu-weather-history.json", "w") as file:
        json.dump(weather_data, file, indent=2)
    
    return weather_entry

# Chargement des données météorologiques depuis un fichier JSON
with open("rdu-weather-history.json", "r") as file:
    weather_data = json.load(file)


    """
    Obtenez des données météorologiques filtrées en fonction des dates spécifiées.

    Args:
        start_date (str): Date de début pour la filtration.
        end_date (str): Date de fin pour la filtration.

    Returns:
        List[dict]: Liste des données météorologiques correspondant à la plage de dates spécifiée.
    """


@app.get("/weather")
async def get_weather_filter_date(
    start_date: str = Query(..., description="Date de début : "),
    end_date: str = Query(..., description="Date de fin : ")
) -> List[dict]:
    # Filtrer les données en fonction des dates spécifiées
    date_data = [data for data in weather_data if start_date <= data["date"] <= end_date]
    return date_data
