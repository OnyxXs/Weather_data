from fastapi import FastAPI, APIRouter
from database.test import router_country
from routers.weather_by_date import router_weather_by_date
from routers.create_date import router_create_date
from routers.modif_date import router_modif_date
from routers.delete_date import router_delete_date
from routers.order_by_prpc import router_order_by_prpc
from routers.order_by_tmax import router_order_by_tmax
from routers.order_by_tmin import router_order_by_tmin

app = FastAPI()


app.include_router(router_country)
app.include_router(router_weather_by_date)
app.include_router(router_create_date)
app.include_router(router_modif_date)
app.include_router(router_delete_date)
app.include_router(router_order_by_prpc)
app.include_router(router_order_by_tmax)
app.include_router(router_order_by_tmin)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)



