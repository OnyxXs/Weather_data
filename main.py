from fastapi import FastAPI, APIRouter
from database.test import router_country
from routers.weather_by_date import router_weather_by_date

app = FastAPI()


app.include_router(router_country)
app.include_router(router_weather_by_date)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)



