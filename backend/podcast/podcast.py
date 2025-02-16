from agents.pipeline import NewsPodcastPipeline
from audio.audio_generation import PodcastAudioGenerator
class PodcastRunner:
    def __init__(self):
        self.pipeline = NewsPodcastPipeline()
        self.audio_generator = PodcastAudioGenerator()

    def run(self):
        script = self.pipeline.generate_podcast()
        self.audio_generator.generate_audio(script)

if __name__ == "__main__":
    runner = PodcastRunner()
    runner.run()

