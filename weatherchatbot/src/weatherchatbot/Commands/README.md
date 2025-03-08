# Weather_Prediction_Multi_Agents
Using LLM Multi Agents to Predict the Weather for a City 

Take-Home-Assignment:
docker build --build-arg OPENAI_API_KEY=your_api_key --build-arg WEATHER_API_KEY=your_weather_key -t crewai-weather .


# To stop or remove unwanted docker containers:
docker ps 
docker stop <container-id>
docker rm <container_id>

# Run in the path where file is present
docker build --no-cache -t crewai-weather .
docker run --rm -it crewai-weather /bin/bash

# Run the docker to verify containers and test the path
docker build --no-cache -t crewai-weather .  
docker run --rm --env-file .env crewai-weather
docker-compose up --build
docker-compose down

docker build --no-cache -t streamlit-application -f Dockerfile.streamlit .
docker run -p 8501:8501 --name streamlit-application streamlit-application
docker run -p 8501:8501 --name streamlit-application streamlit-application

# FastAPI Uvicorn commands to run and test API on different ports:
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
uvicorn app:app --host 127.0.0.1 --port 8000 --reload

# To kill any running ports thats interfering the usecase:
netstat -ano | findstr :8000

python -c "import os; os.system('taskkill /F /IM python.exe')"

# Mandatory Libraries needed to run the code of multiagents:
crewai>=0.79.4
python-dotenv
ipykernel
agentops 
crewai[tools]


