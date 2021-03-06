# Weather Forecast Data

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A repository of weather forecast and nowcast data collected using the ['weather-forecast-collection'](https://github.com/jhrcook/weather_forecast_collection) package.
Data is collected every hour from 4 data sources: [the US National Weather Service](https://www.weather.gov), [Accuweather](https://www.accuweather.com), [ClimaCell](https://www.climacell.co), and [OpenWeatherMap](https://openweathermap.org).

## Setup

```bash
git clone https://github.com/jhrcook/weather-forecast-data.git
pip install -r requirements.txt
```

Make sure the CLI is working by trying the following command.

```bash
./main.py --help
```

## Data

[![Data Collection](https://github.com/jhrcook/weather-forecast-data/actions/workflows/continuous-data-collection.yml/badge.svg)](https://github.com/jhrcook/weather-forecast-data/actions/workflows/continuous-data-collection.yml)

The data collected is available in the "data/" directory of the [`weather-data`](https://github.com/jhrcook/weather-forecast-data/tree/weather-data) branch of the GitHub repo.
The GitHub web interface and API (I use [PyGithub](https://pygithub.readthedocs.io/en/latest/#) to access reposotries within Python) have a limit of only presenting 1,000 files.
To get around this without having to set up a separate data store, I am using a two-level subdirectory data storage system.
In essence, files are stored within two levels of subdirectories in "data/" such that each directory only holds at most 1,000 files.
This method is not perfect nor ideal, but at my scale of data collection, it should last well beyond my lifetime.
All of the data files can be obtained by recursively searching the "data/" directory.

### GitHub Continuous Data Collection

The data is collected every hour using a GitHub Action.
The action uses the [setup-python](https://github.com/actions/setup-python) action to setup the environment with Python 3.9.
The required packages are then installed and the CLI for this project (use `./main.py --help` for help) is used to collect all of the data from each data source.
Finally, the changes are committed to the [`weather-data`](https://github.com/jhrcook/weather-forecast-data/tree/weather-data) branch using the [Add & Commit](https://github.com/marketplace/actions/add-commit) GitHub Action.
