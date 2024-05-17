"""
File for commonly used constant variables for querying the open meteo API:
    - for passing we care most about:
        - wind_speed_10m (wind speed 10 meters above the ground, so how windy is it when the ball's in the air)
        - wind_direction_10m (similar reason to above)
        - precipitation (how wet is the field, or maybe the ball)
        - rain (could be the same as precipitation, but in other contexts possibly not)
        - snowfall (how snowy, could be the same as precipitation in some contexts, but others could be a mix of rain and snow)
        - relative humidity (maybe you dropped the ball because it was slippery)

   - for running we care most about:
        - soil moisture (surface level) [0-7 cm]: It's actually harder to run when it's wet (less traction, more energy required)
            https://www.quora.com/Does-running-on-wet-ground-require-more-energy
        - snow_depth (for the same reason)

    - for kicking we care most about:
        - wind_speed_10m
        - wind_direction_10m
        - wind_speed_100m (ball could go even higher, in which case there might be even more unpredictability in the kicking game)
        - wind_direction_100m
        - precipitation (how wet is the field, or maybe the ball)

- for other general:
    - apparent_temperature (it could feel worse based on humidity)
    - temperature
"""
from shared.hourly_param import HourlyWeatherParam

BASE_HOURLY_PARAMS = [
    HourlyWeatherParam.WIND_SPEED_10M,
    HourlyWeatherParam.WIND_DIRECTION_10M,
    HourlyWeatherParam.WIND_SPEED_100M,
    HourlyWeatherParam.WIND_DIRECTION_100M,
    HourlyWeatherParam.PRECIPITATION,
    HourlyWeatherParam.RAIN,
    HourlyWeatherParam.SNOWFALL,
    HourlyWeatherParam.RELATIVE_HUMIDITY_2M,
    HourlyWeatherParam.APPARENT_TEMPERATURE,
    HourlyWeatherParam.TEMPERATURE_2M,
    HourlyWeatherParam.SOIL_MOISTURE_0_TO_7CM,
    HourlyWeatherParam.SNOW_DEPTH
]