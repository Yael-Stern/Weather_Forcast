"""Open-Meteo API client and response validation."""

from __future__ import annotations

import ssl
from typing import Any

import httpx
import truststore

from .settings import (
    FORECAST_DAYS,
    LATITUDE,
    LONGITUDE,
    OPEN_METEO_FORECAST_URL,
    TIMEZONE,
)

API_DAILY_FIELDS = (
    "weather_code",
    "temperature_2m_max",
    "temperature_2m_min",
    "precipitation_probability_max",
    "wind_speed_10m_max",
    "sunrise",
    "sunset",
)
DAILY_FIELDS = ("time", *API_DAILY_FIELDS)


class WeatherAPIError(RuntimeError):
    """Raised when Open-Meteo returns an unusable response."""


class OpenMeteoClient:
    """Fetch and validate daily forecast data from Open-Meteo."""

    def __init__(
        self,
        transport: httpx.AsyncBaseTransport | None = None,
        timeout: float = 10.0,
    ) -> None:
        self._transport = transport
        self._timeout = timeout

    async def get_daily_forecast(self) -> dict[str, Any]:
        params = {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "daily": ",".join(API_DAILY_FIELDS),
            "forecast_days": FORECAST_DAYS,
            "timezone": TIMEZONE,
        }

        try:
            async with httpx.AsyncClient(
                timeout=self._timeout,
                transport=self._transport,
                verify=truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT),
            ) as client:
                response = await client.get(OPEN_METEO_FORECAST_URL, params=params)
                response.raise_for_status()
                payload = response.json()
        except httpx.HTTPError as error:
            raise WeatherAPIError(f"Open-Meteo request failed: {error}") from error
        except ValueError as error:
            raise WeatherAPIError("Open-Meteo returned invalid JSON.") from error

        return self._validate_payload(payload)

    @staticmethod
    def _validate_payload(payload: Any) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise WeatherAPIError("Open-Meteo response must be a JSON object.")

        daily = payload.get("daily")
        if not isinstance(daily, dict):
            raise WeatherAPIError("Open-Meteo response is missing daily forecast data.")

        columns: dict[str, list[Any]] = {}
        for field in DAILY_FIELDS:
            values = daily.get(field)
            if not isinstance(values, list) or len(values) != FORECAST_DAYS:
                raise WeatherAPIError(
                    f"Open-Meteo returned invalid '{field}' forecast data."
                )
            columns[field] = values

        return {
            "timezone": payload.get("timezone", TIMEZONE),
            "daily": columns,
        }
