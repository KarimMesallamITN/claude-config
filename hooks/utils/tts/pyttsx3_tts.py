#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyttsx3",
# ]
# ///

import sys
import random

def main():
    """
    pyttsx3 TTS Script
    
    Uses pyttsx3 for offline text-to-speech synthesis.
    Accepts optional text prompt as command-line argument.
    
    Usage:
    - ./pyttsx3_tts.py                    # Uses default text
    - ./pyttsx3_tts.py "Your custom text" # Uses provided text
    
    Features:
    - Offline TTS (no API key required)
    - Cross-platform compatibility
    - Configurable voice settings
    - Immediate audio playback
    """
    
    # Get text first
    import sys
    if len(sys.argv) > 1:
        text = " ".join(sys.argv[1:])  # Join all arguments as text
    else:
        # Read from stdin if no arguments
        text = sys.stdin.read().strip()
        if not text:
            # Default completion messages
            completion_messages = [
                "Work complete!",
                "All done!",
                "Task finished!",
                "Job complete!",
                "Ready for next task!"
            ]
            text = random.choice(completion_messages)
    
    # Try espeak directly first (more reliable on Linux)
    try:
        import subprocess
        
        print("🎙️  espeak TTS (free)")
        print("=" * 18)
        print(f"🎯 Text: {text}")
        print("🔊 Speaking...")
        
        # Use espeak directly with good settings
        subprocess.run(["espeak", "-s", "180", "-a", "80", text], check=True)
        
        print("✅ Playback complete!")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to pyttsx3 if espeak fails
        print("⚠️  espeak failed, trying pyttsx3...")
        
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            engine.setProperty('rate', 180)
            engine.setProperty('volume', 0.8)
            
            print("🎙️  pyttsx3 TTS")
            print("=" * 15)
            print(f"🎯 Text: {text}")
            print("🔊 Speaking...")
            
            engine.say(text)
            engine.runAndWait()
            
            print("✅ Playback complete!")
            
        except Exception as e:
            print(f"❌ Both espeak and pyttsx3 failed: {e}")
            sys.exit(1)

    except ImportError:
        print("❌ Error: Required packages not available")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()