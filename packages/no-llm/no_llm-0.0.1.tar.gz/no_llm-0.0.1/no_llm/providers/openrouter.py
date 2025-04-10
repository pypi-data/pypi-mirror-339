from __future__ import annotations

from pydantic import Field

from no_llm.providers.env_var import EnvVar
from no_llm.providers.openai import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    """OpenRouter provider configuration"""

    type: str = "openrouter"
    name: str = "OpenRouter"
    api_key: EnvVar[str] = Field(
        default_factory=lambda: EnvVar[str]("$OPENROUTER_API_KEY"),
        description="Name of environment variable containing API key",
    )
    base_url: str | None = Field(default="https://openrouter.ai/api/v1", description="Base URL for OpenRouter API")
