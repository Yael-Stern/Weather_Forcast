"""Typed result shapes exposed by the forecast tool."""

from typing_extensions import TypedDict


class Location(TypedDict):
    name: str
    latitude: float
    longitude: float
    timezone: str


class DailyForecast(TypedDict):
    date: str
    condition: str
    weather_code: int
    temperature_min_c: float
    temperature_max_c: float
    precipitation_probability_max_percent: int
    wind_speed_max_kmh: float
    sunrise: str
    sunset: str


class WeeklyForecast(TypedDict):
    location: Location
    forecast_days: int
    source: str
    forecast: list[DailyForecast]
