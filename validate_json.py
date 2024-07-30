import json

try:
    with open('response.json', 'r') as json_file:
        response = json.load(json_file)
        print("JSON file is valid.")
        print(json.dumps(response, indent=4))
except json.JSONDecodeError as e:
    print("JSON file is invalid:", e)
except FileNotFoundError:
    print("JSON file not found.")
