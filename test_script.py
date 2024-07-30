import requests

url = "http://192.168.2.30:5000/voice-input"
audio_file_path = r"C:\Users\LENOVO\test_audio.wav"  # Use raw string to handle backslashes

try:
    with open(audio_file_path, "rb") as audio_file:
        response = requests.post(url, data=audio_file)
    
    if response.status_code == 200:
        with open("response.wav", "wb") as f:
            f.write(response.content)
        print("Received audio response saved as response.wav")
    else:
        print(f"Failed to get response: {response.status_code}, {response.text}")
except FileNotFoundError:
    print(f"File not found: {audio_file_path}")
except Exception as e:
    print(f"An error occurred: {e}")
