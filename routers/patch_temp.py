from fastapi import HTTPException, APIRouter
from pydantic import BaseModel  # Importez BaseModel pour définir le modèle de données d'entrée
from database.database import connect_to_database, close_database_connection
from database.models import City

router_patch_temp = APIRouter()

# Créez un modèle Pydantic pour les données de mise à jour partielle


@router_patch_temp.patch('/cities/{city_id}', tags=["City"])
def patch_city(city_id: int, city_update: City):
    """
       Met à jour partiellement les données de City dans la base de données.

       Args:
           city_id (int): L'ID de la date météorologique à mettre à jour.
           city_update (CityUpdate): Un objet CityUpdate contenant les données à mettre à jour.

       Returns:
           dict: Un message de confirmation si la mise à jour est réussie.

       Raises:
           HTTPException (404): Si la city avec l'ID spécifié n'est pas trouvée.
           HTTPException (400): Si les données d'entrée ne sont pas valides.
           HTTPException (500): En cas d'autres erreurs inattendues lors de la mise à jour.
    """
    conn, cursor = connect_to_database()
    try:
        if not isinstance(city_id, int) or city_id <= 0:
            raise HTTPException(status_code=400, detail="ID de city invalide")

        # Vous pouvez maintenant mettre à jour partiellement la ville en fonction des données de city_update
        query = "SELECT * FROM City WHERE id = %s"
        cursor.execute(query, (city_id,))
        city_table = cursor.fetchone()
        if not city_table:
            raise HTTPException(status_code=404, detail="Ville non trouvée")

        # Mettez à jour les champs de la ville en fonction de city_update
        if city_update.name:
            city_table["name"] = city_update.name
        if city_update.country_id:
            city_table["country_id"] = city_update.country_id

        # Mettez à jour la base de données avec les nouvelles valeurs
        query = "UPDATE City SET name = %s, country_id = %s WHERE id = %s"
        values = (city_table["name"], city_table["country_id"], city_id)
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Mise à jour réussie"}
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_database_connection()
