# YouTube Video Transcriber & Summarizer

A Flask-based web application that transcribes YouTube videos and generates AI-powered summaries. The application provides an intuitive interface for users to input YouTube URLs and receive transcripts along with customizable summaries.

## Features

- 🎥 Video Information Display (title, duration, thumbnail)
- 📝 Automatic Video Transcription
- 🤖 Multi-Provider AI Summarization (OpenAI, Anthropic)
  - Configurable model selection
  - Dynamic provider switching
  - Support for multiple API keys
- 💾 Download Transcripts as Text Files
- 📚 History of Previously Processed Videos

## Prerequisites

Before running the application, you'll need:

1. Python 3.11 or later
2. A YouTube Data API key (for video information)
3. At least one AI provider API key:
   - OpenAI API key (starts with 'sk-')
   - Anthropic API key (starts with 'sk-ant-')
4. PostgreSQL database

## Installation

1. Clone the repository:
```bash
git clone https://github.com/s2k14/youtube-transcriber.git
cd youtube-transcriber
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with the following variables:
```env
YOUTUBE_API_KEY=your_youtube_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
SESSION_SECRET=your_secret_key
```

## AI Model Configuration

The application supports multiple AI providers for generating summaries:

### Supported Providers
1. OpenAI
   - Model IDs: gpt-4, gpt-3.5-turbo
   - API Key format: sk-...
2. Anthropic
   - Model IDs: claude-3-opus-20240229, claude-3-sonnet-20240229, claude-3-haiku-20240307
   - API Key format: sk-ant-...

### Adding a New Model
1. Navigate to the AI Models page
2. Click "Add New Model"
3. Enter:
   - Model Name (for display)
   - Provider (OpenAI or Anthropic)
   - Model ID (from supported list)
   - API Key
4. The provider will be automatically detected based on the API key format

### Important Notes
- Only one model can be active at a time
- The application will automatically validate API keys and model IDs
- Models can be activated/deactivated through the UI
- Failed API calls will show detailed error messages

## Usage

1. Visit the application in your web browser
2. Configure an AI model in the AI Models section
3. On the main page:
   - Paste a YouTube video URL
   - Select your desired summary length (short, medium, or long)
   - Click "Transcribe & Summarize"
4. View the video information, summary, and full transcript
5. Download the transcript if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.