import os
from dotenv import load_dotenv
from agents.audio.audio_generation import PodcastAudioGenerator
from agents.pipeline import NewsPodcastPipeline

load_dotenv()  # Load environment variables from .env file

class PodcastRunner:
    def __init__(self):
        self.pipeline = NewsPodcastPipeline(
            perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            mistral_api_key=os.getenv("MISTRAL_API_KEY")
        )
        self.audio_generator = PodcastAudioGenerator(
            api_key=os.getenv("ELEVENLABS_API_KEY")
        )

    def run(self):
        script = self.pipeline.generate_podcast()
        print("Script generated, generating audio...")
        self.audio_generator.generate_audio(script)

if __name__ == "__main__":
    runner = PodcastRunner()
    runner.run()

