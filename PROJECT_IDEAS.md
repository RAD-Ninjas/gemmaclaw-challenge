# Project Ideas

Not sure what to build? Here's a curated list at every skill level. Pick one, remix one, or go totally off-script.

---

## Beginner

| Idea | Description | Hardware | Gemma 4 Feature |
|---|---|---|---|
| **Hello Agent** | Get OpenClaw running, ask it to do something useful | Any | Text generation |
| **File Organizer** | Agent that sorts files in a directory by type/date | Any | Function calling |
| **Daily Briefing** | Reads local text files and gives you a morning summary | Any | Text summarization |
| **Flashcard Generator** | Give it a topic, it generates study flashcards | Any | Text generation |
| **CLI Helper** | Describe what you want in English, get the bash command | Any | Code generation |

## Intermediate

| Idea | Description | Hardware | Gemma 4 Feature |
|---|---|---|---|
| **Telegram Bot** | Personal AI assistant via Telegram, all local inference | Any + internet | Text + function calling |
| **Vision Describer** | Pi Camera captures image, Gemma describes it | Pi + Camera | Vision (image) |
| **Audio Transcriber** | Record from mic, transcribe locally | Any + mic | Audio understanding |
| **Code Reviewer** | Point it at a file, get a code review | Any | Code understanding |
| **Local RAG** | Index local documents, answer questions about them | Any | Long context + text |
| **Edge API Server** | Turn your Pi into a local AI API for other devices | Pi or any | Text + function calling |

## Advanced

| Idea | Description | Hardware | Gemma 4 Feature |
|---|---|---|---|
| **Voice Assistant** | Offline Siri/Alexa — mic in, speech out (Piper TTS) | Pi + mic + speaker | Audio + text |
| **Security Camera** | Motion detection + scene description + alerts | Pi + Camera | Vision + function calling |
| **Multi-Agent System** | Multiple OpenClaw agents collaborating on a task | Any (16GB+ helps) | Function calling |
| **Document Pipeline** | Watch a folder, OCR/summarize/classify new documents | Any | Vision + text |
| **Meeting Summarizer** | Record a meeting, get notes + action items | Any + mic | Audio + text |

## Wildcard

| Idea | Description | Hardware | Gemma 4 Feature |
|---|---|---|---|
| **AI Dungeon Master** | Text-based RPG with an AI narrator | Any | Creative text |
| **Plant Monitor** | Camera watches your plant, tells you if it needs water | Pi + Camera | Vision |
| **Local Translation Kiosk** | Speak in one language, get text in another | Any + mic | Multilingual + audio |
| **Pi Cluster** | Multiple Pis working together as a model-serving cluster | Multiple Pis | Text + networking |
| **Art Critic** | Point camera at art, get a critique | Pi + Camera | Vision |

---

## Tips for Building on Constrained Hardware

1. **Design for 2-5 tok/s.** On Pi, generation is slow. Use streaming output so users see progress. Batch operations where possible.

2. **Keep prompts short.** Shorter prompts = faster time-to-first-token. Be direct.

3. **Use function calling.** Gemma 4's native JSON function calling is fast and reliable — let the model call tools rather than parsing free-form text.

4. **Cache aggressively.** If you're describing the same image repeatedly, cache the result.

5. **Consider the UX.** A loading spinner with "Thinking..." goes a long way when inference takes 10 seconds.

6. **Start simple, extend later.** Get the basic flow working, then add features. A working demo beats a half-finished masterpiece at the showcase.
