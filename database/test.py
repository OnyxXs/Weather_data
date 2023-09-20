from typing import List

from fastapi import FastAPI
from sqlalchemy import select
from database.database import create_database_instance
from database.models import Country, country

app = FastAPI()
database = create_database_instance()


@app.on_event("startup")
async def startup_db_client():
    await database.connect()


@app.on_event("shutdown")
async def shutdown_db_client():
    await database.disconnect()


@app.get("/country/", response_model=List[Country])
async def read_country():
    query = select([country])
    results = await database.fetch_all(query)
    return results
