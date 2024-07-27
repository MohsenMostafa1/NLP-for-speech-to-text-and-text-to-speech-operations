from flask import Flask, request, jsonify, send_file
import io
import torch
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import soundfile as sf
from gtts import gTTS
import json  # Add this import

app = Flask(__name__)

# Load pre-trained models and processors
stt_model_name = "facebook/wav2vec2-base-960h"
stt_processor = Wav2Vec2Processor.from_pretrained(stt_model_name)
stt_model = Wav2Vec2ForCTC.from_pretrained(stt_model_name)

# Speech-to-Text function
def speech_to_text(audio_bytes):
    audio_input, _ = sf.read(io.BytesIO(audio_bytes))
    input_values = stt_processor(audio_input, return_tensors="pt", sampling_rate=16000).input_values
    with torch.no_grad():
        logits = stt_model(input_values).logits
    predicted_ids = torch.argmax(logits, dim=-1)
    transcription = stt_processor.decode(predicted_ids[0])
    return transcription

# Text-to-Speech function
def text_to_speech(text):
    tts = gTTS(text)
    audio_bytes = io.BytesIO()
    tts.write_to_fp(audio_bytes)
    audio_bytes.seek(0)
    return audio_bytes

@app.route('/voice-input', methods=['POST'])
def voice_input():
    audio_bytes = request.data
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
    text = data['input']
    response_text = process_text(text)
    response = {"response": response_text}
    
    # Save response to a JSON file
    with open('response.json', 'w') as json_file:
        json.dump(response, json_file)

    return jsonify(response)

def process_text(text):
    # Basic NLP and business logic processing
    if "move" in text.lower():
        return "Sure, navigating to the adjust page for you."
    elif "receive" in text.lower():
        return "Please specify the quantity and location for the items you want to receive."
    elif "how many items" in text.lower():
        return "You have 500 items in San Diego."
    else:
        return "Hey, how can I assist you today?"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
