"""Content validators for curriculum curator."""


from curriculum_curator.validation.validators.base import BaseValidator

# Import Language validators
from curriculum_curator.validation.validators.language.language_detector import (
    LanguageDetector,
)
from curriculum_curator.validation.validators.quality.readability import (
    ReadabilityValidator,
)

# Import implemented validators
from curriculum_curator.validation.validators.quality.similarity import (
    SimilarityValidator,
)
from curriculum_curator.validation.validators.quality.structure import (
    StructureValidator,
)

# Registry of all available validators
VALIDATOR_REGISTRY: dict[str, type[BaseValidator]] = {
    # Quality validators
    "similarity": SimilarityValidator,
    "structure": StructureValidator,
    "readability": ReadabilityValidator,
    "completeness": None,  # CompletenessValidator
    "coherence": None,  # CoherenceValidator
    "consistency": None,  # ConsistencyValidator
    "generic_detector": None,  # GenericContentDetector
    # Accuracy validators
    "factuality": None,  # FactualityValidator
    "references": None,  # ReferenceValidator
    # Alignment validators
    "objectives": None,  # ObjectiveAlignmentValidator
    "relevance": None,  # RelevanceValidator
    "age_appropriateness": None,  # AgeAppropriatenessValidator
    "instruction_adherence": None,  # InstructionAdherenceValidator
    # Style validators
    "bias": None,  # BiasDetectorValidator
    "tone": None,  # ToneValidator
    # Language validators
    "language_detector": LanguageDetector,
    "grammar": None,  # GrammarValidator
    "spelling": None,  # SpellingValidator
    # Safety validators
    "content_safety": None,  # ContentSafetyValidator
}


def get_validator(validator_name: str, config):
    """Get a validator instance by name.

    Args:
        validator_name: Name of the validator
        config: Configuration for the validator

    Returns:
        BaseValidator: Initialized validator instance

    Raises:
        ValueError: If the validator is not found or implemented
    """
    if validator_name not in VALIDATOR_REGISTRY:
        raise ValueError(
            f"Validator '{validator_name}' not found. Available validators: {', '.join(VALIDATOR_REGISTRY.keys())}"
        )

    validator_class = VALIDATOR_REGISTRY[validator_name]
    if validator_class is None:
        raise ValueError(f"Validator '{validator_name}' is not yet implemented")

    return validator_class(config)
