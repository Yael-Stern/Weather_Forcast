import unittest

import httpx

from jerusalem_weather_mcp.forecast import get_weekly_forecast
from jerusalem_weather_mcp.open_meteo import OpenMeteoClient, WeatherAPIError


def make_payload():
    return {
        "timezone": "Asia/Jerusalem",
        "daily": {
            "time": [f"2026-11-{day:02d}" for day in range(17, 24)],
            "weather_code": [0, 1, 2, 3, 61, 80, 95],
            "temperature_2m_max": [20.0] * 7,
            "temperature_2m_min": [12.0] * 7,
            "precipitation_probability_max": [0, 5, 10, 15, 70, 50, 20],
            "wind_speed_10m_max": [15.0] * 7,
            "sunrise": ["2026-11-17T06:00"] * 7,
            "sunset": ["2026-11-17T16:30"] * 7,
        },
    }


class JerusalemForecastTests(unittest.IsolatedAsyncioTestCase):
    async def test_returns_seven_formatted_forecast_days(self):
        async def handler(request):
            self.assertEqual(request.url.params["latitude"], "31.7683")
            self.assertEqual(request.url.params["longitude"], "35.2137")
            self.assertEqual(request.url.params["forecast_days"], "7")
            self.assertNotIn("time", request.url.params["daily"])
            return httpx.Response(200, json=make_payload())

        client = OpenMeteoClient(transport=httpx.MockTransport(handler))
        forecast = await get_weekly_forecast(client)

        self.assertEqual(forecast["location"]["timezone"], "Asia/Jerusalem")
        self.assertEqual(len(forecast["forecast"]), 7)
        self.assertEqual(forecast["forecast"][4]["condition"], "גשם קל")
        self.assertEqual(forecast["forecast"][0]["temperature_max_c"], 20.0)

    async def test_rejects_missing_daily_fields(self):
        async def handler(request):
            return httpx.Response(200, json={"daily": {}})

        client = OpenMeteoClient(transport=httpx.MockTransport(handler))
        with self.assertRaises(WeatherAPIError):
            await client.get_daily_forecast()

    async def test_reports_http_errors(self):
        async def handler(request):
            return httpx.Response(503)

        client = OpenMeteoClient(transport=httpx.MockTransport(handler))
        with self.assertRaises(WeatherAPIError):
            await client.get_daily_forecast()


if __name__ == "__main__":
    unittest.main()
