from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection
from database.models import Temp

router_modif_temp = APIRouter()


@router_modif_temp.put('/temp/{temp_id}')
def modif_temp(temp_id: int, temp: Temp):
    """
       Met à jour les données de date météorologique dans la base de données.

       Args:
           temp_id (int): L'ID de la date météorologique à mettre à jour.
           temp (Temp): Un objet Temp contenant les nouvelles données de la date météorologique.

       Returns:
           dict: Un message de confirmation si la mise à jour est réussie.

       Raises:
           HTTPException (404): Si la country avec l'ID spécifié n'est pas trouvée.
           HTTPException (400): Si les données d'entrée ne sont pas valides.
           HTTPException (500): En cas d'autres erreurs inattendues lors de la mise à jour.
    """
    conn, cursor = connect_to_database()
    try:
        if not isinstance(temp_id, int) or temp_id <= 0:
            raise HTTPException(status_code=400, detail="ID de temp invalide")
        query = "SELECT * FROM Temp WHERE id = %s"
        cursor.execute(query, (temp_id,))
        temp_table = cursor.fetchone()
        if not temp_table:
            raise HTTPException(status_code=404, detail="Température non trouvé")
        query = "UPDATE Temp SET date = %s, Tmin = %s, Tmax = %s, prpc = %s, snow = %s, swnd = %s, awnd = %s, city_id = %s WHERE id = %s"
        values = (temp.date, temp.Tmin, temp.Tmax, temp.prpc, temp.snow, temp.swnd, temp.awnd, temp.city_id, temp_id)
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Mise à jour réussie"}
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_database_connection()

