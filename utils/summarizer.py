import os
import logging
from openai import OpenAI
import anthropic
from flask import current_app
from models import AIModel
from db import db

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
        try:
            logger.debug(f"Using OpenAI model: {self.model_id}")
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
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise Exception(f"Failed to generate summary with OpenAI: {str(e)}")

    def _anthropic_summary(self, text, max_tokens):
        try:
            logger.debug(f"Using Anthropic model: {self.model_id}")
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
        except Exception as e:
            logger.error(f"Anthropic API error: {str(e)}")
            raise Exception(f"Failed to generate summary with Anthropic: {str(e)}")

def get_active_model():
    """Get the currently active AI model configuration."""
    try:
        with current_app.app_context():
            logger.debug("Querying for active AI model")
            model = AIModel.query.filter_by(is_active=True).first()
            if not model:
                logger.debug("No active model found, checking for OpenAI model")
                model = AIModel.query.filter_by(provider='openai').first()
            if not model:
                raise ValueError("No AI model configured. Please add a model in the AI Models section.")
            logger.debug(f"Using AI model: {model.name} ({model.provider})")
            return model
    except Exception as e:
        logger.error(f"Error getting active model: {str(e)}")
        raise Exception(f"Failed to get active AI model configuration: {str(e)}")

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
        raise Exception(f"Failed to generate summary: {str(e)}")