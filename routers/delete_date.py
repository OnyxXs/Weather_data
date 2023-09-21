from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection
from database.models import Temp

router_delete_date = APIRouter()

@router_delete_date.delete('/delete_date/{temp_id}')
async def delete_temp(temp_id: int):
    conn, cursor = connect_to_database()
    try:
        query = "SELECT * FROM Temp WHERE id = %s"
        cursor.execute(query, (temp_id,))
        temp_table = cursor.fetchone()
        if not temp_table:
            raise HTTPException(status_code=404, detail="Température non trouvé")
        cursor.execute("DELETE FROM Temp WHERE id = %s", (temp_id,))
        conn.commit()
        return {"message": "Température supprimée avec succès"}, 200
    except Exception as e:
        raise e
    finally:
        close_database_connection()