from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

router_country = APIRouter()


@router_country.get('/country')
async def read_country():
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT * FROM country"
        )
        country = cursor.fetchall()
        close_database_connection()
        if not country:
            raise HTTPException(status_code=404, detail="Aucune boisson trouvée pour cet utilisateur")
        return {"country": country}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
