import pytest

from no_llm.config.enums import ModelCapability
from no_llm.config.errors import FixedParameterError, InvalidEnumError, InvalidRangeError, UnsupportedParameterError
from no_llm.config.parameters import (
    ConfigurableModelParameters,
    EnumValidation,
    ModelParameters,
    ParameterValue,
    ParameterVariant,
    ValidationRule,
    RangeValidation,
)


def test_parameter_value_yaml():
    # Variable value with range
    param = ParameterValue.model_validate({'variant': ParameterVariant.VARIABLE, 'value': 0.7, 'range': [0.0, 1.0]})
    assert param.variant == ParameterVariant.VARIABLE
    assert param.value == 0.7
    assert param.get() == 0.7
    assert param.is_variable()


def test_model_parameters_yaml():
    params = ConfigurableModelParameters.model_validate(
        {
            'temperature': 0.7,  # Fixed
            'top_p': {  # Variable with range
                'value': 0.9,
                'range': [0.0, 1.0],
            },
            'frequency_penalty': {  # Variable without range
                'value': 0.5
            },
            'presence_penalty': {  # Variable with None value
                'value': None
            },
            'max_tokens': 100,  # Fixed
            'include_reasoning': True,  # Fixed
        }
    )
    values = params.get_parameters()
    assert values['temperature'] == 0.7
    assert values['top_p'] == 0.9
    assert values['frequency_penalty'] == 0.5
    assert values['max_tokens'] == 100
    assert values['include_reasoning'] is True


def test_parameter_validation():
    # Test range validation
    with pytest.raises(InvalidRangeError) as exc_info:
        ConfigurableModelParameters.model_validate(
            {
                'temperature': {
                    'value': 3.0,  # > 2.0
                    'range': [0.0, 2.0],
                }
            }
        )
    assert 'Value 3.0 outside range [0.0, 2.0]' in str(exc_info.value)
    assert '[0.0, 2.0]' in str(exc_info.value)

    with pytest.raises(InvalidRangeError) as exc_info:
        ConfigurableModelParameters.model_validate(
            {
                'temperature': {
                    'value': -0.1,  # < 0.0
                    'range': [0.0, 2.0],
                }
            }
        )
    assert 'Value -0.1 outside range [0.0, 2.0]' in str(exc_info.value)
    assert '[0.0, 2.0]' in str(exc_info.value)


def test_enum_validation():
    # Test enum validation
    validator = EnumValidation(allowed_values=['low', 'medium', 'high'])

    # Valid value
    validator.validate_value('medium')

    # Invalid value
    with pytest.raises(InvalidEnumError) as exc_info:
        validator.validate_value('invalid')
    assert 'Value not in allowed values' in str(exc_info.value)
    assert "['low', 'medium', 'high']" in str(exc_info.value)


def test_capability_requirements():
    # Test parameter with no capability requirement
    param = ParameterValue(variant=ParameterVariant.VARIABLE, value=0.7)
    assert param.required_capability is None
    assert not param.is_unsupported()

    # Test parameter with capability requirement
    param = ParameterValue(variant=ParameterVariant.VARIABLE, value=True, required_capability=ModelCapability.REASONING)
    assert param.required_capability == ModelCapability.REASONING
    assert not param.is_unsupported()

    # Test capability check when capability is present
    param = param.check_capability({ModelCapability.REASONING})
    assert not param.is_unsupported()
    assert param.get() is True

    # Test capability check when capability is missing
    param = param.check_capability({ModelCapability.STREAMING})
    assert param.is_unsupported()
    assert param.get() == 'UNSUPPORTED'


def test_model_parameters_capabilities():
    params = ConfigurableModelParameters.model_validate(
        {
            'temperature': 0.7,
            'include_reasoning': {'value': True, 'required_capability': ModelCapability.REASONING},
            'reasoning_effort': {'value': 'medium', 'required_capability': ModelCapability.REASONING},
        }
    )

    # Test with reasoning capability
    values = params.validate_parameters(capabilities={ModelCapability.REASONING})
    assert 'include_reasoning' in values
    assert values['include_reasoning'] is True
    assert values['reasoning_effort'] == 'medium'
    assert values['temperature'] == 0.7

    # Test without reasoning capability - reasoning parameters should be dropped
    values = params.validate_parameters(capabilities=set(), drop_unsupported=True)
    assert 'include_reasoning' not in values
    assert 'reasoning_effort' not in values
    assert values['temperature'] == 0.7


