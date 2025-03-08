import streamlit as st
import requests
import time
from crewai import Crew, Process
from weather_crew import *
from flow import WeatherMapFlow

from dotenv import load_dotenv
load_dotenv()

## Configure API KEYS to Support multiple environments
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

# Verifying API KEYS are provided
if not OPENAI_API_KEY or not WEATHER_API_KEY:
    raise ValueError("API keys are missing! Ensure they are set in the environment variables.")
    
# Define API URLs
BATCH_API_URL = "http://127.0.0.1:8000/kickoff-parameters/"


# Page Selection
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Batch Mode", "Chatbot Mode"])

# Function to call FastAPI and display results
def fetch_weather(api_url, query):
    headers = {"Content-Type": "application/json"}
    payload = {"query": query}

    # Send POST request
    st.info("Sending request to the API...")
    post_response = requests.post(api_url, json=payload, headers=headers)

    if post_response.status_code == 200:
        st.success("Request submitted successfully.")
    else:
        st.error(f"Error {post_response.status_code}: {post_response.text}")
        return None

    # Wait for processing
    time.sleep(2)

    # Send GET request to fetch results
    get_response = requests.get(api_url, headers=headers)

    if get_response.status_code == 200:
        return get_response.json().get("Outputs", {})
    else:
        st.error(f"Error {get_response.status_code}: {get_response.text}")
        return None

# **Page 1: Batch Mode**
if page == "Batch Mode":
    st.title("🌤 Batch Mode: Weather Report")
    st.write("Enter a location to get batch weather data.")

    query = st.text_input("Enter query", "what is the weather in New York?")

    if st.button("Get Weather Data"):
        result = fetch_weather(BATCH_API_URL, query)
        if result:
            st.json(result)

# **Page 2: Chatbot Mode**
elif page == "Chatbot Mode":
    st.title("💬 Chatbot Mode: Weather Chat Assistant")
    st.subheader("Ask the chatbot about the weather.")
    
    # User Inputs either Query or fields of Location and Country
    city = st.text_input("Enter City", placeholder="e.g., Vancouver")
    country = st.text_input("Enter Country (Optional, default = USA)", placeholder="e.g., Canada")
    query = st.text_area("Enter Query (Optional)", placeholder="e.g., What is the temperature in Toronto?")

    # Ensure only either of cases in inputs are accepted
    if city and query:
        st.error("❌ Please enter either a city & country OR a query, not both.")
    
    elif st.button("Get Weather"):
        if not city and not query:
            st.error("❌ Please provide a valid input.")
    
        else:
            # Define the Crewai Process to run the crew workflow
            flow = WeatherMapFlow()
            
            weather_results = flow.kickoff(inputs={
                "type_data": "Response",
                "query": query,
              
            })
    
            # Construct the input query based on user inputs
            if city:
                user_query = f"What is the weather in {city}, {country or 'USA'}?"
            else:
                user_query = query.strip()
            
            # Execute crewai sequentially
            request = {
                "type_data": "Response",
                "query": user_query,
              
            }
            st.info("🔍 Fetching weather data... Please wait.")
                
            weather_results = flow.kickoff(inputs=request)
            print(weather_results)
            
            # Display the results
            if weather_results:
                st.success("✅ Weather Prediction Complete!")
                response_text = response_text = weather_results.raw if weather_results.raw else "No response generated."
                st.write(response_text)
            else:
                st.error("❌ No data received. Please check your input.")

