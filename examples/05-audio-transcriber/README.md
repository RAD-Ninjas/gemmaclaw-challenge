# 05 — Audio Transcriber

Record audio from a USB microphone and transcribe it locally using Gemma 4 E2B's audio understanding.

## What It Does

Captures a short audio clip, sends it to Gemma 4 E2B via Ollama, and gets a transcription. Everything runs locally.

## Prerequisites

- USB microphone connected to your Pi or laptop
- `arecord` (comes with ALSA on Raspberry Pi OS) or `sox`
- Ollama running with `gemma4:e2b`
- Python 3 with `requests`

## Run It

```bash
# Record 5 seconds and transcribe
python3 transcribe.py

# Record for a custom duration
python3 transcribe.py --duration 10

# Transcribe an existing audio file
python3 transcribe.py --file recording.wav
```

## How It Works

1. Records audio from the default microphone using `arecord`
2. Sends the audio to Gemma 4 E2B via Ollama's API (native audio input)
3. Prints the transcription

## Extend It

- Build a voice-controlled home assistant
- Add speaker diarization ("who said what")
- Create meeting notes from a recording
- Chain with the Telegram bot for voice messages
