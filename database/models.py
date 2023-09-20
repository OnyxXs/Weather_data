from pydantic import BaseModel
from sqlalchemy import MetaData, Table, Column, Integer, String, select

# Créez un objet de méta-données SQLAlchemy pour définir la structure de la table
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
