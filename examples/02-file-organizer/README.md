# 02 — File Organizer

An AI agent that sorts messy files into folders by type.

## What It Does

Point it at a directory full of random files and it will:
1. Scan the directory
2. Categorize files by type (documents, images, code, etc.)
3. Create subdirectories
4. Move files into the right folders

## Run It

```bash
# Create some test files first
mkdir -p ~/test-mess
touch ~/test-mess/{report.pdf,photo.jpg,script.py,notes.txt,data.csv,song.mp3}

# Let the agent organize them
./run.sh ~/test-mess
```

## How It Works

Uses OpenClaw's `--once` flag to run a single agent task. Gemma 4 E2B uses function calling to run shell commands (ls, mkdir, mv) to organize the files.

## Extend It

- Add date-based sorting (group by month/year)
- Add duplicate detection
- Add a dry-run mode that shows what it would do without moving anything
- Process nested directories recursively
