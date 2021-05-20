#!/usr/bin/env python3

import json
import logging
import shutil
from datetime import datetime
from pathlib import Path
from typing import Callable, Optional

import typer
from pydantic.main import BaseModel
from requests.exceptions import HTTPError
from weather_forecast_collection.apis import accuweather_api as accu
from weather_forecast_collection.apis import climacell_api as cc
from weather_forecast_collection.apis import national_weather_service_api as nws
from weather_forecast_collection.apis import openweathermap_api as owm

logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(asctime)s - %(funcName)s [line %(lineno)d] - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

try:
    import keys
except:
    print("Module 'keys' not found - API keys must be passed by CLI.")
from coordinates import all_cities, get_coordinates

app = typer.Typer()

DATA_DIR = Path("data")
if not DATA_DIR.exists():
    DATA_DIR.mkdir()


def fmt_date(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


def make_next_dir(inside_dir: Path) -> Path:
    all_dirs = [int(d.name) for d in inside_dir.iterdir() if d.is_dir()]
    if len(all_dirs) == 0:
        new_dir_num = 1
    else:
        new_dir_num = max(all_dirs) + 1
    new_dir = inside_dir / str(new_dir_num).rjust(4, "0")
    new_dir.mkdir()
    return new_dir


def get_save_dir() -> Path:
    MAX_FILES = 1000
    for lvl_one in DATA_DIR.iterdir():
        if lvl_one.is_dir():
            num_files_in_lvl_one = len(list(lvl_one.iterdir()))
            if num_files_in_lvl_one >= MAX_FILES:
                continue

            for lvl_two in lvl_one.iterdir():
                if lvl_two.is_dir():
                    num_files = len(list(lvl_two.iterdir()))
                    if num_files < MAX_FILES:
                        return lvl_two
            return make_next_dir(lvl_one)

    _ = make_next_dir(DATA_DIR)
    new_dir = get_save_dir()  # run again to get a directory in this new directory.
    return new_dir


def make_filepath(source: str, city: str) -> Path:
    return get_save_dir() / f"{source}_{city}_{fmt_date(datetime.now())}.json"


def save_data(source: str, city: str, data: BaseModel) -> Path:
    file_path = make_filepath(source=source, city=city)
    with open(file_path, "w") as json_file:
        json.dump(data.json(), json_file)
    return file_path


def read_data(fp: Path, model: Callable):
    with open(fp) as json_file:
        return model(**json.loads(json.load(json_file)))


@app.command()
def migrate_data_files_to_subdir_format() -> None:
    n_files_moved = 0
    for f in DATA_DIR.iterdir():
        if f.is_file() and "json" in f.name:
            new_dir = get_save_dir()
            shutil.move(f, new_dir)
            n_files_moved += 1
    print(f"Number of files relocated: {n_files_moved}")


@app.command()
def national_weather_service(city: str, n_attempt: int = 1) -> None:
    logging.info(f"Sending request for '{city}' to NWS API.")
    coords = get_coordinates(city)
    try:
        forecast = nws.get_nws_forecast(lat=coords.lat, long=coords.long)
        fp = save_data(source="national-weather-service", city=city, data=forecast)
        logging.info(f"Saved results to '{fp.as_posix()}'")
    except HTTPError as http_err:
        logging.error(f"NWS API request error ({http_err.response.status_code}).")
        logging.error(http_err)
        if n_attempt <= 5 and http_err.response.status_code != 404:
            logging.info("Trying NWS API again.")
            national_weather_service(city=city, n_attempt=n_attempt + 1)
    except Exception as err:
        logging.error(err)


@app.command()
def accuweather(
    city: str, api_key: Optional[str] = None, first_attempt: bool = True
) -> None:
    logging.info(f"Sending request for '{city}' to AccuWeather API.")
    if api_key is None:
        try:
            api_key = keys.accuweather_api_key
        except Exception as err:
            logging.error("Unable to get API key for AccuWeather.")
            logging.error(err)
            return

    coords = get_coordinates(city)
    try:
        forecast = accu.get_accuweather_forecast(
            lat=coords.lat, long=coords.long, api_key=api_key
        )
        fp = save_data(source="accuweather", city=city, data=forecast)
        logging.info(f"Saved results to '{fp.as_posix()}'")
    except HTTPError as http_err:
        logging.error(
            f"AccuWeather API request error ({http_err.response.status_code})."
        )
        logging.error(http_err.response.json()["Message"])
        if first_attempt and http_err.response.status_code != 503:
            logging.info("Retrying request to AccuWeather.")
            accuweather(city=city, api_key=api_key, first_attempt=False)
    except Exception as err:
        logging.error(err)


@app.command()
def open_weather_map(
    city: str, api_key: Optional[str] = None, first_attempt: bool = True
) -> None:
    logging.info(f"Sending request for '{city}' to OpenWeatherMap API.")
    if api_key is None:
        try:
            api_key = keys.openweathermap_api_key
        except Exception as err:
            logging.error("Unable to get API key for OpenWeatherMap.")
            logging.error(err)
            return

    coords = get_coordinates(city)

    try:
        forecast = owm.get_openweathermap_data(
            lat=coords.lat, long=coords.long, api_key=api_key
        )
        fp = save_data("open-weather-map", city, forecast)
        logging.info(f"Saved results to '{fp.as_posix()}'")
    except HTTPError as http_err:
        logging.error(
            f"OpenWeatherMap API request error ({http_err.response.status_code})."
        )
        logging.error(http_err.response.json()["detail"])
        if first_attempt:
            logging.info("Retrying request to OpenWeatherMap.")
            open_weather_map(city=city, api_key=api_key, first_attempt=False)
    except Exception as err:
        logging.error(err)


@app.command()
def climacell(
    city: str, api_key: Optional[str] = None, first_attempt: bool = True
) -> None:
    logging.info(f"Sending request for '{city}' to ClimaCell API.")
    if api_key is None:
        try:
            api_key = keys.climacell_api_key
        except Exception as err:
            logging.error("Unable to get API key for ClimaCell.")
            logging.error(err)
            return

    coords = get_coordinates(city)
    try:
        forecast = cc.get_climacell_data(
            lat=coords.lat, long=coords.long, api_key=api_key
        )
        fp = save_data("climacell", city, forecast)
        logging.info(f"Saved results to '{fp.as_posix()}'")
    except HTTPError as http_err:
        logging.error(f"ClimaCell API request error ({http_err.response.status_code}).")
        logging.error(http_err.response.json()["message"])
        if first_attempt:
            logging.info("Retrying request to ClimaCell.")
            climacell(city=city, api_key=api_key, first_attempt=False)
    except Exception as err:
        logging.error(err)


@app.command()
def all_data(
    city: str,
    accu_key: Optional[str] = None,
    owm_key: Optional[str] = None,
    cc_key: Optional[str] = None,
    skip_accuweather: bool = False,
):
    if city == "ALL":
        for c in all_cities():
            all_data(
                city=c,
                accu_key=accu_key,
                owm_key=owm_key,
                cc_key=cc_key,
                skip_accuweather=skip_accuweather,
            )
        return
    national_weather_service(city=city)
    open_weather_map(city=city, api_key=owm_key)
    climacell(city=city, api_key=cc_key)
    if not skip_accuweather:
        accuweather(city=city, api_key=accu_key)


if __name__ == "__main__":
    app()
