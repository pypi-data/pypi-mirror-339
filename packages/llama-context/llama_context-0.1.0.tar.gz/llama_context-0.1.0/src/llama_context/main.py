# Project Structure:
#
# llama_context/
# ├── __init__.py
# ├── config.py
# ├── context_engine.py
# ├── providers/
# │   ├── __init__.py
# │   ├── base.py
# │   ├── anthropic.py
# │   ├── openai.py
# │   └── mock.py
# ├── guardrails/
# │   ├── __init__.py
# │   ├── base.py
# │   ├── keyword_check.py
# │   ├── regex_check.py
# │   └── llm_verification.py
# ├── multimodal/
# │   ├── __init__.py
# │   ├── fusion.py
# │   ├── image_encoder.py
# │   └── text_encoder.py
# ├── temporal/
# │   ├── __init__.py
# │   ├── memory.py
# │   ├── summarization.py
# │   └── rnn_simulator.py
# ├── citation/
# │   ├── __init__.py
# │   ├── generator.py
# │   └── validator.py
# ├── adversarial/
# │   ├── __init__.py
# │   ├── detector.py
# │   └── patterns.py
# ├── ml/
# │   ├── __init__.py
# │   ├── coreml_converter.py
# │   └── mlx_integration.py
# ├── utils/
# │   ├── __init__.py
# │   ├── logger.py
# │   ├── security.py
# │   └── validation.py
# ├── tests/
# │   ├── __init__.py
# │   ├── test_context_engine.py
# │   ├── test_providers.py
# │   ├── test_guardrails.py
# │   ├── test_multimodal.py
# │   ├── test_temporal.py
# │   ├── test_citation.py
# │   ├── test_adversarial.py
# │   └── test_ml.py
# ├── pyproject.toml
# ├── requirements.txt
# ├── requirements-dev.txt
# └── README.md

# First, let's create the package's __init__.py file
# llama_context/__init__.py
"""
llama_context: Advanced context engine for LLM applications.

This package provides a sophisticated context engine for enhancing LLM applications
with query understanding, response generation, provider integration, ethical guardrails,
multimodal fusion, temporal context modeling, citation generation, and adversarial
pattern detection.
"""

__version__ = "1.0.0"

from .config import ContextConfig
from .context_engine import ContextEngine

__all__ = ["ContextEngine", "ContextConfig"]

# llama_context/config.py
"""Configuration module for the llama_context package."""

import os
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional, Union


class ProviderType(Enum):
    """Supported LLM provider types."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    MOCK = "mock"


class GuardrailLevel(Enum):
    """Guardrail strictness levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class ContextConfig:
    """Configuration for the context engine.

    This class holds all configuration parameters for the llama_context engine,
    including provider settings, guardrail configuration, multimodal settings,
    and other operational parameters.

    Attributes:
        provider: LLM provider to use.
        api_key: API key for the provider (defaults to environment variable).
        model: Model name to use with the provider.
        guardrail_level: Strictness level for ethical guardrails.
        enable_multimodal: Whether to enable multimodal fusion capabilities.
        enable_temporal: Whether to enable temporal context modeling.
        enable_citations: Whether to enable citation generation.
        enable_adversarial_detection: Whether to detect adversarial patterns.
        max_context_length: Maximum number of tokens in the context window.
        temperature: Sampling temperature for the LLM.
        top_p: Top-p sampling parameter for the LLM.
        request_timeout: Timeout for LLM API requests in seconds.
        additional_params: Additional provider-specific parameters.
    """

    provider: ProviderType = ProviderType.ANTHROPIC
    api_key: Optional[str] = None
    model: str = "claude-3-sonnet-20240229"
    guardrail_level: GuardrailLevel = GuardrailLevel.MEDIUM
    enable_multimodal: bool = True
    enable_temporal: bool = True
    enable_citations: bool = True
    enable_adversarial_detection: bool = True
    max_context_length: int = 100000
    temperature: float = 0.7
    top_p: float = 0.9
    request_timeout: int = 60
    additional_params: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        """Load API keys from environment variables if not provided."""
        if self.api_key is None:
            env_var_name = f"{self.provider.value.upper()}_API_KEY"
            self.api_key = os.environ.get(env_var_name)

            if self.api_key is None:
                raise ValueError(
                    f"API key not provided and {env_var_name} environment variable not set"
                )


# llama_context/context_engine.py
"""Core context engine implementation."""

