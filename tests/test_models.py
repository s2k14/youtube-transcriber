import unittest
import sys
import os
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models import VideoHistory
from db import db

class TestModels(unittest.TestCase):
    
    def setUp(self):
        # Create an in-memory SQLite database for testing
        self.engine = create_engine('sqlite:///:memory:')
        db.metadata.create_all(self.engine)
        
        # Create a session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
    
    def tearDown(self):
        self.session.close()
    
    def test_video_history_creation(self):
        # Create a new VideoHistory instance
        video = VideoHistory(
            video_id="dQw4w9WgXcQ",
            title="Test Video",
            channel="Test Channel",
            thumbnail="https://example.com/thumbnail.jpg",
            duration="5:30",
            transcript="This is a test transcript.",
            summary="This is a test summary.",
            timestamp=datetime.now()
        )
        
        # Add to session and commit
        self.session.add(video)
        self.session.commit()
        
        # Query to verify it was added
        result = self.session.query(VideoHistory).filter_by(video_id="dQw4w9WgXcQ").first()
        
        self.assertIsNotNone(result)
        self.assertEqual(result.title, "Test Video")
        self.assertEqual(result.channel, "Test Channel")
        self.assertEqual(result.transcript, "This is a test transcript.")
        self.assertEqual(result.summary, "This is a test summary.")
    
    def test_video_history_query(self):
        # Create multiple VideoHistory instances
        video1 = VideoHistory(
            video_id="dQw4w9WgXcQ",
            title="Test Video 1",
            channel="Test Channel",
            thumbnail="https://example.com/thumbnail1.jpg",
            duration="5:30",
            transcript="This is test transcript 1.",
            summary="This is test summary 1.",
            timestamp=datetime(2023, 1, 1, 12, 0, 0)
        )
        
        video2 = VideoHistory(
            video_id="abcdefghijk",
            title="Test Video 2",
            channel="Test Channel",
            thumbnail="https://example.com/thumbnail2.jpg",
            duration="10:45",
            transcript="This is test transcript 2.",
            summary="This is test summary 2.",
            timestamp=datetime(2023, 1, 2, 12, 0, 0)
        )
        
        # Add to session and commit
        self.session.add(video1)
        self.session.add(video2)
        self.session.commit()
        
        # Query all videos
        results = self.session.query(VideoHistory).all()
        self.assertEqual(len(results), 2)
        
        # Query by video_id
        result = self.session.query(VideoHistory).filter_by(video_id="abcdefghijk").first()
        self.assertEqual(result.title, "Test Video 2")
        
        # Order by timestamp
        results = self.session.query(VideoHistory).order_by(VideoHistory.timestamp.desc()).all()
        self.assertEqual(results[0].video_id, "abcdefghijk")  # Most recent first
    
    def test_video_history_update(self):
        # Create a VideoHistory instance
        video = VideoHistory(
            video_id="dQw4w9WgXcQ",
            title="Test Video",
            channel="Test Channel",
            thumbnail="https://example.com/thumbnail.jpg",
            duration="5:30",
            transcript="This is a test transcript.",
            summary="This is a test summary.",
            timestamp=datetime.now()
        )
        
        # Add to session and commit
        self.session.add(video)
        self.session.commit()
        
        # Query, update, and commit
        result = self.session.query(VideoHistory).filter_by(video_id="dQw4w9WgXcQ").first()
        result.title = "Updated Title"
        result.summary = "Updated summary."
        self.session.commit()
        
        # Query again to verify update
        updated = self.session.query(VideoHistory).filter_by(video_id="dQw4w9WgXcQ").first()
        self.assertEqual(updated.title, "Updated Title")
        self.assertEqual(updated.summary, "Updated summary.")
    
    def test_video_history_delete(self):
        # Create a VideoHistory instance
        video = VideoHistory(
            video_id="dQw4w9WgXcQ",
            title="Test Video",
            channel="Test Channel",
            thumbnail="https://example.com/thumbnail.jpg",
            duration="5:30",
            transcript="This is a test transcript.",
            summary="This is a test summary.",
            timestamp=datetime.now()
        )
        
        # Add to session and commit
        self.session.add(video)
        self.session.commit()
        
        # Query, delete, and commit
        result = self.session.query(VideoHistory).filter_by(video_id="dQw4w9WgXcQ").first()
        self.session.delete(result)
        self.session.commit()
        
        # Query again to verify deletion
        deleted = self.session.query(VideoHistory).filter_by(video_id="dQw4w9WgXcQ").first()
        self.assertIsNone(deleted)

if __name__ == '__main__':
    unittest.main()