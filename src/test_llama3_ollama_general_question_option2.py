import requests
import json

# Set the API endpoint URL and the input text
url = "http://localhost:11434/api/generate"
input_text = "what are color of rose?"
prompt = "what are color of rose?"
question = "what are color of rose?"
# Set the request headers
headers = {
    "Content-Type": "application/json"
}

# Convert the input text to JSON format
#data = json.dumps({"prompt": input_text})

data = {
    "model":"llama3",
    "prompt": prompt,
    "question": question
}
# Send a POST request to the API endpoint with the input text
#response = requests.post(url, headers=headers, data=data)
response = requests.post(url, headers=headers, data=json.dumps(data))
#response = requests.post(url, data=json.dumps(data))


# Check if the response was successful (200 OK)
if response.status_code == 200:
    # Get the response text from the JSON response
    #response_text = json.loads(response.content)["response"]
    print(response.status_code)
    print(response.text)
    #print(f"Response: {response_text}")
else:
    print(response.status_code)