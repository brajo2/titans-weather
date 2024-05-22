"""
- File stores all the hourly weather parameters as a Enum class
for ease of use and readability
- Some of these aren't that important & I won't use them, but this works as a catalog
"""
from shared.weather_param import WeatherParam

"""
temperature_2m	Instant	°C (°F)	Air temperature at 2 meters above ground
relative_humidity_2m	Instant	%	Relative humidity at 2 meters above ground
dew_point_2m	Instant	°C (°F)	Dew point temperature at 2 meters above ground
apparent_temperature	Instant	°C (°F)	Apparent temperature is the perceived feels-like temperature combining wind chill factor, relative humidity and solar radiation
pressure_msl
surface_pressure	Instant	hPa	Atmospheric air pressure reduced to mean sea level (msl) or pressure at surface. Typically pressure on mean sea level is used in meteorology. Surface pressure gets lower with increasing elevation.
precipitation	Preceding hour sum	mm (inch)	Total precipitation (rain, showers, snow) sum of the preceding hour. Data is stored with a 0.1 mm precision. If precipitation data is summed up to monthly sums, there might be small inconsistencies with the total precipitation amount.
rain	Preceding hour sum	mm (inch)	Only liquid precipitation of the preceding hour including local showers and rain from large scale systems.
snowfall	Preceding hour sum	cm (inch)	Snowfall amount of the preceding hour in centimeters. For the water equivalent in millimeter, divide by 7. E.g. 7 cm snow = 10 mm precipitation water equivalent
cloud_cover	Instant	%	Total cloud cover as an area fraction
cloud_cover_low	Instant	%	Low level clouds and fog up to 2 km altitude
cloud_cover_mid	Instant	%	Mid level clouds from 2 to 6 km altitude
cloud_cover_high	Instant	%	High level clouds from 6 km altitude
shortwave_radiation	Preceding hour mean	W/m²	Shortwave solar radiation as average of the preceding hour. This is equal to the total global horizontal irradiation
direct_radiation
direct_normal_irradiance	Preceding hour mean	W/m²	Direct solar radiation as average of the preceding hour on the horizontal plane and the normal plane (perpendicular to the sun)
diffuse_radiation	Preceding hour mean	W/m²	Diffuse solar radiation as average of the preceding hour
global_tilted_irradiance	Preceding hour mean	W/m²	Total radiation received on a tilted pane as average of the preceding hour. The calculation is assuming a fixed albedo of 20% and in isotropic sky. Please specify tilt and azimuth parameter. Tilt ranges from 0° to 90° and is typically around 45°. Azimuth should be close to 0° (0° south, -90° east, 90° west). If azimuth is set to "nan", the calculation assumes a horizontal tracker. If tilt is set to "nan", it is assumed that the panel has a vertical tracker. If both are set to "nan", a bi-axial tracker is assumed.
sunshine_duration	Preceding hour sum	Seconds	Number of seconds of sunshine of the preceding hour per hour calculated by direct normalized irradiance exceeding 120 W/m², following the WMO definition.
wind_speed_10m
wind_speed_100m	Instant	km/h (mph, m/s, knots)	Wind speed at 10 or 100 meters above ground. Wind speed on 10 meters is the standard level.
wind_direction_10m
wind_direction_100m	Instant	°	Wind direction at 10 or 100 meters above ground
wind_gusts_10m	Instant	km/h (mph, m/s, knots)	Gusts at 10 meters above ground of the indicated hour. Wind gusts in CERRA are defined as the maximum wind gusts of the preceding hour. Please consult the ECMWF IFS documentation for more information on how wind gusts are parameterized in weather models.
et0_fao_evapotranspiration	Preceding hour sum	mm (inch)	ET₀ Reference Evapotranspiration of a well watered grass field. Based on FAO-56 Penman-Monteith equations ET₀ is calculated from temperature, wind speed, humidity and solar radiation. Unlimited soil water is assumed. ET₀ is commonly used to estimate the required irrigation for plants.
weather_code	Instant	WMO code	Weather condition as a numeric code. Follow WMO weather interpretation codes. See table below for details. Weather code is calculated from cloud cover analysis, precipitation and snowfall. As barely no information about atmospheric stability is available, estimation about thunderstorms is not possible.
snow_depth	Instant	meters	Snow depth on the ground. Snow depth in ERA5-Land tends to be overestimated. As the spatial resolution for snow depth is limited, please use it with care.
vapour_pressure_deficit	Instant	kPa	Vapor Pressure Deificit (VPD) in kilopascal (kPa). For high VPD (>1.6), water transpiration of plants increases. For low VPD (<0.4), transpiration decreases
soil_temperature_0_to_7cm
soil_temperature_7_to_28cm
soil_temperature_28_to_100cm
soil_temperature_100_to_255cm	Instant	°C (°F)	Average temperature of different soil levels below ground.
soil_moisture_0_to_7cm
soil_moisture_7_to_28cm
soil_moisture_28_to_100cm
soil_moisture_100_to_255cm	Instant	m³/m³	Average soil water content as volumetric mixing ratio at 0-7, 7-28, 28-100 and 100-255 cm depths.
"""

from enum import Enum

