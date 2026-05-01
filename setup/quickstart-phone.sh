#!/usr/bin/env bash
# GemmaClaw Challenge — Android Phone Setup (via Termux)
# Experimental! Requires Android 10+ with 6GB+ RAM.
set -euo pipefail

echo "============================================"
echo "  GemmaClaw Challenge — Android (Termux)"
echo "============================================"
echo ""
echo "This script runs INSIDE Termux on your Android device."
echo "Install Termux from F-Droid (NOT Google Play — that version is outdated)."
echo "  https://f-droid.org/en/packages/com.termux/"
echo ""

# ── Check environment ──────────────────────────────────────────
if [ ! -d "$PREFIX" ] 2>/dev/null; then
  echo "ERROR: This doesn't look like Termux. Run this inside Termux on Android."
  exit 1
fi

echo "Step 1/5 — Updating Termux packages..."
pkg update -y && pkg upgrade -y

echo ""
echo "Step 2/5 — Installing dependencies..."
pkg install -y cmake golang git nodejs-lts

echo ""
echo "Step 3/5 — Building Ollama from source..."
echo "(This takes 5-10 minutes on a phone — grab coffee)"
if command -v ollama &> /dev/null; then
  echo "Ollama already installed, skipping build."
else
  cd "$HOME"
  git clone --depth 1 https://github.com/ollama/ollama.git
  cd ollama
  go generate ./...
  go build .
  cp ollama "$PREFIX/bin/"
  cd "$HOME"
  echo "Ollama built and installed."
fi

echo ""
echo "Step 4/5 — Starting Ollama and pulling Gemma 4 E2B..."
ollama serve &
sleep 3
ollama pull gemma4:e2b
echo "Model pulled. (~1.5GB)"

echo ""
echo "Step 5/5 — Installing OpenClaw..."
npm install -g @anthropic/openclaw

# Write config
mkdir -p "$HOME/.openclaw"
cat > "$HOME/.openclaw/openclaw.json" << 'EOF'
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
echo "Quick test:"
echo "  ollama run gemma4:e2b 'Hello from my phone!'"
echo ""
echo "Run OpenClaw:"
echo "  openclaw"
echo ""
echo "TIPS:"
echo "  - Keep Termux in the foreground (or use termux-wake-lock)"
echo "  - Close other apps to free RAM"
echo "  - Expect ~30-50 tok/s on modern phones (Snapdragon 8 Gen 2+)"
echo "  - Battery will drain fast — plug in"
echo ""
