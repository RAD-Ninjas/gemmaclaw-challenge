#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if ! command -v ollama >/dev/null 2>&1; then
  echo "ollama not found — run ../../setup/quickstart-pi.sh first"
  exit 1
fi

if ! ollama list | grep -q "^vibes-judge"; then
  echo "Building vibes-judge model..."
  ollama create vibes-judge -f Modelfile.vibes-judge
fi

python3 -c "import serial" 2>/dev/null || pip3 install pyserial requests

exec python3 pitcher_protocol.py "$@"
