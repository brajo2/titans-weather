from collections import namedtuple
from typing import List

import requests
import json
from tenacity import retry, stop_after_attempt, wait_fixed

from shared.daily_param import DailyWeatherParam
from shared.hourly_param import HourlyWeatherParam
from shared.weather_enum import WeatherLookupWindow, TemperatureUnit, WindSpeedUnit

LANGUAGE = "en"
FORMAT_RESPONSE = "json"
# Add @retry from tenacity to retry the function call no more than 5 times
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def get_geolocations(name, count=4, language=LANGUAGE, format_response=FORMAT_RESPONSE):
    """
    example usage:
        - https://geocoding-api.open-meteo.com/v1/search?name=Berlin&count=10&language=en&format=json

    example return:
         "results": [
            {
              "id": 2950159,
              "name": "Berlin",
              "latitude": 52.52437,
              "longitude": 13.41053,
              "elevation": 74.0,
              "feature_code": "PPLC",
              "country_code": "DE",
              "admin1_id": 2950157,
              "admin2_id": 0,
              "admin3_id": 6547383,
              "admin4_id": 6547539,
              "timezone": "Europe/Berlin",
              "population": 3426354,
              "postcodes": [
                "10967",
                "13347"
              ],
              "country_id": 2921044,
              "country": "Deutschland",
              "admin1": "Berlin",
              "admin2": "",
              "admin3": "Berlin, Stadt",
              "admin4": "Berlin"
            },
            {
              ...
            }]
    :param name: str
    :param count: int
    :param language: str
    :param format_response: str
    :return: dict
    """
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={name}&count={count}&language={language}&format={format_response}"
    # set headers, not implemented
    headers = {}

    # Make the HTTP GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code == 200:
        return response
    else:
        # Raise an exception if the request failed
        response.raise_for_status()