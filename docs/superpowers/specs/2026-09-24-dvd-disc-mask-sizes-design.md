# DVD disc mask sizes — configurable design

**Date:** 2026-09-24  
**Location:** `dvd_labels/`  
**Status:** Approved (approach A)

## Problem

Printing used a full square image (`tyneham.jpg`) at 120×120 mm borderless. Ink covered the center hole and the tray outside the circular disc. A pre-masked annulus was added (`20 mm` inner / `116 mm` outer for hub/small-hole discs), but sizes were hard-coded in a one-off command. If the disc type is wrong (standard vs hub-printable), regenerating the mask requires re-deriving ImageMagick geometry.

## Requirements

1. Change inner/outer sizes by editing a **config file only** (no CLI args for day-to-day use).
2. **Auto-rebuild** the masked PNG when config (or source image) is newer than the output.
3. **Easy preview** of the masked image before committing a disc.
4. Never modify the original source image.
5. Both print entry points stay in sync with the config.

## Approach (A — chosen)

One builder script + thin print wrappers. Rejected: B (all logic in `print_dvd.sh` — hard to preview without print flow), C (Makefile — heavier than needed).

## Components

### `disc.conf`

Shell-sourceable config in `dvd_labels/`:

```bash
INNER_MM=20     # no-ink hole diameter; hub/small-hole ~20–22; standard ~40–43
OUTER_MM=116    # outer print edge; usually 116–118 (physical disc 120)
SOURCE=tyneham.jpg
OUTPUT=tyneham_disc.png
```

Only file edited to retune sizes. Comments document common presets (physical hole is 15 mm; Epson hub minimum is 20 mm).

### `make_disc_mask.sh`

- Optional `--conf PATH` (default: `./disc.conf` next to the script).
- Optional `--preview`: also write `preview.png` (flattened on white so hole/corners are obvious) and print the path; open with `xdg-open` if `$DISPLAY` is set.
- Sources config; validates `INNER_MM >= 15`, `OUTER_MM <= 120`, `INNER_MM < OUTER_MM`.
- Builds annulus mask with ImageMagick (same geometry as the approved manual step):
  - Canvas: 4724×4724 px (= 120 mm at ~1000 dpi); center 2362,2362.
  - White disc radius = `OUTER_MM/2` in px; black hole radius = `INNER_MM/2` in px.
  - **Circle draw uses a point on the circumference:** `(cx, cy - r_px)` — not `(cx, cy - r)` misread as radius-only forms.
  - Composite mask alpha onto resized `SOURCE` (never write to `SOURCE`).
- Writes `OUTPUT` and sidecar `${OUTPUT%.png}.meta` (e.g. `tyneham_disc.meta`) containing `INNER_MM`, `OUTER_MM`, `SOURCE` mtime, build time — used for staleness checks without re-parsing PNG.

### Staleness / auto-rebuild

Rebuild logic lives only in `make_disc_mask.sh --ensure` (no separate `mask_lib.sh`):

- Exit 0 immediately if `OUTPUT` exists and is newer than both `disc.conf` and `SOURCE`, and `.meta` matches current `INNER_MM`/`OUTER_MM`.
- Otherwise run the full build, then exit 0.
- Print scripts and `preview_disc.sh` call `make_disc_mask.sh --ensure` only.
- Builder logs: `Using inner=20mm outer=116mm → tyneham_disc.png`.

### `print_dvd.sh` / `print_tyneham.sh`

- Call `make_disc_mask.sh --ensure` before building the print PDF.
- Print PDF keeps alpha (`convert "$OUTPUT" -alpha on "$PDF"`) so transparent corners/hole do not flatten to white ink.
- Rest of print flow unchanged (copies prompt, load disc, `lp` with `media=120x120mm.Borderless` + `MediaType=Disc`).

### `preview_disc.sh`

Thin wrapper: `make_disc_mask.sh --ensure` then `--preview`. Prints preview path.

## Data flow

```
disc.conf ──┐
tyneham.jpg ─┼─► make_disc_mask.sh ─► tyneham_disc.png + .meta
            │         ▲
            │         │ stale?
print_dvd.sh ─ make_disc_mask.sh --ensure
                  │
                  ▼
            PDF (alpha) ─► lp Canon_TS700_series_USB
```

## Error handling

- Invalid conf values → exit non-zero with message before any print.
- Missing `SOURCE` → exit with path shown.
- Missing ImageMagick `convert` → exit with install hint.
- Print scripts: if mask build fails, do not submit a job.

## Testing

1. `INNER_MM=20 OUTER_MM=116` → alpha 0 at center and outside outer; 255 in the ring (script or `identify` spot checks).
2. Edit conf to `INNER_MM=22` → next `print_dvd.sh` (or `preview_disc.sh`) rebuilds without manual step.
3. Touch `tyneham.jpg` → rebuild triggers; original file bytes unchanged.
4. Invalid conf (`INNER_MM=10` or `OUTER=200`) → clear error, no print.
5. Preview path exists and shows white hole/corners on flatten.

## Out of scope

- CLI size overrides for print (config only, per requirement).
- Changing CUPS/media options or printer setup.
- Editing `tyneham.jpg` or other source assets.
