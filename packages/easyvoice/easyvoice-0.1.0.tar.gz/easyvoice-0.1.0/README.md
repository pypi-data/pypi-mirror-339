# EasyVoice

EasyVoice is a simple Python library for basic NLP, text-to-speech (TTS), and automatic speech recognition (ASR).

## Install

```bash
pip install easyvoice
```

## Usage

```python
from easyvoice import text_summary, text_to_speech, speech_to_text

print(text_summary("Hello. This is a test of summary."))
text_to_speech("Hello world", "hello.mp3")
print(speech_to_text("hello.wav"))
```
