#!/bin/bash
# Remotion Video Generator
# Usage: generate.sh --title "标题" --content "内容" --output video.mp4

set -e

# Default values
TITLE=""
CONTENT=""
ARTICLE=""
OUTPUT="out/video.mp4"
FORMAT="vertical"
DURATION=5
COVER=""
WORKSPACE="$HOME/.openclaw/workspace"
REMOTION_DIR="$WORKSPACE/remotion/generated-video"

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --title)
      TITLE="$2"
      shift 2
      ;;
    --content)
      CONTENT="$2"
      shift 2
      ;;
    --article)
      ARTICLE="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --format)
      FORMAT="$2"
      shift 2
      ;;
    --duration)
      DURATION="$2"
      shift 2
      ;;
    --cover)
      COVER="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required arguments
if [ -z "$TITLE" ] && [ -z "$ARTICLE" ]; then
  echo "Error: --title or --article is required"
  exit 1
fi

# If article is provided, extract title and content
if [ -n "$ARTICLE" ] && [ -f "$ARTICLE" ]; then
  echo "📖 Reading article: $ARTICLE"
  # Extract title from first # heading
  TITLE=$(grep -m 1 "^# " "$ARTICLE" | sed 's/^# //')
  # Extract content (first few paragraphs)
  CONTENT=$(grep -v "^#" "$ARTICLE" | grep -v "^$" | head -20 | tr '\n' '|')
fi

echo "🎬 Generating video..."
echo "   Title: $TITLE"
echo "   Format: $FORMAT"
echo "   Output: $OUTPUT"

# Create Remotion project
mkdir -p "$REMOTION_DIR"/{src,public,out}

# Copy cover image if provided
if [ -n "$COVER" ] && [ -f "$COVER" ]; then
  cp "$COVER" "$REMOTION_DIR/public/cover.jpg"
fi

# Generate video component (simplified)
# In production, this would use a proper template
cat > "$REMOTION_DIR/src/Video.tsx" << 'VIDEO_EOF'
import React from 'react';
import { AbsoluteFill, Sequence, interpolate, useCurrentFrame } from 'remotion';

// Generated video component
VIDEO_EOF

# Generate package.json
cat > "$REMOTION_DIR/package.json" << PKG_EOF
{
  "name": "generated-video",
  "version": "1.0.0",
  "scripts": {
    "render": "remotion render src/index.ts GeneratedVideo out/video.mp4 --browser-executable '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'"
  },
  "dependencies": {
    "@remotion/cli": "^4.0.0",
    "@remotion/player": "^4.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "remotion": "^4.0.0"
  }
}
PKG_EOF

# Install dependencies if needed
if [ ! -d "$REMOTION_DIR/node_modules" ]; then
  echo "📦 Installing dependencies..."
  cd "$REMOTION_DIR" && npm install
fi

# Render video
echo "🎥 Rendering video..."
cd "$REMOTION_DIR"
npm run render

# Copy to output location
mkdir -p "$(dirname "$OUTPUT")"
cp "$REMOTION_DIR/out/video.mp4" "$OUTPUT"

echo "✅ Video generated: $OUTPUT"
ls -lh "$OUTPUT"
