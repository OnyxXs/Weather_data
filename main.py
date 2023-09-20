# Importation des modules nécessaires depuis FastAPI, SQLAlchemy et d'autres bibliothèques.
from fastapi import FastAPI, Query, HTTPException, Depends, status
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

# Configuration de la base de données
DATABASE_URL = "mysql+mysqlconnector://localhost:8889/la_base_de_données"
engine = create_engine(DATABASE_URL)  # Création d'un moteur de base de données SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Création d'une session SQLAlchemy

# Définition de la classe de base pour les modèles SQLAlchemy
Base = declarative_base()

# Définition du modèle SQLAlchemy pour les données météorologiques
class WeatherData(Base):
    __tablename__ = "weather_data"  # Nom de la table dans la base de données

    # Définition des colonnes de la table avec leurs types de données
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=datetime.utcnow)  # Utilisation de la date actuelle comme valeur par défaut
    tmin = Column(Float)
    tmax = Column(Float)
    prcp = Column(Float)
    snow = Column(Float)
    snwd = Column(Float)
    awnd = Column(Float)

# Création de la table dans la base de données (vous ne devez le faire qu'une fois)
Base.metadata.create_all(bind=engine)

# Définition des modèles Pydantic pour la validation des données lors de l'ajout et de la mise à jour
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

# Création d'une instance FastAPI
app = FastAPI()

# Endpoint pour ajouter de nouvelles données météorologiques dans la base de données
@app.post("/add-weather-data", response_model=WeatherData)  # Utilisation de WeatherData comme modèle de réponse
async def add_weather_data(weather_data: WeatherDataCreate):
    db = SessionLocal()  # Création d'une session SQLAlchemy
    db_data = WeatherData(**weather_data.dict())  # Création d'une instance de modèle SQLAlchemy
    db.add(db_data)  # Ajout de l'instance à la session
    db.commit()  # Validation des modifications dans la base de données
    db.refresh(db_data)  # Rafraîchissement de l'instance avec les données de la base de données
    db.close()  # Fermeture de la session
    return db_data  # Renvoi des données ajoutées

# Endpoint pour obtenir toutes les données météorologiques
@app.get("/all-weather-data", response_model=List[WeatherData])
async def get_all_weather_data(skip: int = Query(0, description="Index de début"), limit: int = Query(10, description="Nombre maximum de données à retourner")):
    db = SessionLocal()  # Création d'une session SQLAlchemy
    data = db.query(WeatherData).offset(skip).limit(limit).all()  # Requête pour récupérer les données avec pagination
    db.close()  # Fermeture de la session
    return data  # Renvoi des données récupérées

# Endpoint pour obtenir une seule entrée de données météorologiques par ID
@app.get("/weather-data/{data_id}", response_model=WeatherData)
async def get_weather_data(data_id: int):
    db = SessionLocal()  # Création d'une session SQLAlchemy
    data = db.query(WeatherData).filter(WeatherData.id == data_id).first()  # Requête pour récupérer une entrée par ID
    db.close()  # Fermeture de la session
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Données non trouvées")  # Exception si les données ne sont pas trouvées
    return data  # Renvoi des données récupérées

# Endpoint pour mettre à jour des données météorologiques par ID
@app.put("/update-weather-data/{data_id}", response_model=WeatherData)
async def update_weather_data(data_id: int, weather_data: WeatherDataUpdate):
    db = SessionLocal()  # Création d'une session SQLAlchemy
    db_data = db.query(WeatherData).filter(WeatherData.id == data_id).first()  # Requête pour récupérer une entrée par ID
    if db_data is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Données non trouvées")  # Exception si les données ne sont pas trouvées

    for key, value in weather_data.dict(exclude_unset=True).items():
        setattr(db_data, key, value)  # Mise à jour des données

    db.commit()  # Validation des modifications dans la base de données
    db.refresh(db_data)  # Rafraîchissement de l'instance avec les données de la base de données
    db.close()  # Fermeture de la session
    return db_data  # Renvoi des données mises à jour

# Endpoint pour supprimer des données météorologiques par ID
@app.delete("/delete-weather-data/{data_id}", response_model=dict)
async def delete_weather_data(data_id: int):
    db = SessionLocal() 
    db_data = db.query(WeatherData).filter(WeatherData.id == data_id).first()  # Requête pour récupérer une entrée par ID
    if db_data is None:
        db.close()
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Données non trouvées")  # Exception si les données ne sont pas trouvées

    db.delete(db_data)  # Suppression des données
    db.commit()  # Validation des modifications dans la base de données
    db.close()  # Fermeture de la session
    return {"message": "Données supprimées avec succès"}  # Message de confirmation
