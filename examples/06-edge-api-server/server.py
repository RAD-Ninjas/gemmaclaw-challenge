#!/usr/bin/env python3
"""
Edge API Server — Expose Gemma 4 E2B as a local network REST API.
Requires: pip3 install flask requests
"""

import requests
import base64
from flask import Flask, request, jsonify

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434"
MODEL = "gemma4:e2b"


def query_ollama(messages, timeout=120):
    """Send messages to Ollama and return the response."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False
    }
    response = requests.post(f"{OLLAMA_URL}/api/chat", json=payload, timeout=timeout)
    response.raise_for_status()
    return response.json()["message"]["content"]


@app.route("/api/health", methods=["GET"])
def health():
    """Check if Ollama is running and the model is available."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        model_loaded = any(MODEL.split(":")[0] in m for m in models)
        return jsonify({
            "status": "ok",
            "ollama": "running",
            "model": MODEL,
            "model_available": model_loaded,
            "available_models": models
        })
    except requests.exceptions.ConnectionError:
        return jsonify({"status": "error", "ollama": "not running"}), 503


@app.route("/api/chat", methods=["POST"])
def chat():
    """Send a message and get a response from Gemma 4 E2B."""
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    system_prompt = data.get("system", "You are a helpful assistant running on local hardware.")

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": data["message"]}
    ]

    try:
        response = query_ollama(messages)
        return jsonify({"response": response, "model": MODEL})
    except requests.exceptions.Timeout:
        return jsonify({"error": "Model timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/describe", methods=["POST"])
def describe():
    """Send a base64-encoded image and get a description."""
    data = request.get_json()
    if not data or "image" not in data:
        return jsonify({"error": "Missing 'image' field (base64-encoded)"}), 400

    prompt = data.get("prompt", "Describe what you see in this image.")

    messages = [
        {
            "role": "user",
            "content": prompt,
            "images": [data["image"]]
        }
    ]

    try:
        response = query_ollama(messages, timeout=180)
        return jsonify({"description": response, "model": MODEL})
    except requests.exceptions.Timeout:
        return jsonify({"error": "Vision inference timed out"}), 504
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print(f"Starting Edge API Server with {MODEL}")
    print(f"Endpoints:")
    print(f"  POST /api/chat     — text chat")
    print(f"  POST /api/describe — image description")
    print(f"  GET  /api/health   — status check")
    print()
    # Listen on all interfaces so other devices can reach it
    app.run(host="0.0.0.0", port=5000, debug=False)