def test_model_parameters_unsupported_error():
    params = ConfigurableModelParameters.model_validate(
        {
            'temperature': {'value': 0.7},
            'include_reasoning': {'value': True, 'required_capability': ModelCapability.REASONING},
        }
    )

    # Should raise error when trying to set unsupported parameter and drop_unsupported=False
    with pytest.raises(UnsupportedParameterError) as exc_info:
        params.validate_parameters(
            capabilities=set(),  # No capabilities -> reasoning is unsupported
            drop_unsupported=False,
            include_reasoning=True,  # Trying to set an unsupported parameter
            temperature=0.8,  # This should work
        )
    assert "Parameter 'include_reasoning' is not supported" in str(exc_info.value)

    # Should silently drop unsupported parameter when drop_unsupported=True
    values = params.validate_parameters(
        capabilities=set(),
        drop_unsupported=True,
        include_reasoning=True,  # This should be dropped
        temperature=0.8,  # This should remain
    )
    assert 'include_reasoning' not in values
    assert values['temperature'] == 0.8


def test_fixed_parameter_modification(no_llm_error_settings):
    params = ConfigurableModelParameters.model_validate(
        {'temperature': {'variant': ParameterVariant.FIXED, 'value': 0.7}}
    )
    with pytest.raises(FixedParameterError) as exc_info:
        params.validate_parameters(capabilities=set(), temperature=0.8)
    assert "Cannot modify fixed parameter 'temperature'" in str(exc_info.value)
    assert 'Fixed value: 0.7' in str(exc_info.value)
    assert 'Attempted value: 0.8' in str(exc_info.value)


def test_multiple_validation():
    # Test multiple validation errors are caught
    with pytest.raises(InvalidRangeError) as exc_info:
        ConfigurableModelParameters.model_validate(
            {
                'temperature': {
                    'value': 3.0,  # > 2.0
                    'range': [0.0, 2.0],
                },
                'top_p': {
                    'value': 1.5,  # > 1.0
                    'range': [0.0, 1.0],
                },
            }
        )
    # We'll get the first error encountered
    assert 'outside range' in str(exc_info.value)
    assert 'Valid range:' in str(exc_info.value)


def test_parameter_validation_rules(no_llm_error_settings):
    """Test that validation rules are properly applied"""
    # Range validation
    params = ConfigurableModelParameters.model_validate({'temperature': {'value': 0.7, 'range': [0.0, 2.0]}})
    # Should fail when trying to set outside range
    with pytest.raises(InvalidRangeError) as exc_info:
        params.validate_parameters(capabilities=set(), temperature=3.0)
    assert 'Value 3.0 outside range [0.0, 2.0]' in str(exc_info.value)
    assert '[0.0, 2.0]' in str(exc_info.value)

    # Should work within range
    values = params.validate_parameters(capabilities=set(), temperature=1.5)
    assert values['temperature'] == 1.5


