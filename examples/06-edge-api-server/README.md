# 06 — Edge API Server

Turn your Pi into a local AI API server that other devices on your network can query.

## What It Does

A lightweight HTTP server that exposes Gemma 4 E2B as a REST API on your local network. Any device (phone, laptop, another Pi) can send requests — all inference stays local.

## Prerequisites

- Ollama running with `gemma4:e2b`
- Python 3 with `flask` and `requests`

## Setup

```bash
pip3 install flask requests
```

## Run It

```bash
python3 server.py
```

The server starts on port 5000. From any device on the same network:

```bash
curl http://<your-pi-ip>:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is the capital of France?"}'
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/chat` | Send a message, get a response |
| POST | `/api/describe` | Send a base64 image, get a description |
| GET | `/api/health` | Check if the server and model are running |

## Extend It

- Add authentication (API key header)
- Build a web frontend that calls this API
- Connect multiple Pis for load balancing
- Add rate limiting for shared deployments
