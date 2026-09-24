# DVD Disc Mask Sizes Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make DVD annulus mask sizes (inner hole / outer edge) configurable via `disc.conf`, with auto-rebuild and a preview before print.

**Architecture:** One builder (`make_disc_mask.sh`) reads `disc.conf`, validates sizes, builds `tyneham_disc.png` + `.meta`, and supports `--ensure` / `--preview`. Print scripts only call `--ensure` then convert PNG→PDF with alpha. Original `tyneham.jpg` is never modified.

**Tech Stack:** Bash, ImageMagick (`convert`), PNG alpha, shell-sourced config.

**Spec:** `docs/superpowers/specs/2026-09-24-dvd-disc-mask-sizes-design.md`

**Working directory for all tasks:** `/home/matt/projects/tyneham/dvd_labels` unless noted.

**Test runner:** `bash tests/test_disc_mask.sh` (plain Bash asserts; exit 0 = pass).

---

## File structure

| Action | Path | Responsibility |
|--------|------|----------------|
| Create | `dvd_labels/disc.conf` | Sizes + source/output paths (only file users edit) |
| Create | `dvd_labels/make_disc_mask.sh` | Validate, build mask, `--ensure`, `--preview`, write `.meta` |
| Create | `dvd_labels/preview_disc.sh` | `--ensure` then `--preview` |
| Create | `dvd_labels/tests/test_disc_mask.sh` | End-to-end tests in a temp dir |
| Modify | `dvd_labels/print_dvd.sh` | Use conf OUTPUT; call `--ensure` before PDF |
| Modify | `dvd_labels/print_tyneham.sh` | Same as print_dvd.sh |
| Modify | `dvd_labels/README.md` | Document conf / ensure / preview |

Do not delete `tyneham_disc_smallhole.png` (legacy); new default output is `tyneham_disc.png`.

---

### Task 1: Config + builder skeleton + failing tests

**Files:**
- Create: `dvd_labels/disc.conf`
- Create: `dvd_labels/make_disc_mask.sh`
- Create: `dvd_labels/tests/test_disc_mask.sh`

- [ ] **Step 1: Write `disc.conf`**

```bash
# disc.conf — DVD mask sizes (edit these; scripts read this file)
# Physical hole is 15mm. Hub/small-hole printable: INNER ~20–22.
# Standard (large clear hub) printable: INNER ~40–43.
# OUTER: usually 116–118 (physical disc is 120mm).
INNER_MM=20
OUTER_MM=116
SOURCE=tyneham.jpg
OUTPUT=tyneham_disc.png
```

- [ ] **Step 2: Write failing tests**

Create `tests/test_disc_mask.sh`:

