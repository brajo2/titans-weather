"""
- File stores all the hourly weather parameters as a Enum class
for ease of use and readability
- Some of these aren't that important & I won't use them, but this works as a catalog
"""
from shared.weather_param import WeatherParam

"""
Variable	Unit	Description
weather_code	WMO code	The most severe weather condition on a given day
temperature_2m_max
temperature_2m_min	°C (°F)	Maximum and minimum daily air temperature at 2 meters above ground
apparent_temperature_max
apparent_temperature_min	°C (°F)	Maximum and minimum daily apparent temperature
precipitation_sum	mm	Sum of daily precipitation (including rain, showers and snowfall)
rain_sum	mm	Sum of daily rain
snowfall_sum	cm	Sum of daily snowfall
precipitation_hours	hours	The number of hours with rain
sunrise
sunset	iso8601	Sun rise and set times
sunshine_duration	seconds	The number of seconds of sunshine per day is determined by calculating direct normalized irradiance exceeding 120 W/m², following the WMO definition. Sunshine duration will consistently be less than daylight duration due to dawn and dusk.
daylight_duration	seconds	Number of seconds of daylight per day
wind_speed_10m_max
wind_gusts_10m_max	km/h (mph, m/s, knots)	Maximum wind speed and gusts on a day
wind_direction_10m_dominant	°	Dominant wind direction
shortwave_radiation_sum	MJ/m²	The sum of solar radiaion on a given day in Megajoules
et0_fao_evapotranspiration	mm	Daily sum of ET₀ Reference Evapotranspiration of a well watered grass field
"""

from enum import Enum

class DailyWeatherParam(Enum):
    WEATHER_CODE = WeatherParam("weather_code", "WMO code")
    TEMPERATURE_2M_MAX = WeatherParam("temperature_2m_max", "°C (°F)")
    TEMPERATURE_2M_MIN = WeatherParam("temperature_2m_min", "°C (°F)")
    APPARENT_TEMPERATURE_MAX = WeatherParam("apparent_temperature_max", "°C (°F)")
    APPARENT_TEMPERATURE_MIN = WeatherParam("apparent_temperature_min", "°C (°F)")
    PRECIPITATION_SUM = WeatherParam("precipitation_sum", "mm")
    RAIN_SUM = WeatherParam("rain_sum", "mm")
    SNOWFALL_SUM = WeatherParam("snowfall_sum", "cm")
    PRECIPITATION_HOURS = WeatherParam("precipitation_hours", "hours")
    SUNRISE = WeatherParam("sunrise", "iso8601")
    SUNSET = WeatherParam("sunset", "iso8601")
    SUNSHINE_DURATION = WeatherParam("sunshine_duration", "seconds")
    DAYLIGHT_DURATION = WeatherParam("daylight_duration", "seconds")
    WIND_SPEED_10M_MAX = WeatherParam("wind_speed_10m_max", "km/h (mph, m/s, knots)")
    WIND_GUSTS_10M_MAX = WeatherParam("wind_gusts_10m_max", "km/h (mph, m/s, knots)")
    WIND_DIRECTION_10M_DOMINANT = WeatherParam("wind_direction_10m_dominant", "°")
    SHORTWAVE_RADIATION_SUM = WeatherParam("shortwave_radiation_sum", "MJ/m²")
    ET0_FAO_EVAPOTRANSPIRATION = WeatherParam("et0_fao_evapotranspiration", "mm")
