#!/usr/bin/env python3

import json
from datetime import datetime
from pathlib import Path
from pprint import pprint
from typing import Callable

import typer
from pydantic.main import BaseModel
from weather_forecast_collection.apis import accuweather_api as accu
from weather_forecast_collection.apis import climacell_api as cc
from weather_forecast_collection.apis import national_weather_service_api as nws
from weather_forecast_collection.apis import openweathermap_api as owm

import keys
from coordinates import get_coordinates

app = typer.Typer()

DATA_DIR = Path("data")
if not DATA_DIR.exists():
    DATA_DIR.mkdir()


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def make_filepath(source: str, city: str) -> Path:
    return DATA_DIR / f"{source}_{city}_{fmt_date(datetime.now())}.json"


def save_data(source: str, city: str, data: BaseModel) -> Path:
    file_path = make_filepath(source=source, city=city)
    with open(file_path, "w") as json_file:
        json.dump(data.json(), json_file)
    return file_path


def read_data(fp: Path, model: Callable):
    with open(fp) as json_file:
        return model(**json.loads(json.load(json_file)))


@app.command()
def national_weather_service(city: str) -> Path:
    coords = get_coordinates(city)
    forecast = nws.get_nsw_forecast(lat=coords.lat, long=coords.long)
    fp = save_data(source="national-weather-service", city=city, data=forecast)
    return fp


@app.command()
def accuweather(city: str) -> Path:
    coords = get_coordinates(city)
    forecast = accu.get_accuweather_forecast(
        lat=coords.lat, long=coords.long, api_key=keys.accuweather_api_key
    )
    fp = save_data(source="accuweather", city=city, data=forecast)
    return fp


@app.command()
def open_weather_map(city: str) -> Path:
    coords = get_coordinates(city)
    forecast = owm.get_openweathermap_data(
        lat=coords.lat, long=coords.long, api_key=keys.openweathermap_api_key
    )
    fp = save_data("open-weather-map", city, forecast)
    return fp


@app.command()
def climacell(city: str) -> Path:
    coords = get_coordinates(city)
    forecast = cc.get_climacell_data(
        lat=coords.lat, long=coords.long, api_key=keys.climacell_api_key
    )
    fp = save_data("climacell", city, forecast)
    return fp


@app.command()
def all_data(city: str):
    _ = national_weather_service(city=city)
    _ = accuweather(city=city)
    _ = open_weather_map(city=city)
    _ = climacell(city=city)


if __name__ == "__main__":
    app()

# TODO: GitHub Action to run script and store data.
