
import os
import tiktoken 
import yaml
from crewai import Agent, Task, Crew,Process, LLM
from crewai.project import CrewBase, agent, crew, task
from pydantic import BaseModel, Field, HttpUrl
from tools.weather_tool import WeatherMapTool
from typing import List

# import agentops
from dotenv import load_dotenv
load_dotenv()
import logging

openai_api_key = os.getenv("OPENAI_API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Configure logging for CrewAI
logging.basicConfig(
    level=logging.DEBUG,  # Capture all debug and verbose logs
    format="%(asctime)s - %(levelname)s - %(message)s"
)

files = {
    'agents': r'config\agents.yaml',
    'tasks': r'config\tasks.yaml'
}

weather_tool = WeatherMapTool()

class WeatherChatbot(BaseModel):
    location: str = Field(..., description="The location for which the weather data is provided.")
    temperature: float = Field(..., description="Current temperature in Celsius.")
    humidity: float = Field(..., description="Measured humidity percentage.")
    conditions: str = Field(..., description="Description of the overall weather (e.g., sunny, rainy, cloudy).")
    precipitation: float = Field(None, description="Amount of rainfall or snowfall in mm (if any).")
    wind_speed: float = Field(..., description="Measured wind speed in meters per second.")
    extreme_alerts: str = Field(
        None, description="Any extreme weather conditions or warnings for the location."
    )
    additional_info: str = Field(
        None, description="Additional insights on weather trends, anomalies, or forecast predictions."
    )



# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']

# Define the WeatherChatbot Pydantic Model
class WeatherChatbot(BaseModel):
    location: str = Field(..., description="The location for which the weather data is provided.")
    temperature: float = Field(..., description="Current temperature in Celsius.")
    humidity: float = Field(..., description="Measured humidity percentage.")
    conditions: str = Field(..., description="Description of the overall weather (e.g., sunny, rainy, cloudy).")
    precipitation: float = Field(None, description="Amount of rainfall or snowfall in mm (if any).")
    wind_speed: float = Field(..., description="Measured wind speed in meters per second.")
    extreme_alerts: str = Field(None, description="Any extreme weather conditions or warnings for the location.")
    additional_info: str = Field(None, description="Additional insights on weather trends, anomalies, or forecast predictions.")

# Creating the Meteorologist Agent
meteorologist_agent = Agent(
    config=agents_config['meteorologist'],
    memory=True,  
    verbose=True,  
    allow_delegation=False,
    tools=[weather_tool]  # Weather-related search tool
)

# Creating the Weather Parameter Agent
weather_parameter_agent = Agent(
    config=agents_config['weather_parameter_agent'],
    memory=True,
    verbose=True,
    allow_delegation=False
)

# Creating the Meteorology Task
find_meteorological_task = Task(
    config=tasks_config['meteorologist_task'],
    agent=meteorologist_agent,
    output_pydantic=WeatherChatbot  # Ensuring correct structured output
)

# Creating the parameters Task
weather_parameter_task = Task(
    config=tasks_config['weather_parameter_task'],
    agent=weather_parameter_agent
)

# Creating the Weather Crew (Corrected)
Weather_crew = Crew(
    agents=[meteorologist_agent, weather_parameter_agent],  # Only includes weather-related agents
    tasks=[find_meteorological_task, weather_parameter_task],  # Only includes weather-related tasks
    process=Process.sequential,  # Tasks execute in order
    verbose=True
)

# Test with Query
request = {"query": "What is the temperature in Vancouver and London?"}

# Run the Crew Execution
weather_results = Weather_crew.kickoff(inputs=request)
print(weather_results)


print(f"Tasks Output: {weather_results.tasks_output}")
print(f"Token Usage: {weather_results.token_usage}")
print(Weather_crew.usage_metrics)

