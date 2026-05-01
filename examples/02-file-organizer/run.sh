#!/bin/bash
# File Organizer — sort files into folders by type
TARGET_DIR="${1:-$(pwd)}"
echo "Organizing files in: $TARGET_DIR"
echo ""
openclaw --model ollama/gemma4:e2b --once "Look at the files in $TARGET_DIR. Organize them into subdirectories by type (documents, images, code, data, media, other). Create the subdirectories and move the files. Tell me what you did."
