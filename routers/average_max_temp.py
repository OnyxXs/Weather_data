from fastapi import HTTPException, APIRouter, Query
from database.database import connect_to_database, close_database_connection

router_average_max_temp = APIRouter()


@router_average_max_temp.get('/average_max_temp')
async def average_max_temp(city_id: int = Query(..., description="ID de la ville pour la moyenne Tmax")):
    """
    Calcule la moyenne des températures maximales (Tmax) pour une ville spécifiée.

    Args:
        city_id (int): L'identifiant de la ville pour laquelle calculer la moyenne Tmax.

    Returns:
        dict: Un dictionnaire contenant la moyenne des températures maximales calculée.
            - "average_max_temp" (float): La moyenne des températures maximales (Tmax).

    Raises:
        HTTPException:
            - 404: Si aucune donnée météorologique n'est disponible pour la ville spécifiée.
            - 500: Si une erreur inattendue se produit lors de l'accès à la base de données.
    """
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT AVG(Tmax) as average_max_temp FROM temp WHERE city_id = %s",
            (city_id,)
        )
        data_average_max_temp = cursor.fetchone()
        close_database_connection()
        if not data_average_max_temp:
            raise HTTPException(status_code=404, detail="Aucune donnée météorologique pour la ville spécifiée")
        return {"average_max_temp": data_average_max_temp['average_max_temp']}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
