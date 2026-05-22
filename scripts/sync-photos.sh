#!/usr/bin/env bash
# Copy photos from local Instagram export into docs/public/photos/
# Usage: ./scripts/sync-photos.sh [count]
# Default source: ~/Downloads/Instagram/robert_le.ph

set -euo pipefail

SRC="${PHOTO_SRC:-$HOME/Downloads/Instagram/robert_le.ph}"
DEST="$(cd "$(dirname "$0")/.." && pwd)/docs/public/photos"
COUNT="${1:-12}"

if [[ ! -d "$SRC" ]]; then
  echo "Source not found: $SRC"
  echo "Set PHOTO_SRC to your image folder."
  exit 1
fi

mkdir -p "$DEST"

echo "Copying $COUNT images from $SRC to $DEST ..."

find "$SRC" -maxdepth 1 -type f \( -iname '*.jpg' -o -iname '*.jpeg' -o -iname '*.png' \) \
  -exec ls -l {} \; | sort -k5 -n | head -n "$COUNT" | awk '{print $NF}' | \
  while IFS= read -r file; do
    base=$(basename "$file")
    cp "$file" "$DEST/$base"
    echo "  $base"
  done

echo "Done. Reference in Markdown: /photos/filename.jpg"
