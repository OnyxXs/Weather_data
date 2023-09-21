from fastapi import FastAPI, Query, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional
from database import database

app = FastAPI()

class WeatherDataCreate(BaseModel):
    tmin: float
    tmax: float
    prcp: float
    snow: float
    snwd: float
    awnd: float

class WeatherDataUpdate(BaseModel):
    tmin: Optional[float] = None
    tmax: Optional[float] = None
    prcp: Optional[float] = None
    snow: Optional[float] = None
    snwd: Optional[float] = None
    awnd: Optional[float] = None

@app.post("/add-weather-data", response_model=database.WeatherData)
async def add_weather_data(weather_data: WeatherDataCreate):
    db = database.SessionLocal()
    db_data = database.WeatherData(**weather_data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()
    return db_data

@app.get("/all-weather-data", response_model=List[database.WeatherData])
async def get_all_weather_data(skip: int = Query(0, description="Index de début"), limit: int = Query(10, description="Nombre maximum de données à retourner")):
    db = database.SessionLocal()
    data = db.query(database.WeatherData).offset(skip).limit(limit).all()
    db.close()
    return data

@app.get("/weather-data/{data_id}", response_model=database.WeatherData)
async def get_weather_data(data_id: int):
    db = database.SessionLocal()
    data = db.query(database.WeatherData).filter(database.WeatherData.id == data_id).first()
    db.close()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Données non trouvées")
    return data

@app.put("/update-weather-data/{data_id}", response_model=database.WeatherData)
async def update_weather_data(data_id: int, weather_data: WeatherDataUpdate):
    db = database.SessionLocal()
    db_data = db.query(database.WeatherData).filter(database.WeatherData.id == data_id).first()
    if db_data is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Données non trouvées")

    for key, value in weather_data.dict(exclude_unset=True).items():
        setattr(db_data, key, value)

    db.commit()
    db.refresh(db_data)
    db.close()
    return db_data

@app.delete("/delete-weather-data/{data_id}", response_model=dict)
async def delete_weather_data(data_id: int):
    db = database.SessionLocal()
    db_data = db.query(database.WeatherData).filter(database.WeatherData.id == data_id).first()
    if db_data is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Données non trouvées")

    db.delete(db_data)
    db.commit()
    db.close()
    return {"message": "Données supprimées avec succès"}
