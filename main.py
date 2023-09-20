from fastapi import FastAPI, Query, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# Configuration de la base de données
DATABASE_URL = "mysql+mysqlconnector://localhost:8889/la_base_de_données"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modèle de données SQLAlchemy
Base = declarative_base()

class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)
    tmin = Column(Float)
    tmax = Column(Float)
    prcp = Column(Float)
    snow = Column(Float)
    snwd = Column(Float)
    awnd = Column(Float)

# Création de la table dans la base de données (vous ne devez le faire qu'une fois)
Base.metadata.create_all(bind=engine)

# Modèle Pydantic pour la validation des données lors de l'ajout
class WeatherDataCreate(BaseModel):
    tmin: float
    tmax: float
    prcp: float
    snow: float
    snwd: float
    awnd: float

# Modèle Pydantic pour la validation des données lors de la mise à jour
class WeatherDataUpdate(BaseModel):
    tmin: Optional[float] = None
    tmax: Optional[float] = None
    prcp: Optional[float] = None
    snow: Optional[float] = None
    snwd: Optional[float] = None
    awnd: Optional[float] = None

app = FastAPI()

# Endpoint pour ajouter de nouvelles données météorologiques dans la base de données
@app.post("/add-weather-data", response_model=WeatherData)
async def add_weather_data(weather_data: WeatherDataCreate):
    db = SessionLocal()
    db_data = WeatherData(**weather_data.dict())
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    db.close()
    return db_data

# Endpoint pour obtenir toutes les données météorologiques
@app.get("/all-weather-data", response_model=List[WeatherData])
async def get_all_weather_data(skip: int = Query(0, description="Index de début"), limit: int = Query(10, description="Nombre maximum de données à retourner")):
    db = SessionLocal()
    data = db.query(WeatherData).offset(skip).limit(limit).all()
    db.close()
    return data

# Endpoint pour obtenir une seule entrée de données météorologiques par ID
@app.get("/weather-data/{data_id}", response_model=WeatherData)
async def get_weather_data(data_id: int):
    db = SessionLocal()
    data = db.query(WeatherData).filter(WeatherData.id == data_id).first()
    db.close()
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Données non trouvées")
    return data

# Endpoint pour mettre à jour des données météorologiques par ID
@app.put("/update-weather-data/{data_id}", response_model=WeatherData)
async def update_weather_data(data_id: int, weather_data: WeatherDataUpdate):
    db = SessionLocal()
    db_data = db.query(WeatherData).filter(WeatherData.id == data_id).first()
    if db_data is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Données non trouvées")

    for key, value in weather_data.dict(exclude_unset=True).items():
        setattr(db_data, key, value)

    db.commit()
    db.refresh(db_data)
    db.close()
    return db_data

# Endpoint pour supprimer des données météorologiques par ID
@app.delete("/delete-weather-data/{data_id}", response_model=dict)
async def delete_weather_data(data_id: int):
    db = SessionLocal()
    db_data = db.query(WeatherData).filter(WeatherData.id == data_id).first()
    if db_data is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Données non trouvées")

    db.delete(db_data)
    db.commit()
    db.close()
    return {"message": "Données supprimées avec succès"}

