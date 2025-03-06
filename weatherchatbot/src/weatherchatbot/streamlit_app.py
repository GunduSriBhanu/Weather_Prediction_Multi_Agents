import streamlit as st
from crewai import Crew, Process
from weather_crew import *

# ✅ Configure Streamlit Page
st.set_page_config(page_title="Weather Prediction", layout="wide")

# ✅ Streamlit UI Components
st.title("🌦️ AI-Powered Weather Prediction")
st.markdown("Enter **either** a **city and country** OR a **query** for weather information.")

# 🔹 User Input: Location or Query
city = st.text_input("Enter City", placeholder="e.g., Vancouver")
country = st.text_input("Enter Country (Optional, default = USA)", placeholder="e.g., Canada")
query = st.text_area("Enter Query (Optional)", placeholder="e.g., What is the temperature in Toronto?")

# 🔹 Ensure only one input is provided
if city and query:
    st.error("❌ Please enter either a city & country OR a query, not both.")

elif st.button("Get Weather"):
    if not city and not query:
        st.error("❌ Please provide a valid input.")

    else:
        # 🔥 Define the Weather Crew
        Weather_crew = Crew(
            agents=[meteorologist_agent, weather_parameter_agent],
            tasks=[find_meteorological_task, weather_parameter_task],
            process=Process.sequential,
            verbose=True
        )

        # 🔥 Construct the Input Query
        if city:
            user_query = f"What is the weather in {city}, {country or 'USA'}?"
        else:
            user_query = query.strip()

        request = {"query": user_query}
        st.info("🔍 Fetching weather data... Please wait.")

        # 🔥 Run the CrewAI Execution
        weather_results = Weather_crew.kickoff(inputs=request)
        print(weather_results)
        
        # ✅ Display Results
        if weather_results:
            st.success("✅ Weather Prediction Complete!")
            response_text = response_text = weather_results.raw if weather_results.raw else "No response generated."
            st.write(response_text)
        else:
            st.error("❌ No data received. Please check your input.")

# 🔹 Footer
st.markdown("---")
st.caption("🚀 Powered by **CrewAI & Streamlit**")
