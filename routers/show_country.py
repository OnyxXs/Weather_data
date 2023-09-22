from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

# Création d'un routeur FastAPI pour gérer les opérations liées aux pays
router_show_country = APIRouter()

@router_show_country.get('/show_country')
async def read_country():
    """
    Récupère toutes les données des pays depuis la table "Country" de la base de données.

    Returns:
        dict: Un dictionnaire contenant les données des pays.
            La clé "country" contient la liste des données des pays.
    
    Raises:
        HTTPException: En cas d'erreur 404 si la table "Country" est vide.
        HTTPException: En cas d'erreur 500 en cas d'exception non gérée.
    """
    try:
        conn, cursor = connect_to_database()  # Établissement d'une connexion à la base de données
        cursor.execute(
            "SELECT * FROM Country"
        )
        country = cursor.fetchall()  # Récupération de toutes les données des pays depuis la base de données
        close_database_connection()  # Fermeture de la connexion à la base de données
        if not country:
            raise HTTPException(status_code=404, detail="La Table Country ne contient aucune données")
        return {"country": country}, 200  # Renvoie les données des pays sous forme de réponse JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Gestion des exceptions et renvoi d'une erreur 500 en cas de problème