```bash
#!/usr/bin/env bash
# tests/test_disc_mask.sh — run from dvd_labels/: bash tests/test_disc_mask.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MAKE="$ROOT/make_disc_mask.sh"
PASS=0
FAIL=0

assert_eq() {
  local label="$1" expected="$2" actual="$3"
  if [ "$expected" = "$actual" ]; then
    echo "PASS: $label"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $label (expected [$expected] got [$actual])" >&2
    FAIL=$((FAIL + 1))
  fi
}

assert_ok() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "PASS: $label"
    PASS=$((PASS + 1))
  else
    echo "FAIL: $label" >&2
    FAIL=$((FAIL + 1))
  fi
}

assert_fail() {
  local label="$1"
  shift
  if "$@" >/dev/null 2>&1; then
    echo "FAIL: $label (expected non-zero exit)" >&2
    FAIL=$((FAIL + 1))
  else
    echo "PASS: $label"
    PASS=$((PASS + 1))
  fi
}

# --- workspace -----------------------------------------------------------------
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
cp "$ROOT/tyneham.jpg" "$TMP/"
cp "$ROOT/disc.conf" "$TMP/"

alpha_at() {
  # alpha_at PNG X_frac Y_frac  → integer 0..255 (ImageMagick only)
  local png="$1" fx="$2" fy="$3"
  convert "$png" -format "%[fx:int(round(255*u.p{${fx},${fy}}.a))]" info:
}

# 1) invalid INNER_MM=10 → fail
sed 's/^INNER_MM=.*/INNER_MM=10/' "$TMP/disc.conf" > "$TMP/bad.conf"
assert_fail "rejects INNER_MM=10" \
  "$MAKE" --conf "$TMP/bad.conf"

# 2) invalid OUTER_MM=200 → fail
sed 's/^OUTER_MM=.*/OUTER_MM=200/' "$TMP/disc.conf" > "$TMP/bad2.conf"
assert_fail "rejects OUTER_MM=200" \
  "$MAKE" --conf "$TMP/bad2.conf"

# 3) build default mask in TMP
cp "$TMP/disc.conf" "$TMP/run.conf"
# conf paths are relative to conf directory
assert_ok "builds default mask" "$MAKE" --conf "$TMP/run.conf"
assert_ok "writes OUTPUT png" test -f "$TMP/tyneham_disc.png"
assert_ok "writes meta sidecar" test -f "$TMP/tyneham_disc.meta"

# 4) alpha geometry: hole center=0, just outside hole=255, outside outer=0
# canvas center 0.5,0.5; hole r=10/120 of half → sample 0.5+12/120
# outer r=58/120 → sample at 0.5+59/120
A_CENTER="$(alpha_at "$TMP/tyneham_disc.png" 0.5 0.5)"
A_RING="$(alpha_at "$TMP/tyneham_disc.png" 0.60 0.5)"
A_OUT="$(alpha_at "$TMP/tyneham_disc.png" 0.995 0.5)"
assert_eq "center hole alpha=0" "0" "$A_CENTER"
assert_eq "ring alpha=255" "255" "$A_RING"
assert_eq "outside outer alpha=0" "0" "$A_OUT"

# 5) source never modified
SRC_HASH_BEFORE="$(md5sum "$TMP/tyneham.jpg" | awk '{print $1}')"
"$MAKE" --conf "$TMP/run.conf" >/dev/null
SRC_HASH_AFTER="$(md5sum "$TMP/tyneham.jpg" | awk '{print $1}')"
assert_eq "SOURCE bytes unchanged" "$SRC_HASH_BEFORE" "$SRC_HASH_AFTER"

# 6) --ensure skips when fresh
BEFORE_MTIME="$(stat -c %Y "$TMP/tyneham_disc.png")"
sleep 1
assert_ok "--ensure fresh is ok" "$MAKE" --conf "$TMP/run.conf" --ensure
AFTER_MTIME="$(stat -c %Y "$TMP/tyneham_disc.png")"
assert_eq "--ensure does not rebuild when fresh" "$BEFORE_MTIME" "$AFTER_MTIME"

# 7) conf size change → --ensure rebuilds
sed 's/^INNER_MM=.*/INNER_MM=22/' "$TMP/run.conf" > "$TMP/run2.conf"
mv "$TMP/run2.conf" "$TMP/run.conf"
assert_ok "--ensure rebuilds after conf edit" "$MAKE" --conf "$TMP/run.conf" --ensure
META="$(cat "$TMP/tyneham_disc.meta")"
case "$META" in
  *INNER_MM=22*) echo "PASS: meta records INNER_MM=22"; PASS=$((PASS+1)) ;;
  *) echo "FAIL: meta missing INNER_MM=22 [$META]" >&2; FAIL=$((FAIL+1)) ;;
esac

# 8) touch SOURCE → --ensure rebuilds
sleep 1
touch "$TMP/tyneham.jpg"
M1="$(stat -c %Y "$TMP/tyneham_disc.png")"
sleep 1
assert_ok "--ensure rebuilds after SOURCE touch" "$MAKE" --conf "$TMP/run.conf" --ensure
M2="$(stat -c %Y "$TMP/tyneham_disc.png")"
if [ "$M2" -gt "$M1" ]; then
  echo "PASS: mtime advanced after SOURCE touch"
  PASS=$((PASS + 1))
else
  echo "FAIL: no rebuild after SOURCE touch" >&2
  FAIL=$((FAIL + 1))
fi

# 9) --preview writes preview.png
assert_ok "--preview writes preview.png" "$MAKE" --conf "$TMP/run.conf" --preview
assert_ok "preview.png exists" test -f "$TMP/preview.png"

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
```

