from datetime import datetime
from db import db

class VideoHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(255), nullable=False)
    video_title = db.Column(db.String(255))
    video_duration = db.Column(db.String(50))
    video_thumbnail = db.Column(db.String(255))
    transcript = db.Column(db.Text)
    summary = db.Column(db.Text)
    summary_length = db.Column(db.String(20))  # 'short', 'medium', or 'long'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AIModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    provider = db.Column(db.String(50), nullable=False)  # 'openai', 'anthropic', 'google', 'deepseek'
    model_id = db.Column(db.String(50), nullable=False)  # e.g., 'gpt-4', 'claude-2', etc.
    api_key = db.Column(db.String(255), nullable=False)
    is_active = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('provider', 'model_id', name='unique_provider_model'),
    )