#!/usr/bin/env python3
"""
Interactive Mixkit Sound Browser & Downloader
This script helps you browse and download sound effects from Mixkit
"""

import os
import requests
from pathlib import Path
import json

# Curated list of Mixkit sound effect IDs (these are more reliable)
# Format: {filename: mixkit_id}
RECOMMENDED_SOUNDS = {
    # These IDs are from Mixkit's free sound effects library
    # Visit https://mixkit.co/free-sound-effects/ to browse more
    
    # UI Sounds
    "pop.wav": 2568,           # Pop
    "click.wav": 2997,         # Modern click
    "button.wav": 2013,        # Button click
    
    # Whoosh/Transitions  
    "whoosh.wav": 2573,        # Fast whoosh
    "swoosh.wav": 1354,        # Swoosh
    
    # Success/Positive
    "success.wav": 2000,       # Success notification
    "success_bell.wav": 2001,  # Success bell
    "achievement.wav": 2018,   # Achievement
    
    # Error/Negative
    "error.wav": 2577,         # Error buzz
    "buzzer.wav": 2003,        # Buzzer
    
    # Tech/Digital
    "tech_beep.wav": 2869,     # Tech beep
    "digital_pop.wav": 2019,   # Digital pop
    "robot_beep.wav": 2533,    # Robot beep
    
    # Processing/Build
    "build.wav": 2570,         # Processing
    "processing.wav": 2869,    # Tech processing
    
    # Magic/Special
    "magic.wav": 2018,         # Magic chime
    "sparkle.wav": 2000,       # Sparkle
    
    # Writing/Typing
    "write.wav": 2585,         # Write
    "keyboard.wav": 2589,      # Keyboard
    
    # Data Transfer
    "upload.wav": 2869,        # Upload beep
    "download.wav": 2585,      # Download
    "transfer.wav": 2570,      # Data transfer
}

def download_mixkit_sound(sound_id, destination):
    """
    Download a sound from Mixkit using its ID
    Mixkit sound URLs follow the pattern:
    https://assets.mixkit.co/active_storage/sfx/{id}/{id}.wav
    """
    url = f"https://assets.mixkit.co/active_storage/sfx/{sound_id}/{sound_id}.wav"
    
    try:
        print(f"  → {destination.name} (ID: {sound_id})...", end=" ")
        
        # Try with headers to avoid 403 errors
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
            'Referer': 'https://mixkit.co/'
        }
        
        response = requests.get(url, stream=True, timeout=30, headers=headers)
        response.raise_for_status()
        
        # Create parent directory if needed
        destination.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        size_kb = destination.stat().st_size // 1024
        print(f"✓ ({size_kb} KB)")
        return True
        
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(f"✗ (Access denied - try downloading manually from mixkit.co)")
        else:
            print(f"✗ (HTTP {e.response.status_code})")
        return False
    except Exception as e:
        print(f"✗ ({str(e)[:50]})")
        return False

def download_essential_sounds():
    """Download essential sounds for the Docker animation"""
    script_dir = Path(__file__).parent
    sounds_dir = script_dir / "sounds"
    sounds_dir.mkdir(exist_ok=True)
    
    essential = {
        "pop.wav": 2568,
        "whoosh.wav": 2573,
        "success.wav": 2000,
        "error.wav": 2577,
        "tech_beep.wav": 2869,
        "build.wav": 2570,
        "magic.wav": 2018,
        "write.wav": 2585,
        "click.wav": 2997,
    }
    
    print("\n" + "="*60)
    print("Essential Sounds for Docker Animation")
    print("="*60)
    
    success_count = 0
    for filename, sound_id in essential.items():
        destination = sounds_dir / filename
        if download_mixkit_sound(sound_id, destination):
            success_count += 1
    
    return success_count, len(essential)

