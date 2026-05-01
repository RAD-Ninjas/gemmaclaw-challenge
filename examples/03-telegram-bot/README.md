# 03 — Telegram Bot

A personal AI assistant that runs entirely on your device — no cloud APIs.

## What It Does

A Telegram bot backed by Gemma 4 E2B running locally via Ollama. Messages go to Telegram's servers (for delivery), but all AI inference happens on your hardware.

## Prerequisites

- Ollama running with `gemma4:e2b`
- A Telegram account
- A bot token from [@BotFather](https://t.me/BotFather)

## Setup

1. Message `@BotFather` on Telegram, send `/newbot`, follow prompts, save your token
2. Install dependencies:

```bash
pip3 install python-telegram-bot requests
```

3. Set your token:

```bash
export TELEGRAM_BOT_TOKEN="your-token-here"
```

4. Run:

```bash
python3 bot.py
```

## How It Works

1. User sends a message to the Telegram bot
2. Bot forwards the message to Ollama's local API
3. Gemma 4 E2B generates a response locally
4. Bot sends the response back via Telegram

## Extend It

- Add `/image` command using Gemma 4's vision (send a photo, get a description)
- Add conversation memory (store last N messages per user)
- Add `/translate` using Gemma 4's multilingual support
- Deploy on Pi as an always-on personal assistant
