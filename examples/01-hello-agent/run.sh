#!/bin/bash
# Hello Agent — simplest OpenClaw + Gemma 4 test
echo "Running Hello Agent..."
echo "This will ask Gemma 4 E2B to list and describe the files in this directory."
echo ""
openclaw --model ollama/gemma4:e2b --once "List the files in the current directory and tell me what you see."
