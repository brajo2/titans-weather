from collections import namedtuple
from typing import List

import requests
import json
from tenacity import retry, stop_after_attempt, wait_fixed

from shared.daily_param import DailyWeatherParam
from shared.hourly_param import HourlyWeatherParam
from shared.weather_enum import WeatherLookupWindow, TemperatureUnit, WindSpeedUnit, Timezone, Forecast


# Add @retry from tenacity to retry the function call no more than 5 times
@retry(stop=stop_after_attempt(5), wait=wait_fixed(2))
def get_weather(latitude, longitude, start_date, end_date,
                forecast_type=Forecast.ARCHIVE,
                api_key=None,
                window=WeatherLookupWindow.HOURLY,
                timezone=Timezone.AUTO,
                temperature_unit=TemperatureUnit.FAHRENHEIT,
                wind_speed_unit=WindSpeedUnit.KILOMETERS_PER_HOUR,
                variables: list[HourlyWeatherParam | DailyWeatherParam] = []):
    """
    example usage:
        - https://archive-api.open-meteo.com/v1/archive?latitude=52.52&longitude=13.41&start_date=2024-04-27&end_date=2024-04-27&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m,wind_speed_100m&temperature_unit=fahrenheit&timeformat=unixtime
    :param latitude: float
    :param longitude: float
    :param start_date: str (YYYY-MM-DD)
    :param end_date: str (YYYY-MM-DD)
    :param api_key: str
    :param window: WeatherLookupWindow
    :param temperature_unit: TemperatureUnit
    :param wind_speed_unit: WindSpeedUnit
    :param variables: list of HourlyWeatherParam or DailyWeatherParam
    :return: dict
    """
    variable_names_unpacked = [v.value.param_name for v in variables]
    url = f"https://archive-api.open-meteo.com/v1/{forecast_type}?latitude={latitude}&longitude={longitude}&start_date={start_date}&end_date={end_date}&{window.value}={','.join(variable_names_unpacked)}&temperature_unit={temperature_unit.value}&wind_speed_unit={wind_speed_unit.value}&timezone={timezone.value}"

    # set headers, not implemented
    headers = {}

    # Make the HTTP GET request
    response = requests.get(url, headers=headers)

    # Check if the request was successful
    if response.status_code != 200:
        # Raise an exception if the request failed
        response.raise_for_status()

    if window == WeatherLookupWindow.HOURLY:
        resp = parse_hourly_weather_response(response.json(), variable_names_unpacked)
    elif window == WeatherLookupWindow.DAILY:
        resp = parse_daily_weather_response(response.json(), variable_names_unpacked)
    return resp


def parse_hourly_weather_response(response: dict, variables: List[str]) -> dict:
    """
        Clearly "hourly" is a set of synchronous arrays, where each index corresponds to the same time.
        Therefore, we can zip the arrays together to get a list of dictionaries,
        where each dictionary is a set of key-value pairs for each time.
    """
    metric_keys = variables
    all_fields = ['hour_index', 'time', *metric_keys]
    HourlyTuple = namedtuple('HourlyTuple', all_fields)

    num_records = len(response['hourly']['time'])
    hourly_records = []
    for i in range(num_records):
        hour_rec = []
        for field in all_fields:
            if field == 'hour_index':
                hour_rec.append(i)
            else:
                hour_rec.append(response['hourly'][field][i])
        # Create a named tuple for this record and add it to the list
        hourly_records.append(HourlyTuple(*hour_rec))

    data = {
        'latitude': response['latitude'],
        'longitude': response['longitude'],
        'generationtime_ms': response['generationtime_ms'],
        'timezone': response['timezone'],
        'timezone_abbreviation': response['timezone_abbreviation'],
        'hourly': hourly_records,
        'hourly_units': response['hourly_units']
    }

    return data


####### not really using right now
def parse_daily_weather_response(response: dict, variables: List[str]) -> dict:
    """
        Clearly "daily" is a set of synchronous arrays, where each index corresponds to the same time.
        Therefore, we can zip the arrays together to get a list of dictionaries,
        where each dictionary is a set of key-value pairs for each time.
    """
    metric_keys = variables
    all_fields = ['time', *metric_keys]
    DailyTuple = namedtuple('DailyTuple', all_fields)

    num_records = len(response['daily']['time'])
    daily_records = []
    for i in range(num_records):
        values = [response['daily'][field][i] for field in all_fields]
        # Create a named tuple for this record and add it to the list
        daily_records.append(DailyTuple(*values))

    data = {
        'latitude': response['latitude'],
        'longitude': response['longitude'],
        'generationtime_ms': response['generationtime_ms'],
        'timezone': response['timezone'],
        'timezone_abbreviation': response['timezone_abbreviation'],
        'daily': daily_records,
        'daily_units': response['daily_units']
    }

    return data