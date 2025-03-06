# Use the official Python image
FROM python:3.12.4

# Set the working directory
WORKDIR /app

# Copy project files
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Define environment variables
ARG OPENAI_API_KEY
ARG WEATHER_API_KEY

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV WEATHER_API_KEY=${WEATHER_API_KEY}

# Default command
CMD ["python3", "-u", "weather_crew.py"]
