#!/bin/bash

# Manim Media Cleaner Script
# This script removes all intermediate files and keeps only the final output videos

echo "🧹 Cleaning Manim media files..."

# Remove partial movie files (intermediate render files)
if [ -d "media/videos" ]; then
    echo "Removing partial movie files..."
    find media/videos -type d -name "partial_movie_files" -exec rm -rf {} + 2>/dev/null
    echo "✓ Partial movie files removed"
fi

if [ -d "videos/partial_movie_files" ]; then
    echo "Removing videos/partial_movie_files..."
    rm -rf videos/partial_movie_files
    echo "✓ Videos partial files removed"
fi

# Remove text/image cache files
if [ -d "media/texts" ]; then
    echo "Removing text cache files..."
    rm -rf media/texts
    echo "✓ Text cache removed"
fi

# Remove temp files
if [ -d "videos/temp_files" ]; then
    echo "Removing temp files..."
    rm -rf videos/temp_files
    echo "✓ Temp files removed"
fi

# Remove Python cache
if [ -d "__pycache__" ]; then
    echo "Removing Python cache..."
    rm -rf __pycache__
    echo "✓ Python cache removed"
fi

echo ""
echo "✨ Cleanup complete!"
echo ""

# Create video folder in the current directory if it doesn't exist
echo "Creating video output folder..."
mkdir -p video

# Move final videos to video folder
echo "Moving final videos to video folder..."
final_videos=$(find media/videos -type f -name "*.mp4" ! -path "*/partial_movie_files/*" 2>/dev/null)

if [ -z "$final_videos" ]; then
    echo "⚠ No final videos found!"
else
    echo "$final_videos" | while read video; do
        # Get the filename only (without path)
        filename=$(basename "$video")
        echo "  Moving: $filename"
        mv "$video" "video/$filename"
    done
    echo "✓ Videos moved to video/"
fi

echo ""
echo "Final videos are now located in:"
ls -lh video/*.mp4 2>/dev/null || echo "No videos found in video/"

echo ""
echo "Total final video files: $(ls -1 video/*.mp4 2>/dev/null | wc -l)"
