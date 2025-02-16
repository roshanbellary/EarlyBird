import sys 
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
import logging
from podcast import PodcastRunner
from podcast.agents.pipeline import NewsPodcastPipeline
from typing import Dict, Any
import json
<<<<<<< HEAD

from global_instances import rl_model, graph

=======
>>>>>>> afff0e1fa6a1c14c0104a1de41bac770724c91c1
import whisper
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
CORS(app)
app.config.from_object(Config)

@app.route("/", methods=["GET"])
def build():
    """Health check endpoint."""
    return jsonify({"message": "Podcast generation service is running"})

@app.route("/generate", methods=["POST"])  # Ensure it's POST method
def generate():
    """Handles user request, generates a podcast, and returns the file URL."""
    try:
        # data = request.get_json()
        # if not data:
        #     return jsonify({"error": "Invalid JSON data"}), 400

        # interests = data.get("interests", "")
        # logger.info(f"Received interests: {interests}")  # Log interests to see them

        # if not interests:
        #     logger.error(f"Missing interests: {interests}")
        #     return jsonify({"error": "Missing interests"}), 400
        
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
        
        for audio_path_instance in audio_path:
            if audio_path_instance is None or not os.path.exists(audio_path_instance):
                logger.error(f"Audio file not found at path: {audio_path_instance}")
                return jsonify({"error": "Podcast generation failed"}), 500

    except Exception as e:
        logger.exception(f"Error in /generate route: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

    try:
        if audio_path:  # Ensure audio_path is not None
            filenames = os.path.basename(podcast_dir)
            return jsonify({"file_urls": filenames, "podcast_dir": podcast_dir, "transcript_path": transcript_path}), 200
        else:
            logger.error("Audio path is not set.")
            return jsonify({"error": "Internal server error"}), 500
    except Exception as e:
        logger.exception(f"Error serving file {filenames}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500


@app.route("/download/<filename>/<num>", methods=["GET"])
def download(filename, num = 1):
    """Serves the generated MP3 file from the podcast directory."""
    try:
        # Using configured podcast directory
        podcast_dir = app.config['PODCAST_DIR']
        if not os.path.exists(podcast_dir):
            logger.error(f"Podcast directory not found: {podcast_dir}")
            return jsonify({"error": "Podcast directory not found"}), 500
        
        # Build the full path to the MP3 file
        podcast_audio_path = os.path.join(podcast_dir, filename, f"interaction_{num}.mp3")
        logger.info(f"Podcast audio path: {podcast_audio_path}")
        if not os.path.exists(podcast_audio_path):
            logger.error(f"Audio file not found: {podcast_audio_path}")
            return jsonify({"error": "File not found"}), 404

        # Serve the file
        return send_from_directory(os.path.dirname(podcast_audio_path), os.path.basename(podcast_audio_path), as_attachment=True)
    
    except Exception as e:
        logger.error(f"Error serving file {filename}: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500
@app.route("/get/transcripts", methods=["GET"])
def get_all_transcript_files():
    """Returns a list of all transcript files and their metadata."""
    try:
        podcast_dir = app.config['PODCAST_DIR']
        metadata_file_path = os.path.join(podcast_dir, "podcast_metadata.json")
        
        if not os.path.exists(metadata_file_path):
            logger.error(f"Metadata file not found: {metadata_file_path}")
            return jsonify({"error": "Metadata file not found"}), 404
        
        with open(metadata_file_path, 'r') as f:
            metadata = json.load(f)
            return jsonify({"metadata": metadata}), 200
    except Exception as e:
        logger.error(f"Error retrieving transcripts: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

<<<<<<< HEAD
@app.route("/api/graph_data/<mode>", methods=["GET"])
def get_3d_graph(mode, selected_point=None):
    # if mode == 'init':
    #     graph.generate_init_nodes()
    #     graph.update_interest_scores()
    # elif mode == 'update':
    #     graph.update_rl_model(selected_point[0], selected_point[1], selected_point[2])
    #     graph.update_interest_scores()

    # nodes = []
    # for i in range(len(graph.nodes)):
    #     nodes.append({'id': i, 'position': graph.nodes[i].embedding_3d})
    # print(nodes)
    nodes = [{'id': 1, 'position': [0, 0, 0]}]

    # Return JSON in a format convenient for your frontend
    return jsonify({"nodes": nodes, "edges": []})
=======
>>>>>>> afff0e1fa6a1c14c0104a1de41bac770724c91c1
@app.route("/interrupt", methods=["POST"])
def get_response():
    """Transcribes the audio blob and returns an expert response."""
    try:
        if 'audio' not in request.files:
            logger.error("No audio file part in the request")
            return jsonify({"error": "No audio file part in the request"}), 400
        
        audio_file = request.files['audio']
        file_path = request.form.get('file_path')
        if audio_file.filename == '':
            logger.error("No selected file")
            return jsonify({"error": "No selected file"}), 400
        
        # Save the audio file temporarily
        temp_audio_path = os.path.join(app.config['PODCAST_DIR'], "temp_audio.wav")
        audio_file.save(temp_audio_path)
        
        # Use Whisper to transcribe the audio file
        model = whisper.load_model("base")
        result = model.transcribe(temp_audio_path)
        transcription = result["text"]
        logger.info(f"Transcription: {transcription}")
        logger.info(f"File path: {file_path}")
        # Call the response function to generate an expert response
        pipeline = NewsPodcastPipeline()
        interrupt_path = pipeline.user_ask_expert(question=transcription, filepath=file_path)
        logger.info(f"Expert response: {interrupt_path}")
        
        # Clean up the temporary audio file
        os.remove(temp_audio_path)
        
        return jsonify({"response": interrupt_path}), 200
    except Exception as e:
        logger.error(f"Error processing audio file: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

def generate_expert_response(transcription: str) -> str:
    """Generates an expert response based on the transcription."""
    # Placeholder function - replace with actual implementation
    return f"Expert response to: {transcription}"

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
