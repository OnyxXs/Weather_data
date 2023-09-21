from fastapi import HTTPException, APIRouter, Query
from pydantic import BaseModel
from pymysql import Date

from database.database import connect_to_database, close_database_connection
from fastapi import Query
router_create_date = APIRouter()


class Temp(BaseModel):
    date: Date
    Tmin: float
    Tmax: float
    prpc: float
    snow: float
    swnd: float
    awnd: float
    city_id: int


@router_create_date.post('/create_date', tags=["Temp"])
async def create_date(temp: Temp):
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "INSERT INTO Temp (date, Tmin, Tmax, prpc, snow, swnd, awnd, city_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (temp.date, temp.Tmin, temp.Tmax, temp.prpc, temp.snow, temp.swnd, temp.awnd, temp.city_id)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Oui"}, 200
    except AttributeError as e:
        conn.rollback()
        return {"error": "Une erreur d'attribut s'est produite.", "details": str(e)}, 400
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


