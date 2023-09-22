from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection


# Création d'un routeur FastAPI pour gérer la suppression de données de température par ID
router_suppr_country = APIRouter()


@router_suppr_country.delete('/delete_country/{country_id}')
async def delete_country(country_id: int):
    """
    Supprime une entrée de données de température de la table "Temp" de la base de données
    en utilisant l'ID spécifié.

    Args:
        country_id (int): L'ID de l'entrée de données de température à supprimer.

    Returns:
        dict: Un dictionnaire contenant un message de confirmation de la suppression.

    Raises:
        HTTPException: En cas d'erreur 404 si l'entrée de données de Country n'est pas trouvée.
        Exception: En cas d'exception non gérée.
    """
    conn, cursor = connect_to_database()  # Établissement d'une connexion à la base de données
    try:
        query = "SELECT * FROM Country WHERE id = %s"
        cursor.execute(query, (country_id,))
        country_table = cursor.fetchone()  # Recherche de l'entrée de données de country par ID
        if not country_table:
            raise HTTPException(status_code=404, detail="Country non trouvée")
        cursor.execute("DELETE FROM Country WHERE id = %s", (country_id,))  # Supp de données de country par ID
        conn.commit()  # Validation des modifications dans la base de données
        return {"message": "Country supprimée avec succès"}, 200  # Renvoie un message de confirmation
    except Exception as e:
        raise e  # Gestion des exceptions et renvoi de l'exception en cas de problème
    finally:
        close_database_connection()  # Fermeture de la connexion à la base de données en toutes circonstances
