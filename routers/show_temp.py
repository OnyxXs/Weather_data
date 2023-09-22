from fastapi import HTTPException, APIRouter, Query
from database.database import connect_to_database, close_database_connection

# Création d'un routeur FastAPI pour gérer les opérations liées aux températures
router_show_temp = APIRouter()


@router_show_temp.get('/temp', tags=["Temp"])
async def read_temp(page_number: int = Query(1, description="Numéro de la page"),
                    rows_per_page: int = Query(..., description="Nombre de lignes par page")):
    """
    Récupère toutes les données de température depuis la table "Temp" de la base de données. Paginée

    Args:
        page_number (int): Numéro de la page (par défaut : 1).
        rows_per_page (int): Nombre de lignes par page (par défaut : 10).

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
            f"SELECT * FROM Temp "
            f"LIMIT {rows_per_page} OFFSET {(page_number - 1) * rows_per_page}"
        )
        temp = cursor.fetchall()  # Récupération de toutes les données de température depuis la base de données
        close_database_connection()  # Fermeture de la connexion à la base de données
        if not temp:
            raise HTTPException(status_code=404, detail="La Table Temp ne contient aucune données")
        return {"temp": temp}, 200  # Renvoie les données de température sous forme de réponse JSON
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))  # Gestion des exceptions et renvoi d'une erreur 500 en cas de problème
