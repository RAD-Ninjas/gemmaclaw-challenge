#!/usr/bin/env python3
"""
RuView client — pulls presence + motion signals from the RuView server.

RuView (https://github.com/ruvnet/RuView) exposes a JSON API on the Pi/laptop
running its sensing server. We just need the shape `{count, motion, breathing, ...}`.

If the server is unreachable we return a degraded snapshot so the pipeline can
keep running on vision alone — better than crashing during a live demo.
"""

import os
import time
import requests
from dataclasses import dataclass, asdict


@dataclass
class Signals:
    count: int
    motion_level: float        # 0.0 = still, 1.0 = animated
    breathing_bpm: float       # avg across detected people, 0 if unknown
    confidence: float          # RuView's own confidence in the count
    source: str                # "ruview" | "ruview-degraded"
    last_pitcher_min_ago: float | None = None

    def as_prompt_json(self) -> dict:
        d = asdict(self)
        d["motion_level"] = round(self.motion_level, 2)
        d["breathing_bpm"] = round(self.breathing_bpm, 1)
        d["confidence"] = round(self.confidence, 2)
        if self.last_pitcher_min_ago is not None:
            d["last_pitcher_min_ago"] = round(self.last_pitcher_min_ago, 1)
        return d


def fetch_signals(url: str, last_pitcher_ts: float | None, timeout: float = 3.0) -> Signals:
    last_min = (
        (time.time() - last_pitcher_ts) / 60.0 if last_pitcher_ts else None
    )

    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        payload = r.json()
    except (requests.RequestException, ValueError) as e:
        print(f"[ruview] degraded: {e}")
        return Signals(
            count=0,
            motion_level=0.0,
            breathing_bpm=0.0,
            confidence=0.0,
            source="ruview-degraded",
            last_pitcher_min_ago=last_min,
        )

    return Signals(
        count=int(payload.get("count", payload.get("presence_count", 0))),
        motion_level=float(payload.get("motion", payload.get("motion_level", 0.0))),
        breathing_bpm=float(payload.get("breathing_bpm", payload.get("breathing", 0.0))),
        confidence=float(payload.get("confidence", 0.0)),
        source="ruview",
        last_pitcher_min_ago=last_min,
    )


if __name__ == "__main__":
    url = os.environ.get("RUVIEW_URL", "http://localhost:3000/api/presence")
    sig = fetch_signals(url, None)
    print(sig.as_prompt_json())
