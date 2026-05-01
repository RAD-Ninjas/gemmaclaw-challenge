# Getting Started

Get OpenClaw + Gemma 4 running locally in under 15 minutes.

---

## Choose Your Platform

- [Raspberry Pi 5](#raspberry-pi-5-recommended)
- [Mac](#mac)
- [Linux (x86)](#linux-x86)
- [Android Phone](#android-experimental)

---

## Raspberry Pi 5 (Recommended)

### Prerequisites

- Raspberry Pi 5 with **8GB RAM** (4GB works for Gemma 3 270M only)
- MicroSD card (32GB+) flashed with **Raspberry Pi OS Lite 64-bit (Bookworm)**
- Internet connection for initial setup
- SSH access or keyboard + display

### Step 1: Update your Pi

```bash
sudo apt update && sudo apt upgrade -y
```

### Step 2: Run the quickstart script

```bash
curl -fsSL https://raw.githubusercontent.com/RAD-Ninjas/gemmaclaw-challenge/main/setup/quickstart-pi.sh | bash
```

This installs:
- **Ollama** (local model runtime)
- **Gemma 4 E2B** (~1.5GB download)
- **Node.js 22** (required by OpenClaw)
- **OpenClaw** (AI agent framework)

### Step 3: Test Gemma 4

```bash
ollama run gemma4:e2b "Describe what an AI agent is in one sentence."
```

You should see Gemma 4 respond at ~2-5 tokens/second. That's normal for Pi 5.

### Step 4: Launch OpenClaw

```bash
openclaw --model ollama/gemma4:e2b
```

You now have a local AI agent. Try asking it to list files, create a script, or summarize a document.

### Step 5: Verify everything works

```bash
curl -fsSL https://raw.githubusercontent.com/RAD-Ninjas/gemmaclaw-challenge/main/setup/verify-setup.sh | bash
```

---

## Mac

### Prerequisites

- macOS 12+ on Apple Silicon (M1/M2/M3/M4) or Intel
- 8GB+ RAM (16GB recommended for E4B)

### Quick Setup

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Gemma 4 E2B
ollama pull gemma4:e2b

# Test it
ollama run gemma4:e2b "Hello! What can you help me with?"

# Install OpenClaw (requires Node.js 22+)
# If you don't have Node.js:
brew install node

# Install OpenClaw
npm install -g openclaw

# Launch
openclaw --model ollama/gemma4:e2b
```

On Apple Silicon you'll see 30-45 tokens/second — much faster than Pi.

Got 16GB+ RAM? Try the more powerful E4B:

```bash
ollama pull gemma4:e4b
openclaw --model ollama/gemma4:e4b
```

---

## Linux (x86)

### Quick Setup

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Gemma 4 E2B
ollama pull gemma4:e2b

# Test it
ollama run gemma4:e2b "Hello!"

# Install Node.js 22+ (if needed)
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# Install OpenClaw
npm install -g openclaw

# Launch
openclaw --model ollama/gemma4:e2b
```

---

## Android (Experimental)

Gemma 4 E2B was designed for phones — it runs at ~48 tok/s on Snapdragon 8 Gen 3.

### Setup via Termux

1. Install **Termux** from F-Droid (not Google Play)
2. Open Termux and run:

```bash
pkg update && pkg upgrade -y
pkg install curl nodejs-lts git

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull Gemma 4 E2B
ollama pull gemma4:e2b

# Test it
ollama run gemma4:e2b "Hello from my phone!"

# Install OpenClaw
npm install -g openclaw
openclaw --model ollama/gemma4:e2b
```

Note: This is experimental. Some OpenClaw features that need full filesystem access may not work in Termux's sandboxed environment.

---

## OpenClaw Configuration

OpenClaw reads its config from `~/.openclaw/openclaw.json`. The quickstart scripts create this automatically, but if you need to configure manually:

```json
{
  "llm": {
    "provider": "ollama",
    "baseUrl": "http://localhost:11434",
    "model": "gemma4:e2b"
  }
}
```

**Important**: Use the native Ollama API URL (`http://localhost:11434`) — NOT the `/v1` OpenAI-compatible endpoint. OpenClaw's Ollama integration uses the native `/api/chat` endpoint which supports Gemma 4's tool calling.

---

## What's Next?

1. Check out [PROJECT_IDEAS.md](PROJECT_IDEAS.md) for inspiration
2. Browse the [examples/](examples/) directory for working starter projects
3. Pick an idea and start building!

---

## Troubleshooting

See [resources/TROUBLESHOOTING.md](resources/TROUBLESHOOTING.md) for common issues, or ask in the GDG MV Discord/Slack.
