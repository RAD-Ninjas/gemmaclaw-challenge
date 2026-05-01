#!/bin/bash
# GemmaClaw Challenge — Mac Quickstart
# Installs Ollama, Gemma 4 E2B, and OpenClaw

set -e

echo "============================================"
echo "  GemmaClaw Challenge — Mac Quickstart"
echo "  github.com/RAD-Ninjas/gemmaclaw-challenge"
echo "============================================"
echo ""

# Step 1: Install Ollama
echo "[1/3] Installing Ollama..."
if command -v ollama &> /dev/null; then
    echo "Ollama already installed: $(ollama --version)"
else
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Pull Gemma 4 E2B
echo ""
echo "[2/3] Pulling Gemma 4 E2B (~1.5GB download)..."
ollama pull gemma4:e2b

# Step 3: Install OpenClaw
echo ""
echo "[3/3] Installing OpenClaw..."
if ! command -v node &> /dev/null; then
    echo "Node.js not found. Install it via: brew install node"
    echo "Then re-run this script."
    exit 1
fi

if command -v openclaw &> /dev/null; then
    echo "OpenClaw already installed"
else
    npm install -g openclaw
fi

# Configure
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
echo "============================================"
echo "  Setup complete!"
echo "============================================"
echo ""
echo "  Test:    ollama run gemma4:e2b \"Hello!\""
echo "  Launch:  openclaw --model ollama/gemma4:e2b"
echo ""

# Suggest E4B if enough RAM
TOTAL_RAM=$(sysctl -n hw.memsize 2>/dev/null || echo 0)
RAM_GB=$((TOTAL_RAM / 1073741824))
if [ "$RAM_GB" -ge 16 ]; then
    echo "  You have ${RAM_GB}GB RAM — try the more powerful E4B:"
    echo "  ollama pull gemma4:e4b"
    echo ""
fi

echo "  Now go build something!"
echo "============================================"
