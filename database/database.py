from decouple import config
from databases import Database
from fastapi import FastAPI
import os
from dotenv import load_dotenv

# Créer une instance de base de données à partir de l'URL de la base de données (qui est dans le fichier env)


def create_database_instance():
    load_dotenv()
    database_url = os.environ.get("DATABASE_URL")
    return Database(database_url)


database = create_database_instance()
app = FastAPI()


# fonction d'événement pour démarrer la connexion à la bdd au démarrage de l'application
@app.on_event("startup")
async def startup_db_client():
    await database.connect()


#  fonction d'événement pour arréter la connexion à la bddd à l'arrêt de l'application
@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()
