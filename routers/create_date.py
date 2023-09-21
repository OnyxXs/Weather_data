from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection
from database.models import Temp

router_create_date = APIRouter()


@router_create_date.post('/create_date', tags=["Temp"])
async def create_date(temp: Temp):
    """
     Crée une nouvelle entrée de date météorologique dans la base de données.

     Args:
         temp (Temp): Un objet Temp contenant les données de la date météorologique.

     Returns:
         dict: Un message de confirmation si la date est créée avec succès.

     Raises:
         HTTPException (400): En cas d'erreur attributaire.
         HTTPException (500): En cas d'autres erreurs inattendues.
     """
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "INSERT INTO Temp (date, Tmin, Tmax, prpc, snow, swnd, awnd, city_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (temp.date, temp.Tmin, temp.Tmax, temp.prpc, temp.snow, temp.swnd, temp.awnd, temp.city_id)
        )
        conn.commit()
        close_database_connection()
        return {"message": "La date a bien été crée"}, 200
    except AttributeError as e:
        conn.rollback()
        return {"error": "Une erreur d'attribut s'est produite.", "details": str(e)}, 400
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


