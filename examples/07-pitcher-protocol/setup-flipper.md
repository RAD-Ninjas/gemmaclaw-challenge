# Setup — Flipper Zero + Wireless Doorbell

The Flipper needs to know how to ring your specific doorbell. You record the doorbell's remote button once, save the signal, and from then on the Pi can tell the Flipper to replay it.

## What you need

- Flipper Zero (any current firmware)
- A 433 MHz wireless doorbell (cheap, generic — the chime button itself is the remote)
- The doorbell's chime unit (the receiver — this is what you'll hide near the bar)

## Capture the chime signal

1. Flipper main menu → **Sub-GHz** → **Read**.
2. Hold the doorbell's remote / button next to the Flipper. Press it.
3. Flipper shows the detected protocol (usually Princeton, EV1527, or similar at 433.92 MHz).
4. Press the right arrow → **Save**.
5. Name it `pitcher`. Confirm.
6. The file is now at `/ext/subghz/pitcher.sub` on the Flipper's SD card. Don't move it.

## Test it from the Flipper UI

1. **Sub-GHz** → **Saved** → `pitcher` → **Send**.
2. The doorbell should chime. If it doesn't:
   - Check distance (within ~5m for a stock doorbell).
   - Try **Read RAW** instead of **Read** if Flipper couldn't identify the protocol — save and use the raw file the same way.

## Test it from the Pi

```bash
# With Flipper plugged into the Pi via USB
ls /dev/ttyACM*       # should show /dev/ttyACM0 (or ACM1)

DRY_RUN=0 python3 flipper_trigger.py
```

You should hear the chime. If not, check:

- Flipper isn't in another app / locked — leave it on the main menu.
- `/dev/ttyACM0` exists. If a different ACM number, set `FLIPPER_PORT=/dev/ttyACM1`.
- Your user has access to the serial device (`sudo usermod -aG dialout $USER` then re-login).
- The file path on the Flipper: `subghz tx_from_file /ext/subghz/pitcher.sub` — adjust `FLIPPER_SUB_PATH` if you named it something else.

## On the day of the showcase

- **Test the doorbell range from your demo spot.** Bars have a lot of RF noise on 433 MHz.
- **Stash the chime unit behind the bar, plugged in.** Cheap doorbells are loud — warn the bartender.
- **Pre-cache the model.** Run one inference before the lightning talks start so Gemma is warm.
- **DRY_RUN mode** is your friend during rehearsal — same logs, no chime.
