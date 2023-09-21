from mysql.connector import Date
from pydantic import BaseModel


class Country(BaseModel):
    id: int
    name: str


class Temp(BaseModel):
    date: Date
    Tmin: float
    Tmax: float
    prpc: float
    snow: float
    swnd: float
    awnd: float
    city_id: int
