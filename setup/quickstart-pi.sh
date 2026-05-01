#!/bin/bash
# GemmaClaw Challenge — Raspberry Pi 5 Quickstart
# Installs Ollama, Gemma 4 E2B, Node.js 22, and OpenClaw
# Tested on Raspberry Pi OS Lite 64-bit (Bookworm)

set -e

echo "============================================"
echo "  GemmaClaw Challenge — Pi 5 Quickstart"
echo "  github.com/RAD-Ninjas/gemmaclaw-challenge"
echo "============================================"
echo ""

# Check architecture
ARCH=$(uname -m)
if [ "$ARCH" != "aarch64" ]; then
    echo "Warning: Expected aarch64 (64-bit ARM), got $ARCH"
    echo "Make sure you're running 64-bit Raspberry Pi OS"
    exit 1
fi

# Check RAM
TOTAL_RAM=$(free -m | awk '/^Mem:/{print $2}')
echo "Detected RAM: ${TOTAL_RAM}MB"
if [ "$TOTAL_RAM" -lt 3500 ]; then
    echo "Warning: Less than 4GB RAM detected. Gemma 4 E2B needs ~1.5GB."
    echo "You may want to use Gemma 3 270M instead: ollama pull gemma3:270m"
fi
echo ""

# Step 1: System dependencies
echo "[1/5] Installing system dependencies..."
sudo apt update -qq
sudo apt install -y -qq curl git build-essential

# Step 2: Install Ollama
echo ""
echo "[2/5] Installing Ollama..."
if command -v ollama &> /dev/null; then
    echo "Ollama already installed: $(ollama --version)"
else
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Start Ollama service
echo "Starting Ollama service..."
sudo systemctl enable ollama 2>/dev/null || true
sudo systemctl start ollama 2>/dev/null || true
sleep 2

# Step 3: Pull Gemma 4 E2B
echo ""
echo "[3/5] Pulling Gemma 4 E2B (~1.5GB download)..."
echo "This may take a few minutes on slower connections."
ollama pull gemma4:e2b

# Step 4: Install Node.js 22
echo ""
echo "[4/5] Installing Node.js 22..."
if command -v node &> /dev/null; then
    NODE_VER=$(node --version | cut -d'.' -f1 | tr -d 'v')
    if [ "$NODE_VER" -ge 22 ]; then
        echo "Node.js $(node --version) already installed"
    else
        echo "Node.js $(node --version) found but need v22+. Upgrading..."
        curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
        sudo apt install -y -qq nodejs
    fi
else
    curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
    sudo apt install -y -qq nodejs
fi

# Step 5: Install OpenClaw
echo ""
echo "[5/5] Installing OpenClaw..."
if command -v openclaw &> /dev/null; then
    echo "OpenClaw already installed"
else
    npm install -g openclaw
fi

# Configure OpenClaw for local Gemma 4
echo ""
echo "Configuring OpenClaw for local Gemma 4 E2B..."
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
echo "  Test Gemma 4:  ollama run gemma4:e2b \"Hello!\""
echo "  Launch agent:  openclaw --model ollama/gemma4:e2b"
echo ""
echo "  Now go build something!"
echo "  Project ideas: github.com/RAD-Ninjas/gemmaclaw-challenge"
echo "============================================"
