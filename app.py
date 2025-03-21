import os
import logging
from flask import Flask, render_template, request, jsonify, send_file
from io import BytesIO
from utils.youtube import get_video_transcript, get_video_info
from utils.summarizer import generate_summary
from models import VideoHistory
from db import db

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# create the app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# configure the database
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_recycle": 300,
    "pool_pre_ping": True,
}

# initialize the app with the extension
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Get the last 5 processed videos
    history = VideoHistory.query.order_by(VideoHistory.created_at.desc()).limit(5).all()
    return render_template('index.html', history=history)

@app.route('/process', methods=['POST'])
def process_video():
    try:
        youtube_url = request.form.get('youtube_url')
        summary_length = request.form.get('summary_length', 'medium')

        if not youtube_url:
            return jsonify({'error': 'Please provide a YouTube URL'}), 400

        # Get video information
        video_info = get_video_info(youtube_url)

        # Get video transcript
        transcript = get_video_transcript(youtube_url)
        if not transcript:
            return jsonify({'error': 'Could not extract transcript from the video'}), 400

        # Generate summary
        summary = generate_summary(transcript, summary_length)

        # Save to history
        history = VideoHistory(
            video_url=youtube_url,
            video_title=video_info['title'],
            video_duration=video_info['duration'],
            video_thumbnail=video_info['thumbnail'],
            transcript=transcript,
            summary=summary,
            summary_length=summary_length
        )
        db.session.add(history)
        db.session.commit()

        return jsonify({
            'success': True,
            'video_info': video_info,
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