import os
from openai import OpenAI
import logging

logger = logging.getLogger(__name__)

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai = OpenAI(api_key=OPENAI_API_KEY)

SUMMARY_LENGTH_TOKENS = {
    'short': 250,
    'medium': 500,
    'long': 1000
}

def generate_summary(text, length='medium'):
    """Generate a summary of the given text using OpenAI's GPT model."""
    try:
        if not text or not text.strip():
            raise ValueError("Empty transcript provided")

        if not OPENAI_API_KEY:
            raise ValueError("OpenAI API key not found")

        max_tokens = SUMMARY_LENGTH_TOKENS.get(length, 500)
        length_prompt = f"Create a {length} summary"

        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": f"You are a skilled summarizer. {length_prompt} of the following transcript. Focus on the main points and key takeaways."
                },
                {"role": "user", "content": text}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except ValueError as e:
        logger.error(f"Validation error in generate_summary: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise Exception("Failed to generate summary. Please try again later.")