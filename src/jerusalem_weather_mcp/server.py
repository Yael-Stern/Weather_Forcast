"""MCP server entry point."""

from mcp.server.fastmcp import FastMCP

from .forecast import get_weekly_forecast
from .models import WeeklyForecast

mcp = FastMCP("jerusalem-weather")


@mcp.tool()
async def jerusalem_weekly_forecast() -> WeeklyForecast:
    """Get the next seven days of weather in Jerusalem.

    Returns daily conditions in Hebrew, temperatures in Celsius, maximum
    precipitation probability, maximum wind speed in km/h, and sunrise/sunset
    times in Jerusalem local time.
    """
    return await get_weekly_forecast()


def main() -> None:
    """Run the MCP server over standard input/output."""
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
