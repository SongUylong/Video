# Manim Audio Guide 🔊

## Overview

Manim supports adding audio directly to scenes through:

1. **Background music** - Continuous audio throughout the scene
2. **Sound effects** - Short sounds synced with animations
3. **Voiceover** - Narration (using manim-voiceover plugin)

## Method 1: Using `self.add_sound()`

The simplest way to add sounds is using `self.add_sound()`:

```python
# Play a sound effect at the current time
self.add_sound("path/to/sound.mp3")

# With gain control (volume)
self.add_sound("path/to/sound.wav", gain=-10)  # Reduce by 10dB
```

### Example: Syncing with Animations

```python
# Whoosh sound when object moves
self.play(obj.animate.shift(RIGHT*3))
self.add_sound("sounds/whoosh.mp3")

# Pop sound when object appears
self.add_sound("sounds/pop.wav")
self.play(FadeIn(circle))

# Multiple sounds for sequence
self.add_sound("sounds/beep1.wav")
self.play(Write(text1))
self.add_sound("sounds/beep2.wav")
self.play(Write(text2))
```

## Method 2: Background Music

For continuous background music:

```python
def construct(self):
    # Add background music at start
    self.add_sound("music/background.mp3", gain=-15)

    # Your animations here
    self.play(...)
```

## Method 3: Using AudioSegment for Precise Timing

For more control, use AudioSegment:

```python
from pydub import AudioSegment

def construct(self):
    # Load sound
    sound = AudioSegment.from_mp3("sound.mp3")

    # Adjust volume
    sound = sound - 10  # Reduce 10dB

    # Export and use
    sound.export("temp_sound.wav", format="wav")
    self.add_sound("temp_sound.wav")
```

## Where to Get Sound Effects

### Free Sound Libraries:

1. **Freesound.org** - https://freesound.org/
2. **Zapsplat** - https://www.zapsplat.com/
3. **Mixkit** - https://mixkit.co/free-sound-effects/
4. **YouTube Audio Library** - Free sounds from YouTube Studio

### Recommended Sounds for Animations:

- **Whoosh** - Object movements, transitions
- **Pop/Click** - Objects appearing
- **Beep/Blip** - UI elements, text
- **Swoosh** - Fast transitions
- **Success Chime** - Checkmarks, completions
- **Error Buzz** - X marks, failures
- **Digital/Tech** - Code, tech concepts
- **Ambient** - Background atmosphere

## Audio File Formats

Manim supports:

- `.mp3` - Most common, good compression
- `.wav` - Uncompressed, best quality
- `.ogg` - Good alternative to mp3

**Tip:** Use `.wav` for short sound effects (better sync), `.mp3` for music.

## Volume Control Best Practices

```python
# Background music should be quieter
self.add_sound("music.mp3", gain=-20)

# Sound effects can be louder
self.add_sound("pop.wav", gain=-5)

# Very subtle ambient
self.add_sound("ambient.mp3", gain=-30)
```

## Timing Tips

1. **Simultaneous with animation:**

```python
self.add_sound("sound.wav")
self.play(animation)  # Starts at same time
```

2. **Sound during animation:**

```python
self.play(animation, run_time=2)
# Sound plays after animation starts
```

3. **Sound before animation:**

```python
self.add_sound("sound.wav")
self.wait(0.5)  # Let sound play a bit
self.play(animation)
```

## Common Patterns for Docker Animation

```python
# Logo appears - magical chime
self.add_sound("sounds/magic_chime.wav")
self.play(FadeIn(docker_logo, scale=0.5))

# Container builds - tech beep
self.add_sound("sounds/tech_beep.wav")
self.play(GrowFromCenter(container))

# Data transfer - whoosh
self.add_sound("sounds/data_whoosh.mp3")
self.play(obj.animate.move_to(target))

# Success - ding
self.add_sound("sounds/success_ding.wav")
self.play(FadeIn(checkmark))

# Failure - buzz
self.add_sound("sounds/error_buzz.wav")
self.play(FadeIn(x_mark))
```

## Rendering with Audio

No special flags needed - just render normally:

```bash
manim -pql scene.py SceneName  # Audio automatically included
```

## Troubleshooting

### Audio not playing in video:

- Check file path is correct
- Ensure audio file format is supported
- Try converting to `.wav` for best compatibility

### Audio out of sync:

- Use `self.wait()` to adjust timing
- Check that `run_time` in animations matches expected timing
- Consider using shorter, punchier sound effects

### Audio too loud/quiet:

- Adjust `gain` parameter (in dB)
- Negative values reduce volume
- Typical range: -30 to 0 dB

## Advanced: Creating Sound Directory Structure

```
video/
├── sounds/
│   ├── ui/
│   │   ├── pop.wav
│   │   ├── click.wav
│   │   └── beep.wav
│   ├── transitions/
│   │   ├── whoosh.wav
│   │   └── swoosh.wav
│   ├── feedback/
│   │   ├── success.wav
│   │   └── error.wav
│   └── music/
│       └── background.mp3
└── scene/
    └── your_scene.py
```

Then in your code:

```python
SOUND_DIR = "sounds/"

self.add_sound(f"{SOUND_DIR}ui/pop.wav")
self.add_sound(f"{SOUND_DIR}feedback/success.wav")
```
