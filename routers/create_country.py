from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection
from database.models import Country

router_create_country = APIRouter()


@router_create_country.post('/countries', tags=["Country"])
async def create_country(country: Country):
    """
     Crée un nouveau pays dans la base de données.

     Args:
         country (Country): Un objet Country contenant les données du pays.

     Returns:
         dict: Un message de confirmation si le pays est créé avec succès.

     Raises:
         HTTPException (400): En cas d'erreur attributaire.
         HTTPException (500): En cas d'autres erreurs inattendues.
     """
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "INSERT INTO Country (name) VALUES (%s)",
            (country.name,)
        )
        conn.commit()
        close_database_connection()
        return {"message": "Le pays a bien été crée"}, 200
    except AttributeError as e:
        conn.rollback()
        return {"error": "Une erreur d'attribut s'est produite.", "details": str(e)}, 400
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))


