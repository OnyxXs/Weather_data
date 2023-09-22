from fastapi import HTTPException, APIRouter, Query
from database.database import connect_to_database, close_database_connection

router_absolute_average = APIRouter()


@router_absolute_average.get('/absolute_average')
async def average_temp(city_id: int = Query(..., description="ID de la ville pour calculer la moyenne de la température minimale et maximale")):
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT AVG((Tmin + Tmax) / 2) as average_temp FROM temp WHERE city_id = %s",
            (city_id,)
        )
        average_temp_result = cursor.fetchone()
        close_database_connection()
        if not average_temp_result:
            raise HTTPException(status_code=404, detail="Aucune données météorologiques pour la ville spécifiée")
        return {"average_temp": average_temp_result['average_temp']}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

