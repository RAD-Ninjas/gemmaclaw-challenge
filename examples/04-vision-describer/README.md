# 04 — Vision Describer

Use the Pi Camera + Gemma 4 E2B's native vision to describe what it sees.

## What It Does

Captures an image from the Pi Camera, sends it to Gemma 4 E2B, and gets a natural language description.

## Prerequisites

- Raspberry Pi 5 with Camera Module v2 or v3
- `libcamera` installed (comes with Raspberry Pi OS)

## Run It

```bash
python3 capture-and-describe.py
```

## How It Works

1. Captures a still image using `libcamera-still`
2. Sends the image to Gemma 4 E2B via Ollama's API (native vision support)
3. Prints Gemma's description of the scene

## Extend It

- Loop it for continuous descriptions (security camera style)
- Add motion detection — only describe when something changes
- Use Gemma 4's multilingual support to describe in different languages
- Add audio output with Piper TTS for a "talking camera"
