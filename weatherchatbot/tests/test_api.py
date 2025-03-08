import requests
import time

###  TEST CASE FOR BATCH DATA

# Define API URL
BASE_URL = "http://127.0.0.1:8000/kickoff-parameters/"

# Step 1: Send a POST request to store input
payload = {
    "query": "What is the weather in New York?"
}
headers = {"Content-Type": "application/json"}

print("Sending POST request...")
post_response = requests.post(BASE_URL, json=payload, headers=headers)

# Check if POST request was successful
if post_response.status_code == 200:
    print("POST request successful.")
else:
    print(f"POST request failed: {post_response.status_code}, {post_response.text}")
    exit()

# Step 2: Wait for processing (if necessary)
time.sleep(2)

# Step 3: Send a GET request to retrieve results
print("Sending GET request to fetch results...")
get_response = requests.get(BASE_URL, headers=headers)

# Check if GET request was successful
if get_response.status_code == 200:
    outputs = get_response.json().get('Outputs', {})
    print("Outputs:", outputs)
else:
    print(f"GET request failed: {get_response.status_code}, {get_response.text}")

#### TEST CASE FOR CHATBOT

# Define API URL
BASE_URL_CHATBOT = "http://127.0.0.1:8000/kickoff-chatbot/"

# Step 1: Send a POST request to store input
payload = {
    "query": "What is the weather in New York?"
}
headers = {"Content-Type": "application/json"}

print("Sending POST request...")
post_response = requests.post(BASE_URL_CHATBOT, json=payload, headers=headers)

# Check if POST request was successful
if post_response.status_code == 200:
    print("POST request successful.")
else:
    print(f"POST request failed: {post_response.status_code}, {post_response.text}")
    exit()

# Step 2: Wait for processing (if necessary)
time.sleep(2)

# Step 3: Send a GET request to retrieve results
print("Sending GET request to fetch results...")
get_response = requests.get(BASE_URL_CHATBOT, headers=headers)

# Check if GET request was successful
if get_response.status_code == 200:
    outputs = get_response.json().get('Outputs', {})
    print("Outputs:", outputs)
else:
    print(f"GET request failed: {get_response.status_code}, {get_response.text}")