def test_model_parameters_direct_yaml():
    """Test that parameters can be loaded directly through model configuration"""
    from no_llm.config.model import ModelConfiguration

    config = {
        'identity': {
            'id': 'test-model',
            'name': 'Test Model',
            'version': '1.0.0',
            'description': 'Test model',
            'creator': 'test',  # Added required field
        },
        'provider_id': 'test',
        'mode': 'chat',
        'capabilities': ['streaming', 'reasoning'],
        'constraints': {
            'context_window': 1024,
            'max_input_tokens': 1000,
            'max_output_tokens': 500,
            'token_encoding': 'test',
        },
        'properties': {
            'speed': {'score': 50.0, 'label': 'test', 'description': 'test'},
            'quality': {'score': 50.0, 'label': 'test', 'description': 'test'},
        },
        'parameters': {
            'temperature': 0.7,
            'top_p': {'value': 0.9, 'range': [0.0, 1.0]},
            'frequency_penalty': {'value': 0.5},
            'presence_penalty': {'value': None},
            'max_tokens': 100,
            'top_k': 'unsupported',
            'include_reasoning': {'value': True, 'required_capability': 'reasoning'},
        },
        'metadata': {
            'privacy_level': ['basic'],  # Changed to list
            'pricing': {'token_prices': {'input_price_per_1k': 0.01, 'output_price_per_1k': 0.02}},
            'release_date': '2024-01-01T00:00:00Z',
        },
    }

    model = ModelConfiguration.model_validate(config)

    # Test that parameters were loaded correctly
    params = model.parameters

    # Test fixed value
    assert params.temperature.is_fixed()
    assert params.temperature.get() == 0.7

    # Test variable with range
    assert params.top_p.is_variable()
    assert params.top_p.get() == 0.9
    assert params.top_p.validation_rule is not None
    assert params.top_p.validation_rule.min_value == 0.0
    assert params.top_p.validation_rule.max_value == 1.0

    # Test variable without range
    assert params.frequency_penalty.is_variable()
    assert params.frequency_penalty.get() == 0.5

    # Test variable with None value
    assert params.presence_penalty.is_variable()
    assert params.presence_penalty.get() is None

    # Test fixed value
    assert params.max_tokens.get() == 100

    # Test unsupported parameter
    assert params.top_k.is_unsupported()
    assert params.top_k.get() == 'UNSUPPORTED'

    # Test parameter with capability
    assert params.include_reasoning.required_capability == ModelCapability.REASONING
    assert params.include_reasoning.get() is True

    # Test parameter validation
    values = model.parameters.get_parameters()
    assert values['temperature'] == 0.7
    assert values['top_p'] == 0.9
    assert values['frequency_penalty'] == 0.5
    assert values['max_tokens'] == 100
    assert values['include_reasoning'] is True
    assert 'top_k' not in values  # Unsupported parameter should be dropped


def test_model_parameters_validation(no_llm_error_settings):
    """Test parameter validation through model configuration"""
    from no_llm.config.model import ModelConfiguration

    config = {
        'identity': {
            'id': 'test-model',
            'name': 'Test Model',
            'version': '1.0.0',
            'description': 'Test model',
            'creator': 'test',  # Added required field
        },
        'provider_id': 'test',
        'mode': 'chat',
        'capabilities': ['streaming'],
        'constraints': {
            'context_window': 1024,
            'max_input_tokens': 1000,
            'max_output_tokens': 500,
            'token_encoding': 'test',
        },
        'properties': {
            'speed': {'score': 50.0, 'label': 'test', 'description': 'test'},
            'quality': {'score': 50.0, 'label': 'test', 'description': 'test'},
        },
        'parameters': {'temperature': {'variant': 'fixed', 'value': 0.7}, 'top_p': {'value': 0.9, 'range': [0.0, 1.0]}},
        'metadata': {
            'privacy_level': ['basic'],  # Changed to list
            'pricing': {'token_prices': {'input_price_per_1k': 0.01, 'output_price_per_1k': 0.02}},
            'release_date': '2024-01-01T00:00:00Z',
        },
    }

    model = ModelConfiguration.model_validate(config)

    # Test fixed parameter modification
    with pytest.raises(FixedParameterError) as exc_info:
        model.parameters.validate_parameters(temperature=0.8)
    assert "Cannot modify fixed parameter 'temperature'" in str(exc_info.value)

    # Test range validation
    with pytest.raises(InvalidRangeError) as exc_info:
        model.parameters.validate_parameters(top_p=1.5)  # Outside [0.0, 1.0]
    assert 'Value 1.5 outside range [0.0, 1.0]' in str(exc_info.value)

    # Test valid modification
    values = model.parameters.validate_parameters(top_p=0.5)
    assert values['temperature'] == 0.7  # Fixed value unchanged
    assert values['top_p'] == 0.5  # New value within range


