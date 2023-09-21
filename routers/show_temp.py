from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

router_show_temp = APIRouter()


@router_show_temp.get('/show_temp')
async def read_temp():
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT * FROM Temp"
        )
        temp = cursor.fetchall()
        close_database_connection()
        if not temp:
            raise HTTPException(status_code=404, detail="La Table Temp ne contient aucune données")
        return {"temp": temp}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
