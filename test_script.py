import requests

url = "http://192.168.1.6:5000/voice-input"
audio_file_path = "D:\AI/test_audio.wav"

with open(audio_file_path, "rb") as audio_file:
    response = requests.post(url, data=audio_file)

with open("response.wav", "wb") as f:
    f.write(response.content)

print("Received audio response saved as response.wav")
