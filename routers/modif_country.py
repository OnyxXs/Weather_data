from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection
from database.models import Country

router_modif_country = APIRouter()


@router_modif_country.put('/country/{country_id}')
def modif_country(country_id: int, country: Country):
    """
       Met à jour les données de Country dans la base de données.

       Args:
           country_id (int): L'ID de la date météorologique à mettre à jour.
           country (Country): Un objet Country contenant les anciennes données

       Returns:
           dict: Un message de confirmation si la mise à jour est réussie.

       Raises:
           HTTPException (404): Si la country avec l'ID spécifié n'est pas trouvée.
           HTTPException (400): Si les données d'entrée ne sont pas valides.
           HTTPException (500): En cas d'autres erreurs inattendues lors de la mise à jour.
    """
    conn, cursor = connect_to_database()
    try:
        # Valider les données d'entrée
        if not isinstance(country_id, int) or country_id <= 0:
            raise HTTPException(status_code=400, detail="ID de pays invalide")
        if not country.name:
            raise HTTPException(status_code=400, detail="Le nom du pays ne peut pas être vide")

        query = "SELECT * FROM Country WHERE id = %s"
        cursor.execute(query, (country_id,))
        country_table = cursor.fetchone()
        if not country_table:
            raise HTTPException(status_code=404, detail="Pays non trouvé")
        query = "UPDATE Country SET name = %s WHERE id = %s"
        values = (country.name, country_id)
        cursor.execute(query, values)
        conn.commit()
        return {"message": "Mise à jour réussie"}
    except HTTPException as http_error:
        raise http_error
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        close_database_connection()
