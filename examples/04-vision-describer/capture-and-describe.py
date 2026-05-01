#!/usr/bin/env python3
"""
Vision Describer — Capture image from Pi Camera, describe with Gemma 4 E2B.
Requires: Raspberry Pi + Camera Module, Ollama with gemma4:e2b
"""

import subprocess
import requests
import base64
import sys
import os
from datetime import datetime

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma4:e2b"
IMAGE_PATH = "/tmp/gemmaclaw-capture.jpg"


def capture_image():
    """Capture an image from the Pi Camera."""
    print("Capturing image...")
    try:
        subprocess.run(
            ["libcamera-still", "-o", IMAGE_PATH, "-t", "2000", "--width", "640", "--height", "480", "-n"],
            check=True,
            capture_output=True
        )
        print(f"Image saved to {IMAGE_PATH}")
        return IMAGE_PATH
    except FileNotFoundError:
        print("Error: libcamera-still not found. Is a camera connected?")
        print("On Pi OS: sudo apt install libcamera-apps")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print(f"Error capturing image: {e}")
        sys.exit(1)


def describe_image(image_path, prompt="Describe what you see in this image in detail."):
    """Send image to Gemma 4 E2B via Ollama and get a description."""
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode("utf-8")

    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": prompt,
                "images": [image_base64]
            }
        ],
        "stream": False
    }

    print(f"Sending to {MODEL}...")
    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        result = response.json()
        return result["message"]["content"]
    except requests.exceptions.ConnectionError:
        print("Error: Can't connect to Ollama. Is it running? Try: ollama serve")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Error: Request timed out. Gemma 4 E2B on Pi can be slow — try again.")
        sys.exit(1)


def main():
    prompt = sys.argv[1] if len(sys.argv) > 1 else "Describe what you see in this image. Be specific about objects, colors, and the setting."

    print("=" * 50)
    print("  Vision Describer — Gemma 4 E2B + Pi Camera")
    print("=" * 50)
    print()

    image_path = capture_image()
    print()

    description = describe_image(image_path, prompt)
    print()
    print("--- Gemma 4 says ---")
    print(description)
    print("---")
    print()
    print(f"Captured at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


if __name__ == "__main__":
    main()
