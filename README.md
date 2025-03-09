# Weather_Prediction_Multi_Agents
Using LLM Multi Agents to Predict the Weather for a City 

Take-Home-Assignment:

## Steps to run Code:
### Step 1: 
Ensure Python 3.12 is installed
Create env **python -m venv myenv**
activate env using **myenv\Scripts\activate**

### Step 2:
Add .env file with assigned following parameters:
- MODEL="gpt-4o-mini"
- OPEN_API_KEY = "<open_api_key>"
- WEATHER_API_KEY="<weather_api_key>"
- HOST_FASTAPI=<IPV4_Address>  
- AGENTOPS_API_KEY = <agentops_Key>
  - 'which are used for both streamlit and fastapi"

### Step 3:
- Go to path **weatherchatbot\src\weatherchatbot**
- Use command **docker-compose up --build** to build the docker compose file that builds overall Crewai flow, fast api and streamlit application.

### Step 4:
Use the **http://localhost:8501** url to test the streamlit application for weather prediction.

## Flow of Crewai:
![image](https://github.com/user-attachments/assets/1a934bb1-4f5f-4082-b4fa-7cd145f068a7)

This code is designed to create a **multi-agent system** using the **CrewAI** framework to process and respond to weather-related queries. Let's break it down step by step to explain each part of the code:

### **1. Importing Dependencies**

- `from crewai.flow.flow import Flow, listen, start`: These imports are used to work with the **CrewAI** framework, specifically for creating the flow and using listeners for agent-based processing.
- `from dotenv import load_dotenv`: This is used to load environment variables from a `.env` file (though it isn't actively used in this script).
- `from weather_crew import *`: This imports weather-related modules, agents, and tasks from the `weather_crew` module (which is assumed to contain predefined tasks and agents for weather processing).
- `import logging`: Sets up logging to monitor the flow’s activities. The logging level is set to `INFO`, so the system will log informational messages.

### **2. Define the `Weather_State` Class**

- `Weather_State` is a **data model** used to define the state for each flow. It uses `BaseModel` (presumably from **Pydantic**) to validate and define the data structure. It contains:
  - `query`: A string representing the weather query that the user will ask (e.g., "What is the weather like in New York?").
  - `type_data`: A string that indicates the mode of execution. It can be either `"Batch"` (for parameters only) or `"Response"` (for the full output with detailed information).

### **3. Define the `WeatherMapFlow` Class**

- `WeatherMapFlow` inherits from `Flow[Weather_State]`, which means it is a **CrewAI flow** that operates based on the `Weather_State` model.

#### **Flow Start:**

- The `start_flow` function is defined as the **starting point** of the flow. It logs a message indicating the flow has started.

#### **Data Initialization:**

- This function, `data_initializer`, ensures that the initial request is properly initialized when the flow starts. In this case, the initial state for the `query` and `type_data`.

#### **Routing Logic (`crew_router`):**

- The `crew_router` decides which path the flow should take based on the `type_data` field in `Weather_State`. It either routes to `"Parameters"` mode (for **Batch** mode) or `"Response"` mode for a **full response**. It logs which path it will take.

#### **Parameters Mode (`weather_Batch`):**

- If the flow is routed to `"Parameters"` (Batch mode), the `weather_Batch` function is executed. It uses the `CrewAI` framework to initialize a **crew** (group of agents) and assign them tasks. Here:
  - The `meteorologist_agent` and the `find_meteorological_task` are presumably pre-defined agents and tasks for weather prediction.
  - `Process.sequential` indicates that the tasks will be processed sequentially.
  - The `kickoff` function initiates the process, using the `query` passed in the state.
  - The results from the task execution (weather-related results) are returned which are in pydantic form and can be further used as parameters to store in any database.

#### **Response Mode (`weather_Chatbot`):**

- If the flow is routed to `"Response"` mode, the `weather_Chatbot` function is executed. It involves a **chatbot-like processing** where multiple agents (`meteorologist_agent` and `weather_parameter_agent`) and tasks (`find_meteorological_task` and `weather_parameter_task`) are used to return a full response. This includes both **parameters** and **detailed response** in a logical sentence, which is used for chatbot Qna applications.

### **4. Plotting the Flow Image**

- This part of the code uses **CrewAI's** `plot` method to generate a flow diagram that visually represents how the agents interact and work together in the weather prediction process. The diagram will be saved as `"flow.png"`.

### **5. Flow Kickoff (Running the Flow)**

- The flow can be started by calling `flow.kickoff()`, passing the necessary inputs (e.g., query and type of data). This step is commented out, but it shows where the flow could be triggered with specific inputs.

### **Summary:**

- The **`WeatherMapFlow`** class uses the **CrewAI** framework to build a **multi-agent system** that processes weather-related queries in two modes:
  - **Batch mode** (`Parameters`): Extracts meteorological parameters (e.g., temperature, humidity) without detailed information.
  - **Response mode** (`Response`): Returns a full, detailed response based on the query.
- The flow uses **agents** and **tasks** to process data sequentially.
- The system routes between different modes based on the `type_data` in the `Weather_State` (which can be either `"Batch"` or `"Response"`).
- The flow diagram is plotted to visualize the interaction of agents and tasks in the process.

This code represents a system that intelligently routes weather-related queries through different processing modes (either parameter-based or full response) using AI agents, ensuring the process is both efficient and adaptive to the type of query being made.

## Fast API created APIs:
- The FastAPI application provides two types of routes: one for processing chatbot queries (full responses) and one for processing batch queries (only meteorological parameters).
- The input query is passed through CrewAI agents for processing.
- The results are stored globally for later retrieval and are returned to the user through POST and GET requests.
- The application uses FastAPI for building a web service to handle these requests and CrewAI for handling the complex weather data processing.

## Streamlit Application:
### Batch Mode:
- In Batch Mode, users are asked to input a location (e.g., "What is the weather in New York?") via a text input field.
- When the user presses the "Get Weather Data" button, the fetch_weather function is invoked, and the weather data is returned and displayed in JSON format. This is typically used to get basic meteorological parameters like temperature, humidity, and conditions.

### Chatbot Mode:
- In Chatbot Mode, users can input a city and optionally a country (e.g., "Enter City: Vancouver" and "Enter Country: Canada"). Alternatively, users can provide a query like "What is the temperature in Toronto?".
- The app checks that only one type of input is provided: either a city and country or a query. If both are provided, it shows an error message.
- The flow then creates a query based on the user's input (either from the city/country or the provided query).
- The query is passed into the CrewAI workflow to trigger the WeatherMapFlow process. The flow interacts with the CrewAI agents and processes the query in Response mode, which provides a more detailed weather prediction.
- The results are then displayed as a response text generated by the WeatherMapFlow. If the process returns an error or no data, an error message is shown.

#### Flow with CrewAI:
- Inside the Chatbot Mode, a CrewAI flow is initialized to handle the weather query. The WeatherMapFlow is used to kick off a weather query and process it sequentially, using the predefined weather agents in the CrewAI framework.
- The response is then processed and displayed to the user in a readable format.

### User Interaction:
- The user interacts with the web interface using the Streamlit widgets:
- Text inputs for the query or city/country.
- Buttons to trigger the weather data retrieval.
- Info, success, and error messages to guide the user through the process.
- Based on the mode selected (Batch or Chatbot), the respective API is called, and the weather data is displayed.

### Key Highlights:
- Batch Mode: Provides weather parameters (e.g., temperature, humidity) for a given location.
- Chatbot Mode: Allows users to ask more complex weather queries and gets a detailed response.
- Interaction with FastAPI: The app communicates with a FastAPI backend that processes the weather data using CrewAI agents.
- Environment Variables: API keys for OpenAI and Weather API are retrieved from environment variables to ensure security.
- User-friendly Interface: The application is built using Streamlit for quick web deployment, providing real-time feedback for user inputs and API responses.

## Conclusion:
This script enables users to interact with a weather chatbot via a web interface, choosing between simple parameter queries or detailed weather reports. It utilizes CrewAI to process the queries and FastAPI for handling API requests, making it easy to integrate AI-driven weather predictions into the app using Openweather API tool on open ai Chat GPT-4.0-mini Model.