def test_parameter_conversion_flow():
    """Test conversion from ConfigurableModelParameters to ModelParameters"""
    config_params = ConfigurableModelParameters.model_validate(
        {
            'temperature': {
                'value': 0.7,
                'range': [0.0, 2.0]
            },
            'include_reasoning': {
                'value': True,
                'required_capability': 'reasoning'
            }
        }
    )

    # Test validation with required capability
    validated = config_params.validate_parameters(
        capabilities={ModelCapability.REASONING},
        temperature=0.8
    )
    # Create ModelParameters with validated values
    model_params = ModelParameters(**validated)
    assert model_params.temperature == 0.8
    assert model_params.include_reasoning is True

    # Test validation without required capability
    validated = config_params.validate_parameters(
        capabilities=set(),  # No capabilities
        temperature=0.8
    )
    # Create ModelParameters with validated values
    model_params = ModelParameters(**validated)
    assert model_params.temperature == 0.8
    assert model_params.include_reasoning == 'NOT_GIVEN'  # Default when not provided


def test_parameter_override_validation():
    """Test parameter validation during conversion"""
    config_params = ConfigurableModelParameters.model_validate(
        {
            'temperature': {
                'value': 0.7,
                'range': [0.0, 2.0]
            },
            'top_p': {
                'variant': 'fixed',
                'value': 0.9
            }
        }
    )

    # Test valid override
    validated = config_params.validate_parameters(temperature=1.5)
    model_params = ModelParameters(**validated)
    assert model_params.temperature == 1.5
    assert model_params.top_p == 0.9


def test_not_given_handling():
    """Test handling of NOT_GIVEN vs None values"""
    config_params = ConfigurableModelParameters.model_validate(
        {
            'temperature': {'value': 0.7},
            'max_tokens': {'value': None},  # Explicitly set to None
            'top_p': 'unsupported'  # Will not be included
        }
    )

    validated = config_params.validate_parameters()
    model_params = ModelParameters(**validated)
    assert model_params.temperature == 0.7
    assert model_params.max_tokens == 'NOT_GIVEN'  # Default when not provided
    assert model_params.top_p == 'NOT_GIVEN'  # Default when not provided


def test_model_parameters_merge():
    """Test merging ModelParameters instances"""
    base_params = ModelParameters(
        temperature=0.7,
        max_tokens=100
    )

    override_params = ModelParameters(
        temperature=0.8,
        top_p=0.9
    )

    # Test merging with & - left-hand takes precedence
    merged = override_params & base_params
    assert merged.temperature == 0.8  # From override
    assert merged.max_tokens == 100  # From base
    assert merged.top_p == 0.9  # From override


def test_parameter_dump_and_get():
    """Test parameter dumping and getting methods"""
    config_params = ConfigurableModelParameters.model_validate(
        {
            'temperature': {'value': 0.7},
            'max_tokens': {'value': None},
            'top_p': 'unsupported'
        }
    )

    # Get parameters (excludes None values and unsupported)
    params = config_params.get_parameters()
    model_params = ModelParameters(**params)
    dumped = model_params.dump_parameters(with_defaults=False)
    assert dumped == {'temperature': 0.7}  # Only non-default values


def test_validation_rule_base():
    """Test base ValidationRule class"""
    rule = ValidationRule()
    # Base class validate_value should not raise
    rule.validate_value("any value")
    rule.validate_value(None)


def test_parameter_value_serialization():
    """Test ParameterValue serialization"""
    # Test unsupported parameter
    param = ParameterValue(variant=ParameterVariant.UNSUPPORTED, value=None)
    assert param.serialize_model() == "unsupported"
    
    # Test fixed value
    param = ParameterValue(variant=ParameterVariant.FIXED, value=0.7)
    assert param.serialize_model() == 0.7
    
    # Test variable with range validation
    param = ParameterValue(
        variant=ParameterVariant.VARIABLE,
        value=0.7,
        validation_rule=RangeValidation(min_value=0.0, max_value=1.0)
    )
    serialized = param.serialize_model()
    assert serialized["value"] == 0.7
    assert serialized["range"] == [0.0, 1.0]
    
    # Test variable with enum validation
    param = ParameterValue(
        variant=ParameterVariant.VARIABLE,
        value="medium",
        validation_rule=EnumValidation(allowed_values=["low", "medium", "high"])
    )
    serialized = param.serialize_model()
    assert serialized["value"] == "medium"
    assert serialized["values"] == ["low", "medium", "high"]


