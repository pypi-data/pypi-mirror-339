from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime
from typing import Literal

from pydantic import Field

from no_llm.config import (
    ConfigurableModelParameters,
    EnumValidation,
    IntegrationAliases,
    ModelCapability,
    ModelConfiguration,
    ModelConstraints,
    ModelIdentity,
    ModelMetadata,
    ModelMode,
    ModelPricing,
    ModelProperties,
    ParameterValue,
    ParameterVariant,
    PrivacyLevel,
    QualityProperties,
    SpeedProperties,
    TokenPrices,
)
from no_llm.config.parameters import NOT_GIVEN, NotGiven
from no_llm.providers import AzureProvider, OpenAIProvider, OpenRouterProvider, Provider


class O3MiniConfiguration(ModelConfiguration):
    """Configuration for O3 Mini Low model"""

    identity: ModelIdentity = ModelIdentity(
        id="o3-mini-low",
        name="O3 Mini Low",
        version="2024.02",
        description="Newest and most advanced model from OpenAI with the most advanced performance and speed.",
        creator="OpenAI",
    )

    providers: Sequence[Provider] = [AzureProvider(), OpenRouterProvider(), OpenAIProvider()]

    mode: ModelMode = ModelMode.CHAT

    capabilities: set[ModelCapability] = {
        ModelCapability.JSON_MODE,
        ModelCapability.REASONING,
        ModelCapability.FUNCTION_CALLING,
        ModelCapability.TOOLS,
    }

    constraints: ModelConstraints = ModelConstraints(
        context_window=128000, max_input_tokens=128000, max_output_tokens=65536
    )

    properties: ModelProperties | None = ModelProperties(
        speed=SpeedProperties(score=42.0, label="High", description="Average (1-3 seconds)"),
        quality=QualityProperties(score=82.0, label="Very High", description="Very High Quality"),
    )

    metadata: ModelMetadata = ModelMetadata(
        privacy_level=[PrivacyLevel.BASIC],
        pricing=ModelPricing(token_prices=TokenPrices(input_price_per_1k=0.01, output_price_per_1k=0.02)),
        release_date=datetime(2024, 9, 12),
        data_cutoff_date=datetime(2023, 10, 1),
    )

    integration_aliases: IntegrationAliases | None = IntegrationAliases(
        pydantic_ai="o3-mini", litellm="openai/o3-mini", langfuse="o3-mini-low", openrouter="openai/o3-mini"
    )

    class Parameters(ConfigurableModelParameters):
        model_config = ConfigurableModelParameters.model_config
        temperature: ParameterValue[float | NotGiven] = Field(
            default_factory=lambda: ParameterValue[float | NotGiven](variant=ParameterVariant.FIXED, value=1.0)
        )
        top_p: ParameterValue[float | NotGiven] = Field(
            default_factory=lambda: ParameterValue[float | NotGiven](variant=ParameterVariant.FIXED, value=1.0)
        )
        top_k: ParameterValue[int | NotGiven] = Field(
            default_factory=lambda: ParameterValue[int | NotGiven](
                variant=ParameterVariant.UNSUPPORTED, value=NOT_GIVEN
            )
        )
        frequency_penalty: ParameterValue[float | NotGiven] = Field(
            default_factory=lambda: ParameterValue[float | NotGiven](
                variant=ParameterVariant.UNSUPPORTED, value=NOT_GIVEN
            )
        )
        presence_penalty: ParameterValue[float | NotGiven] = Field(
            default_factory=lambda: ParameterValue[float | NotGiven](
                variant=ParameterVariant.UNSUPPORTED, value=NOT_GIVEN
            )
        )
        max_tokens: ParameterValue[int | NotGiven] = Field(
            default_factory=lambda: ParameterValue[int | NotGiven](
                variant=ParameterVariant.UNSUPPORTED, value=NOT_GIVEN
            )
        )
        stop: ParameterValue[list[str] | NotGiven] = Field(
            default_factory=lambda: ParameterValue[list[str] | NotGiven](
                variant=ParameterVariant.VARIABLE, value=NOT_GIVEN
            )
        )
        seed: ParameterValue[int | NotGiven] = Field(
            default_factory=lambda: ParameterValue[int | NotGiven](
                variant=ParameterVariant.UNSUPPORTED, value=NOT_GIVEN
            )
        )
        reasoning_effort: ParameterValue[Literal["low", "medium", "high"] | NotGiven] = Field(
            default_factory=lambda: ParameterValue[Literal["low", "medium", "high"] | NotGiven](
                variant=ParameterVariant.VARIABLE,
                value="low",
                validation_rule=EnumValidation(allowed_values=["low", "medium", "high"]),
            )
        )

    parameters: ConfigurableModelParameters = Field(default_factory=Parameters)
