#!/usr/bin/env python3

import os
import re
import sys
import uuid
from pydub import AudioSegment
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_KEY")
if not ELEVENLABS_API_KEY:
    print("Please set the ELEVENLABS_API_KEY environment variable.")
    sys.exit(1)

# Map speaker names to voice IDs
# Update these to your desired ElevenLabs voice IDs
SPEAKER_VOICES = {
    "host": "9BWtsMINqrJLrRacOk9x",   # Aria
    "expert": "CwhRBWXzGAHq8TQ4Fs17" # Roger
}

# Initialize the ElevenLabs client
client = ElevenLabs(api_key=ELEVENLABS_API_KEY)

def text_to_speech_file(text: str, voice_id: str) -> str:
    """Converts text to speech using ElevenLabs with the specified voice, saves to an MP3 file."""
    response = client.text_to_speech.convert(
        voice_id=voice_id,
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_turbo_v2_5",  # Low latency model
        voice_settings=VoiceSettings(
            stability=0.0,
            similarity_boost=1.0,
            style=0.0,
            use_speaker_boost=True,
        ),
    )
    file_path = f"{uuid.uuid4()}.mp3"
    with open(file_path, "wb") as f:
        for chunk in response:
            if chunk:
                f.write(chunk)
    return file_path

def generate_podcast_audio(transcript_file: str, output_file: str):
    """Reads a transcript with XML-like tags, converts to TTS, and merges all clips."""
    with open(transcript_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Split by tags and process each section
    clips = []
    parts = re.findall(r'<(HOST|EXPERT)>\s*(.*?)\s*</\1>', content, re.DOTALL)
    
    for speaker, text in parts:
        speaker = speaker.lower()
        # Get the voice ID for the speaker, or default to host if missing
        voice_id = SPEAKER_VOICES.get(speaker, SPEAKER_VOICES["host"])
        print(f"Converting for {speaker}: {text}")
        mp3_path = text_to_speech_file(text, voice_id)
        clips.append(mp3_path)

    # Combine all clips into one final MP3
    if not clips:
        print("No audio clips created.")
        return

    final_audio = AudioSegment.empty()
    for clip in clips:
        final_audio += AudioSegment.from_mp3(clip)
        os.remove(clip)  # Clean up temporary files

    final_audio.export(output_file, format="mp3")
    print(f"Merged podcast saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python audio_generation.py <transcript_file> <output_file>")
        sys.exit(1)

    transcript_path = sys.argv[1]
    output_path = sys.argv[2]

    generate_podcast_audio(transcript_path, output_path)