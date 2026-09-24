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
  # alpha_at PNG X_frac Y_frac  → integer 0..255 (ImageMagick pixel coords)
  local png="$1" fx="$2" fy="$3"
  convert "$png" -format "%[fx:int(round(255*u.p{${fx}*w,${fy}*h}.a))]" info:
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

# 10) empty OUTPUT + --ensure → rebuilds
: > "$TMP/tyneham_disc.png"
assert_ok "rebuilds after empty OUTPUT" "$MAKE" --conf "$TMP/run.conf" --ensure
assert_ok "empty OUTPUT rebuilt non-empty" test -s "$TMP/tyneham_disc.png"
assert_ok "empty OUTPUT rebuilt valid PNG" identify "$TMP/tyneham_disc.png"

# 11) garbage/truncated non-empty OUTPUT + --ensure → rebuilds
printf 'not-a-real-png-just-garbage' > "$TMP/tyneham_disc.png"
assert_ok "rebuilds after garbage OUTPUT" "$MAKE" --conf "$TMP/run.conf" --ensure
assert_ok "garbage OUTPUT rebuilt valid PNG" identify "$TMP/tyneham_disc.png"
assert_ok "garbage OUTPUT rebuilt non-empty" test -s "$TMP/tyneham_disc.png"

# 12) --help exits 0
assert_ok "--help exits 0" "$MAKE" --help

# 13) INNER_MM=abc → non-zero, stderr has ERROR:, no Traceback
sed 's/^INNER_MM=.*/INNER_MM=abc/' "$TMP/disc.conf" > "$TMP/abc.conf"
assert_fail "rejects INNER_MM=abc" "$MAKE" --conf "$TMP/abc.conf"
ABC_ERR="$("$MAKE" --conf "$TMP/abc.conf" 2>&1 >/dev/null || true)"
case "$ABC_ERR" in
  *ERROR:*) echo "PASS: INNER_MM=abc stderr contains ERROR:"; PASS=$((PASS + 1)) ;;
  *) echo "FAIL: INNER_MM=abc stderr missing ERROR: [$ABC_ERR]" >&2; FAIL=$((FAIL + 1)) ;;
esac
case "$ABC_ERR" in
  *Traceback*) echo "FAIL: INNER_MM=abc stderr contains Traceback" >&2; FAIL=$((FAIL + 1)) ;;
  *) echo "PASS: INNER_MM=abc stderr has no Traceback"; PASS=$((PASS + 1)) ;;
esac

echo ""
echo "Results: $PASS passed, $FAIL failed"
[ "$FAIL" -eq 0 ]