def test_configurable_parameters_serialization():
    """Test ConfigurableModelParameters serialization"""
    params = ConfigurableModelParameters()
    
    # Set some non-default values
    params.temperature = ParameterValue(
        variant=ParameterVariant.VARIABLE,
        value=0.7,
        validation_rule=RangeValidation(min_value=0.0, max_value=1.0)
    )
    params.top_p = ParameterValue(
        variant=ParameterVariant.UNSUPPORTED,
        value=None
    )
    
    serialized = params.serialize_model()
    
    # Check that non-default values are included
    assert "temperature" in serialized
    assert isinstance(serialized["temperature"], ParameterValue)
    assert serialized["temperature"].value == 0.7
    
    # Check that unsupported parameter is included
    assert "top_p" in serialized
    assert isinstance(serialized["top_p"], ParameterValue)
    assert serialized["top_p"].variant == ParameterVariant.UNSUPPORTED
    
    # Check that default values are excluded
    assert "max_tokens" not in serialized


def test_parameter_value_direct_serialization():
    """Test ParameterValue direct serialization"""
    # Test unsupported parameter
    param = ParameterValue(variant=ParameterVariant.UNSUPPORTED, value=None)
    serialized = param.serialize_model()
    assert serialized == "unsupported"
    
    # Test fixed value
    param = ParameterValue(variant=ParameterVariant.FIXED, value=0.7)
    serialized = param.serialize_model()
    assert serialized == 0.7
    
    # Test variable with range validation
    param = ParameterValue(
        variant=ParameterVariant.VARIABLE,
        value=0.7,
        validation_rule=RangeValidation(min_value=0.0, max_value=1.0)
    )
    serialized = param.serialize_model()
    assert isinstance(serialized, dict)
    assert serialized["value"] == 0.7
    assert serialized["range"] == [0.0, 1.0]


def test_model_parameters_with_overrides():
    """Test ModelParameters with model-specific overrides"""
    params = ModelParameters(
        temperature=0.7,
        model_override={
            "gpt-4": ModelParameters(temperature=0.8),
            "gpt-3.5": ModelParameters(temperature=0.6)
        }
    )
    
    # Test dumping without overrides
    base_params = params.dump_parameters(with_defaults=False)
    assert base_params["temperature"] == 0.7
    
    # Test dumping with specific model override
    gpt4_params = params.dump_parameters(with_defaults=False, model_override="gpt-4")
    assert gpt4_params["temperature"] == 0.8
    
    # Test dumping with non-existent model override
    other_params = params.dump_parameters(with_defaults=False, model_override="other-model")
    assert other_params["temperature"] == 0.7


def test_parameter_value_not_given():
    """Test handling of NOT_GIVEN values in validation"""
    param = ParameterValue(
        variant=ParameterVariant.VARIABLE,
        value="NOT_GIVEN",
        validation_rule=RangeValidation(min_value=0.0, max_value=1.0)
    )
    
    # NOT_GIVEN should pass validation
    param.validate_model()
    
    # NOT_GIVEN should be preserved in get()
    assert param.get() == "NOT_GIVEN"


def test_configurable_parameters_validation_modes():
    """Test different validation modes for ConfigurableModelParameters"""
    from no_llm.settings import ValidationMode
    import no_llm.settings as settings
    
    params = ConfigurableModelParameters()
    params.temperature = ParameterValue(
        variant=ParameterVariant.VARIABLE,
        value=0.7,
        validation_rule=RangeValidation(min_value=0.0, max_value=1.0)
    )
    
    # Test CLAMP mode
    settings.settings.validation_mode = ValidationMode.CLAMP
    validated = params.validate_parameters(temperature=1.5)
    assert validated["temperature"] == 1.0  # Clamped to max
    
    validated = params.validate_parameters(temperature=-0.5)
    assert validated["temperature"] == 0.0  # Clamped to min
    
    # Reset validation mode
    settings.settings.validation_mode = ValidationMode.ERROR
