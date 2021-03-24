# Weather Forecast Data

[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![License: GPLv3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

A repository of weather forecast and nowcast data collected using the ['weather-forecast-collection'](https://github.com/jhrcook/weather_forecast_collection) package.

This is currently under development, but the goal is to have it run as a chron-job on GitHub Actions every hour to collect the current weather and weather predictions.

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

The data collected is available in the "data/" directory of the [`weather-data`](https://github.com/jhrcook/weather-forecast-data/tree/weather-data) branch of the GitHub repo.

### GitHub Continuous Data Collection

The data is collected every hour using a GitHub Action.
The action uses the [setup-python](https://github.com/actions/setup-python) action to setup the environment with Python 3.9.
The required packages are then installed and the CLI for this project (use `./main.py --help` for help) is used to collect all of the data from each data source.
Finally, the changes are committed to the [`weather-data`](https://github.com/jhrcook/weather-forecast-data/tree/weather-data) branch using the [Add & Commit](https://github.com/marketplace/actions/add-commit) GitHub Action.
