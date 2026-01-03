# Laravel Docker Animation - Setup & Run Guide

This is a Manim animation project that creates a 2-minute video explaining Laravel Docker setup in TikTok format (9:16 aspect ratio, 1080x1920).

## Prerequisites

- Python 3.8 or higher
- FFmpeg (for video rendering)

## Installation

A virtual environment has been created in the `docker` directory with all necessary dependencies.

### Activate the Virtual Environment

```bash
cd /Users/eric/code/Video/docker
source venv/bin/activate
```

### If You Need to Reinstall Dependencies

```bash
pip install -r requirements.txt
```

## Running the Animation

### Basic Render (720p, 30fps)
```bash
manim laravel_with_docker.py LaravelDockerStory
```

### High Quality Render (1080p, 60fps - as configured in the script)
```bash
manim laravel_with_docker.py LaravelDockerStory -pqh
```

### Low Quality Render (480p - for testing)
```bash
manim laravel_with_docker.py LaravelDockerStory -pql
```

## Command Options

- `-p` : Preview the video after rendering
- `-q` : Quality settings:
  - `-ql` : Low quality (480p)
  - `-qm` : Medium quality (720p)
  - `-qh` : High quality (1080p)
  - `-qk` : 4K quality
- `--save_last_frame` : Only save the last frame as an image
- `--disable_caching` : Disable caching (slower but ensures fresh render)

## Output Location

Rendered videos will be saved in:
```
/Users/eric/code/Video/docker/media/videos/laravel_with_docker/
```

## Project Structure

- `laravel_with_docker.py` - Main animation script
- `sounds/` - Audio files for sound effects
- `asset/` - Images and SVG files used in the animation
- `venv/` - Virtual environment (already set up)
- `requirements.txt` - Python dependencies

## Troubleshooting

### If you get "command not found: manim"
Make sure the virtual environment is activated:
```bash
source venv/bin/activate
```

### If assets are missing
The script will gracefully fall back to text/emoji if image files are not found in the `asset/` directory.

### If FFmpeg is not installed
Install FFmpeg using Homebrew:
```bash
brew install ffmpeg
```

## Deactivating the Virtual Environment

When you're done, deactivate the virtual environment:
```bash
deactivate
```
