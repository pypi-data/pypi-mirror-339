from __future__ import annotations

from pydantic import Field

from no_llm.providers.base import Provider
from no_llm.providers.env_var import EnvVar


class AnthropicProvider(Provider):
    """Anthropic provider configuration"""

    type: str = "anthropic"
    name: str = "Anthropic"
    api_key: EnvVar[str] = Field(
        default_factory=lambda: EnvVar[str]("$ANTHROPIC_API_KEY"),
        description="Name of environment variable containing API key",
    )
    base_url: EnvVar[str] | None = Field(default=None, description="Optional base URL override")