- [ ] **Step 3: Run tests — expect FAIL (script missing or no real build)**

```bash
bash tests/test_disc_mask.sh
```

Expected: non-zero exit; messages like `FAIL: rejects INNER_MM=10` or cannot execute `make_disc_mask.sh`.

- [ ] **Step 4: Implement full `make_disc_mask.sh`**

```bash
#!/usr/bin/env bash
# make_disc_mask.sh — build annulus-masked DVD PNG from disc.conf
#
# Usage:
#   ./make_disc_mask.sh [--conf PATH] [--ensure] [--preview]
#
# --ensure   rebuild only if OUTPUT stale vs conf/SOURCE/meta
# --preview  also write preview.png (white flatten) and print path
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONF="$SCRIPT_DIR/disc.conf"
DO_ENSURE=0
DO_PREVIEW=0

usage() {
  echo "Usage: $0 [--conf PATH] [--ensure] [--preview]" >&2
  exit 2
}

while [ $# -gt 0 ]; do
  case "$1" in
    --conf)
      [ $# -ge 2 ] || usage
      CONF="$2"
      shift 2
      ;;
    --ensure) DO_ENSURE=1; shift ;;
    --preview) DO_PREVIEW=1; shift ;;
    -h|--help) usage ;;
    *) echo "Unknown option: $1" >&2; usage ;;
  esac
done

if [ ! -f "$CONF" ]; then
  echo "ERROR: config not found: $CONF" >&2
  exit 1
fi

# Resolve paths relative to the config file's directory
CONF_DIR="$(cd "$(dirname "$CONF")" && pwd)"
# shellcheck source=/dev/null
source "$CONF"

: "${INNER_MM:?INNER_MM missing in $CONF}"
: "${OUTER_MM:?OUTER_MM missing in $CONF}"
: "${SOURCE:?SOURCE missing in $CONF}"
: "${OUTPUT:?OUTPUT missing in $CONF}"

# Relative paths in conf are relative to conf dir
case "$SOURCE" in /*) ;; *) SOURCE="$CONF_DIR/$SOURCE" ;; esac
case "$OUTPUT" in /*) ;; *) OUTPUT="$CONF_DIR/$OUTPUT" ;; esac
META="${OUTPUT%.png}.meta"
PREVIEW="$(dirname "$OUTPUT")/preview.png"

die() { echo "ERROR: $*" >&2; exit 1; }

# Validate sizes (integers or simple decimals)
python3 - "$INNER_MM" "$OUTER_MM" <<'PY' || die "invalid INNER_MM/OUTER_MM"
import sys
inner, outer = float(sys.argv[1]), float(sys.argv[2])
ok = inner >= 15 and outer <= 120 and inner < outer
sys.exit(0 if ok else 1)
PY

if [ ! -f "$SOURCE" ]; then
  die "SOURCE not found: $SOURCE"
fi

if ! command -v convert >/dev/null 2>&1; then
  die "ImageMagick 'convert' not found (install imagemagick)"
fi

is_stale() {
  [ -f "$OUTPUT" ] || return 0
  [ -f "$META" ] || return 0
  # OUTPUT must be newer than conf and source
  [ "$OUTPUT" -nt "$CONF" ] || return 0
  [ "$OUTPUT" -nt "$SOURCE" ] || return 0
  # meta must match current sizes
  grep -qx "INNER_MM=$INNER_MM" "$META" || return 0
  grep -qx "OUTER_MM=$OUTER_MM" "$META" || return 0
  grep -qx "SOURCE=$SOURCE" "$META" || return 0
  return 1
}

build() {
  local canvas=4724
  local cx=$((canvas / 2))
  local cy=$((canvas / 2))
  # px per mm on 120mm canvas
  local px_per_mm
  px_per_mm="$(python3 -c "print($canvas / 120.0)")"
  local r_out r_in
  r_out="$(python3 -c "print(round(float('$OUTER_MM')/2 * $px_per_mm))")"
  r_in="$(python3 -c "print(round(float('$INNER_MM')/2 * $px_per_mm))")"

  local tmp_mask tmp_img
  tmp_mask="$(mktemp /tmp/disc_mask.XXXXXX.png)"
  tmp_img="$(mktemp /tmp/disc_img.XXXXXX.png)"
  # shellcheck disable=SC2064
  trap "rm -f '$tmp_mask' '$tmp_img'" RETURN

  # circle CX,CY PX,PY — PX,PY is a point on the circumference: (cx, cy - r)
  convert -size "${canvas}x${canvas}" xc:none \
    -fill white -draw "circle $cx,$cy $cx,$((cy - r_out))" \
    -fill black -draw "circle $cx,$cy $cx,$((cy - r_in))" \
    "$tmp_mask"

  # Fit source into outer diameter box, center on full canvas, keep alpha
  local box
  box="$(python3 -c "print(round(float('$OUTER_MM')/120 * $canvas))")"
  convert "$SOURCE" -resize "${box}x${box}" -gravity center \
    -background none -extent "${canvas}x${canvas}" \
    "$tmp_img"

  convert "$tmp_img" "$tmp_mask" -alpha off -compose CopyOpacity -composite \
    "$OUTPUT"

  {
    echo "INNER_MM=$INNER_MM"
    echo "OUTER_MM=$OUTER_MM"
    echo "SOURCE=$SOURCE"
    echo "BUILT_AT=$(date -Iseconds)"
  } > "$META"

  echo "Using inner=${INNER_MM}mm outer=${OUTER_MM}mm → $(basename "$OUTPUT")"
}

preview() {
  convert "$OUTPUT" -background white -alpha remove -alpha off "$PREVIEW"
  echo "Preview: $PREVIEW"
  if [ -n "${DISPLAY:-}" ] && command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$PREVIEW" >/dev/null 2>&1 || true
  fi
}

if [ "$DO_ENSURE" -eq 1 ]; then
  if is_stale; then
    build
  else
    echo "Mask up to date: inner=${INNER_MM}mm outer=${OUTER_MM}mm → $(basename "$OUTPUT")"
  fi
else
  build
fi

if [ "$DO_PREVIEW" -eq 1 ]; then
  preview
fi
```

