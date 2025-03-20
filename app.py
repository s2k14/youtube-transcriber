import os
import logging
from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for
from io import BytesIO
from utils.youtube import get_video_transcript, get_video_info
from utils.summarizer import generate_summary
from models import VideoHistory, AIModel # Assuming AIModel is defined elsewhere
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
        try:
            video_info = get_video_info(youtube_url)
        except Exception as e:
            logger.error(f"Error getting video info: {str(e)}")
            return jsonify({'error': str(e)}), 500

        # Get video transcript
        try:
            transcript = get_video_transcript(youtube_url)
            if not transcript:
                return jsonify({'error': 'Could not extract transcript from the video'}), 500
        except Exception as e:
            logger.error(f"Error getting transcript: {str(e)}")
            return jsonify({'error': str(e)}), 500

        # Generate summary
        try:
            summary = generate_summary(transcript, summary_length)
        except Exception as e:
            logger.error(f"Error generating summary: {str(e)}")
            return jsonify({'error': str(e)}), 500

        # Save to history
        try:
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
        except Exception as e:
            logger.error(f"Error saving to history: {str(e)}")
            db.session.rollback()
            return jsonify({'error': 'Failed to save video history'}), 500

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

@app.route('/models', methods=['GET'])
def list_models():
    models = AIModel.query.all()
    return render_template('models.html', models=models)

@app.route('/models/add', methods=['GET', 'POST'])
def add_model():
    if request.method == 'POST':
        try:
            api_key = request.form['api_key']
            # Auto-detect provider based on API key format
            provider = request.form['provider']
            if api_key.startswith('sk-ant-'):
                provider = 'anthropic'
            elif api_key.startswith('sk-'):
                provider = 'openai'

            model = AIModel(
                name=request.form['name'],
                provider=provider,
                model_id=request.form['model_id'],
                api_key=api_key
            )
            db.session.add(model)
            db.session.commit()
            return redirect(url_for('list_models'))
        except Exception as e:
            logger.error(f"Error adding model: {str(e)}")
            return jsonify({'error': str(e)}), 500

    return render_template('add_model.html')

@app.route('/models/<int:model_id>/activate', methods=['POST'])
def activate_model(model_id):
    try:
        # Deactivate all models first
        AIModel.query.update({AIModel.is_active: False})

        # Activate the selected model
        model = AIModel.query.get_or_404(model_id)
        model.is_active = True
        db.session.commit()

        return redirect(url_for('list_models'))
    except Exception as e:
        logger.error(f"Error activating model: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/models/active', methods=['GET'])
def get_active_model_info():
    try:
        model = AIModel.query.filter_by(is_active=True).first()
        if model:
            return jsonify({
                'name': model.name,
                'provider': model.provider,
                'model_id': model.model_id,
                'is_active': model.is_active
            })
        return jsonify({'error': 'No active model found'}), 404
    except Exception as e:
        logger.error(f"Error getting active model info: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)