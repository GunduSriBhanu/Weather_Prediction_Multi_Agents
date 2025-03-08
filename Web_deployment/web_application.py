import streamlit as st
import requests
import time
import os 
from dotenv import load_dotenv
load_dotenv()

HOST_FASTAPI = os.getenv("HOST_FASTAPI")
    
# Define API URLs
# BATCH_API_URL = "http://127.0.0.1:8000/kickoff-parameters/"
# BATCH_API_URL = "http://10.0.0.6:8000/kickoff-parameters/"
BATCH_API_URL = F"http://{HOST_FASTAPI}:8000/kickoff-parameters/"


# Page Selection
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Batch Mode"])

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
