from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

router_order_by_tmax = APIRouter()


@router_order_by_tmax.get('/order_by_tmax')
async def order_by_tmax():
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT date,Tmax FROM temp ORDER BY Tmax"
        )
        order_tmax = cursor.fetchall()
        close_database_connection()
        if not order_tmax:
            raise HTTPException(status_code=404, detail="Aucune données météorologiques")
        return {"date_order_tmax": order_tmax}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
