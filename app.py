import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
from utils.youtube import get_video_transcript
from utils.summarizer import generate_summary

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_video():
    try:
        youtube_url = request.form.get('youtube_url')
        if not youtube_url:
            return jsonify({'error': 'Please provide a YouTube URL'}), 400

        # Get video transcript
        transcript = get_video_transcript(youtube_url)
        if not transcript:
            return jsonify({'error': 'Could not extract transcript from the video'}), 400

        # Generate summary
        summary = generate_summary(transcript)

        return jsonify({
            'success': True,
            'transcript': transcript,
            'summary': summary
        })

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/download-transcript', methods=['POST'])
def download_transcript():
    try:
        transcript = request.form.get('transcript')
        if not transcript:
            return jsonify({'error': 'No transcript provided'}), 400

        # Create a binary buffer for the file
        buffer = BytesIO()
        buffer.write(transcript.encode('utf-8'))
        buffer.seek(0)

        logger.debug("Sending transcript file for download")
        return send_file(
            buffer,
            mimetype='text/plain',
            as_attachment=True,
            download_name='transcript.txt'
        )

    except Exception as e:
        logger.error(f"Error downloading transcript: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)