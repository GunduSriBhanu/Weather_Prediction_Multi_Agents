
import os
from dotenv import load_dotenv
load_dotenv()
# import agentops
# agentops.init(api_key=os.getenv('AGENTOPS_API_KEY'))
from crewai.flow.flow import Flow, listen, start
from dotenv import load_dotenv
from crewai.flow.flow import Flow, listen, start, router, or_
from weather_crew import *

import logging
logging.basicConfig(level=logging.INFO)

# Define Weather_State
class Weather_State(BaseModel):
    query: str = Field("", description="Query for weather data.")
    type_data: str = Field("Response", description="Mode of execution: 'Batch' for parameters or 'Response' for full output")

# Define WeatherMapFlow
class WeatherMapFlow(Flow[Weather_State]):   
    
    # Start the flow of CrewAI
    @start()
    def start_flow(self):
        logging.info("🌟 Starting the Weather Prediction Flow.")
       
    # Initialize the data
    @listen(start_flow)
    def data_initializer(self):
        """Ensure the initial request is properly initialized."""
        # self.state.type_data = None
        # self.state.query = None        
        
    # Router is worked based on decision made either for Parameters mode or Full Response mode.
    @router(data_initializer)
    def crew_router(self):
        """Route AI to either **parameters-only** or **full response mode**."""
        logging.info(f"📌 Routing AI to: {self.state.type_data}")
        
        if self.state.type_data == "Batch":
            return "Parameters"
        else:
            return "Response"

    # Batch mode is used for batch processing and creating APIs that could be used to interact and store results in database.
    @listen("Parameters")
    def weather_Batch(self, assigned_crew):
        """Execute AI processing for either **Parameters or Full Response mode**."""      
        
        logging.info("Running in **Parameters Mode**.")
        Weather_crew = Crew(
            agents=[meteorologist_agent],  
            tasks=[find_meteorological_task],
            process=Process.sequential,
            verbose=True
        )
        
        request = {"query": self.state.query}
        weather_results = Weather_crew.kickoff(inputs=request)
        return weather_results
        
    # Response Mode is used for Chatbot Application especially frontend applications     
    @listen("Response")
    def weather_Chatbot(self, assigned_crew):
        """Execute AI processing for **Full Response mode**."""       
        
        logging.info("Running in **Chatbot Response Mode**.")
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

## Testing the flow of Router with results.
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

# weather_results = flow.kickoff(inputs={
#     "type_data": "Response",
#     "query": "What is the weather of New York?",
    
# })
# print(weather_results)
# agentops.end_session("Success") 