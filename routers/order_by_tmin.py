from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

router_order_by_tmin = APIRouter()


@router_order_by_tmin.get('/order_by_tmin')
async def order_by_tmin():
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT date,Tmin FROM temp ORDER BY Tmin"
        )
        order_tmin = cursor.fetchall()
        close_database_connection()
        if not order_tmin:
            raise HTTPException(status_code=404, detail="Aucune données météorologiques")
        return {"date_order_tmin": order_tmin}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
