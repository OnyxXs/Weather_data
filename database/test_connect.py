from typing import List
from urllib.parse import urlparse

from databases import Database
from fastapi import FastAPI
from pydantic import BaseModel
import pymysql
from sqlalchemy import MetaData, Table, Column, Integer, String, select

DATABASE_URL = "mysql+pymysql://root:root@127.0.0.1:8889/Weather?serverVersion=5.7"

database = Database(DATABASE_URL)

metadata = MetaData()

country = Table(
    "country",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("name", String),
)


class Country(BaseModel):
    id: int
    name: str


app = FastAPI()


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
