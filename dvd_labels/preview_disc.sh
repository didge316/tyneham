#!/usr/bin/env bash
# preview_disc.sh — rebuild mask if stale, then show preview.png
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
"$SCRIPT_DIR/make_disc_mask.sh" --ensure --preview
