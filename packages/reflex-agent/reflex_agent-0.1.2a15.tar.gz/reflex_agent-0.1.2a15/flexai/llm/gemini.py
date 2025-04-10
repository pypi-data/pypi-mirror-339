import os
from dataclasses import dataclass, field, InitVar
from flexai.llm.openai import OpenAIClient


@dataclass(frozen=True)
class GeminiClient(OpenAIClient):
    """Client for the Gemini API."""

    # The API key to use for interacting with the model.
    api_key: InitVar[str] = field(default=os.environ.get("GEMINI_API_KEY", ""))

    # The base URL for the Gemini API.
    base_url: InitVar[str] = field(
        default=os.environ.get(
            "GEMINI_BASE_URL",
            "https://generativelanguage.googleapis.com/v1beta/openai/",
        )
    )

    # The model to use for the client.
    model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-exp-03-25")
