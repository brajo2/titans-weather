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
from shared.daily_param import DailyWeatherParam
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

"""
But for variables that are potentially affected by the venue:
"""
PRECIPITATION_VARIABLES = [
    # hourly
    HourlyWeatherParam.SOIL_TEMPERATURE_0_TO_7CM,
    HourlyWeatherParam.SOIL_TEMPERATURE_7_TO_28CM,
    HourlyWeatherParam.SOIL_TEMPERATURE_28_TO_100CM,
    HourlyWeatherParam.SOIL_TEMPERATURE_100_TO_255CM,
    HourlyWeatherParam.SOIL_MOISTURE_0_TO_7CM,
    HourlyWeatherParam.SOIL_MOISTURE_7_TO_28CM,
    HourlyWeatherParam.SOIL_MOISTURE_28_TO_100CM,
    HourlyWeatherParam.SOIL_MOISTURE_100_TO_255CM,
    HourlyWeatherParam.SNOW_DEPTH,
    HourlyWeatherParam.ET0_FAO_EVAPOTRANSPIRATION,
    HourlyWeatherParam.PRECIPITATION,
    HourlyWeatherParam.RAIN,
    HourlyWeatherParam.SNOWFALL,
    # daily
    DailyWeatherParam.PRECIPITATION_SUM,
    DailyWeatherParam.RAIN_SUM,
    DailyWeatherParam.SNOWFALL_SUM,
    DailyWeatherParam.ET0_FAO_EVAPOTRANSPIRATION,
    DailyWeatherParam.PRECIPITATION_HOURS
]

NON_PRECIPITATION_VARIABLES = [
    # hourly
    HourlyWeatherParam.TEMPERATURE_2M,
    HourlyWeatherParam.RELATIVE_HUMIDITY_2M,
    HourlyWeatherParam.DEW_POINT_2M,
    HourlyWeatherParam.APPARENT_TEMPERATURE,
    HourlyWeatherParam.PRESSURE_MSL,
    HourlyWeatherParam.SURFACE_PRESSURE,
    HourlyWeatherParam.CLOUD_COVER,
    HourlyWeatherParam.CLOUD_COVER_LOW,
    HourlyWeatherParam.CLOUD_COVER_MID,
    HourlyWeatherParam.CLOUD_COVER_HIGH,
    HourlyWeatherParam.SHORTWAVE_RADIATION,
    HourlyWeatherParam.DIRECT_NORMAL_IRRADIANCE,
    HourlyWeatherParam.DIFFUSE_RADIATION,
    HourlyWeatherParam.GLOBAL_TILTED_IRRADIANCE,
    HourlyWeatherParam.SUNSHINE_DURATION,
    HourlyWeatherParam.WIND_SPEED_10M,
    HourlyWeatherParam.WIND_SPEED_100M,
    HourlyWeatherParam.WIND_DIRECTION_10M,
    HourlyWeatherParam.WIND_DIRECTION_100M,
    HourlyWeatherParam.WIND_GUSTS_10M,
    HourlyWeatherParam.VAPOUR_PRESSURE_DEFICIT,
    HourlyWeatherParam.WEATHER_CODE,
    # daily
    DailyWeatherParam.WEATHER_CODE,
    DailyWeatherParam.TEMPERATURE_2M_MAX,
    DailyWeatherParam.TEMPERATURE_2M_MIN,
    DailyWeatherParam.APPARENT_TEMPERATURE_MAX,
    DailyWeatherParam.APPARENT_TEMPERATURE_MIN,
    DailyWeatherParam.SUNRISE,
    DailyWeatherParam.SUNSET,
    DailyWeatherParam.SUNSHINE_DURATION,
    DailyWeatherParam.DAYLIGHT_DURATION,
    DailyWeatherParam.WIND_SPEED_10M_MAX,
    DailyWeatherParam.WIND_GUSTS_10M_MAX,
    DailyWeatherParam.WIND_DIRECTION_10M_DOMINANT,
    DailyWeatherParam.SHORTWAVE_RADIATION_SUM
]


## misc
GAME_LENGTH = 3  # hours
PRE_GAME_WINDOW = 2  # hours