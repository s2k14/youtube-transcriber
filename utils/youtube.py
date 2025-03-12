from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import os
import requests
import logging

logger = logging.getLogger(__name__)

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY")

def extract_video_id(url):
    """Extract the video ID from a YouTube URL."""
    parsed_url = urlparse(url)

    if parsed_url.hostname in ('youtu.be', 'www.youtu.be'):
        return parsed_url.path[1:]

    if parsed_url.hostname in ('youtube.com', 'www.youtube.com'):
        if parsed_url.path == '/watch':
            return parse_qs(parsed_url.query)['v'][0]
        elif parsed_url.path.startswith('/embed/'):
            return parsed_url.path.split('/')[2]
        elif parsed_url.path.startswith('/v/'):
            return parsed_url.path.split('/')[2]

    raise ValueError("Invalid YouTube URL format")

def get_video_info(url):
    """Get video information using YouTube Data API."""
    try:
        video_id = extract_video_id(url)
        api_url = f"https://www.googleapis.com/youtube/v3/videos"
        params = {
            'key': YOUTUBE_API_KEY,
            'id': video_id,
            'part': 'snippet,contentDetails'
        }

        response = requests.get(api_url, params=params)
        response.raise_for_status()
        data = response.json()

        if not data['items']:
            raise ValueError("Video not found")

        video_data = data['items'][0]
        return {
            'title': video_data['snippet']['title'],
            'duration': video_data['contentDetails']['duration'],
            'thumbnail': video_data['snippet']['thumbnails']['high']['url']
        }

    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}")
        raise Exception("Failed to get video information")

def get_video_transcript(url):
    """Get the transcript of a YouTube video."""
    try:
        video_id = extract_video_id(url)
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)

        # Combine all transcript pieces into one text
        full_transcript = ' '.join([entry['text'] for entry in transcript_list])
        return full_transcript

    except Exception as e:
        logger.error(f"Error getting transcript: {str(e)}")
        raise Exception("Failed to get video transcript. Please make sure the video exists and has subtitles available.")