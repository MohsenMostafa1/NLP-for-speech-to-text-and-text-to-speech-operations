import requests
import json

url = "http://192.168.1.6:5000/text-input"

data = {"input": "How many items do we have in San Diego?"}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.json())
