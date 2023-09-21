from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

router_order_by_prpc = APIRouter()


@router_order_by_prpc.get('/order_by_prpc')
async def order_by_prpc():
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT date,prpc FROM `temp` ORDER BY prpc"
        )
        order_prpc = cursor.fetchall()
        close_database_connection()
        if not order_prpc:
            raise HTTPException(status_code=404, detail="Aucune données météorologiques")
        return {"date_order_by_prpc": order_prpc}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
