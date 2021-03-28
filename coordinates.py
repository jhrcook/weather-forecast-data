#!/usr/bin/env python3

from typing import List

from pydantic import BaseModel


class CityCoords(BaseModel):
    city: str
    lat: float
    long: float


cities = {
    "boston": CityCoords(city="Boston", lat=42.361145, long=-71.057083),
    "los-angeles": CityCoords(city="Los Angeles", lat=34.05223, long=-118.24368),
    "chicago": CityCoords(city="Chicago", lat=41.85003, long=-87.65005),
    "new-york": CityCoords(city="New York", lat=40.71427, long=-74.00597),
    "houston": CityCoords(city="Houston", lat=29.76328, long=-95.36327),
    "seattle": CityCoords(city="Seattle", lat=47.60621, long=-122.33207),
    "detroit": CityCoords(city="Detroit", lat=42.331429, long=-83.045753),
    "miami": CityCoords(city="Miama", lat=25.77427, long=-80.19366),
    "tulsa": CityCoords(city="Tulsa", lat=36.15398, long=-95.99277),
    "las-vegas": CityCoords(city="Las Vegas", lat=36.17497, long=-115.13722),
    "tuscon": CityCoords(city="Tuscon", lat=32.253460, long=-110.911789),
    "denver": CityCoords(city="Denver", lat=39.73915, long=-104.9847),
    "portland": CityCoords(city="Portland", lat=45.52345, long=-122.67621),
    "boise": CityCoords(city=" Boise", lat=43.6135, long=-116.20345),
}


def get_coordinates(city: str) -> CityCoords:
    try:
        return cities[city.lower()]
    except:
        raise ValueError(f"Coordinates for the city '{city}' are not available.")


def all_cities() -> List[str]:
    return list(cities.keys())
