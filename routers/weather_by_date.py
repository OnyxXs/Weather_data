from fastapi import HTTPException, APIRouter, Query
from database.database import connect_to_database, close_database_connection
from fastapi import Query
router_weather_by_date = APIRouter()


@router_weather_by_date.get('/weather_by_date')
async def read_weather_by_date(
    start_date: str = Query(..., description="Date de début : "),
    end_date: str = Query(..., description="Date de fin : ")
):
    """
          Obtenez des données météorologiques filtrées en fonction des dates spécifiées.

          Args:
              start_date (str): Date de début pour la filtration.
              end_date (str): Date de fin pour la filtration.

          Returns:
              tuple: Un tuple contenant le dictionnaire des données météorologiques avec la clé "weather"
               et le code de statut HTTP (200 en cas de succès).
    """
    try:
        conn, cursor = connect_to_database()
        cursor.execute(
            "SELECT * FROM temp WHERE date > %s AND date < %s",
            (start_date, end_date)
        )
        weather = cursor.fetchall()
        close_database_connection()
        if not weather:
            raise HTTPException(status_code=404, detail="Aucune donnéees météorologiques trouvées")
        return {"weather": weather}, 200
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