class HourlyWeatherParam(Enum):
    TEMPERATURE_2M = WeatherParam("temperature_2m", "°C (°F)")
    RELATIVE_HUMIDITY_2M = WeatherParam("relative_humidity_2m", "%")
    DEW_POINT_2M = WeatherParam("dew_point_2m", "°C (°F)")
    APPARENT_TEMPERATURE = WeatherParam("apparent_temperature", "°C (°F)")
    PRESSURE_MSL = WeatherParam("pressure_msl", "hPa")
    SURFACE_PRESSURE = WeatherParam("surface_pressure", "hPa")
    PRECIPITATION = WeatherParam("precipitation", "mm (inch)")
    RAIN = WeatherParam("rain", "mm (inch)")
    SNOWFALL = WeatherParam("snowfall", "cm (inch)")
    CLOUD_COVER = WeatherParam("cloud_cover", "%")
    CLOUD_COVER_LOW = WeatherParam("cloud_cover_low", "%")
    CLOUD_COVER_MID = WeatherParam("cloud_cover_mid", "%")
    CLOUD_COVER_HIGH = WeatherParam("cloud_cover_high", "%")
    SHORTWAVE_RADIATION = WeatherParam("shortwave_radiation", "W/m²")
    DIRECT_NORMAL_IRRADIANCE = WeatherParam("direct_normal_irradiance", "W/m²")
    DIFFUSE_RADIATION = WeatherParam("diffuse_radiation", "W/m²")
    GLOBAL_TILTED_IRRADIANCE = WeatherParam("global_tilted_irradiance", "W/m²")
    SUNSHINE_DURATION = WeatherParam("sunshine_duration", "Seconds")
    WIND_SPEED_10M = WeatherParam("wind_speed_10m", "km/h (mph, m/s, knots)")
    WIND_SPEED_100M = WeatherParam("wind_speed_100m", "km/h (mph, m/s, knots)")
    WIND_DIRECTION_10M = WeatherParam("wind_direction_10m", "°")
    WIND_DIRECTION_100M = WeatherParam("wind_direction_100m", "°")
    WIND_GUSTS_10M = WeatherParam("wind_gusts_10m", "km/h (mph, m/s, knots)")
    ET0_FAO_EVAPOTRANSPIRATION = WeatherParam("et0_fao_evapotranspiration", "mm (inch)")
    WEATHER_CODE = WeatherParam("weather_code", "WMO code")
    SNOW_DEPTH = WeatherParam("snow_depth", "meters")
    VAPOUR_PRESSURE_DEFICIT = WeatherParam("vapour_pressure_deficit", "kPa")
    SOIL_TEMPERATURE_0_TO_7CM = WeatherParam("soil_temperature_0_to_7cm", "°C (°F)")
    SOIL_TEMPERATURE_7_TO_28CM = WeatherParam("soil_temperature_7_to_28cm", "°C (°F)")
    SOIL_TEMPERATURE_28_TO_100CM = WeatherParam("soil_temperature_28_to_100cm", "°C (°F)")
    SOIL_TEMPERATURE_100_TO_255CM = WeatherParam("soil_temperature_100_to_255cm", "°C (°F)")
    SOIL_MOISTURE_0_TO_7CM = WeatherParam("soil_moisture_0_to_7cm", "m³/m³")
    SOIL_MOISTURE_7_TO_28CM = WeatherParam("soil_moisture_7_to_28cm", "m³/m³")
    SOIL_MOISTURE_28_TO_100CM = WeatherParam("soil_moisture_28_to_100cm", "m³/m³")
    SOIL_MOISTURE_100_TO_255CM = WeatherParam("soil_moisture_100_to_255cm", "m³/m³")
    ############################################################
    # extension for (future) weather forecast parameters:
    # I would've extended the HourlyWeatherParam class, but it's an Enum
    ############################################################
    WIND_SPEED_80M_FUTURE = WeatherParam("wind_speed_80m", "km/h (mph, m/s, knots)")
    WIND_SPEED_120M_FUTURE = WeatherParam("wind_speed_120m", "km/h (mph, m/s, knots)")
    WIND_SPEED_180M_FUTURE = WeatherParam("wind_speed_180m", "km/h (mph, m/s, knots)")
    WIND_DIRECTION_80M_FUTURE = WeatherParam("wind_direction_80m", "°")
    WIND_DIRECTION_120M_FUTURE = WeatherParam("wind_direction_120m", "°")
    WIND_DIRECTION_180M_FUTURE = WeatherParam("wind_direction_180m", "°")
    CAPE_FUTURE = WeatherParam("cape", "J/kg")
    PRECIPITATION_PROBABILITY_FUTURE = WeatherParam("precipitation_probability", "%")
    SHOWERS_FUTURE = WeatherParam("showers", "mm (inch)")
    FREEZING_LEVEL_HEIGHT_FUTURE = WeatherParam("freezing_level_height", "meters")
    VISIBILITY_FUTURE = WeatherParam("visibility", "meters")
    SOIL_TEMPERATURE_0CM_FUTURE = WeatherParam("soil_temperature_0cm", "°C (°F)")
    SOIL_TEMPERATURE_6CM_FUTURE = WeatherParam("soil_temperature_6cm", "°C (°F)")
    SOIL_TEMPERATURE_18CM_FUTURE = WeatherParam("soil_temperature_18cm", "°C (°F)")
    SOIL_TEMPERATURE_54CM_FUTURE = WeatherParam("soil_temperature_54cm", "°C (°F)")
    SOIL_MOISTURE_0_TO_1CM_FUTURE = WeatherParam("soil_moisture_0_to_1cm", "m³/m³")
    SOIL_MOISTURE_1_TO_3CM_FUTURE = WeatherParam("soil_moisture_1_to_3cm", "m³/m³")
    SOIL_MOISTURE_3_TO_9CM_FUTURE = WeatherParam("soil_moisture_3_to_9cm", "m³/m³")
    SOIL_MOISTURE_9_TO_27CM_FUTURE = WeatherParam("soil_moisture_9_to_27cm", "m³/m³")
    SOIL_MOISTURE_27_TO_81CM_FUTURE = WeatherParam("soil_moisture_27_to_81cm", "m³/m³")
    IS_DAY_FUTURE = WeatherParam("is_day", "")