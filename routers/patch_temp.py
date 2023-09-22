from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection
from database.models import Temp

router_patch_temp = APIRouter()


@router_patch_temp.patch('/temps/{temp_id}', tags=["Temp"])
def patch_temp(temp_id: int, temp_patch: Temp):
    """
       Met à jour sélectivement les données de date météorologique dans la base de données.

       Args:
           temp_id (int): L'ID de la date météorologique à mettre à jour.
           temp_patch (Temp): Un objet Temp contenant les données à mettre à jour.

       Returns:
           dict: Un message de confirmation si la mise à jour est réussie.

       Raises:
           HTTPException (404): Si la date météorologique avec l'ID spécifié n'est pas trouvée.
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
            raise HTTPException(status_code=404, detail="Température non trouvée")

        # Créez un dictionnaire avec les valeurs à mettre à jour
        update_values = {}
        if temp_patch.date is not None:
            update_values['date'] = temp_patch.date
        if temp_patch.Tmin is not None:
            update_values['Tmin'] = temp_patch.Tmin
        if temp_patch.Tmax is not None:
            update_values['Tmax'] = temp_patch.Tmax
        if temp_patch.prpc is not None:
            update_values['prpc'] = temp_patch.prpc
        if temp_patch.snow is not None:
            update_values['snow'] = temp_patch.snow
        if temp_patch.swnd is not None:
            update_values['swnd'] = temp_patch.swnd
        if temp_patch.awnd is not None:
            update_values['awnd'] = temp_patch.awnd
        if temp_patch.city_id is not None:
            update_values['city_id'] = temp_patch.city_id

        # Mettez à jour les valeurs dans la base de données
        if update_values:
            query = "UPDATE Temp SET "
            query += ", ".join([f"{key} = %s" for key in update_values.keys()])
            query += " WHERE id = %s"
            values = list(update_values.values()) + [temp_id]
            cursor.execute(query, values)
            conn.commit()

        return {"message": "Mise à jour réussie"}
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_database_connection()
