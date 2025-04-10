import nltk
from gtts import gTTS
import speech_recognition as sr

# Download NLTK data if not present
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

from nltk.tokenize import sent_tokenize

def text_summary(text):
    sentences = sent_tokenize(text)
    return sentences[0] if sentences else ""

def text_to_speech(text, filename="output.mp3"):
    tts = gTTS(text)
    tts.save(filename)
    return filename

def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
    return recognizer.recognize_google(audio)
