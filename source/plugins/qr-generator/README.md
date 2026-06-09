# qr-generator

Convert a URL (or any short string) into a scannable QR code PNG.

Install: `/plugin install qr-generator@my-agents`

## What's inside

| Component | Type | Role |
| --- | --- | --- |
| `qr-generator` | skill | Generate a QR PNG from a URL. Pick the right backend for the platform (macOS / Linux), pick sane defaults for size and error correction, write the file where the user wanted it. |

## Use it

> "Make a QR for `https://example.com/my-course` and put it in `assets/`."

The skill picks one of three backends in order of availability:

1. **macOS — `CoreImage` via Swift** (default on macOS). Zero deps; ships with
   the OS.
2. **Python — `qrcode` or `segno`** (cross-platform). Used if either library
   is importable.
3. **CLI — `qrencode`** (cross-platform, common on Linux). Used if the binary
   is on PATH.

If none are available the skill explains how to install one. It does **not**
bypass network firewalls or hit external QR-as-a-service URLs — the QR is
generated locally so the URL never leaves the machine.

Defaults: ~1500×1500 PNG, error-correction level **H** (~30% damage tolerance,
survives compression and partial occlusion at IG / LinkedIn feed scale).

## Conventions

Marketplace conventions: edit under `source/`, run `scripts/build.py`, bump
the version on changes.
