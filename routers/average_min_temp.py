from fastapi import HTTPException, APIRouter, Query
from database.database import connect_to_database, close_database_connection

router_average_min_temp = APIRouter()


@router_average_min_temp.get('/average_min_temp')
async def average_min_temp(city_id: int = Query(..., description="ID de la ville pour la moyenne Tmin")):
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT AVG(Tmin) as average_min_temp FROM temp WHERE city_id = %s",
            (city_id,)
        )
        data_average_min_temp = cursor.fetchone()
        close_database_connection()
        if not data_average_min_temp:
            raise HTTPException(status_code=404, detail="Aucune données météorologiques pour la ville spécifiée")
        return {"average_min_temp": data_average_min_temp['average_min_temp']}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))