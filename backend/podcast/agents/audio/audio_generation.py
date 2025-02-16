#!/usr/bin/env python3

import os
import re
import sys
import uuid
from pydub import AudioSegment
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

class PodcastAudioGenerator:
    def __init__(self):
        self.ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_KEY")
        if not self.ELEVENLABS_API_KEY:
            raise ValueError("Please set the ELEVENLABS_KEY environment variable.")

        # Map speaker names to voice IDs
        self.SPEAKER_VOICES = {
            "host": "9BWtsMINqrJLrRacOk9x",   # Aria
            "expert": "CwhRBWXzGAHq8TQ4Fs17"  # Roger
        }

        # Initialize the ElevenLabs client
        self.client = ElevenLabs(api_key=self.ELEVENLABS_API_KEY)
        
        # Create audio files directory if it doesn't exist
        self.audio_dir = os.path.join('backend', 'podcast', 'agents', 'audio', 'audio_files')
        os.makedirs(self.audio_dir, exist_ok=True)

    def text_to_speech_file(self, text: str, voice_id: str) -> str:
        """Converts text to speech using ElevenLabs with the specified voice, saves to an MP3 file."""
        response = self.client.text_to_speech.convert(
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
        temp_file_path = os.path.join(self.audio_dir, f"{uuid.uuid4()}.mp3")
        with open(temp_file_path, "wb") as f:
            for chunk in response:
                if chunk:
                    f.write(chunk)
        return temp_file_path

    def generate_audio(self, script: str) -> str:
        """
        Generates audio from a script with XML-like tags.
        Returns the path to the generated audio file.
        """
        # Create a unique filename for the final podcast
        timestamp = uuid.uuid4()
        output_file = os.path.join(self.audio_dir, f"podcast_{timestamp}.mp3")

        # Split by tags and process each section
        clips = []
        parts = re.findall(r'<(HOST|EXPERT)>\s*(.*?)\s*</\1>', script, re.DOTALL)
        
        if not parts:
            raise ValueError("No valid script sections found")

        try:
            for speaker, text in parts:
                speaker = speaker.lower()
                # Get the voice ID for the speaker, or default to host if missing
                voice_id = self.SPEAKER_VOICES.get(speaker, self.SPEAKER_VOICES["host"])
                print(f"Converting for {speaker}: {text[:100]}...")  # Print first 100 chars
                mp3_path = self.text_to_speech_file(text, voice_id)
                clips.append(mp3_path)

            # Combine all clips into one final MP3
            final_audio = AudioSegment.empty()
            for clip in clips:
                final_audio += AudioSegment.from_mp3(clip)
                os.remove(clip)  # Clean up temporary files

            final_audio.export(output_file, format="mp3")
            print(f"Merged podcast saved to {output_file}")
            return output_file

        except Exception as e:
            # Clean up any temporary files in case of error
            for clip in clips:
                if os.path.exists(clip):
                    os.remove(clip)
            raise e

if __name__ == "__main__":
    # Example usage
    generator = PodcastAudioGenerator()
    script = """
    <HOST>Welcome to our podcast!</HOST>
    <EXPERT>Thank you for having me.</EXPERT>
    """
    generator.generate_audio(script)