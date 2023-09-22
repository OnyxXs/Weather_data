from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

# Création d'un routeur FastAPI pour gérer les opérations liées aux villes
router_show_city = APIRouter()

@router_show_city.get('/show_city')
async def read_city():
    """
    Récupère toutes les données des villes depuis la table "City" de la base de données.

    Returns:
        dict: Un dictionnaire contenant les données des villes.
            La clé "city" contient la liste des données des villes.
    
    Raises:
        HTTPException: En cas d'erreur 404 si la table "City" est vide.
        HTTPException: En cas d'erreur 500 en cas d'exception non gérée.
    """
    try:
        conn, cursor = connect_to_database()  # Établissement d'une connexion à la base de données
        cursor.execute(
            "SELECT * FROM City"
        )
        city = cursor.fetchall()  # Récupération de toutes les données des villes depuis la base de données
        close_database_connection()  # Fermeture de la connexion à la base de données
        if not city:
            raise HTTPException(status_code=404, detail="La Table City ne contient aucune données")
        return {"city": city}, 200  # Renvoie les données des villes sous forme de réponse JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Gestion des exceptions et renvoi d'une erreur 500 en cas de problème
