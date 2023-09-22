from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

# Création d'un routeur FastAPI pour gérer les opérations liées aux températures
router_show_temp = APIRouter()

@router_show_temp.get('/show_temp')
async def read_temp():
    """
    Récupère toutes les données de température depuis la table "Temp" de la base de données.

    Returns:
        dict: Un dictionnaire contenant les données de température.
            La clé "temp" contient la liste des données de température.
    
    Raises:
        HTTPException: En cas d'erreur 404 si la table "Temp" est vide.
        HTTPException: En cas d'erreur 500 en cas d'exception non gérée.
    """
    try:
        conn, cursor = connect_to_database()  # Établissement d'une connexion à la base de données
        cursor.execute(
            "SELECT * FROM Temp"
        )
        temp = cursor.fetchall()  # Récupération de toutes les données de température depuis la base de données
        close_database_connection()  # Fermeture de la connexion à la base de données
        if not temp:
            raise HTTPException(status_code=404, detail="La Table Temp ne contient aucune données")
        return {"temp": temp}, 200  # Renvoie les données de température sous forme de réponse JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Gestion des exceptions et renvoi d'une erreur 500 en cas de problème
