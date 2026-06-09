---
name: qr-generator
description: Generate a scannable QR code PNG from a URL or short string. Use whenever a slide, infographic, flyer, printed asset, or visual deliverable needs a scan target. The skill picks the best locally-available backend (macOS CoreImage via Swift, Python qrcode/segno, or qrencode CLI) and writes a high-resolution PNG with high error correction by default.
---

# QR generator

Generate a scannable QR code PNG from a URL or short string. The QR is
generated **locally** — the input never leaves the machine.

## When to use

- A carousel / slide / infographic needs a scan target because the platform
  isn't tappable (Instagram, print, video frames).
- A reproducible build artifact needs a checked-in QR pointing at a URL that
  may change in the future (course link, sign-up form, asset catalog).
- A user asks "make me a QR for this link", "create a QR code", or similar.

## Inputs

The user provides a URL (required) and optionally an output path and size:

```
url:    <string>          # required — what the QR should encode
out:    <path>            # optional — defaults to ./qr.png
size:   <px>              # optional — final PNG width/height in pixels.
                          #   default 1500. picked because IG/LinkedIn feed
                          #   compresses aggressively, and a 1500px PNG
                          #   downscales cleanly to any slide-sized box.
ec:     L | M | Q | H     # optional — error-correction level. default H
                          #   (~30% damage tolerance — survives glare,
                          #   moiré, and partial occlusion when scanned
                          #   from a phone camera).
```

If `url` is missing, ask the user for it. Don't invent.

## Process

1. **Resolve the output path.** If the user gave a directory, append `qr.png`.
   If they gave a filename without `.png`, append it. If they gave nothing,
   default to `./qr.png` in the working directory.
2. **Verify the parent directory exists.** Don't auto-create deep nested
   trees without checking — flag and ask if the path looks like a typo.
3. **Pick a backend** (in order — first one that works wins):
   - **macOS** → run the bundled Swift script:
     ```bash
     swift "${CLAUDE_PLUGIN_ROOT}/skills/qr-generator/scripts/generate_qr.swift" \
       "<url>" "<out>" [<size>] [<ec>]
     ```
     Zero dependencies — uses CoreImage's `CIQRCodeGenerator` which ships
     with the OS.
   - **Python `qrcode`** → quick check `python3 -c "import qrcode"`. If it
     imports, run a tiny inline Python program (see snippet below) that
     writes the PNG with PIL.
   - **Python `segno`** → quick check `python3 -c "import segno"`. If it
     imports, run a tiny inline Python program (see snippet below).
   - **`qrencode` CLI** → quick check `command -v qrencode`. If present:
     ```bash
     qrencode -o "<out>" -s 28 -l H "<url>"
     ```
4. **Verify the file landed** with `ls -la <out>` and report size + dimensions
   to the user.
5. **Suggest a quick scan test:** open the PNG and scan it with the user's
   phone camera before they ship the asset.

If no backend is available, tell the user. Suggest they install one:
- macOS: already installed (Swift ships with Xcode CLI tools).
- Linux: `apt install qrencode` or `pip install qrcode[pil]`.
- Anywhere with Python: `pip install qrcode[pil]` (or `pip install segno`).

Do **not** call out to external QR-as-a-service URLs — that leaks the input
URL to a third party, and the user already trusted you with a local task.

## Backend snippets

### macOS — Swift (bundled script, default path)

The script lives at `scripts/generate_qr.swift`. It accepts:

```
swift generate_qr.swift <url> [<out=qr.png>] [<size=1500>] [<ec=H>]
```

### Python — `qrcode` library (write inline; do not check anything in)

```python
import qrcode
img = qrcode.make("<url>", error_correction=qrcode.constants.ERROR_CORRECT_H, box_size=20)
img.resize((1500, 1500)).save("<out>")
```

### Python — `segno` (alternative)

```python
import segno
segno.make("<url>", error="h").save("<out>", scale=20)
```

### CLI — `qrencode`

```bash
qrencode -o "<out>" -s 28 -l H "<url>"
```

## Defaults — why these values

- **1500×1500 px:** covers a slide hero or print at 4–5 inches comfortably,
  and downscales cleanly. Smaller (~500 px) is fine for inline web use.
- **Error correction H (~30%):** the highest level. Adds redundancy modules
  so the code still scans through compression artifacts, glare from a phone
  screen, and small graphic overlays (a logo in the center is feasible at H).
- **No logo overlay by default:** asks the user if they want one. A logo
  changes the design constraints (must be ≤ 25% of the QR area).

## Output format expected from the assistant

After generating, tell the user:

```
Wrote <out> — <bytes> bytes, <width>×<height>, encoding: <url>
```

…and offer to either embed it in an HTML/Markdown asset they're working on,
or leave it as a standalone PNG.

## Reproducibility tip (optional, on request)

If the user wants the QR to be **regenerable** (e.g., the URL might change
later, or it lives in a checked-in campaign), suggest a small co-located
reproducer:

```
<asset-folder>/
  qr-link.txt        ← the URL, one line, single source of truth
  generate-qr.sh     ← a one-liner that calls this skill's backend
  qr.png             ← the generated PNG (regenerate from the script above)
```

That keeps the URL in one place and re-running the script after editing
`qr-link.txt` produces an updated QR.