- [ ] **Step 5: Make executable and run tests — expect PASS**

```bash
chmod +x make_disc_mask.sh
bash tests/test_disc_mask.sh
```

Expected: `Results: N passed, 0 failed` and exit 0.

- [ ] **Step 6: Commit**

```bash
cd /home/matt/projects/tyneham
git add dvd_labels/disc.conf dvd_labels/make_disc_mask.sh dvd_labels/tests/test_disc_mask.sh
git commit -m "feat(dvd_labels): configurable disc mask builder with ensure/preview"
```

---

### Task 2: `preview_disc.sh`

**Files:**
- Create: `dvd_labels/preview_disc.sh`

- [ ] **Step 1: Write `preview_disc.sh`**

```bash
#!/usr/bin/env bash
# preview_disc.sh — rebuild mask if stale, then show preview.png
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/make_disc_mask.sh" --ensure --preview
```

- [ ] **Step 2: Smoke-test preview**

```bash
chmod +x preview_disc.sh
./preview_disc.sh
```

Expected: line `Using inner=...` or `Mask up to date: ...` and `Preview: .../preview.png`; file exists.

- [ ] **Step 3: Commit**

```bash
cd /home/matt/projects/tyneham
git add dvd_labels/preview_disc.sh
git commit -m "feat(dvd_labels): preview_disc.sh wrapper"
```

