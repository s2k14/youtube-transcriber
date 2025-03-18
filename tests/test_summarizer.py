import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.summarizer import generate_summary

class TestSummarizer(unittest.TestCase):
    
    @patch('utils.summarizer.os.environ.get')
    @patch('utils.summarizer.openai.OpenAI')
    def test_generate_summary_short(self, mock_openai, mock_env_get):
        # Mock environment variable
        mock_env_get.return_value = "fake_api_key"
        
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Mock chat completion
        mock_chat_completion = MagicMock()
        mock_client.chat.completions.create.return_value = mock_chat_completion
        
        # Mock response content
        mock_message = MagicMock()
        mock_message.content = "This is a short summary."
        mock_chat_completion.choices = [MagicMock(message=mock_message)]
        
        transcript = "This is a sample transcript that is long enough to be summarized."
        result = generate_summary(transcript, length="short")
        
        self.assertEqual(result, "This is a short summary.")
        mock_client.chat.completions.create.assert_called_once()
        
        # Check that "short" was in the system message
        args, kwargs = mock_client.chat.completions.create.call_args
        messages = kwargs.get('messages', [])
        system_message = next((m for m in messages if m.get('role') == 'system'), None)
        self.assertIn("short", system_message.get('content', '').lower())
    
    @patch('utils.summarizer.os.environ.get')
    @patch('utils.summarizer.openai.OpenAI')
    def test_generate_summary_medium(self, mock_openai, mock_env_get):
        # Mock environment variable
        mock_env_get.return_value = "fake_api_key"
        
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Mock chat completion
        mock_chat_completion = MagicMock()
        mock_client.chat.completions.create.return_value = mock_chat_completion
        
        # Mock response content
        mock_message = MagicMock()
        mock_message.content = "This is a medium length summary with more details."
        mock_chat_completion.choices = [MagicMock(message=mock_message)]
        
        transcript = "This is a sample transcript that is long enough to be summarized."
        result = generate_summary(transcript, length="medium")
        
        self.assertEqual(result, "This is a medium length summary with more details.")
        
        # Check that "medium" was in the system message
        args, kwargs = mock_client.chat.completions.create.call_args
        messages = kwargs.get('messages', [])
        system_message = next((m for m in messages if m.get('role') == 'system'), None)
        self.assertIn("medium", system_message.get('content', '').lower())
    
    @patch('utils.summarizer.os.environ.get')
    @patch('utils.summarizer.openai.OpenAI')
    def test_generate_summary_long(self, mock_openai, mock_env_get):
        # Mock environment variable
        mock_env_get.return_value = "fake_api_key"
        
        # Mock OpenAI client
        mock_client = MagicMock()
        mock_openai.return_value = mock_client
        
        # Mock chat completion
        mock_chat_completion = MagicMock()
        mock_client.chat.completions.create.return_value = mock_chat_completion
        
        # Mock response content
        mock_message = MagicMock()
        mock_message.content = "This is a comprehensive long summary with more details and analysis."
        mock_chat_completion.choices = [MagicMock(message=mock_message)]
        
        transcript = "This is a sample transcript that is long enough to be summarized."
        result = generate_summary(transcript, length="long")
        
        self.assertEqual(result, "This is a comprehensive long summary with more details and analysis.")
        
        # Check that "long" or "comprehensive" was in the system message
        args, kwargs = mock_client.chat.completions.create.call_args
        messages = kwargs.get('messages', [])
        system_message = next((m for m in messages if m.get('role') == 'system'), None)
        system_content = system_message.get('content', '').lower()
        self.assertTrue("long" in system_content or "comprehensive" in system_content)
    
    @patch('utils.summarizer.os.environ.get')
    def test_generate_summary_missing_api_key(self, mock_env_get):
        # Mock missing API key
        mock_env_get.return_value = None
        
        transcript = "This is a sample transcript."
        with self.assertRaises(Exception):
            generate_summary(transcript)
    
    @patch('utils.summarizer.os.environ.get')
    @patch('utils.summarizer.openai.OpenAI')
    def test_generate_summary_empty_transcript(self, mock_openai, mock_env_get):
        # Mock environment variable
        mock_env_get.return_value = "fake_api_key"
        
        with self.assertRaises(ValueError):
            generate_summary("")

if __name__ == '__main__':
    unittest.main()