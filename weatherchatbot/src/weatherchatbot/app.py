import logging
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
from typing import Dict, Any

# Import CrewAI Flow
from weather_crew import *
from flow import WeatherMapFlow

from fastapi import FastAPI
from fastapi.responses import FileResponse


# @app.get("/favicon.ico", include_in_schema=False)
# async def favicon():
#     return FileResponse("favicon.ico")  # Ensure you have a favicon.ico file

app = FastAPI()

# Root Route
@app.get("/")
def read_root():
    return {"message": "Weather Chatbot API is running. Use /docs for API documentation."}

# Configure Logging
logging.basicConfig(level=logging.INFO)

flow = WeatherMapFlow()

# Global Storage for Chatbot & Batch Mode
latest_chatbot_inputs = {}
latest_chatbot_result = {}

latest_batch_inputs = {}
latest_batch_result = {}

# Define Input Model
class Inputs(BaseModel):
    query: str
    #type_data: str  # "Response" for full AI output

class ChatbotOutputs(BaseModel):
    Response: str
    # type_data: str  # "Response" for full AI output

# Define output Model.
class BatchOutputs(BaseModel):
    location: str  # City Name
    temperature: float
    humidity: int
    conditions: str
    precipitation: float
    wind_speed: float
    extreme_alerts: str
    additional_info: str

# Batch Mode: Kickoff Processing
@app.post("/kickoff-parameters/")
async def kickoff_batch(inputs: Inputs):
    """Process chatbot-specific queries."""
    
    weather_inputs={"type_data": "Batch", "query": inputs.query}

    # Initialize and Run Flow
    #flow = WeatherMapFlow()
    try:
        Weather_crew = Crew(
            agents=[meteorologist_agent],  
            tasks=[find_meteorological_task],
            process=Process.sequential,
            verbose=True
        )
        weather_results = Weather_crew.kickoff(inputs={"type_data": "Batch", "query": inputs.query})
        # weather_results = flow.kickoff(inputs={"type_data": "Batch", "query": inputs.query})
    except Exception as e:
        logging.error(f"Error in WeatherMapFlow: {e}")
        return {"status": "error", "message": "Weather processing failed."}

    

    # Store latest Chatbot inputs & results
    global latest_batch_inputs, latest_batch_result
    latest_batch_inputs = weather_inputs
    latest_batch_result = {
        "Location": weather_results["location"],
        "Temperature (°C)": weather_results["temperature"],
        "Humidity (%)": weather_results["humidity"],
        "Weather Conditions": weather_results["conditions"],
        "Precipitation (mm)": weather_results["precipitation"],
        "Wind Speed (km/h)": weather_results["wind_speed"],
        "Extreme Alerts": weather_results["extreme_alerts"],
        "Additional Information": weather_results["additional_info"]
    }
    
    return {"Inputs": latest_batch_inputs}

# Get the results of pydantic output in Json format for Batch processing.
@app.get("/kickoff-parameters/")
async def get_last_result():
    if latest_batch_result is None or latest_batch_inputs is None:
        return {"message": "No results available. Please make a POST request to /kickoff/ first."}
    return {"Inputs": latest_batch_inputs, "Outputs": latest_batch_result}

# chatbot Mode: Kickoff Processing for sending input as query
@app.post("/kickoff-chatbot/")
async def kickoff_chatbot(inputs: Inputs):
    """Process chatbot-specific queries."""
    
    weather_inputs={"query": inputs.query}

    # Initialize and Run Flow
    #flow = WeatherMapFlow()
    try:
        Weather_crew = Crew(
            agents=[meteorologist_agent, weather_parameter_agent],
            tasks=[find_meteorological_task, weather_parameter_task],
            process=Process.sequential,
            verbose=True
        )
        weather_results = Weather_crew.kickoff(inputs={"query": inputs.query})
        # weather_results = flow.kickoff(inputs={"type_data": "Batch", "query": inputs.query})
    except Exception as e:
        logging.error(f"Error in WeatherMapFlow: {e}")
        return {"status": "error", "message": "Weather processing failed."}

    

    # Store latest Chatbot inputs & results
    global latest_chatbot_inputs, latest_chatbot_result
    latest_chatbot_inputs = weather_inputs
    # latest_chatbot_result = {
    #     "Response": weather_results       
    # }
    latest_chatbot_result = weather_results.raw
    
    return {"Inputs": latest_batch_inputs}

# Get the results for Chatbot QnA format.
@app.get("/kickoff-chatbot/")
async def get_last_chat_result():
    if latest_chatbot_result is None or latest_chatbot_inputs is None:
        return {"message": "No results available. Please make a POST request to /kickoff/ first."}
    return {"Inputs": latest_chatbot_inputs, "Outputs": latest_chatbot_result}

#  Run FastAPI Server when it needs to run using python cmd.
# if __name__ == "__main__":
#     uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
