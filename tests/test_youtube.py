import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.youtube import extract_video_id, get_video_transcript, get_video_info

class TestYouTubeUtils(unittest.TestCase):
    
    def test_extract_video_id_standard_url(self):
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")
    
    def test_extract_video_id_short_url(self):
        url = "https://youtu.be/dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")
    
    def test_extract_video_id_embed_url(self):
        url = "https://www.youtube.com/embed/dQw4w9WgXcQ"
        self.assertEqual(extract_video_id(url), "dQw4w9WgXcQ")
        
    def test_extract_video_id_invalid_url(self):
        url = "https://www.example.com"
        with self.assertRaises(ValueError):
            extract_video_id(url)
    
    @patch('utils.youtube.YouTubeTranscriptApi')
    def test_get_video_transcript_success(self, mock_transcript_api):
        # Mock successful transcript retrieval
        mock_transcript_api.get_transcript.return_value = [
            {'text': 'Hello', 'start': 0.0, 'duration': 1.0},
            {'text': 'world', 'start': 1.0, 'duration': 1.0}
        ]
        
        result = get_video_transcript("dQw4w9WgXcQ")
        self.assertEqual(result, "Hello world")
        mock_transcript_api.get_transcript.assert_called_once_with("dQw4w9WgXcQ")
    
    @patch('utils.youtube.YouTubeTranscriptApi')
    def test_get_video_transcript_no_transcript(self, mock_transcript_api):
        # Mock transcript not available
        mock_transcript_api.get_transcript.side_effect = Exception("Transcript not available")
        
        with self.assertRaises(Exception):
            get_video_transcript("dQw4w9WgXcQ")
    
    @patch('utils.youtube.os.environ.get')
    @patch('utils.youtube.googleapiclient.discovery.build')
    def test_get_video_info_success(self, mock_build, mock_env_get):
        # Mock environment variable
        mock_env_get.return_value = "fake_api_key"
        
        # Mock YouTube API response
        mock_service = MagicMock()
        mock_build.return_value = mock_service
        
        mock_videos_list = MagicMock()
        mock_service.videos.return_value = mock_videos_list
        
        mock_list_execute = MagicMock()
        mock_videos_list.list.return_value = mock_list_execute
        
        # Set up the mock API response
        mock_list_execute.execute.return_value = {
            "items": [{
                "snippet": {
                    "title": "Test Video",
                    "thumbnails": {"high": {"url": "https://example.com/thumbnail.jpg"}},
                    "channelTitle": "Test Channel"
                },
                "contentDetails": {
                    "duration": "PT5M30S"  # 5 minutes and 30 seconds
                }
            }]
        }
        
        result = get_video_info("dQw4w9WgXcQ")
        
        self.assertEqual(result["title"], "Test Video")
        self.assertEqual(result["channel"], "Test Channel")
        self.assertEqual(result["thumbnail"], "https://example.com/thumbnail.jpg")
        self.assertEqual(result["duration"], "5:30")
    
    @patch('utils.youtube.os.environ.get')
    def test_get_video_info_missing_api_key(self, mock_env_get):
        # Mock missing API key
        mock_env_get.return_value = None
        
        with self.assertRaises(Exception):
            get_video_info("dQw4w9WgXcQ")

if __name__ == '__main__':
    unittest.main()