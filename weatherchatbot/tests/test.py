import requests

# Set API URL (for Docker environment)
API_URL = "http://localhost:8000"  # If FastAPI is running on host
# API_URL = "http://host.docker.internal:8000"  # If testing from a container
# API_URL = "http://fastapi_app:8000"  # If using docker-compose

# Test Root Endpoint
response = requests.get(f"{API_URL}/")
print("Status Code:", response.status_code)
print("Response:", response.json())


