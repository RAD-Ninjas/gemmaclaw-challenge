# Troubleshooting

Common issues and how to fix them.

## Ollama won't start

```bash
# Check if it's already running
curl http://localhost:11434/api/tags

# If not, start it
ollama serve

# On Pi, start as a service
sudo systemctl start ollama
sudo systemctl status ollama
```

## "Model not found" error

```bash
# Make sure you pulled the model
ollama list                    # See what's installed
ollama pull gemma4:e2b         # Pull if missing
```

## Out of memory / model won't load

- Gemma 4 E2B needs ~1.5GB RAM (Q4). If your device has 4GB total, close other apps
- Try Gemma 3 270M instead: `ollama pull gemma3:270m` (only 125MB)
- On Pi, disable the desktop environment: `sudo raspi-config` → Boot Options → Console

## Very slow inference (< 1 tok/s)

- Make sure you're running **64-bit** OS: `uname -m` should show `aarch64` on Pi
- Close other processes: `htop` to check what's eating CPU/RAM
- Make sure swap isn't being heavily used: `free -h`
- Try the Q4 quantization (default) — higher quantizations use more RAM

## OpenClaw can't connect to Ollama

- Verify Ollama is running: `curl http://localhost:11434/api/tags`
- Check your config uses the right URL: `http://localhost:11434` (NOT `/v1`)
- Check `~/.openclaw/openclaw.json` exists and has the right model name

## Pi Camera not working

```bash
# Test camera
libcamera-hello    # Should show preview
libcamera-still -o test.jpg   # Should capture image

# If not working:
# 1. Check cable connection (silver contacts face the board)
# 2. Enable camera: sudo raspi-config → Interface Options → Camera
# 3. Reboot: sudo reboot
```

## Node.js version too old

```bash
node --version    # Need v22+

# Upgrade on Pi/Linux:
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs

# On Mac:
brew install node
```

## Still stuck?

Ask in the GDG Mountain View Discord/Slack — someone has probably hit the same issue.
