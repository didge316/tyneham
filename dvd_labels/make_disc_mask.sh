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

# Temps cleaned on any exit (set -e / signals)
TMP_MASK=""
TMP_IMG=""
TMP_OUT=""
TMP_META=""
cleanup() {
  local rc=$?
  set +e
  [ -n "$TMP_MASK" ] && rm -f "$TMP_MASK"
  [ -n "$TMP_IMG" ] && rm -f "$TMP_IMG"
  [ -n "$TMP_OUT" ] && rm -f "$TMP_OUT"
  [ -n "$TMP_META" ] && rm -f "$TMP_META"
  return "$rc"
}
trap cleanup EXIT
trap 'exit 130' INT
trap 'exit 143' TERM
trap 'exit 129' HUP

usage() {
  echo "Usage: $0 [--conf PATH] [--ensure] [--preview]" >&2
  exit 2
}

usage_stdout() {
  echo "Usage: $0 [--conf PATH] [--ensure] [--preview]"
  exit 0
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
    -h|--help) usage_stdout ;;
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

if [ -d "$OUTPUT" ]; then
  die "OUTPUT path is a directory: $OUTPUT"
fi

# Validate sizes (integers or simple decimals); no Python traceback on bad input
is_num() {
  [[ "${1:-}" =~ ^[0-9]+([.][0-9]+)?$ ]]
}
if ! is_num "$INNER_MM" || ! is_num "$OUTER_MM"; then
  die "invalid INNER_MM/OUTER_MM"
fi
python3 - "$INNER_MM" "$OUTER_MM" 2>/dev/null <<'PY' || die "invalid INNER_MM/OUTER_MM"
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

output_looks_valid() {
  [ -s "$OUTPUT" ] || return 1
  [ -r "$OUTPUT" ] || return 1
  if command -v identify >/dev/null 2>&1; then
    identify "$OUTPUT" >/dev/null 2>&1 || return 1
  else
    convert "$OUTPUT" -format '' info: >/dev/null 2>&1 || return 1
  fi
  return 0
}

is_stale() {
  output_looks_valid || return 0
  [ -f "$META" ] || return 0
  # OUTPUT must be newer than conf and source
  [ "$OUTPUT" -nt "$CONF" ] || return 0
  [ "$OUTPUT" -nt "$SOURCE" ] || return 0
  # meta must match current sizes
  grep -qxF "INNER_MM=$INNER_MM" "$META" || return 0
  grep -qxF "OUTER_MM=$OUTER_MM" "$META" || return 0
  grep -qxF "SOURCE=$SOURCE" "$META" || return 0
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

  TMP_MASK="$(mktemp /tmp/disc_mask.XXXXXX.png)"
  TMP_IMG="$(mktemp /tmp/disc_img.XXXXXX.png)"
  # Atomic OUTPUT: temp in same directory, then mv
  TMP_OUT="$(mktemp "$(dirname "$OUTPUT")/.disc_out.XXXXXX.png")"

  # circle CX,CY PX,PY — PX,PY is a point on the circumference: (cx, cy - r)
  convert -size "${canvas}x${canvas}" xc:none \
    -fill white -draw "circle $cx,$cy $cx,$((cy - r_out))" \
    -fill black -draw "circle $cx,$cy $cx,$((cy - r_in))" \
    "$TMP_MASK"

  # Fit source into outer diameter box, center on full canvas, keep alpha
  local box
  box="$(python3 -c "print(round(float('$OUTER_MM')/120 * $canvas))")"
  convert "$SOURCE" -resize "${box}x${box}" -gravity center \
    -background none -extent "${canvas}x${canvas}" \
    "$TMP_IMG"

  convert "$TMP_IMG" "$TMP_MASK" -alpha off -compose CopyOpacity -composite \
    "$TMP_OUT"
  mv -f "$TMP_OUT" "$OUTPUT"
  TMP_OUT=""

  # Atomic META: write temp in same directory, then mv
  TMP_META="$(mktemp "$(dirname "$META")/.disc_meta.XXXXXX")"
  {
    echo "INNER_MM=$INNER_MM"
    echo "OUTER_MM=$OUTER_MM"
    echo "SOURCE=$SOURCE"
    echo "BUILT_AT=$(date -Iseconds)"
  } > "$TMP_META"
  mv -f "$TMP_META" "$META"
  TMP_META=""

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
