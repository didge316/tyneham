# DVD Label Printing — Canon TS700 on Debian

DVD/CD label printing is now working on this Debian machine. This doc explains
everything: what was fixed, how to print, and the quirks.

---

## The commands you need

```bash
cd /home/matt/projects/tyneham/dvd_labels

# Change sizes (hub/small-hole vs standard):
#   edit disc.conf → INNER_MM / OUTER_MM

./preview_disc.sh    # rebuild if needed + open/show preview.png
./print_dvd.sh       # ask copies, load disc, print
```

`print_dvd.sh` / `print_tyneham.sh` call `make_disc_mask.sh --ensure`, so the
mask always matches `disc.conf` and `tyneham.jpg`.

### disc.conf

| Key | Meaning | Typical |
|-----|---------|---------|
| `INNER_MM` | No-ink hole diameter | hub/small-hole **20–22**; standard **40–43** |
| `OUTER_MM` | Outer print edge | **116–118** (disc is 120) |
| `SOURCE` | Original image (never modified) | `tyneham.jpg` |
| `OUTPUT` | Masked PNG | `tyneham_disc.png` |

Physical hole is 15 mm. Do not set `INNER_MM` below 15.

---

## How it works

- **Printer:** Canon PIXMA TS700 series (USB)
- **Driver:** driverless CUPS (IPP), managed by `cups-browsed`
- **Disc print area:** 120×120mm borderless, rear disc feeder
- **Image:** masked annulus from `disc.conf` — derived from `tyneham.jpg`
  (original untouched), masked to the printable ring only (transparent centre
  hole + corners so no ink hits the tray)

### What was fixed

The printer was detected but disc prints got stuck. The fixes:

1. **`cups-browsed`** — enabled `CreateUSBPrinters Yes` in
   `/etc/cups/cups-browsed.conf` so the local USB printer gets a proper
   `implicitclass://` device URI (without the broken `@localhost` suffix).

2. **Disc tray + paper tray must both be engaged** — the printer will not
   accept a disc print unless:
   - the **disc tray** (front multi-purpose tray) is inserted with the disc, **and**
   - the **paper output tray** is pushed all the way in.

   If either is missing, the printer shows a warning and does nothing.

### Disc loading (from the official Canon manual)

1. Wait for the printer LCD to prompt you to load the disc.
2. Push the paper output tray all the way in.
3. **Print side UP** on the multi-purpose tray, press against the lock at the
   bottom.
4. Insert the top of the disc into the slits.
5. Slide the tray straight in horizontally until the arrows align.
6. Press **OK** — the tray draws in and printing starts.

---

## Troubleshooting

| Symptom | Cause / fix |
|---------|-------------|
| Job stuck at "processing", nothing prints | Both trays must be engaged. Load disc + push paper tray in. |
| Printer says "spool area full" | Stale CUPS state — `sudo cancel -a` then `sudo lpadmin -p Canon_TS700_series_USB -E`. The real blocker is the trays. |
| "No longer ready for disc printing" | Cancel job, reset printer state (`sudo lpadmin -p Canon_TS700_series_USB -E`), reload disc. |
| Printer idle but no jobs | Queue may be blocked by a stuck job — `sudo cancel -a`. |

### Reset commands

```bash
sudo cancel -a                                   # clear all jobs
sudo lpadmin -p Canon_TS700_series_USB -E        # enable + accept jobs
```

---

## Other files

- `disc.conf` — sizes (edit this)
- `make_disc_mask.sh` — build/ensure/preview mask
- `preview_disc.sh` — ensure + preview
- `print_dvd.sh` — **main launcher** (copies prompt + print)
- `print_tyneham.sh` — quick print (no copy prompt)
- `tyneham_disc.png` — generated masked image
- `tyneham_disc.meta` — build metadata
- `tyneham.jpg` — source (never modified)
- `tyneham_disc_smallhole.png` — optional/legacy pre-masked annulus
- `make_dvd_label.sh` — generate text-based DVD labels (title + subtitle)
- `print_dvd_label.sh` — print a generated label PDF

---

## Notes

- Disc prints are slow — allow a few minutes per copy (the disc cycles in,
  prints, then ejects).
- The printer is `Canon_TS700_series_USB` in CUPS.
- Works without any proprietary Canon drivers — fully driverless.
