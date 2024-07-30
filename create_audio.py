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
audio_segment.export(r"C:\Users\LENOVO\test_audio.wav", format="wav")  # Use a raw string
