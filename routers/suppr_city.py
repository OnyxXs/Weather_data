from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

# Création d'un routeur FastAPI pour gérer la suppression de données de température par ID
router_suppr_city = APIRouter()


@router_suppr_city.delete('/delete_city/{city_id}')
async def delete_city(city_id: int):
    """
    Supprime une entrée de données de température de la table "City" de la base de données
    en utilisant l'ID spécifié.

    Args:
        city_id (int): L'ID de l'entrée de données de température à supprimer.

    Returns:
        dict: Un dictionnaire contenant un message de confirmation de la suppression.

    Raises:
        HTTPException: En cas d'erreur 404 si l'entrée de données de city n'est pas trouvée.
        Exception: En cas d'exception non gérée.
    """
    conn, cursor = connect_to_database()  # Établissement d'une connexion à la base de données
    try:
        query = "SELECT * FROM City WHERE id = %s"
        cursor.execute(query, (city_id,))
        city_table = cursor.fetchone()  # Recherche de l'entrée de données de city par ID
        if not city_table:
            raise HTTPException(status_code=404, detail="city non trouvée")
        cursor.execute("DELETE FROM city WHERE id = %s", (city_id,))  # Suppression de l'entrée de données de city
        conn.commit()  # Validation des modifications dans la base de données
        return {"message": "city supprimée avec succès"}, 200  # Renvoie un message de confirmation
    except AttributeError as e:
        raise HTTPException(status_code=404, detail=str(e))  # Gestion des exceptions et renvoi d'une erreur 500 en cas de problème
    finally:
        close_database_connection()  # Fermeture de la connexion à la base de données en toutes circonstances
