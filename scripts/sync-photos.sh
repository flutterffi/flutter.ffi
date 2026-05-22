#!/usr/bin/env bash
# Copy & compress photos from local library into docs/public/photos/
# Usage: ./scripts/sync-photos.sh [count] [start_index]
# Env: PHOTO_SRC (default ~/Downloads/Instagram/robert_le.ph)

set -euo pipefail

SRC="${PHOTO_SRC:-$HOME/Downloads/Instagram/robert_le.ph}"
DEST="$(cd "$(dirname "$0")/.." && pwd)/docs/public/photos"
COUNT="${1:-12}"
START="${2:-1}"

if [[ ! -d "$SRC" ]]; then
  echo "Source not found: $SRC"
  exit 1
fi

mkdir -p "$DEST"
command -v sips >/dev/null || { echo "macOS sips required"; exit 1; }

echo "Copying $COUNT images from $SRC → $DEST (from index $START)"

find "$SRC" -maxdepth 1 -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) \
  -exec ls -l {} \; | sort -k5 -n | head -n "$COUNT" | awk '{print $NF}' | \
  while IFS= read -r file; do
    idx=$(printf '%02d' "$START")
    out="$DEST/photo-$idx.jpg"
    thumb="$DEST/thumb-$idx.jpg"
    sips -s format jpeg "$file" --out "$out" >/dev/null
    sips -Z 1200 -s format jpeg -s formatOptions 58 "$out" --out "$out" >/dev/null
    sips -Z 640 -s format jpeg -s formatOptions 52 "$out" --out "$thumb" >/dev/null
    echo "  photo-$idx.jpg ($(du -h "$out" | cut -f1)) thumb-$(du -h "$thumb" | cut -f1)"
    START=$((START + 1))
  done

echo "Done. Article banner: /photos/thumb-XX.jpg · inline: /photos/photo-XX.jpg"
