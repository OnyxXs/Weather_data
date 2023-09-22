from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

# Création d'un routeur FastAPI pour gérer la suppression de données de température par ID
router_suppr_date = APIRouter()


@router_suppr_date.delete('/temp/{temp_id}', tags=["Temp"])
async def suppr_temp(temp_id: int):
    """
    Supprime une entrée de données de température de la table "Temp" de la base de données
    en utilisant l'ID spécifié.

    Args:
        temp_id (int): L'ID de l'entrée de données de température à supprimer.

    Returns:
        dict: Un dictionnaire contenant un message de confirmation de la suppression.

    Raises:
        HTTPException: En cas d'erreur 404 si l'entrée de données de température n'est pas trouvée.
        Exception: En cas d'exception non gérée.
    """
    conn, cursor = connect_to_database()  # Établissement d'une connexion à la base de données
    try:
        query = "SELECT * FROM Temp WHERE id = %s"
        cursor.execute(query, (temp_id,))
        temp_table = cursor.fetchone()  # Recherche de l'entrée de données de température par ID
        if not temp_table:
            raise HTTPException(status_code=404, detail="Température non trouvée")
        cursor.execute("DELETE FROM Temp WHERE id = %s", (temp_id,))  # Suppression de l'entrée de données de température par ID
        conn.commit()  # Validation des modifications dans la base de données
        return {"message": "Température supprimée avec succès"}, 200  # Renvoie un message de confirmation
    except AttributeError as e:
        raise HTTPException(status_code=404,detail=str(e))  # Gestion des exceptions et renvoi d'une erreur 500 en cas de problème
    finally:
        close_database_connection()  # Fermeture de la connexion à la base de données en toutes circonstances
