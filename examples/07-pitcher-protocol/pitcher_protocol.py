#!/usr/bin/env python3
"""
Pitcher Protocol — main orchestrator.

Loop:
  1. Pull sensor signals from RuView (or degrade gracefully).
  2. Snap a Pi Camera frame.
  3. Ask Gemma 4 E2B (Ollama) whether the table needs another pitcher.
  4. If yes and cooldown elapsed: fire Flipper -> sub-GHz -> doorbell -> bartender.

All local. No cloud. Built for the GemmaClaw Challenge showcase.
"""

import os
import sys
import json
import time
import base64
import subprocess
import requests

from ruview_client import fetch_signals
from flipper_trigger import fire, FlipperError


OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat")
MODEL = os.environ.get("MODEL", "vibes-judge")
RUVIEW_URL = os.environ.get("RUVIEW_URL", "http://localhost:3000/api/presence")
FLIPPER_PORT = os.environ.get("FLIPPER_PORT", "/dev/ttyACM0")
FLIPPER_SUB_PATH = os.environ.get("FLIPPER_SUB_PATH", "/ext/subghz/pitcher.sub")
COOLDOWN_SEC = int(os.environ.get("PITCHER_COOLDOWN_SEC", "600"))
POLL_SEC = int(os.environ.get("POLL_INTERVAL_SEC", "15"))
DRY_RUN = os.environ.get("DRY_RUN", "") == "1"
VISION_ONLY = "--vision-only" in sys.argv

IMAGE_PATH = "/tmp/pitcher-frame.jpg"


def capture_frame() -> str | None:
    try:
        subprocess.run(
            [
                "libcamera-still", "-o", IMAGE_PATH, "-t", "800",
                "--width", "640", "--height", "480", "-n",
            ],
            check=True, capture_output=True,
        )
        return IMAGE_PATH
    except FileNotFoundError:
        print("[cam] libcamera-still not found — install libcamera-apps, or run on Pi.")
        return None
    except subprocess.CalledProcessError as e:
        print(f"[cam] capture failed: {e.stderr.decode(errors='replace')[:200]}")
        return None


def ask_gemma(image_path: str | None, signals_json: dict) -> dict:
    user_text = (
        "Here are the live sensor signals from the table:\n"
        f"{json.dumps(signals_json)}\n\n"
        "Look at the photo and decide. Respond with the JSON object only."
    )

    message = {"role": "user", "content": user_text}

    if image_path:
        with open(image_path, "rb") as f:
            message["images"] = [base64.b64encode(f.read()).decode("utf-8")]

    payload = {
        "model": MODEL,
        "messages": [message],
        "stream": False,
        "format": "json",
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    raw = r.json()["message"]["content"].strip()

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        start = raw.find("{")
        end = raw.rfind("}")
        if start >= 0 and end > start:
            return json.loads(raw[start : end + 1])
        raise


def banner(decision: dict, signals_json: dict) -> None:
    print()
    print("=" * 60)
    print(f"  order:      {decision.get('order')}")
    print(f"  people:     {decision.get('people')}  (ruview said {signals_json.get('count')})")
    print(f"  confidence: {decision.get('confidence')}")
    print(f"  reason:     {decision.get('reason')}")
    print()
    print(f"  >> {decision.get('announce', '')}")
    print("=" * 60)


def main() -> None:
    print("Pitcher Protocol — armed.")
    print(f"  model={MODEL}  poll={POLL_SEC}s  cooldown={COOLDOWN_SEC}s  dry_run={DRY_RUN}")
    if VISION_ONLY:
        print("  mode=VISION_ONLY (RuView disabled)")

    last_pitcher_ts: float | None = None

    while True:
        cycle_start = time.time()

        if VISION_ONLY:
            from ruview_client import Signals
            last_min = (
                (time.time() - last_pitcher_ts) / 60.0 if last_pitcher_ts else None
            )
            signals = Signals(
                count=0, motion_level=0.0, breathing_bpm=0.0,
                confidence=0.0, source="vision-only", last_pitcher_min_ago=last_min,
            )
        else:
            signals = fetch_signals(RUVIEW_URL, last_pitcher_ts)

        frame = capture_frame()
        if not frame and signals.source != "ruview":
            print("[skip] no cam frame and no ruview data — sleeping.")
        else:
            try:
                decision = ask_gemma(frame, signals.as_prompt_json())
            except Exception as e:
                print(f"[gemma] error: {e}")
                decision = None

            if decision:
                banner(decision, signals.as_prompt_json())

                should_order = bool(decision.get("order"))
                cooling_down = (
                    last_pitcher_ts is not None
                    and (time.time() - last_pitcher_ts) < COOLDOWN_SEC
                )

                if should_order and cooling_down:
                    remaining = int(COOLDOWN_SEC - (time.time() - last_pitcher_ts))
                    print(f"[cooldown] would order, but {remaining}s left on lockout.")
                elif should_order:
                    try:
                        fire(FLIPPER_SUB_PATH, FLIPPER_PORT, dry_run=DRY_RUN)
                        last_pitcher_ts = time.time()
                        print("[order] pitcher dispatched.")
                    except FlipperError as e:
                        print(f"[flipper] {e}")

        elapsed = time.time() - cycle_start
        sleep_for = max(0.0, POLL_SEC - elapsed)
        time.sleep(sleep_for)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nPitcher Protocol — stood down.")
