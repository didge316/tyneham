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
