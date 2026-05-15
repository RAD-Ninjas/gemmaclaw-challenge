# 07 — Pitcher Protocol

> Local AI decides when your table needs another pitcher, then physically orders one. No cloud, no humans-in-the-loop (until the bartender shows up).

Built for the **GemmaClaw Challenge** showcase at Sports Page, Mountain View.

## What it does

A Raspberry Pi 5 watches your table using two senses:

1. **WiFi CSI** — an ESP32-S3 running [RuView](https://github.com/ruvnet/RuView) streams Channel State Information. The Pi turns that into a person count and motion/breathing-rate signals.
2. **Vision** — a Pi Camera grabs a still of the table every few seconds.

Both signals get handed to **Gemma 4 E2B** (multimodal, running locally via Ollama) with one job: decide whether the table has crossed the *pitcher threshold*.

When Gemma says yes, the Pi pokes a **Flipper Zero** over USB. The Flipper transmits a recorded 433 MHz sub-GHz signal. A wireless doorbell stashed behind the bar chimes. The bartender brings the pitcher.

## Why this is a good demo

- **All inference is local** — Gemma 4 E2B on Pi 5, RuView on ESP32-S3. No cloud calls.
- **Real multimodality** — image bytes + structured sensor JSON to one model in one call.
- **The LLM has agency** — it's not narrating, it's choosing when to take a physical action.
- **You can see it work** — the doorbell rings. There is no faking this.

## Bill of materials

| Item | Notes |
|------|-------|
| Raspberry Pi 5 (4GB+) | Runs Ollama + the orchestrator |
| Pi Camera Module 3 | Any libcamera-compatible cam works |
| ESP32-S3 dev board | For RuView CSI streaming (~$9) |
| Flipper Zero | Sub-GHz transmitter + USB CDC control |
| 433 MHz wireless doorbell | Cheap, ~$10. Capture the chime button with Flipper |
| Sub-GHz remote (the doorbell's) | Needed once, to record the signal |

## Quick start

```bash
# 1. Make sure Ollama has Gemma 4 E2B
ollama pull gemma4:e2b

# 2. Build the vibes-judge model (low temp, JSON-only output)
ollama create vibes-judge -f Modelfile.vibes-judge

# 3. Capture the doorbell sub-GHz signal once (see setup-flipper.md)

# 4. Make sure RuView server is up and reporting
curl http://<esp32-ip>:3000/api/presence

# 5. Plug Flipper Zero into the Pi via USB

# 6. Run it
./run.sh
```

## Configuration (env vars)

| Var | Default | What |
|-----|---------|------|
| `RUVIEW_URL` | `http://localhost:3000/api/presence` | RuView server presence endpoint |
| `FLIPPER_PORT` | `/dev/ttyACM0` | Flipper USB CDC device |
| `FLIPPER_SUB_PATH` | `/ext/subghz/pitcher.sub` | Saved sub-GHz file on Flipper SD |
| `PITCHER_COOLDOWN_SEC` | `600` | Min seconds between pitchers (don't get cut off) |
| `POLL_INTERVAL_SEC` | `15` | How often Gemma re-evaluates the table |
| `OLLAMA_URL` | `http://localhost:11434/api/chat` | Local Ollama endpoint |
| `MODEL` | `vibes-judge` | Ollama model to call |

## What Gemma is asked

Gemma sees:

- The latest cam frame (640x480 JPEG)
- A compact JSON of RuView signals: `{count, breathing_bpm, motion_level, last_pitcher_min_ago, ...}`

And is required to respond as:

```json
{
  "order": true,
  "confidence": 0.82,
  "reason": "4 people, no full glasses visible, animated breathing rate, last pitcher 22 min ago",
  "announce": "Round 3 incoming. Table 1 has officially given up on shipping code tonight."
}
```

The `announce` line is printed for the showcase — and read aloud if you wire up a speaker.

## Safety / showcase notes

- **Cooldown defaults to 10 minutes.** The Flipper will refuse to transmit again sooner.
- **Demo mode**: set `DRY_RUN=1` to skip the Flipper transmit and just print the decision. Useful for rehearsing before the bartender wonders why their bell is going off.
- **The bartender is in on it.** Tell them. This is a workshop demo, not a heist.

## How it falls back

| If this breaks | Demo still does |
|----------------|-----------------|
| ESP32-S3 / RuView | Vision-only count via Gemma 4 (see `--vision-only`) |
| Pi Camera | RuView-only count, no vibe assessment |
| Flipper | Decision printed loudly; you ring the bell manually |
| Ollama | Hard fail — that's the headliner |
