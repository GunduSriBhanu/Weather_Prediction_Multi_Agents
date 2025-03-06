import logging
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# ✅ Import CrewAI Flow
from weather_crew import *
from flow import WeatherMapFlow

# ✅ Configure Logging
logging.basicConfig(level=logging.INFO)

# ✅ Initialize FastAPI
app = FastAPI()

# ✅ Root Route
@app.get("/")
def read_root():
    return {"message": "Weather Chat BOT Application."}

# ✅ Define Request Model
class WeatherRequest(BaseModel):
    query: str
    type_data: str  # "Batch" for parameters or "Response" for full AI output

# ✅ GET: Chatbot Mode
@app.get("/get-chatbot")
def get_chatbot(query: str, type_data: str = "Response"):
    """Fetch weather data using GET request (Chatbot Mode)."""
    logging.info(f"📌 GET Request Received: query={query}, type_data={type_data}")

    # ✅ Initialize and Run Flow
    flow = WeatherMapFlow()
    weather_results = flow.kickoff(inputs={"type_data": type_data, "query": query})

    return {
        "status": "success",
        "weather_data": weather_results.json_dict if hasattr(weather_results, "json_dict") else "No data available"
    }

# ✅ PUT: Chatbot Mode
@app.put("/put-chatbot")
def put_chatbot(request: WeatherRequest):
    """Process weather query via PUT request (Chatbot Mode)."""
    logging.info(f"📌 PUT Request Received: {request}")

    # ✅ Initialize and Run Flow
    flow = WeatherMapFlow()
    weather_results = flow.kickoff(inputs={"type_data": request.type_data, "query": request.query})

    return {
        "status": "success",
        "weather_data": weather_results.json_dict if hasattr(weather_results, "json_dict") else "No data available"
    }

# ✅ GET: Parameters Mode
@app.get("/get-parameters")
def get_parameters(query: str, type_data: str = "Batch"):
    """Fetch weather parameters using GET request."""
    logging.info(f"📌 GET Request Received: query={query}, type_data={type_data}")

    # ✅ Initialize and Run Flow
    flow = WeatherMapFlow()
    weather_results = flow.kickoff(inputs={"type_data": type_data, "query": query})

    return {
        "status": "success",
        "weather_data": weather_results.json_dict if hasattr(weather_results, "json_dict") else "No data available"
    }

# ✅ PUT: Parameters Mode
@app.put("/put-parameters")
def put_parameters(request: WeatherRequest):
    """Process weather query via PUT request (Parameters Mode)."""
    logging.info(f"📌 PUT Request Received: {request}")

    # ✅ Initialize and Run Flow
    flow = WeatherMapFlow()
    weather_results = flow.kickoff(inputs={"type_data": request.type_data, "query": request.query})

    return {
        "status": "success",
        "weather_data": weather_results.json_dict if hasattr(weather_results, "json_dict") else "No data available"
    }

# ✅ Run FastAPI Server
if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)

