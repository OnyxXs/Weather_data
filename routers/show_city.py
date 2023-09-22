from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

router_show_city = APIRouter()


@router_show_city.get('/show_city')
async def read_city():
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT * FROM City"
        )
        city = cursor.fetchall()
        close_database_connection()
        if not city:
            raise HTTPException(status_code=404, detail="La Table City ne contient aucune données")
        return {"city": city}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
