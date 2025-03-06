from typing import Type
import sys
sys.path.append("..")  # Add the parent directory to path
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import os  # If using environment variables for API keys
import json  # For parsing API responses
import requests  # For making HTTP requests
from dotenv import load_dotenv
from typing import Annotated, Optional, Any, Type
load_dotenv()


class WeatherMapToolInput(BaseModel):
    """Input schema for WeatherMapTool."""
    location: Annotated[str, Field(description="The location for which to fetch weather data.")]
    units: Annotated[
        str,
        Field(
            description="Units of measurement: 'metric' (Celsius, m/s) or 'imperial' (Fahrenheit, mph)",
            choices=["metric", "imperial"],
        ),
    ] = "metric"

class WeatherMapTool(BaseTool):
    name: str = "Weather Map Tool"
    description: str = "Fetches real-time weather data, including temperature, humidity, precipitation, and wind speed for a given location."
    args_schema: Type[BaseModel] = WeatherMapToolInput

    def _run(self, location: str, units: str = "metric") -> str:
        """Fetch weather data for a given location using OpenWeatherMap API."""
        api_key = os.getenv("WEATHER_API_KEY")  # Ensure API key is set in environment variables
        if not api_key:
            return "Error: API key is missing. Please set WEATHER_API_KEY."

        url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units={units}"
        response = requests.get(url)

        if response.status_code != 200:
            return f"Error: Unable to fetch weather data. Status code: {response.status_code}"

        data = response.json()  # Convert response to JSON

        # Debugging step to inspect API response
        print("API Response:", json.dumps(data, indent=4))

        # Extract weather details safely
        try:
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            conditions = data["weather"][0]["description"].capitalize()
            wind_speed = data["wind"]["speed"]
            precipitation = data.get("rain", {}).get("1h", 0)  # Get rainfall in mm (last 1 hour), default to 0

            unit_symbol = "°C" if units == "metric" else "°F"
            wind_unit = "m/s" if units == "metric" else "mph"

            return (
                f"Weather in {location}:\n"
                f"- Temperature: {temperature}{unit_symbol}\n"
                f"- Humidity: {humidity}%\n"
                f"- Conditions: {conditions}\n"
                f"- Precipitation: {precipitation} mm\n"
                f"- Wind Speed: {wind_speed} {wind_unit}"
            )
        except KeyError:
            return "Error: Unexpected API response structure."

# Test the API with an example
# if __name__ == "__main__":
#     weather_tool = WeatherMapTool()
#     result = weather_tool._run("New York")
#     print(result)
