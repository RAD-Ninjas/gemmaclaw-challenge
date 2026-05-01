#!/usr/bin/env python3
"""
Audio Transcriber — Record and transcribe with Gemma 4 E2B.
Requires: USB microphone, Ollama with gemma4:e2b
"""

import subprocess
import requests
import base64
import sys
import os
import argparse
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma4:e2b"
AUDIO_PATH = "/tmp/gemmaclaw-audio.wav"


def record_audio(duration=5):
    """Record audio from the default microphone."""
    print(f"Recording {duration} seconds of audio...")
    try:
        # Try arecord first (ALSA, common on Pi)
        subprocess.run(
            ["arecord", "-d", str(duration), "-f", "S16_LE", "-r", "16000", "-c", "1", AUDIO_PATH],
            check=True,
            capture_output=True
        )
    except FileNotFoundError:
        try:
            # Fall back to sox
            subprocess.run(
                ["sox", "-d", "-r", "16000", "-c", "1", "-b", "16", AUDIO_PATH, "trim", "0", str(duration)],
                check=True,
                capture_output=True
            )
        except FileNotFoundError:
            print("Error: Neither arecord nor sox found.")
            print("  Pi/Linux: sudo apt install alsa-utils")
            print("  Mac: brew install sox")
            sys.exit(1)

    print(f"Audio saved to {AUDIO_PATH}")
    return AUDIO_PATH


def transcribe_audio(audio_path, prompt="Transcribe this audio accurately. Output only the transcription."):
    """Send audio to Gemma 4 E2B for transcription."""
    if not os.path.exists(audio_path):
        print(f"Error: Audio file not found: {audio_path}")
        sys.exit(1)

    with open(audio_path, "rb") as f:
        audio_base64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "audio": [audio_base64]
            }
        ],
        "stream": False
    }

    print(f"Sending to {MODEL} for transcription...")
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["message"]["content"]
    except requests.exceptions.ConnectionError:
        print("Error: Can't connect to Ollama. Is it running? Try: ollama serve")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Timed out. Try shorter audio or check model is loaded.")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Record and transcribe audio with Gemma 4 E2B")
    parser.add_argument("--duration", type=int, default=5, help="Recording duration in seconds (default: 5)")
    parser.add_argument("--file", type=str, help="Transcribe an existing audio file instead of recording")
    args = parser.parse_args()

    print("=" * 50)
    print("  Audio Transcriber — Gemma 4 E2B")
    print("=" * 50)
    print()

    if args.file:
        audio_path = args.file
    else:
        audio_path = record_audio(args.duration)

    print()
    transcription = transcribe_audio(audio_path)
    print()
    print("--- Transcription ---")
    print(transcription)
    print("---")
    print()
    print(f"Transcribed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
