from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv
from crewai.flow.flow import Flow, listen, start, router, or_
from weather_crew import *
import logging
logging.basicConfig(level=logging.INFO)



# ✅ Define Weather_State
class Weather_State(BaseModel):
    # row_number: int = 0
    # location: str = Field("", description="Geographical location for the weather data.")
    # temperature: float = Field(None, description="Current temperature in Celsius.")
    # humidity: int = Field(None, description="Humidity percentage.")
    # conditions: str = Field("", description="Weather condition like sunny, cloudy.")
    # precipitation: float = Field(None, description="Precipitation amount in mm.")
    # wind_speed: float = Field(None, description="Wind speed in meters per second.")
    # extreme_alerts: str = Field("None", description="Any extreme weather alerts.")
    # additional_info: str = Field("", description="Additional weather-related insights.")
    query: str = Field("", description="Query for weather data.")
    type_data: str = Field("Response", description="Mode of execution: 'Batch' for parameters or 'Response' for full output")

# ✅ Define WeatherMapFlow
class WeatherMapFlow(Flow[Weather_State]):   

    @start()
    def start_flow(self):
        logging.info("🌟 Starting the Weather Prediction Flow.")
       

    @listen(start_flow)
    def data_initializer(self):
        """Ensure the initial request is properly initialized."""
        # self.state.type_data = None
        # self.state.query = None        
        

    @router(data_initializer)
    def crew_router(self):
        """Route AI to either **parameters-only** or **full response mode**."""
        logging.info(f"📌 Routing AI to: {self.state.type_data}")
        
        if self.state.type_data == "Batch":
            return "Parameters"
        else:
            return "Response"

    
    @listen("Parameters")
    def weather_Batch(self, assigned_crew):
        """Execute AI processing for either **Parameters or Full Response mode**."""      
        
        logging.info("📌 Running in **Parameters Mode**.")
        Weather_crew = Crew(
            agents=[meteorologist_agent],  
            tasks=[find_meteorological_task],
            process=Process.sequential,
            verbose=True
        )
        
        request = {"query": self.state.query}
        weather_results = Weather_crew.kickoff(inputs=request)

        return weather_results
        
        
    @listen("Response")
    def weather_Chatbot(self, assigned_crew):
        """Execute AI processing for either **Parameters or Full Response mode**."""       
        
        logging.info("📌 Running in **Parameters Mode**.")
        Weather_crew = Crew(
            agents=[meteorologist_agent, weather_parameter_agent],
            tasks=[find_meteorological_task, weather_parameter_task],
            process=Process.sequential,
            verbose=True
        )
        request = {"query": self.state.query}
        weather_results = Weather_crew.kickoff(inputs=request)

        return weather_results

# Plot the flow image of crew ai Multi agents work flow
flow = WeatherMapFlow()
flow_plot = flow.plot("flow.png")

# weather_results = flow.kickoff()

# flow = WeatherMapFlow(state=Weather_State(
#     type_data="Batch",  # "Batch" for parameters, "Response" for full output
#     query="What is the weather of New York?"
# ))


# flow = WeatherMapFlow()
# weather_results = flow.kickoff(inputs={
#     "type_data": "Batch",
#     "query": "What is the weather of New York?",
    
# })

# Response
# weather_results = flow.kickoff(inputs={
#     "type_data": "Response",
#     "query": "What is the weather of New York?",
    
# })
# print(weather_results)