---

### Task 3: Wire `print_dvd.sh` to conf + `--ensure`

**Files:**
- Modify: `dvd_labels/print_dvd.sh`

- [ ] **Step 1: Replace header IMAGE setup and pre-print mask step**

Replace the block from `PRINTER=` through the end of the file with:

```bash
#!/usr/bin/env bash
#
# print_dvd.sh — Print the configured disc image, choosing copies.
#
# Sizes come from disc.conf; mask is rebuilt automatically if stale.
#
# Usage:  ./print_dvd.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PRINTER="${PRINTER:-Canon_TS700_series_USB}"
CONF="$SCRIPT_DIR/disc.conf"
PDF="/tmp/tyneham_disc.pdf"

# shellcheck source=/dev/null
source "$CONF"
OUTPUT_PATH="$OUTPUT"
case "$OUTPUT_PATH" in /*) ;; *) OUTPUT_PATH="$SCRIPT_DIR/$OUTPUT_PATH" ;; esac

# --- 0. Rebuild mask if needed (fails closed: no job if build fails) --------
"$SCRIPT_DIR/make_disc_mask.sh" --conf "$CONF" --ensure

# --- 1. Pick number of copies ---------------------------------------------
read -r -p "How many copies? [1] " COPIES
COPIES="${COPIES:-1}"
if ! [[ "$COPIES" =~ ^[0-9]+$ ]] || [ "$COPIES" -lt 1 ]; then
  echo "Invalid copy count. Using 1." >&2
  COPIES=1
fi

echo ""
echo "=================================================="
echo "  PRINTING $COPIES COPY(COPIES) ONTO DVD"
echo "=================================================="
echo "  Mask: inner=${INNER_MM}mm outer=${OUTER_MM}mm → $OUTPUT"
echo ""
echo "LOAD THE DISC NOW:"
echo "  1. Insert the disc tray (front multi-purpose tray)"
echo "     - print side UP, press against the lock at the bottom"
echo "  2. Push the paper output tray ALL THE WAY IN"
echo "  3. Press OK on the printer"
echo ""
echo "Then press ENTER here once the disc is loaded..."
read -r

# --- 2. Build the 120x120mm label PDF (keep alpha: no ink in hole/corners) --
echo "Preparing image..."
convert "$OUTPUT_PATH" -alpha on "$PDF"

# --- 3. Send to printer ----------------------------------------------------
echo "Sending to $PRINTER ..."
sudo lp -d "$PRINTER" \
  -n "$COPIES" \
  -o media=120x120mm.Borderless \
  -o MediaType=Disc \
  "$PDF"

echo ""
echo "Job submitted. Status:"
lpstat -o 2>/dev/null || true
echo ""
echo "The disc will cycle (in, print, out). Allow a few minutes per copy."
```

- [ ] **Step 2: Static check (no printer)**

```bash
bash -n print_dvd.sh && echo OK
```

Expected: `OK`

Optional dry check of ensure-only path:

```bash
./make_disc_mask.sh --ensure
```

Expected: `Mask up to date: ...` or rebuild line; exit 0.

- [ ] **Step 3: Commit**

```bash
cd /home/matt/projects/tyneham
git add dvd_labels/print_dvd.sh
git commit -m "feat(dvd_labels): print_dvd.sh uses disc.conf and --ensure"
```

---

### Task 4: Wire `print_tyneham.sh` the same way

**Files:**
- Modify: `dvd_labels/print_tyneham.sh`

- [ ] **Step 1: Replace file contents**