import logging
from typing import Any, Dict, List, Optional, Tuple, Union

from .adversarial.detector import AdversarialDetector
from .citation.generator import CitationGenerator
from .config import ContextConfig, ProviderType
from .guardrails.base import BaseGuardrail
from .guardrails.keyword_check import KeywordCheckGuardrail
from .guardrails.llm_verification import LLMVerificationGuardrail
from .guardrails.regex_check import RegexCheckGuardrail
from .multimodal.fusion import MultimodalFusion
from .providers.anthropic import AnthropicProvider
from .providers.base import BaseProvider
from .providers.mock import MockProvider
from .providers.openai import OpenAIProvider
from .temporal.memory import ContextMemory
from .utils.logger import setup_logger


class ContextEngine:
    """Advanced context engine for LLM applications.

    This class provides the main interface for the llama_context package, handling
    query understanding, response generation, provider integration, ethical guardrails,
    multimodal fusion, temporal context modeling, citation generation, and adversarial
    pattern detection.

    Attributes:
        config: Configuration for the context engine.
        provider: LLM provider instance.
        guardrails: List of ethical guardrails.
        multimodal_fusion: Multimodal fusion engine (if enabled).
        context_memory: Temporal context memory (if enabled).
        citation_generator: Citation generator (if enabled).
        adversarial_detector: Adversarial pattern detector (if enabled).
        logger: Logger instance.
    """

    def __init__(self, config: Optional[ContextConfig] = None):
        """Initialize the context engine.

        Args:
            config: Configuration for the context engine. If not provided,
                a default configuration will be used.
        """
        self.config = config or ContextConfig()
        self.logger = setup_logger("llama_context")

        # Initialize provider
        self.provider = self._init_provider()

        # Initialize guardrails
        self.guardrails = self._init_guardrails()

        # Initialize multimodal fusion (if enabled)
        self.multimodal_fusion = None
        if self.config.enable_multimodal:
            self.multimodal_fusion = MultimodalFusion()

        # Initialize temporal context memory (if enabled)
        self.context_memory = None
        if self.config.enable_temporal:
            self.context_memory = ContextMemory()

        # Initialize citation generator (if enabled)
        self.citation_generator = None
        if self.config.enable_citations:
            self.citation_generator = CitationGenerator()

        # Initialize adversarial detector (if enabled)
        self.adversarial_detector = None
        if self.config.enable_adversarial_detection:
            self.adversarial_detector = AdversarialDetector()

        self.logger.info("ContextEngine initialized successfully")

    def _init_provider(self) -> BaseProvider:
        """Initialize the appropriate LLM provider based on configuration.

        Returns:
            Initialized provider instance.

        Raises:
            ValueError: If an unsupported provider is specified.
        """
        if self.config.provider == ProviderType.ANTHROPIC:
            return AnthropicProvider(
                api_key=self.config.api_key,
                model=self.config.model,
                max_tokens=self.config.max_context_length,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                timeout=self.config.request_timeout,
                **self.config.additional_params,
            )
        elif self.config.provider == ProviderType.OPENAI:
            return OpenAIProvider(
                api_key=self.config.api_key,
                model=self.config.model,
                max_tokens=self.config.max_context_length,
                temperature=self.config.temperature,
                top_p=self.config.top_p,
                timeout=self.config.request_timeout,
                **self.config.additional_params,
            )
        elif self.config.provider == ProviderType.MOCK:
            return MockProvider()
        else:
            raise ValueError(f"Unsupported provider: {self.config.provider}")

    def _init_guardrails(self) -> List[BaseGuardrail]:
        """Initialize ethical guardrails based on configuration.

        Returns:
            List of initialized guardrail instances.
        """
        guardrails = []

        # Add keyword check guardrail
        guardrails.append(KeywordCheckGuardrail(level=self.config.guardrail_level))

        # Add regex check guardrail
        guardrails.append(RegexCheckGuardrail(level=self.config.guardrail_level))

        # Add LLM verification guardrail for higher strictness levels
        if self.config.guardrail_level in [GuardrailLevel.MEDIUM, GuardrailLevel.HIGH]:
            guardrails.append(
                LLMVerificationGuardrail(provider=self.provider, level=self.config.guardrail_level)
            )

        return guardrails

    async def process_query(
        self,
        query: str,
        images: Optional[List[bytes]] = None,
        context: Optional[Dict[str, Any]] = None,
        search_results: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        """Process a query through the context engine.

        This method handles the complete query processing pipeline:
        1. Check for adversarial patterns
        2. Apply multimodal fusion (if enabled and images provided)
        3. Apply temporal context modeling (if enabled)
        4. Generate response using the LLM provider
        5. Apply ethical guardrails
        6. Generate citations (if enabled and search results provided)

        Args:
            query: User query text.
            images: Optional list of image data to process.
            context: Optional additional context information.
            search_results: Optional search results for citation generation.

        Returns:
            Dictionary containing the processed response and metadata.

        Raises:
            ValueError: If query fails validation or violates guardrails.
        """
        self.logger.info(f"Processing query: {query[:50]}...")
        context = context or {}

        # Check for adversarial patterns
        if self.adversarial_detector:
            is_adversarial, detection_info = self.adversarial_detector.detect(query)
            if is_adversarial:
                self.logger.warning(f"Adversarial pattern detected: {detection_info}")
                return {
                    "response": "I cannot process this query as it contains potentially harmful patterns.",
                    "status": "rejected",
                    "reason": "adversarial_pattern",
                    "detection_info": detection_info,
                }

        # Apply multimodal fusion if enabled and images provided
        if self.multimodal_fusion and images:
            self.logger.info(f"Applying multimodal fusion with {len(images)} images")
            multimodal_context = await self.multimodal_fusion.process(query, images)
            context.update({"multimodal": multimodal_context})

        # Apply temporal context modeling if enabled
        if self.context_memory:
            self.logger.info("Applying temporal context modeling")
            temporal_context = self.context_memory.get_context()
            context.update({"temporal": temporal_context})

        # Prepare the prompt for the LLM
        prompt = self._prepare_prompt(query, context)

        # Generate response using the LLM provider
        raw_response = await self.provider.generate(prompt)

        # Apply ethical guardrails
        for guardrail in self.guardrails:
            is_valid, validation_info = guardrail.validate(query, raw_response)
            if not is_valid:
                self.logger.warning(f"Guardrail violation: {validation_info}")
                return {
                    "response": "I cannot provide the requested information due to ethical constraints.",
                    "status": "rejected",
                    "reason": "guardrail_violation",
                    "validation_info": validation_info,
                }

        # Generate citations if enabled and search results provided
        citations = []
        if self.citation_generator and search_results:
            self.logger.info("Generating citations")
            citations = self.citation_generator.generate(raw_response, search_results)

        # Update temporal context if enabled
        if self.context_memory:
            self.logger.info("Updating temporal context")
            self.context_memory.update(query, raw_response)

        return {
            "response": raw_response,
            "status": "success",
            "citations": citations,
            "metadata": {
                "provider": self.config.provider.value,
                "model": self.config.model,
                "multimodal_applied": bool(self.multimodal_fusion and images),
                "temporal_applied": bool(self.context_memory),
                "citations_generated": bool(citations),
            },
        }

    def _prepare_prompt(self, query: str, context: Dict[str, Any]) -> str:
        """Prepare the prompt for the LLM provider.

        Args:
            query: User query text.
            context: Additional context information.

        Returns:
            Formatted prompt string.
        """
        prompt_parts = []

        # Add system instructions
        prompt_parts.append(
            "You are a helpful assistant. Provide accurate, ethical, and helpful responses."
        )

        # Add multimodal context if available
        if "multimodal" in context:
            prompt_parts.append(f"Image context: {context['multimodal']}")

        # Add temporal context if available
        if "temporal" in context:
            prompt_parts.append(f"Conversation history: {context['temporal']}")

        # Add any other context
        for key, value in context.items():
            if key not in ["multimodal", "temporal"]:
                prompt_parts.append(f"{key}: {value}")

        # Add the query
        prompt_parts.append(f"User query: {query}")

        return "\n\n".join(prompt_parts)


# llama_context/providers/base.py
"""Base class for LLM providers."""

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional


class BaseProvider(ABC):
    """Abstract base class for LLM providers.

    This class defines the interface that all provider implementations must follow.

    Attributes:
        api_key: API key for the provider.
        model: Model name to use with the provider.
        max_tokens: Maximum number of tokens in the response.
        temperature: Sampling temperature for the LLM.
        top_p: Top-p sampling parameter for the LLM.
        timeout: Timeout for API requests in seconds.
    """

    def __init__(
        self,
        api_key: str,
        model: str,
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 0.9,
        timeout: int = 60,
        **kwargs,
    ):
        """Initialize the provider.

        Args:
            api_key: API key for the provider.
            model: Model name to use with the provider.
            max_tokens: Maximum number of tokens in the response.
            temperature: Sampling temperature for the LLM.
            top_p: Top-p sampling parameter for the LLM.
            timeout: Timeout for API requests in seconds.
            **kwargs: Additional provider-specific parameters.
        """
        self.api_key = api_key
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature
        self.top_p = top_p
        self.timeout = timeout
        self.additional_params = kwargs

    @abstractmethod
    async def generate(self, prompt: str) -> str:
        """Generate a response from the LLM.

        Args:
            prompt: Input prompt for the LLM.

        Returns:
            Generated response text.

        Raises:
            Exception: If an error occurs during generation.
        """
        pass

    @abstractmethod
    async def generate_with_json(self, prompt: str, json_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured JSON response from the LLM.

        Args:
            prompt: Input prompt for the LLM.
            json_schema: JSON schema definition for the response.

        Returns:
            Generated response as a structured dictionary.

        Raises:
            Exception: If an error occurs during generation.
        """
        pass

    @abstractmethod
    async def embed(self, text: str) -> list:
        """Generate embeddings for the input text.

        Args:
            text: Input text to embed.

        Returns:
            List of embedding values.

        Raises:
            Exception: If an error occurs during embedding.
        """
        pass


# llama_context/providers/anthropic.py
"""Anthropic Claude provider implementation."""

import json
import logging
from typing import Any, Dict, List, Optional

import anthropic
from anthropic.types import MessageParam

from .base import BaseProvider


class AnthropicProvider(BaseProvider):
    """Anthropic Claude provider implementation.

    This class provides integration with Anthropic's Claude models through
    their official Python SDK.

    Attributes:
        client: Anthropic API client instance.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "claude-3-sonnet-20240229",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 0.9,
        timeout: int = 60,
        **kwargs,
    ):
        """Initialize the Anthropic provider.

        Args:
            api_key: Anthropic API key.
            model: Claude model name.
            max_tokens: Maximum number of tokens in the response.
            temperature: Sampling temperature for the LLM.
            top_p: Top-p sampling parameter for the LLM.
            timeout: Timeout for API requests in seconds.
            **kwargs: Additional Anthropic-specific parameters.
        """
        super().__init__(api_key, model, max_tokens, temperature, top_p, timeout, **kwargs)
        self.client = anthropic.Anthropic(api_key=api_key)
        self.logger = logging.getLogger("llama_context.providers.anthropic")

    async def generate(self, prompt: str) -> str:
        """Generate a response from Claude.

        Args:
            prompt: Input prompt for Claude.

        Returns:
            Generated response text.

        Raises:
            Exception: If an error occurs during generation.
        """
        try:
            # Prepare the message
            system = None
            user = prompt

            # Check if prompt contains a system message
            if prompt.startswith("System:"):
                parts = prompt.split("\n\n", 1)
                if len(parts) > 1:
                    system = parts[0].replace("System:", "").strip()
                    user = parts[1]

            # Create the messages list
            messages: List[MessageParam] = [{"role": "user", "content": user}]

            # Make the API request
            response = await self.client.messages.create(
                model=self.model,
                system=system,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                timeout=self.timeout,
                **self.additional_params,
            )

            return response.content[0].text

        except Exception as e:
            self.logger.error(f"Error generating response from Anthropic: {str(e)}")
            raise

    async def generate_with_json(self, prompt: str, json_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured JSON response from Claude.

        Args:
            prompt: Input prompt for Claude.
            json_schema: JSON schema definition for the response.

        Returns:
            Generated response as a structured dictionary.

        Raises:
            Exception: If an error occurs during generation.
        """
        try:
            # Prepare the message with JSON instruction
            json_instruction = (
                f"Please respond with a JSON object that follows this schema:\n"
                f"{json.dumps(json_schema, indent=2)}\n\n"
                f"Ensure your response is valid JSON and matches the schema exactly."
            )

            full_prompt = f"{prompt}\n\n{json_instruction}"

            # Generate the response
            json_response = await self.generate(full_prompt)

            # Extract the JSON portion
            json_start = json_response.find("{")
            json_end = json_response.rfind("}") + 1

            if json_start >= 0 and json_end > json_start:
                json_str = json_response[json_start:json_end]
                return json.loads(json_str)
            else:
                raise ValueError("Generated response does not contain valid JSON")

        except Exception as e:
            self.logger.error(f"Error generating JSON response from Anthropic: {str(e)}")
            raise

    async def embed(self, text: str) -> list:
        """Generate embeddings for the input text using Claude.

        Args:
            text: Input text to embed.

        Returns:
            List of embedding values.

        Raises:
            Exception: If an error occurs during embedding.
        """
        try:
            response = await self.client.embeddings.create(
                model="claude-3-sonnet-20240229-embeddings",  # Using appropriate embedding model
                input=text,
                **self.additional_params,
            )

            return response.embedding

        except Exception as e:
            self.logger.error(f"Error generating embeddings from Anthropic: {str(e)}")
            raise


# llama_context/providers/openai.py
"""OpenAI provider implementation."""

import json
import logging
from typing import Any, Dict, List, Optional

import openai
from openai import AsyncOpenAI

from .base import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI provider implementation.

    This class provides integration with OpenAI's models through
    their official Python SDK.

    Attributes:
        client: OpenAI API client instance.
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-turbo",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 0.9,
        timeout: int = 60,
        **kwargs,
    ):
        """Initialize the OpenAI provider.

        Args:
            api_key: OpenAI API key.
            model: OpenAI model name.
            max_tokens: Maximum number of tokens in the response.
            temperature: Sampling temperature for the LLM.
            top_p: Top-p sampling parameter for the LLM.
            timeout: Timeout for API requests in seconds.
            **kwargs: Additional OpenAI-specific parameters.
        """
        super().__init__(api_key, model, max_tokens, temperature, top_p, timeout, **kwargs)
        self.client = AsyncOpenAI(api_key=api_key)
        self.logger = logging.getLogger("llama_context.providers.openai")

    async def generate(self, prompt: str) -> str:
        """Generate a response from OpenAI.

        Args:
            prompt: Input prompt for OpenAI.

        Returns:
            Generated response text.

        Raises:
            Exception: If an error occurs during generation.
        """
        try:
            # Prepare the message
            system = "You are a helpful assistant."
            user = prompt

            # Check if prompt contains a system message
            if prompt.startswith("System:"):
                parts = prompt.split("\n\n", 1)
                if len(parts) > 1:
                    system = parts[0].replace("System:", "").strip()
                    user = parts[1]

            # Make the API request
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                timeout=self.timeout,
                **self.additional_params,
            )

            return response.choices[0].message.content

        except Exception as e:
            self.logger.error(f"Error generating response from OpenAI: {str(e)}")
            raise

    async def generate_with_json(self, prompt: str, json_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a structured JSON response from OpenAI.

        Args:
            prompt: Input prompt for OpenAI.
            json_schema: JSON schema definition for the response.

        Returns:
            Generated response as a structured dictionary.

        Raises:
            Exception: If an error occurs during generation.
        """
        try:
            # Prepare the message
            system = "You are a helpful assistant."
            user = prompt

            # Check if prompt contains a system message
            if prompt.startswith("System:"):
                parts = prompt.split("\n\n", 1)
                if len(parts) > 1:
                    system = parts[0].replace("System:", "").strip()
                    user = parts[1]

            # Make the API request with function calling
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
                response_format={"type": "json_object"},
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                top_p=self.top_p,
                timeout=self.timeout,
                **self.additional_params,
            )

            return json.loads(response.choices[0].message.content)

        except Exception as e:
            self.logger.error(f"Error generating JSON response from OpenAI: {str(e)}")
            raise

    async def embed(self, text: str) -> list:
        """Generate embeddings for the input text using OpenAI.

        Args:
            text: Input text to embed.

        Returns:
            List of embedding values.

        Raises:
            Exception: If an error occurs during embedding.
        """
        try:
            response = await self.client.embeddings.create(
                model="text-embedding-3-large", input=text, **self.additional_params
            )

            return response.data[0].embedding

        except Exception as e:
            self.logger.error(f"Error generating embeddings from OpenAI: {str(e)}")
            raise


# llama_context/providers/mock.py
"""Mock provider for testing and development."""

import json
import logging
import random
from typing import Any, Dict, List

from .base import BaseProvider


class MockProvider(BaseProvider):
    """Mock provider for testing and development.

    This class provides a mock implementation of the provider interface
    that returns deterministic responses for testing purposes.
    """

    def __init__(
        self,
        api_key: str = "mock_api_key",
        model: str = "mock_model",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 0.9,
        timeout: int = 60,
        **kwargs,
    ):
        """Initialize the mock provider.

        Args:
            api_key: Mock API key (not used).
            model: Mock model name (not used).
            max_tokens: Maximum number of tokens in the response (not used).
            temperature: Sampling temperature for the LLM (not used).
            top_p: Top-p sampling parameter for the LLM (not used).
            timeout: Timeout for API requests in seconds (not used).
            **kwargs: Additional parameters (not used).
        """
        super().__init__(api_key, model, max_tokens, temperature, top_p, timeout, **kwargs)
        self.logger = logging.getLogger("llama_context.providers.mock")

    async def generate(self, prompt: str) -> str:
        """Generate a mock response.

        Args:
            prompt: Input prompt (not used).

        Returns:
            Predefined mock response.
        """
        self.logger.info("Using mock provider to generate response")

        # Sample responses for different types of queries
        responses = [
            "This is a mock response for testing purposes.",
            "I'm a deterministic mock provider that returns predefined responses.",
            "Your query has been processed by the mock provider.",
            "In a production environment, this would be replaced with a real LLM response.",
        ]

        # Choose a response based on the hash of the prompt for determinism
        index = hash(prompt) % len(responses)
        return responses[index]

    async def generate_with_json(self, prompt: str, json_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a mock JSON response."""
        # In a real implementation, this would call an LLM constrained by the schema
        # Here, we return a placeholder based on the schema keys
        mock_response = {}
        for key, schema_info in json_schema.get("properties", {}).items():
            type = schema_info.get("type")
            if type == "string":
                mock_response[key] = f"Mock string for {key}"
            elif type == "integer":
                mock_response[key] = hash(prompt + key) % 1000
            elif type == "number":
                mock_response[key] = (hash(prompt + key) % 1000) / 100.0
            elif type == "boolean":
                mock_response[key] = (hash(prompt + key) % 2) == 0
            else:
                mock_response[key] = None
        return mock_response


# llama_context/providers/mock.py
"""Mock provider for testing and development."""

import json
import logging
import random
from typing import Any, Dict, List

from .base import BaseProvider


class MockProvider(BaseProvider):
    """Mock provider for testing and development.

    This class provides a mock implementation of the provider interface
    that returns deterministic responses for testing purposes.
    """

    def __init__(
        self,
        api_key: str = "mock_api_key",
        model: str = "mock_model",
        max_tokens: int = 1000,
        temperature: float = 0.7,
        top_p: float = 0.9,
        timeout: int = 60,
        **kwargs,
    ):
        """Initialize the mock provider.

        Args:
            api_key: Mock API key (not used).
            model: Mock model name (not used).
            max_tokens: Maximum number of tokens in the response (not used).
            temperature: Sampling temperature for the LLM (not used).
            top_p: Top-p sampling parameter for the LLM (not used).
            timeout: Timeout for API requests in seconds (not used).
            **kwargs: Additional parameters (not used).
        """
        super().__init__(api_key, model, max_tokens, temperature, top_p, timeout, **kwargs)
        self.logger = logging.getLogger("llama_context.providers.mock")

    async def generate(self, prompt: str) -> str:
        """Generate a mock response.

        Args:
            prompt: Input prompt (not used).

        Returns:
            Predefined mock response.
        """
        self.logger.info("Using mock provider to generate response")

        # Sample responses for different types of queries
        responses = [
            "This is a mock response for testing purposes.",
            "I'm a deterministic mock provider that returns predefined responses.",
            "Your query has been processed by the mock provider.",
            "In a production environment, this would be replaced with a real LLM response.",
        ]

        # Choose a response based on the hash of the prompt for determinism
        index = hash(prompt) % len(responses)
        return responses[index]

    async def generate_with_json(self, prompt: str, json_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a mock JSON response."""
        # In a real implementation, this would call an LLM constrained by the schema
        # Here, we return a placeholder based on the schema keys
        mock_response = {}
        for key, schema_info in json_schema.get("properties", {}).items():
            type = schema_info.get("type")
            if type == "string":
                mock_response[key] = f"Mock string for {key}"
            elif type == "integer":
                mock_response[key] = hash(prompt + key) % 1000
            elif type == "number":
                mock_response[key] = (hash(prompt + key) % 1000) / 100.0
            elif type == "boolean":
                mock_response[key] = (hash(prompt + key) % 2) == 0
            else:
                mock_response[key] = None
        return mock_response
