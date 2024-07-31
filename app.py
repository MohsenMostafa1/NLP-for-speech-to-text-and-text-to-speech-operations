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
