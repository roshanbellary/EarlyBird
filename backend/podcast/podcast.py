import os
from dotenv import load_dotenv
from agents.audio.audio_generation import PodcastAudioGenerator
from agents.pipeline import NewsPodcastPipeline

load_dotenv()  # Load environment variables from .env file

class PodcastRunner:
    def __init__(self):
        # Get the absolute path to the project root
        self.project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        # Define the output directory with 'backend' prefix
        self.output_dir = os.path.join(self.project_root, 'backend', 'podcast', 'agents', 'audio', 'finished_podcasts')
        # Create the directory if it doesn't exist
        os.makedirs(self.output_dir, exist_ok=True)
        
        self.pipeline = NewsPodcastPipeline(
            perplexity_api_key=os.getenv("PERPLEXITY_API_KEY"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            mistral_api_key=os.getenv("MISTRAL_API_KEY")
        )
        # Pass the output directory to PodcastAudioGenerator
        self.audio_generator = PodcastAudioGenerator(output_dir=self.output_dir)

    def run(self):
        script = self.pipeline.generate_podcast()
        print("Script generated, generating audio...")
        audio_path = self.audio_generator.generate_audio(script)
        print(f"Podcast saved to: {audio_path}")

if __name__ == "__main__":
    runner = PodcastRunner()
    runner.run()

