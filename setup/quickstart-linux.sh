#!/bin/bash
# GemmaClaw Challenge — Linux (x86_64) Quickstart
set -e

echo "============================================"
echo "  GemmaClaw Challenge — Linux Quickstart"
echo "  github.com/RAD-Ninjas/gemmaclaw-challenge"
echo "============================================"
echo ""

echo "[1/3] Installing Ollama..."
command -v ollama &>/dev/null && echo "Ollama already installed" || curl -fsSL https://ollama.com/install.sh | sh

echo ""
echo "[2/3] Pulling Gemma 4 E2B (~1.5GB)..."
ollama pull gemma4:e2b

echo ""
echo "[3/3] Installing OpenClaw..."
if ! command -v node &>/dev/null; then
    echo "Installing Node.js 22..."
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt install -y -qq nodejs
fi
command -v openclaw &>/dev/null && echo "OpenClaw already installed" || npm install -g openclaw

mkdir -p ~/.openclaw
cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "llm": {
    "provider": "ollama",
    "baseUrl": "http://localhost:11434",
    "model": "gemma4:e2b"
  }
}
EOF

echo ""
echo "Done! Run: openclaw --model ollama/gemma4:e2b"
