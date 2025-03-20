import os
from openai import OpenAI
import anthropic
import logging
from models import AIModel

logger = logging.getLogger(__name__)

SUMMARY_LENGTH_TOKENS = {
    'short': 250,
    'medium': 500,
    'long': 1000
}

class ModelProvider:
    def __init__(self, model_config):
        self.provider = model_config.provider
        self.model_id = model_config.model_id
        self.api_key = model_config.api_key

    def generate_summary(self, text, max_tokens):
        if self.provider == 'openai':
            return self._openai_summary(text, max_tokens)
        elif self.provider == 'anthropic':
            return self._anthropic_summary(text, max_tokens)
        else:
            raise ValueError(f"Unsupported provider: {self.provider}")

    def _openai_summary(self, text, max_tokens):
        client = OpenAI(api_key=self.api_key)
        response = client.chat.completions.create(
            model=self.model_id,
            messages=[
                {
                    "role": "system",
                    "content": "You are a skilled summarizer. Create a summary of the following transcript. Focus on the main points and key takeaways."
                },
                {"role": "user", "content": text}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

    def _anthropic_summary(self, text, max_tokens):
        client = anthropic.Anthropic(api_key=self.api_key)
        response = client.messages.create(
            model=self.model_id,
            max_tokens=max_tokens,
            messages=[
                {
                    "role": "user",
                    "content": f"Please summarize the following text, focusing on key points: {text}"
                }
            ]
        )
        return response.content[0].text

def get_active_model():
    """Get the currently active AI model configuration."""
    model = AIModel.query.filter_by(is_active=True).first()
    if not model:
        # Fall back to OpenAI if no active model is set
        model = AIModel.query.filter_by(provider='openai').first()
    return model

def generate_summary(text, length='medium'):
    """Generate a summary of the given text using the selected AI model."""
    try:
        if not text or not text.strip():
            raise ValueError("Empty transcript provided")

        model_config = get_active_model()
        if not model_config:
            raise ValueError("No AI model configured")

        max_tokens = SUMMARY_LENGTH_TOKENS.get(length, 500)
        provider = ModelProvider(model_config)

        return provider.generate_summary(text, max_tokens)
    except ValueError as e:
        logger.error(f"Validation error in generate_summary: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise Exception("Failed to generate summary. Please try again later.")