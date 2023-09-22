from fastapi import HTTPException, APIRouter
from database.database import connect_to_database, close_database_connection

# Création d'un routeur FastAPI pour la gestion des requêtes liées à l'ordre par précipitations
router_order_by_prpc = APIRouter()

@router_order_by_prpc.get('/order_by_prpc')
async def order_by_prpc():
    """
    Gère la requête GET pour obtenir des données météorologiques triées par précipitations.

    Raises:
        HTTPException: En cas d'erreur, renvoie une réponse HTTP appropriée avec un code d'erreur.

    Returns:
        dict: Un dictionnaire contenant les données météorologiques triées par précipitations et leur date.
    """
    try:
        # Établit une connexion à la base de données
        conn, cursor = connect_to_database()

        # Exécute une requête SQL pour sélectionner les données météorologiques dans la table 'temp' triées par prpc
        cursor.execute(
            "SELECT date, prpc FROM `temp` ORDER BY prpc"
        )

        # Récupère les résultats de la requête
        order_prpc = cursor.fetchall()

        # Ferme la connexion à la base de données
        close_database_connection()

        # Si aucune donnée n'a été trouvée, lève une exception HTTP avec un code 404
        if not order_prpc:
            raise HTTPException(status_code=404, detail="Aucune données météorologiques")

        # Retourne les données météorologiques triées par précipitations et leur date sous forme de dictionnaire
        return {"date_order_by_prpc": order_prpc}, 200

    except Exception as e:
        # En cas d'erreur non prévue, lève une exception HTTP avec un code 500 et détaille l'erreur
        raise HTTPException(status_code=500, detail=str(e))