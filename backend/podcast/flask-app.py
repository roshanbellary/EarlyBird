from flask import Flask, request, send_from_directory, jsonify
import os
import logging
from podcast import PodcastRunner
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# App configuration
class Config:
    PODCAST_DIR = os.getenv('PODCAST_DIR', 'finished_podcasts/')
    DEBUG = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 8000))

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/", methods=["GET"])
def build():
    """Health check endpoint."""
    return jsonify({"message": "Podcast generation service is running"})

@app.route("/generate", methods=["POST"])  # Ensure it's POST method
def generate():
    """Handles user request, generates a podcast, and returns the file URL."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        interests = data.get("interests", "")
        logger.info(f"Received interests: {interests}")  # Log interests to see them

        if not interests:
            logger.error(f"Missing interests: {interests}")
            return jsonify({"error": "Missing interests"}), 400
        
        runner = PodcastRunner()
        logger.info("Running the podcast runner")
        result = runner.run()
        logger.info(f"PodcastRunner result: {result}")  # Log the full result to inspect it
        
        if result is None or not isinstance(result, Dict):
            logger.error(f"Invalid response from podcast runner: {result}")
            return jsonify({"error": "Invalid response from podcast runner"}), 500

        audio_path = result.get("audio_path")
        podcast_dir = result.get("podcast_dir")
        transcript_path = result.get("transcript_path")

        if audio_path is None or not os.path.exists(audio_path):
            logger.error(f"Audio file not found at path: {audio_path}")
            return jsonify({"error": "Podcast generation failed"}), 500

    except Exception as e:
        logger.exception(f"Error in /generate route: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    try:
        if audio_path:  # Ensure audio_path is not None
            filename = os.path.basename(audio_path)
            return jsonify({"file_url": f"/download/{filename}", "podcast_dir": podcast_dir, "transcript_path": transcript_path})
        else:
            logger.error("Audio path is not set.")
            return jsonify({"error": "Internal server error"}), 500
    except Exception as e:
        logger.exception(f"Error serving file {filename}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/download/<filename>", methods=["GET"])
def download(filename):
    """Serves the generated MP3 file from the podcast directory."""
    try:
        # Using configured podcast directory
        podcast_dir = app.config['PODCAST_DIR']
        if not os.path.exists(podcast_dir):
            logger.error(f"Podcast directory not found: {podcast_dir}")
            return jsonify({"error": "Podcast directory not found"}), 500

        # Get the latest podcast directory
        try:
            latest_podcast_dir = sorted(
                [d for d in os.listdir(podcast_dir) if os.path.isdir(os.path.join(podcast_dir, d))],
                reverse=True
            )[0]
        except (IndexError, FileNotFoundError) as e:
            logger.error(f"Error finding latest podcast directory: {str(e)}")
            return jsonify({"error": "No podcast directories found"}), 404

        # Build the full path to the MP3 file
        podcast_audio_path = os.path.join(podcast_dir, latest_podcast_dir, f"podcast_audio.mp3")
        logger.info(f"Podcast audio path: {podcast_audio_path}")
        if not os.path.exists(podcast_audio_path):
            logger.error(f"Audio file not found: {podcast_audio_path}")
            return jsonify({"error": "File not found"}), 404

        # Serve the file
        return send_from_directory(os.path.join(podcast_dir, latest_podcast_dir), f"podcast_audio.mp3", as_attachment=True)
    
    except Exception as e:
        logger.error(f"Error serving file {filename}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(Exception)
def handle_error(error):
    """Global error handler for all exceptions."""
    logger.error(f"Unhandled error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=True
    )
