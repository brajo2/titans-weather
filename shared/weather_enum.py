from enum import Enum


class WeatherLookupWindow(Enum):
    HOURLY = "hourly"
    DAILY = "daily"


class TemperatureUnit(Enum):
    CELSIUS = "celsius"
    FAHRENHEIT = "fahrenheit"


class WindSpeedUnit(Enum):
    KILOMETERS_PER_HOUR = "kmh"
    MILES_PER_HOUR = "mph"
    METERS_PER_SECOND = "ms"
    KNOTS = "knots"
