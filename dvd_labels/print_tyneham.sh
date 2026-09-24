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
