from sqlalchemy import Column, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))


class City(Base):
    __tablename__ = "city"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    temp_id = Column(Integer, ForeignKey('temp.id'))
    country_id = Column(Integer, ForeignKey('country.id'))

    country = relationship("Country", back_populates="cities")
    temperatures = relationship("Temperature", back_populates="city")


class Temperature(Base):
    __tablename__ = "temp"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(String(255))
    Tmin = Column(Float)
    Tmax = Column(Float)
    prpc = Column(Float)
    snow = Column(Float)
    swnd = Column(Float)
    awnd = Column(Float)
    city_id = Column(Integer, ForeignKey('city.id'))

    city = relationship("City", back_populates="temperatures")
