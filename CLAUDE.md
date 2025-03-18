# YouTube Transcriber Project Guidelines

## Commands
- Run app: `python main.py`
- Install dependencies: `pip install -e .` or `pip install -r requirements.txt`
- Format code: `black .`
- Lint: `flake8 *.py utils/`
- Run all tests: `python run_tests.py`
- Run single test: `python -m unittest tests.test_youtube.TestYouTubeUtils.test_extract_video_id_standard_url`

## Environment Setup
Required env vars: YOUTUBE_API_KEY, OPENAI_API_KEY, DATABASE_URL, SESSION_SECRET

## Code Style
- Python 3.11+ with type hints recommended but not required
- Follow PEP 8 conventions
- Use docstrings for functions/classes
- Exception handling with specific error messages
- Standard Python logging (already configured)
- Organize imports: stdlib first, then third-party, then local modules

## Project Structure
- Flask app with SQLAlchemy ORM
- utils/ for helper modules (youtube.py, summarizer.py)
- templates/ for HTML, static/ for CSS/JS
- tests/ for unit and integration tests
- Error handling with meaningful user feedback

## Testing
- Use unittest framework with mocking (unittest.mock)
- Test database operations with in-memory SQLite
- Mock external API calls in tests (YouTube API, OpenAI API)
- Test both success and error cases