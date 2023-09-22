from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection
from database.models import City

router_modif_city = APIRouter()


@router_modif_city.put('/city/{city_id}', tags=["City"])
def modif_city(city_id: int, city: City):
    """
       Met à jour les données de City dans la base de données.

       Args:
           city_id (int): L'ID de la date météorologique à mettre à jour.
           city (City): Un objet City contenant les anciennes données

       Returns:
           dict: Un message de confirmation si la mise à jour est réussie.

       Raises:
           HTTPException (404): Si la country avec l'ID spécifié n'est pas trouvée.
           HTTPException (400): Si les données d'entrée ne sont pas valides.
           HTTPException (500): En cas d'autres erreurs inattendues lors de la mise à jour.
    """
    conn, cursor = connect_to_database()
    try:
        if not isinstance(city_id, int) or city_id <= 0:
            raise HTTPException(status_code=400, detail="ID de city invalide")
        if not city.name:
            raise HTTPException(status_code=400, detail="Le nom de la city ne peut pas être vide")
        query = "SELECT * FROM City WHERE id = %s"
        cursor.execute(query, (city_id,))
        city_table = cursor.fetchone()
        if not city_table:
            raise HTTPException(status_code=404, detail="Ville non trouvé")
        query = "UPDATE City SET name = %s, country_id = %s WHERE id = %s"
        values = (city.name, city.country_id, city_id)
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Mise à jour réussie"}
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_database_connection()
