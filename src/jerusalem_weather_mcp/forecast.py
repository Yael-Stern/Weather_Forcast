"""Use case for presenting the Jerusalem weekly forecast."""

from __future__ import annotations

from typing import Any

from .models import DailyForecast, WeeklyForecast
from .open_meteo import OpenMeteoClient
from .settings import FORECAST_DAYS, LATITUDE, LOCATION_NAME, LONGITUDE, TIMEZONE

_CONDITIONS_HE = {
    0: "בהיר",
    1: "בהיר ברובו",
    2: "מעונן חלקית",
    3: "מעונן",
    45: "ערפל",
    48: "ערפל עם כפור",
    51: "טפטוף קל",
    53: "טפטוף",
    55: "טפטוף כבד",
    56: "טפטוף קופא קל",
    57: "טפטוף קופא כבד",
    61: "גשם קל",
    63: "גשם",
    65: "גשם כבד",
    66: "גשם קופא קל",
    67: "גשם קופא כבד",
    71: "שלג קל",
    73: "שלג",
    75: "שלג כבד",
    77: "גרגירי שלג",
    80: "ממטרים קלים",
    81: "ממטרים",
    82: "ממטרים כבדים",
    85: "ממטרי שלג קלים",
    86: "ממטרי שלג כבדים",
    95: "סופת רעמים",
    96: "סופת רעמים עם ברד קל",
    99: "סופת רעמים עם ברד כבד",
}


def _number(value: Any, field: str, day: int) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"Invalid {field} value for forecast day {day}.")
    return float(value)


def _integer(value: Any, field: str, day: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(f"Invalid {field} value for forecast day {day}.")
    return value


def _text(value: Any, field: str, day: int) -> str:
    if not isinstance(value, str):
        raise ValueError(f"Invalid {field} value for forecast day {day}.")
    return value


async def get_weekly_forecast(client: OpenMeteoClient | None = None) -> WeeklyForecast:
    """Return seven days of forecast data for Jerusalem."""
    weather_client = client if client is not None else OpenMeteoClient()
    result = await weather_client.get_daily_forecast()
    daily = result["daily"]
    days: list[DailyForecast] = []

    for index in range(FORECAST_DAYS):
        code = _integer(daily["weather_code"][index], "weather_code", index)
        days.append(
            {
                "date": _text(daily["time"][index], "time", index),
                "condition": _CONDITIONS_HE.get(code, "תנאי מזג אוויר לא ידועים"),
                "weather_code": code,
                "temperature_min_c": _number(
                    daily["temperature_2m_min"][index], "temperature_2m_min", index
                ),
                "temperature_max_c": _number(
                    daily["temperature_2m_max"][index], "temperature_2m_max", index
                ),
                "precipitation_probability_max_percent": _integer(
                    daily["precipitation_probability_max"][index],
                    "precipitation_probability_max",
                    index,
                ),
                "wind_speed_max_kmh": _number(
                    daily["wind_speed_10m_max"][index], "wind_speed_10m_max", index
                ),
                "sunrise": _text(daily["sunrise"][index], "sunrise", index),
                "sunset": _text(daily["sunset"][index], "sunset", index),
            }
        )

    return {
        "location": {
            "name": LOCATION_NAME,
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "timezone": result["timezone"] or TIMEZONE,
        },
        "forecast_days": FORECAST_DAYS,
        "source": "Open-Meteo",
        "forecast": days,
    }