```bash
#!/usr/bin/env bash
#
# print_tyneham.sh — Print configured disc image (no copy prompt).
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

PRINTER="${PRINTER:-Canon_TS700_series_USB}"
CONF="$SCRIPT_DIR/disc.conf"
PDF="/tmp/tyneham_disc.pdf"

# shellcheck source=/dev/null
source "$CONF"
OUTPUT_PATH="$OUTPUT"
case "$OUTPUT_PATH" in /*) ;; *) OUTPUT_PATH="$SCRIPT_DIR/$OUTPUT_PATH" ;; esac

"$SCRIPT_DIR/make_disc_mask.sh" --conf "$CONF" --ensure

if ! [ -f "$OUTPUT_PATH" ]; then
  echo "ERROR: $OUTPUT_PATH not found" >&2
  exit 1
fi

echo "Preparing masked disc image from $OUTPUT_PATH ..."
echo "  (inner=${INNER_MM}mm outer=${OUTER_MM}mm)"
convert "$OUTPUT_PATH" -alpha on "$PDF"
echo "PDF created: $PDF"
echo ""
echo "Printing to $PRINTER (120x120mm Borderless, Disc feeder)..."
sudo lp -d "$PRINTER" \
  -o media=120x120mm.Borderless \
  -o MediaType=Disc \
  "$PDF"
echo ""
echo "Job submitted. Status:"
lpstat -o 2>/dev/null || true
echo ""
echo "Note: if the job shows 'processing-stopped' and the printer alert says"
echo "'spool area full', empty the TS700's waste-paper spool tray (rear cassette)"
echo "and the print will continue. Disc prints are slow — allow a few minutes."
```

- [ ] **Step 2: Syntax check**

```bash
bash -n print_tyneham.sh && echo OK
```

Expected: `OK`

- [ ] **Step 3: Commit**

```bash
cd /home/matt/projects/tyneham
git add dvd_labels/print_tyneham.sh
git commit -m "feat(dvd_labels): print_tyneham.sh uses disc.conf and --ensure"
```

---

### Task 5: README + full test run

**Files:**
- Modify: `dvd_labels/README.md`

- [ ] **Step 1: Update README “one command” and files list**

In `README.md`, update the quick-start section to:

```markdown
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
```

Also update **Other files** list to include `disc.conf`, `make_disc_mask.sh`, `preview_disc.sh`, `tyneham_disc.png`, `tyneham_disc.meta`.

- [ ] **Step 2: Run full test suite**

```bash
cd /home/matt/projects/tyneham/dvd_labels
bash tests/test_disc_mask.sh
bash -n make_disc_mask.sh print_dvd.sh print_tyneham.sh preview_disc.sh
```

Expected: all tests `PASS`, exit 0; `bash -n` silent/OK.

- [ ] **Step 3: Commit**

```bash
cd /home/matt/projects/tyneham
git add dvd_labels/README.md
git commit -m "docs(dvd_labels): document disc.conf, ensure, and preview"
```

---

## Spec coverage check

| Spec requirement | Task |
|------------------|------|
| Config file only for sizes | Task 1 (`disc.conf`) |
| Auto-rebuild when stale | Task 1 (`--ensure`), Tasks 3–4 |
| Easy preview | Tasks 1–2 (`--preview`, `preview_disc.sh`) |
| Never modify SOURCE | Task 1 build uses temp files; test #5 |
| Both print entry points in sync | Tasks 3–4 |
| Validation / fail closed | Task 1 tests #1–2; print scripts `set -e` + ensure |
| Alpha preserved on PDF | Tasks 3–4 `-alpha on` |
| README | Task 5 |

## Self-review notes

- No TBD/TODO placeholders; all code blocks complete.
- Function/flag names consistent: `--ensure`, `--preview`, `--conf`, `INNER_MM`, `OUTER_MM`, `OUTPUT`.
- Meta format: newline `KEY=value` lines matching tests (`INNER_MM=22`).
