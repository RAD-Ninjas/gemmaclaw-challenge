#!/usr/bin/env python3
"""
Flipper Zero trigger — fires a saved sub-GHz file over USB CDC.

Flipper exposes a serial CLI on /dev/ttyACM0 (Linux) when plugged in.
We send: `subghz tx_from_file /ext/subghz/pitcher.sub`
then read until the prompt returns.

Capture the doorbell signal first via the Flipper UI:
  Sub-GHz → Read → press doorbell remote → Save as "pitcher".
See setup-flipper.md for details.
"""

import os
import time
import serial


class FlipperError(Exception):
    pass


def fire(
    sub_path: str = "/ext/subghz/pitcher.sub",
    port: str = "/dev/ttyACM0",
    baud: int = 115200,
    dry_run: bool = False,
) -> str:
    if dry_run:
        msg = f"[flipper] DRY_RUN — would tx {sub_path}"
        print(msg)
        return msg

    try:
        with serial.Serial(port, baud, timeout=5) as ser:
            time.sleep(0.2)
            ser.reset_input_buffer()
            ser.write(b"\r\n")
            time.sleep(0.1)
            ser.reset_input_buffer()

            cmd = f"subghz tx_from_file {sub_path}\r\n".encode()
            ser.write(cmd)

            deadline = time.time() + 8.0
            buf = bytearray()
            while time.time() < deadline:
                chunk = ser.read(256)
                if chunk:
                    buf.extend(chunk)
                    if b">: " in buf or b"\r\n>: " in buf:
                        break
                else:
                    if buf:
                        break

            out = buf.decode("utf-8", errors="replace")
            low = out.lower()
            if "error" in low or "not found" in low or "failed" in low:
                raise FlipperError(f"Flipper rejected command:\n{out}")
            return out
    except serial.SerialException as e:
        raise FlipperError(f"Could not open {port}: {e}") from e


if __name__ == "__main__":
    sub = os.environ.get("FLIPPER_SUB_PATH", "/ext/subghz/pitcher.sub")
    port = os.environ.get("FLIPPER_PORT", "/dev/ttyACM0")
    dry = os.environ.get("DRY_RUN", "") == "1"
    try:
        result = fire(sub, port, dry_run=dry)
        print(result)
        print("[flipper] sent.")
    except FlipperError as e:
        print(f"[flipper] FAILED: {e}")
        raise SystemExit(1)
