from flask import Flask, request, send_from_directory, jsonify
import os
import logging
from podcast.podcast import PodcastRunner
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# App configuration
class Config:
    PODCAST_DIR = os.getenv('PODCAST_DIR', 'podcast/finished_podcasts')
    DEBUG = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    PORT = int(os.getenv('FLASK_PORT', 5000))

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/", methods=["GET"])
def build():
    """Health check endpoint."""
    return jsonify({"message": "Podcast generation service is running"})

@app.route("/generate", methods=["POST"])
def generate():
    """Handles user request, generates a podcast, and returns the file URL."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON data"}), 400

        interests = data.get("interests", "")
        if not interests:
            return jsonify({"error": "Missing interests"}), 400

        runner = PodcastRunner()
        result = runner.run()

        if not isinstance(result, Dict):
            return jsonify({"error": "Invalid response from podcast runner"}), 500

        audio_path = result.get("audio_path")
        podcast_dir = result.get("podcast_dir")

        if not audio_path or not os.path.exists(audio_path):
            logger.error(f"Audio file not found at path: {audio_path}")
            return jsonify({"error": "Podcast generation failed"}), 500
    except Exception as e:
        print(e)

    filename = os.path.basename(audio_path)

    return jsonify({"file_url": f"/download/{filename}", "podcast_dir": podcast_dir})

@app.route("/download/<filename>")
def download(filename):
    """Serves the generated MP4 file."""
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

        full_path = os.path.join(podcast_dir, latest_podcast_dir)
        
        if not os.path.exists(os.path.join(full_path, filename)):
            logger.error(f"File not found: {filename}")
            return jsonify({"error": "File not found"}), 404

        return send_from_directory(full_path, filename, as_attachment=True)
    
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
        debug=app.config['DEBUG']
    )
