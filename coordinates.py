#!/usr/bin/env python3

from pydantic import BaseModel


class CityCoords(BaseModel):
    city: str
    lat: float
    long: float


cities = {"boston": CityCoords(city="Boston", lat=42.361145, long=-71.057083)}


def get_coordinates(city: str) -> CityCoords:
    try:
        return cities[city.lower()]
    except:
        raise ValueError(f"Coordinates for the city '{city}' are not available.")
