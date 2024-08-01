# NLP-for-speech-to-text-and-text-to-speech-operations
<figure>
        <img src="https://fireflies.ai/blog/content/images/size/w2000/2022/12/Speech-to-Text-Software--1-.jpg" alt ="Audio Art" style='width:800px;height:500px;'>
        <figcaption>

This report covers the implementation and functionality of five Python scripts: create_audio.py, app.py, test_flask.py, test_script.py, and validate_json.py. These scripts are part of a Flask web application designed to handle speech-to-text and text-to-speech operations.

### 1- create_audio.py
Purpose

The create_audio.py script generates an MP3 audio file from text and converts it into a WAV file using the gTTS library and pydub.
#### Code
 ```python
from gtts import gTTS
from pydub import AudioSegment
from pydub.utils import which

AudioSegment.converter = which("ffmpeg")
AudioSegment.ffmpeg = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# Define the text you want to convert to speech
text = "This is a test audio for the Flask application."

# Generate speech using gTTS
tts = gTTS(text=text, lang='en')

# Save the generated speech to an mp3 file
tts.save("test_audio.mp3")

# Convert mp3 to wav format
audio_segment = AudioSegment.from_mp3("test_audio.mp3")
audio_segment.export(r"D:\AI\test_audio.wav", format="wav")
```
### Functionality

Text-to-Speech: Converts a given text into an MP3 file using Google Text-to-Speech (gTTS).
Format Conversion: Converts the generated MP3 file into a WAV file using pydub.

Dependencies

gTTS
pydub
ffmpeg

### 2- app.py
#### Purpose

The app.py script sets up a Flask web server that provides endpoints for speech-to-text and text-to-speech processing.
#### Code
 ```python
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import soundfile as sf
from gtts import gTTS
import json

app = Flask(__name__)
CORS(app)  # Enable CORS support

# Load pre-trained models and processors
stt_model_name = "facebook/wav2vec2-base-960h"
stt_processor = Wav2Vec2Processor.from_pretrained(stt_model_name)
stt_model = Wav2Vec2ForCTC.from_pretrained(stt_model_name)

# Root endpoint for testing
@app.route('/')
def index():
    return "Welcome to the Flask App"

# Speech-to-Text function
def speech_to_text(audio_bytes):
    print("Processing audio for speech-to-text")
    audio_input, _ = sf.read(io.BytesIO(audio_bytes))
    input_values = stt_processor(audio_input, return_tensors="pt", sampling_rate=16000).input_values
    with torch.no_grad():
        logits = stt_model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = stt_processor.decode(predicted_ids[0])
    print(f"Transcription: {transcription}")
    return transcription

# Text-to-Speech function
def text_to_speech(text):
    print(f"Generating speech for text: {text}")
    tts = gTTS(text)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

@app.route('/voice-input', methods=['POST'])
def voice_input():
    audio_bytes = request.data
    print(f"Received audio bytes: {len(audio_bytes)} bytes")
    text = speech_to_text(audio_bytes)
    response_text = process_text(text)
    audio_response = text_to_speech(response_text)
    return send_file(
        audio_response,
        mimetype="audio/wav",
        as_attachment=True,
        attachment_filename="response.wav"
    )

@app.route('/text-input', methods=['POST'])
def text_input():
    data = request.get_json()
    print(f"Received text input: {data}")
    text = data['input']
    response_text = process_text(text)
    response = {"response": response_text}
    
    # Save response to a JSON file
    with open('response.json', 'w') as json_file:
        json.dump(response, json_file)
    
    print(f"Response text: {response_text}")
    return jsonify(response)

def process_text(text):
    # Basic NLP and business logic processing
    print(f"Processing text: {text}")
    if "move" in text.lower():
        return "Sure, navigating to the adjust page for you."
    elif "receive" in text.lower():
        return "Please specify the quantity and location for the items you want to receive."
    elif "how many items" in text.lower():
        return "You have 500 items in San Diego."
    else:
        return "Hey, how can I assist you today?"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```
### Functionality

Speech-to-Text Endpoint (/voice-input):
 Accepts audio data.
 Converts the audio to text using Wav2Vec2.
 Processes the text and generates a response.
 Converts the response text back to audio and returns it.

Text-to-Speech Endpoint (/text-input):
 Accepts JSON data containing text.
 Processes the text and generates a response.
 Returns the response as JSON.

Text Processing:
 Basic NLP logic to interpret and respond to the user's text.

### Dependencies

Flask
torch
transformers
soundfile
gTTS

### 3- test_flask.py
#### Purpose

The test_flask.py script is used to test the /text-input endpoint of the Flask application.
#### Code
```python
import requests
import json

url = "http://127.0.0.1:5000/text-input"

data = {"input": "How many items do we have in San Diego?"}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

print(response.json())
```
### Functionality

    Sends a POST request to the /text-input endpoint with a sample text input.
    Prints the JSON response from the server.

#### Dependencies

    requests

### 4- test_script.py
#### Purpose

The test_script.py script is used to test the /voice-input endpoint of the Flask application.
#### Code 
```python
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
```
### Functionality

Sends a POST request to the /voice-input endpoint with a sample WAV audio file.
Saves the audio response from the server as response.wav.

#### Dependencies

requests

### 5- validate_json.py
#### Purpose

The validate_json.py script validates the structure and content of the response.json file created by the Flask application.
#### Code  
```python
import json
import os

try:
    with open('response.json', 'r') as json_file:
        response = json.load(json_file)
        print("JSON file is valid.")
        print(json.dumps(response, indent=4))
except json.JSONDecodeError as e:
    print("JSON file is invalid:", e)
except FileNotFoundError:
    print("JSON file not found.")
```
### Functionality

Checks if response.json exists.
Validates the JSON structure and prints it.
Reports any errors in the JSON format.

#### Dependencies

json
os
    
