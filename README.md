# GemmaClaw Challenge

**GDG Mountain View | Build with AI 2026 | Hosted by [RAD Ninjas](https://github.com/RAD-Ninjas)**

> Can you build a useful AI agent that runs entirely on a Raspberry Pi? No cloud. No GPU rental. No API costs.

Build a project using **OpenClaw** + **Google's Gemma 4** on constrained hardware — Raspberry Pi, Jetson Nano, old laptop, even your phone. Then show it off at our community showcase at Sports Page in Mountain View.

---

## What You'll Use

- **[Gemma 4 E2B](https://ai.google.dev/gemma/docs/core)** — Google's newest open model (April 2026). Quad-modal (text + image + audio + video), 128K context, native function calling. Fits in 1.5GB of RAM
- **[OpenClaw](https://github.com/openclaw/openclaw)** — The 332K-star open-source AI agent framework that gives LLMs real computer control
- **[Ollama](https://ollama.com)** — One command to install: `ollama pull gemma4:e2b`
- **Your hardware** — Whatever you've got

## Quickstart (15 minutes)

### Raspberry Pi 5

```bash
curl -fsSL https://raw.githubusercontent.com/RAD-Ninjas/gemmaclaw-challenge/main/setup/quickstart-pi.sh | bash
ollama run gemma4:e2b "What can you help me with?"
openclaw --model ollama/gemma4:e2b
```

### Mac / Linux

```bash
curl -fsSL https://raw.githubusercontent.com/RAD-Ninjas/gemmaclaw-challenge/main/setup/quickstart-mac.sh | bash
ollama run gemma4:e2b "What can you help me with?"
openclaw --model ollama/gemma4:e2b
```

### Android (Experimental)

```bash
# Install Termux from F-Droid, then:
pkg install curl
curl -fsSL https://raw.githubusercontent.com/RAD-Ninjas/gemmaclaw-challenge/main/setup/quickstart-phone.sh | bash
```

See **[GETTING_STARTED.md](GETTING_STARTED.md)** for detailed step-by-step instructions.

---

## Project Ideas

Not sure what to build? Check out **[PROJECT_IDEAS.md](PROJECT_IDEAS.md)** for curated ideas at every skill level — from a simple file organizer to a fully offline voice assistant.

Working starter examples are in the [`examples/`](examples/) directory — fork one and extend it.

---

## The Showcase

Ad-hoc community showcase at **Sports Page, Mountain View**. Show up with your project, give a 3-minute lightning talk if you want to present. No pre-registration required.

**RSVP on the [GDG Mountain View event page](#).**

Awards voted on by the audience:
- **Best Overall**
- **Most Creative**
- **Best Beginner Project**
- **"How Did You Even Do That?"**
- **Best Use of Multimodal** (vision, audio, or video)

---

## Gemma 4 at a Glance

| Model | Size (Q4) | Best For | Modalities | Context |
|---|---|---|---|---|
| **Gemma 4 E2B** | ~1.5GB | Pi 5, phones, IoT | Text + image + audio + video | 128K |
| **Gemma 4 E4B** | ~3GB | Jetson, mid-range laptops | Text + image + audio + video | 128K |
| **Gemma 4 26B-A4B** | ~15GB | Laptops with GPU | Text + image | 256K |

See **[GEMMA4_GUIDE.md](GEMMA4_GUIDE.md)** for the full breakdown.

---

## Repo Structure

```
setup/          → One-command quickstart scripts for every platform
configs/        → Pre-configured OpenClaw + Ollama configs
examples/       → Working starter projects to fork and extend
benchmarks/     → Benchmark scripts and community results
resources/      → Hardware guide, troubleshooting, links
```

## Resources

- [OpenClaw Docs](https://github.com/openclaw/openclaw)
- [Gemma 4 Docs](https://ai.google.dev/gemma/docs/core)
- [Ollama + OpenClaw Integration](https://docs.ollama.com/integrations/openclaw)
- [Hardware Guide](resources/HARDWARE_GUIDE.md)
- [Troubleshooting](resources/TROUBLESHOOTING.md)

---

## License

MIT
