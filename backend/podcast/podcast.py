from agents.pipeline import NewsPodcastPipeline
from audio.audio_generation import PodcastAudioGenerator
class PodcastRunner:
    def __init__(self):
        self.pipeline = NewsPodcastPipeline()
        self.audio_generator = PodcastAudioGenerator()

    def run(self):
        scripts = self.pipeline.generate_podcast()
        for script in scripts:
            self.audio_generator.generate_audio(script["scripts"])

if __name__ == "__main__":
    runner = PodcastRunner()
    runner.run()

