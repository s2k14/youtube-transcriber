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