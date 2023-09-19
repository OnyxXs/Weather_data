import json
from typing import List, Dict
from fastapi import FastAPI, Query, HTTPException, Body

app = FastAPI()

# Chargement des données météorologiques depuis un fichier JSON
with open("rdu-weather-history.json", "r") as file:
    weather_data = json.load(file)






