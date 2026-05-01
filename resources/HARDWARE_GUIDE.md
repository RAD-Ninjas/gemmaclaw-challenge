# Hardware Guide

What to use, what to buy, and what you might already own.

## Recommended: Raspberry Pi 5 (8GB) — ~$80

The sweet spot for this challenge. Gemma 4 E2B runs at 2-5 tok/s.

**What you need**:
- Raspberry Pi 5 (8GB) — ~$80
- MicroSD card (32GB+) — ~$8
- USB-C power supply (5V/5A, official recommended) — ~$12
- Optional: Pi Camera Module v2/v3 — ~$25-30 (for vision projects)
- Optional: USB microphone — ~$10 (for audio projects)

**Total**: ~$80-130 depending on accessories

**Where to buy**: [raspberrypi.com](https://www.raspberrypi.com/products/), Amazon, Adafruit, SparkFun, Micro Center (Mountain View has one!)

## Budget Option: Use What You Have

| Hardware | Works? | Model to Use | Notes |
|---|---|---|---|
| **Any laptop (8GB+ RAM)** | Yes | Gemma 4 E2B | Fastest path — no Pi needed |
| **Mac M1/M2/M3/M4** | Yes | E2B, E4B, or 26B | Best experience by far |
| **Raspberry Pi 4 (8GB)** | Yes | Gemma 4 E2B (slow) | ~1-3 tok/s but works |
| **Raspberry Pi 4 (4GB)** | Barely | Gemma 3 270M only | Very limited |
| **Android phone (6GB+ RAM)** | Experimental | Gemma 4 E2B | Via Termux |
| **Jetson Nano** | Yes | E2B or E4B | GPU acceleration helps a lot |
| **Old Linux box** | Probably | E2B | If it has 8GB RAM |

## Pro Hardware

| Hardware | Cost | Why |
|---|---|---|
| **Jetson Orin Nano** | ~$250 | GPU acceleration — 20-30 tok/s on E2B |
| **Pi 5 + AI Camera (IMX500)** | ~$105+$25 | On-chip vision inference at 10-15fps |
| **Pi 5 + Hailo-8L AI Kit** | ~$80+$70 | NPU accelerated inference |

## You Don't Need to Buy Anything

Seriously — a laptop works fine. The challenge is about local, cloud-free AI, not specifically about Raspberry Pi. Pi projects are impressive at the showcase but a laptop project is equally valid.
