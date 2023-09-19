import json
from typing import List, Dict
from fastapi import FastAPI, Query, HTTPException, Body

app = FastAPI()

# Chargement des données météorologiques depuis un fichier JSON
try:
    with open("rdu-weather-history.json", "r") as file:
        weather_data = json.load(file)
except FileNotFoundError:
    weather_data = []

# Fonction pour enregistrer les données dans le fichier JSON
def save_data_to_json():
    with open("rdu-weather-history.json", "w") as file:
        json.dump(weather_data, file, indent=4)

# Endpoint pour obtenir toutes les données météorologiques
@app.get("/all-weather-data")
async def get_all_weather_data():
    return weather_data

# Endpoint pour ajouter une nouvelle entrée de données météorologiques
@app.post("/add-weather-data")
async def add_weather_data(new_data: Dict):
    weather_data.append(new_data)
    save_data_to_json()  # Enregistrer les données dans le fichier JSON
    return {"message": "Nouvelles données ajoutées avec succès"}

# Endpoint pour supprimer des données météorologiques par date
@app.delete("/delete-weather-data")
async def delete_weather_data_by_date(
    start_date: str = Query(..., description="Date de début : "),
    end_date: str = Query(..., description="Date de fin : ")
):
    global weather_data
    # Filtrer les données à conserver (toutes sauf celles dans la plage de dates spécifiée)
    weather_data = [data for data in weather_data if not (start_date <= data["date"] <= end_date)]
    save_data_to_json()  # Enregistrer les données dans le fichier JSON
    return {"message": "Données supprimées avec succès"}

# Endpoint pour mettre à jour des données météorologiques par date
@app.put("/update-weather-data")
async def update_weather_data_by_date(
    start_date: str = Query(..., description="Date de début : "),
    end_date: str = Query(..., description="Date de fin : "),
    updated_data: Dict = Body(..., description="Données mises à jour : ")
):
    global weather_data
    # Mettre à jour les données existantes avec les nouvelles données
    for i, data in enumerate(weather_data):
        if start_date <= data["date"] <= end_date:
            weather_data[i].update(updated_data)
    save_data_to_json()  # Enregistrer les données dans le fichier JSON
    return {"message": "Données mises à jour avec succès"}
