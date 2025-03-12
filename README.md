# YouTube Video Transcriber & Summarizer

A Flask-based web application that transcribes YouTube videos and generates AI-powered summaries. The application provides an intuitive interface for users to input YouTube URLs and receive transcripts along with customizable summaries.

## Features

- 🎥 Video Information Display (title, duration, thumbnail)
- 📝 Automatic Video Transcription
- 🤖 AI-Powered Summarization with adjustable length (short, medium, long)
- 💾 Download Transcripts as Text Files
- 📚 History of Previously Processed Videos

## Prerequisites

Before running the application, you'll need:

1. Python 3.11 or later
2. A YouTube Data API key (for video information)
3. An OpenAI API key (for summarization)
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
OPENAI_API_KEY=your_openai_api_key
DATABASE_URL=postgresql://username:password@localhost:5432/dbname
SESSION_SECRET=your_secret_key
```

## Local Development

1. Create and set up the database:
```bash
# Using psql
createdb youtube_transcriber
```

2. Run the Flask application:
```bash
python main.py
```

The application will be available at `http://localhost:5000`

## Usage

1. Visit the application in your web browser
2. Paste a YouTube video URL in the input field
3. Select your desired summary length (short, medium, or long)
4. Click "Transcribe & Summarize"
5. View the video information, summary, and full transcript
6. Download the transcript if needed

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