def download_all_sounds():
    """Download all recommended sounds"""
    script_dir = Path(__file__).parent
    sounds_dir = script_dir / "sounds"
    sounds_dir.mkdir(exist_ok=True)
    
    print("\n" + "="*60)
    print("Downloading All Recommended Sounds")
    print("="*60)
    
    success_count = 0
    for filename, sound_id in RECOMMENDED_SOUNDS.items():
        destination = sounds_dir / filename
        if download_mixkit_sound(sound_id, destination):
            success_count += 1
    
    return success_count, len(RECOMMENDED_SOUNDS)

def list_downloaded_sounds():
    """List all sounds currently downloaded"""
    script_dir = Path(__file__).parent
    sounds_dir = script_dir / "sounds"
    
    if not sounds_dir.exists():
        print("No sounds directory found.")
        return
    
    sound_files = list(sounds_dir.glob("*.wav")) + list(sounds_dir.glob("*.mp3"))
    
    if not sound_files:
        print("No sound files found.")
        return
    
    print("\n" + "="*60)
    print(f"Downloaded Sounds ({len(sound_files)} files)")
    print("="*60)
    
    for sound_file in sorted(sound_files):
        size_kb = sound_file.stat().st_size // 1024
        print(f"  ✓ {sound_file.name} ({size_kb} KB)")

def create_sound_map():
    """Create a reference file mapping sound purposes"""
    script_dir = Path(__file__).parent
    sounds_dir = script_dir / "sounds"
    
    sound_map = {
        "UI & Interactions": ["pop.wav", "click.wav", "button.wav"],
        "Transitions": ["whoosh.wav", "swoosh.wav"],
        "Success/Positive": ["success.wav", "success_bell.wav", "achievement.wav"],
        "Error/Negative": ["error.wav", "buzzer.wav"],
        "Tech/Digital": ["tech_beep.wav", "digital_pop.wav", "robot_beep.wav"],
        "Processing/Building": ["build.wav", "processing.wav"],
        "Magic/Special": ["magic.wav", "sparkle.wav"],
        "Writing/Typing": ["write.wav", "keyboard.wav"],
        "Data Transfer": ["upload.wav", "download.wav", "transfer.wav"]
    }
    
    readme_path = sounds_dir / "README.md"
    with open(readme_path, 'w') as f:
        f.write("# Sound Effects Reference\n\n")
        f.write("This directory contains sound effects for Manim animations.\n\n")
        f.write("## Sound Categories\n\n")
        
        for category, sounds in sound_map.items():
            f.write(f"### {category}\n")
            for sound in sounds:
                f.write(f"- `{sound}`\n")
            f.write("\n")
        
        f.write("## Source\n")
        f.write("All sounds from [Mixkit](https://mixkit.co/free-sound-effects/)\n")
        f.write("Licensed under Mixkit Sound Effects Free License\n\n")
        f.write("## Usage in Manim\n\n")
        f.write("```python\n")
        f.write('self.add_sound("sounds/pop.wav", gain=-10)\n')
        f.write("```\n")
    
    print(f"\n✓ Created sound reference: {readme_path}")

def main():
    print("="*60)
    print("Mixkit Sound Effects Downloader for Manim")
    print("="*60)
    print("\nOptions:")
    print("  1. Download essential sounds (9 files)")
    print("  2. Download all recommended sounds (20+ files)")
    print("  3. List downloaded sounds")
    print("  4. Exit")
    
    choice = input("\nEnter choice (1-4) [default: 1]: ").strip() or "1"
    
    if choice == "1":
        success, total = download_essential_sounds()
        create_sound_map()
        list_downloaded_sounds()
        
        print("\n" + "="*60)
        print(f"Download Complete: {success}/{total} sounds")
        print("="*60)
        print("\n✓ Ready to use! Run your animation with:")
        print("  manim -pql docker/docker_with_audio.py DockerTikTokWithAudio")
        
    elif choice == "2":
        success, total = download_all_sounds()
        create_sound_map()
        list_downloaded_sounds()
        
        print("\n" + "="*60)
        print(f"Download Complete: {success}/{total} sounds")
        print("="*60)
        
    elif choice == "3":
        list_downloaded_sounds()
        
    else:
        print("Exiting...")

if __name__ == "__main__":
    main()
