from fastapi import HTTPException, APIRouter, Query
from database.database import connect_to_database, close_database_connection

router_average_temp_country = APIRouter()


@router_average_temp_country.get('/average_temp_by_country')
async def average_temp_by_country(country_id: int = Query(..., description="ID du pays pour la moyenne des températures")):
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT AVG((temp.Tmin + temp.Tmax) / 2) as average_temp "
            "FROM temp "
            "INNER JOIN city ON temp.city_id = city.id "
            "WHERE city.country_id = %s",
            (country_id,)
        )
        average_temp_result = cursor.fetchone()
        close_database_connection()
        if not average_temp_result:
            raise HTTPException(status_code=404, detail="Aucune données météorologiques pour le pays spécifié")
        return {"average_temp": average_temp_result['average_temp']}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
