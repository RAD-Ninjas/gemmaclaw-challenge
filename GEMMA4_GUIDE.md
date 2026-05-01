# Gemma 4 Guide

Everything you need to know about Google's Gemma 4 model family for this challenge.

---

## The Gemma 4 Family

Released April 2, 2026, Gemma 4 is Google's latest open model family. The "E" models (E2B, E4B) use **Per-Layer Embeddings (PLE)** — an architecture innovation that reduces active memory during inference, making them ideal for edge hardware.

| Model | Effective Params | Total Params | Modalities | Context | Size (Q4) |
|---|---|---|---|---|---|
| **Gemma 4 E2B** | 2.3B | ~5.1B | Text, image, audio, video | 128K | ~1.5GB |
| **Gemma 4 E4B** | 4B | ~8B | Text, image, audio, video | 128K | ~3GB |
| **Gemma 4 26B-A4B** | 4B active (MoE) | 26B | Text, image | 256K | ~15GB |
| **Gemma 4 31B** | 31B (dense) | 31B | Text, image | 128K | ~18GB |

---

## Which Model Should You Use?

| Your Hardware | RAM | Recommended Model | Ollama Command |
|---|---|---|---|
| **Raspberry Pi 5** | 8GB | Gemma 4 E2B | `ollama pull gemma4:e2b` |
| **Raspberry Pi 4** | 8GB | Gemma 4 E2B (slow) | `ollama pull gemma4:e2b` |
| **Raspberry Pi 4** | 4GB | Gemma 3 270M (fallback) | `ollama pull gemma3:270m` |
| **Android Phone** | 6GB+ | Gemma 4 E2B | `ollama pull gemma4:e2b` |
| **Mac M1/M2 (8GB)** | 8GB | Gemma 4 E2B | `ollama pull gemma4:e2b` |
| **Mac M1/M2 (16GB+)** | 16GB+ | Gemma 4 E4B or 26B | `ollama pull gemma4:e4b` |
| **Jetson Nano** | 4-8GB | Gemma 4 E2B | `ollama pull gemma4:e2b` |
| **Jetson Orin Nano** | 8GB | Gemma 4 E4B | `ollama pull gemma4:e4b` |
| **Desktop (16GB+)** | 16GB+ | Gemma 4 26B-A4B | `ollama pull gemma4:26b` |

---

## Performance Expectations

| Hardware | Model | Speed (tok/s) | Notes |
|---|---|---|---|
| Raspberry Pi 5 (8GB) | E2B Q4 | 2-5 | Usable for agents, slow for long generation |
| Raspberry Pi 4 (8GB) | E2B Q4 | 1-3 | Works but noticeably slow |
| Mac M1 (8GB) | E2B Q4 | 30-45 | Fast and smooth |
| Mac M1 (16GB) | E4B Q4 | 25-35 | More capable, still fast |
| Pixel 8 / modern Android | E2B Q4 | ~48 | Surprisingly fast on mobile SoCs |
| Jetson Orin Nano | E2B Q4 | 20-30 | GPU acceleration helps a lot |

**Design around 2-5 tok/s on Pi.** That's ~10-25 words per second — fine for agent tasks, but plan for latency. Batch tasks, use streaming output, give the user feedback while waiting.

---

## Key Features for This Challenge

### Native Function Calling
Gemma 4 supports structured JSON function calling out of the box. OpenClaw leverages this for tool use — the model can call system commands, read files, make API calls.

### Quad-Modal Input
E2B and E4B accept text, images, audio, and video natively. No separate models needed.

### 128K Context Window
Even on Pi, you get a 128K context window (though you'll want to use 32K or less to keep RAM usage manageable).

### Quantization-Aware Training (QAT)
Gemma 4 models were trained with quantization in mind. Q4_K_M (the Ollama default) loses very little quality compared to full precision.

---

## Gemma 4 E2B vs Gemma 3 2B

| Feature | Gemma 3 2B | Gemma 4 E2B |
|---|---|---|
| Parameters | 2B | 2.3B effective (~5.1B total) |
| Modalities | Text only | Text + image + audio + video |
| Context | 8K | 128K |
| Function calling | No | Native JSON |
| Architecture | Standard | PLE (lower memory at inference) |
| RAM needed (Q4) | ~1.5GB | ~1.5GB |

Same RAM footprint, dramatically more capable. Always use Gemma 4 E2B unless your hardware can't handle it.

---

## Fallback: Gemma 3 270M

For ultra-constrained hardware (Pi Zero 2 W, old phones, 4GB Pi 4):

```bash
ollama pull gemma3:270m
```

- Only 125MB quantized
- Text only, 4K context
- Very limited but runs on almost anything
- Good for classification, short Q&A, simple routing

---

## Custom Ollama Modelfiles

Want to customize temperature, context length, or system prompts? See the pre-made Modelfiles in [`configs/ollama-modelfiles/`](configs/ollama-modelfiles/):

- **Creative** — High temperature for brainstorming
- **Code** — Low temperature for precise code generation
- **Concise** — Short responses, small context for speed

```bash
# Example: create a custom model
cd configs/ollama-modelfiles
ollama create gemma4-creative -f Modelfile.gemma4-e2b-creative
ollama run gemma4-creative "Give me 5 project ideas"
```
