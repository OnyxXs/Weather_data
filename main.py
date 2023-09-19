from fastapi import FastAPI
import json

app = FastAPI()

# Charger les données depuis un fichier JSON
def charger_donnees():
    try:
        with open("rdu-weather-history.json", "r") as fichier:
            donnees = json.load(fichier)
        return donnees
    except FileNotFoundError:
        return {"message": "Fichier JSON non trouvé"}
    except json.JSONDecodeError as e:
        return {"error": "Erreur de décodage JSON", "details": str(e)}

# Endpoint pour afficher les données du fichier JSON
@app.get("/afficher-donnees")
async def afficher_donnees():
    donnees = charger_donnees()
    return donnees

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
