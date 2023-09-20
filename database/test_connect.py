from fastapi import FastAPI
from database.database import SessionLocal


app = FastAPI()


# Votre code FastAPI

@app.get("/")
async def read_root():
    # Créez une session SQLAlchemy pour interagir avec la base de données
    db = SessionLocal()

    try:
        # Exemple : Effectuez une requête pour récupérer des données depuis la base de données
        result = db.execute("SELECT * FROM city").fetchall()
        return {"data": result}
    except Exception as e:
        return {"error": str(e)}
    finally:
        # Fermez la session lorsque vous avez terminé
        db.close()
