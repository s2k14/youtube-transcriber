import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import json

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app
from models import VideoHistory

class TestApp(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        # Skip DB initialization for tests
        app.config["TESTING"] = True
    
    def test_index_route(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'YouTube Video Transcriber', response.data)
    
    @patch('app.get_video_transcript')
    @patch('app.get_video_info')
    @patch('app.generate_summary')
    @patch('app.db.session.add')
    @patch('app.db.session.commit')
    def test_process_route_success(self, mock_commit, mock_add, mock_generate_summary, 
                                 mock_get_video_info, mock_get_video_transcript):
        # Mock transcript
        mock_get_video_transcript.return_value = "This is a test transcript."
        
        # Mock video info
        mock_get_video_info.return_value = {
            "title": "Test Video",
            "channel": "Test Channel",
            "thumbnail": "https://example.com/thumbnail.jpg",
            "duration": "5:30"
        }
        
        # Mock summary
        mock_generate_summary.return_value = "This is a test summary."
        
        # Test request
        response = self.app.post('/process', json={
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'summary_length': 'medium'
        })
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        
        self.assertEqual(data['title'], "Test Video")
        self.assertEqual(data['transcript'], "This is a test transcript.")
        self.assertEqual(data['summary'], "This is a test summary.")
        
        # Check db operations
        mock_add.assert_called_once()
        mock_commit.assert_called_once()
    
    @patch('app.get_video_transcript')
    def test_process_route_invalid_url(self, mock_get_video_transcript):
        # Mock exception when getting transcript
        mock_get_video_transcript.side_effect = ValueError("Invalid YouTube URL")
        
        # Test request with invalid URL
        response = self.app.post('/process', json={
            'url': 'https://www.example.com',
            'summary_length': 'short'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
    
    @patch('app.get_video_transcript')
    @patch('app.get_video_info')
    @patch('app.generate_summary')
    def test_process_route_api_error(self, mock_generate_summary, 
                                    mock_get_video_info, mock_get_video_transcript):
        # Mock transcript success
        mock_get_video_transcript.return_value = "This is a test transcript."
        
        # Mock video info success
        mock_get_video_info.return_value = {
            "title": "Test Video",
            "channel": "Test Channel",
            "thumbnail": "https://example.com/thumbnail.jpg",
            "duration": "5:30"
        }
        
        # Mock summary API error
        mock_generate_summary.side_effect = Exception("OpenAI API Error")
        
        # Test request
        response = self.app.post('/process', json={
            'url': 'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
            'summary_length': 'medium'
        })
        
        self.assertEqual(response.status_code, 500)
        data = json.loads(response.data)
        self.assertIn('error', data)
        self.assertIn('OpenAI API Error', data['error'])
    
    @patch('app.send_file')
    def test_download_transcript_route(self, mock_send_file):
        # Mock send_file to return a test response
        mock_response = MagicMock()
        mock_send_file.return_value = mock_response
        
        # Test request
        response = self.app.post('/download-transcript', json={
            'title': 'Test Video',
            'transcript': 'This is a test transcript.'
        })
        
        # We can't fully test the file download response,
        # but we can check that send_file was called
        mock_send_file.assert_called_once()
    
    def test_download_transcript_route_missing_data(self):
        # Test request with missing title
        response = self.app.post('/download-transcript', json={
            'transcript': 'This is a test transcript.'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)
        
        # Test request with missing transcript
        response = self.app.post('/download-transcript', json={
            'title': 'Test Video'
        })
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.data)
        self.assertIn('error', data)

if __name__ == '__main__':
    unittest.main()