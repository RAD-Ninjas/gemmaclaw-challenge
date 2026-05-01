# 01 — Hello Agent

The simplest possible test — verify OpenClaw + Gemma 4 E2B work together.

## Run It

```bash
./run.sh
```

Or manually:

```bash
openclaw --model ollama/gemma4:e2b --once "List the files in the current directory and tell me what you see."
```

## What Happens

OpenClaw sends your prompt to Gemma 4 E2B, which uses function calling to run `ls` (or equivalent), reads the output, and gives you a natural language summary.

If this works, your setup is good. Move on to the next example.
