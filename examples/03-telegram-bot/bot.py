#!/usr/bin/env python3
"""
Telegram Bot powered by Gemma 4 E2B via Ollama.
All inference runs locally — no cloud AI APIs.

Usage:
  export TELEGRAM_BOT_TOKEN="your-token-here"
  python3 bot.py

Requires: pip3 install python-telegram-bot requests
"""

import os
import sys
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma4:e2b"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def check_ollama():
    """Verify Ollama is running and the model is available."""
    try:
        r = requests.get("http://localhost:11434/api/tags", timeout=5)
        models = [m["name"] for m in r.json().get("models", [])]
        if not any(MODEL.split(":")[0] in m for m in models):
            print(f"Warning: {MODEL} not found. Available: {models}")
            print(f"Run: ollama pull {MODEL}")
        return True
    except requests.exceptions.ConnectionError:
        print("Error: Ollama not running. Start with: ollama serve")
        return False


def ask_gemma(message: str) -> str:
    """Send a message to Gemma 4 E2B and get a response."""
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a helpful, concise assistant running locally on edge hardware. Keep responses brief."},
            {"role": "user", "content": message}
        ],
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=120)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except requests.exceptions.Timeout:
        return "Sorry, that took too long. Try a shorter question?"
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        return "Something went wrong talking to the local model."


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hey! I'm powered by Gemma 4 E2B running locally — no cloud APIs involved.\n"
        "Just send me a message and I'll respond."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    logger.info(f"Message from {update.effective_user.first_name}: {user_msg[:50]}...")

    # Send typing indicator while we wait for inference
    await update.message.chat.send_action("typing")

    response = ask_gemma(user_msg)
    await update.message.reply_text(response)


def main():
    token = os.environ.get("TELEGRAM_BOT_TOKEN")
    if not token:
        print("Error: Set TELEGRAM_BOT_TOKEN environment variable")
        print("Get one from @BotFather on Telegram")
        sys.exit(1)

    if not check_ollama():
        sys.exit(1)

    print(f"Starting bot with {MODEL}...")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running! Send a message on Telegram.")
    app.run_polling()


if __name__ == "__main__":
    main()
