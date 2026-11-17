# Jerusalem Weather MCP

A local MCP server that provides seven-day weather forecasts for Jerusalem using the [Open-Meteo API](https://open-meteo.com/). It is built with Python and can be used with VS Code Copilot. No API key is required.

The forecast includes daily conditions in Hebrew, minimum and maximum temperatures in Celsius, maximum precipitation probability, maximum wind speed in km/h, and sunrise and sunset times in Jerusalem local time.

## Requirements

- Python 3.10 or later
- An internet connection when requesting a forecast
- VS Code with GitHub Copilot, if you want to use the included MCP configuration

## Install

Open PowerShell in the project directory and create a virtual environment:

```powershell
py -3 -m venv .venv
```

Install the project and its dependencies:

```powershell
& ".\.venv\Scripts\python.exe" -m pip install -e .
```

If the `py` command is unavailable, create the virtual environment with your Python executable instead:

```powershell
python -m venv .venv
```

## Run with VS Code

The project includes an MCP configuration at `.vscode/mcp.json`. Open the project folder in VS Code, then:

1. Press `Ctrl+Shift+P`.
2. Run **MCP: List Servers**.
3. Select **jerusalem-weather**, then choose **Start Server**.
4. In Copilot Chat, select **Agent** mode and ask it to use `jerusalem_weekly_forecast`.

The MCP server runs locally over `stdio`. VS Code starts it when needed; you do not need to start a separate HTTP server.

## Run manually

To start the MCP server from PowerShell:

```powershell
& ".\.venv\Scripts\python.exe" -m jerusalem_weather_mcp
```

The server waits for requests from an MCP client.

## MCP tool

`jerusalem_weekly_forecast` returns the next seven days of weather for Jerusalem, including the location, timezone, data source, and daily forecast details.

## Tests

Run the test suite with:

```powershell
& ".\.venv\Scripts\python.exe" -m unittest discover -s tests
```
