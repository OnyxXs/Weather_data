from fastapi import HTTPException, APIRouter, Query
from database.database import connect_to_database, close_database_connection

router_average_min_temp = APIRouter()


@router_average_min_temp.get('/average_min_temp')
async def average_min_temp(city_id: int = Query(..., description="ID de la ville pour la moyenne Tmin")):
    """
    Calcule la moyenne des températures minimales (Tmin) pour une ville spécifiée.

    Args:
        city_id (int): L'identifiant de la ville pour laquelle calculer la moyenne Tmin.

    Returns:
        dict: Un dictionnaire contenant la moyenne des températures minimales calculée.
            - "average_min_temp" (float): La moyenne des températures minimales (Tmin).

    Raises:
        HTTPException:
            - 404: Si aucune donnée météorologique n'est disponible pour la ville spécifiée.
            - 500: Si une erreur inattendue se produit lors de l'accès à la base de données.
    """
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT AVG(Tmin) as average_min_temp FROM temp WHERE city_id = %s",
            (city_id,)
        )
        data_average_min_temp = cursor.fetchone()
        close_database_connection()
        if not data_average_min_temp:
            raise HTTPException(status_code=404, detail="Aucune donnée météorologique pour la ville spécifiée")
        return {"average_min_temp": data_average_min_temp['average_min_temp']}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
