from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection
from database.models import City

router_create_city = APIRouter()


@router_create_city.post('/cities', tags=["City"])
async def create_city(city: City):
    """
     Crée une nouvelle ville dans la base de données.

     Args:
         city (City): Un objet City contenant les données de la ville.

     Returns:
         dict: Un message de confirmation si la ville est créée avec succès.

     Raises:
         HTTPException (400): En cas d'erreur attributaire.
         HTTPException (500): En cas d'autres erreurs inattendues.
     """
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "INSERT INTO City (name, country_id) VALUES (%s, %s)",
            (city.name, city.country_id)
        )
        conn.commit()
        close_database_connection()
        return {"message": "La ville a bien été crée"}, 200
    except AttributeError as e:
        conn.rollback()
        return {"error": "Une erreur d'attribut s'est produite.", "details": str(e)}, 400
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


