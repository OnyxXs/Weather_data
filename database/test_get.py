from fastapi import FastAPI
from pydantic import BaseModel
from database import get_database_connection  # Importez la fonction de connexion depuis database.py

app = FastAPI()


# Route GET pour récupérer la première ligne de la table "city"
@app.get("/country")
def get_first_city():
    try:
        connection = get_database_connection()  # Utilisez la fonction de connexion
        if connection and connection.is_connected():
            cursor = connection.cursor()
            cursor.execute("SELECT name FROM country LIMIT 1;")
            row = cursor.fetchone()
            if row:
                name = row
                return {"name": name}
            else:
                return {"message": "No data found in 'country' table."}
    except Exception as e:
        return {"error": f"Error while connecting to MySQL: {str(e)}"}
