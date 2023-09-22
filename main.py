from fastapi import FastAPI
from starlette.requests import Request

# import des modules de route
from routers.show_temp import router_show_temp
from routers.show_city import router_show_city
from routers.show_country import router_show_country
from routers.weather_by_date import router_weather_by_date
from routers.create_date import router_create_date
from routers.create_city import router_create_city
from routers.create_country import router_create_country
from routers.modif_temp import router_modif_temp
from routers.modif_city import router_modif_city
from routers.modif_country import router_modif_country
from routers.suppr_date import router_suppr_date
from routers.order_by_prpc import router_order_by_prpc
from routers.order_by_tmax import router_order_by_tmax
from routers.order_by_tmin import router_order_by_tmin
from routers.order_by_snow import router_order_by_snow
from routers.order_by_swnd import router_order_by_swnd
from routers.order_by_awnd import router_order_by_awnd
from routers.average_min_temp import router_average_min_temp
from routers.average_max_temp import router_average_max_temp
from routers.absolute_average import router_absolute_average
from routers.average_temp_country import router_average_temp_country
from routers.suppr_city import router_suppr_city
from routers.suppr_country import router_suppr_country
from routers.patch_temp import router_patch_temp


app = FastAPI()
# compteur global de routes et définition des routes à exclures
route_counter = 0
excluded_routes = ["/redoc", "/openapi.json", "/docs"]


# Middleware personnalisé pour compter les routes
@app.middleware("http")
async def count_routes(request: Request, call_next):
    global route_counter
    if request.url.path not in excluded_routes:
        route_counter += 1
        print(f"Route {request.method} {request.url.path} a été utilisée. Compteur : {route_counter}")
    response = await call_next(request)
    return response

# inclusion des routes dans l'app
app.include_router(router_show_temp)
app.include_router(router_show_city)
app.include_router(router_show_country)
app.include_router(router_create_date)
app.include_router(router_create_city)
app.include_router(router_create_country)
app.include_router(router_modif_temp)
app.include_router(router_modif_city)
app.include_router(router_modif_country)
app.include_router(router_suppr_date)
app.include_router(router_weather_by_date)
app.include_router(router_order_by_prpc)
app.include_router(router_order_by_tmax)
app.include_router(router_order_by_tmin)
app.include_router(router_order_by_snow)
app.include_router(router_order_by_swnd)
app.include_router(router_order_by_awnd)
app.include_router(router_average_min_temp)
app.include_router(router_average_max_temp)
app.include_router(router_absolute_average)
app.include_router(router_average_temp_country)
app.include_router(router_suppr_city)
app.include_router(router_suppr_country)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
