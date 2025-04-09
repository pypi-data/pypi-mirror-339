"""AIGateway provides a unified interface to multiple LLM providers.

This module implements the core gateway that abstracts away the differences
between various LLM providers and offers advanced features like routing,
differential privacy, and comprehensive logging.
"""

import logging
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from llama_integrations.logging.audit import AuditLogger
from llama_integrations.providers.anthropic import AnthropicProvider
from llama_integrations.providers.base import BaseProvider
from llama_integrations.providers.google import GoogleProvider
from llama_integrations.providers.huggingface import HuggingFaceProvider
from llama_integrations.providers.openai import OpenAIProvider
from llama_integrations.routing.router import MLXRouter
from llama_integrations.routing.strategies import (
    CostAwareStrategy,
    LatencyAwareStrategy,
    ParallelPrivacyStrategy,
)
from llama_integrations.security.api_keys import APIKeyManager
from llama_integrations.security.tee import TEEModelServer
from llama_integrations.utils.config import ConfigManager
from llama_integrations.utils.coreml import CoreMLConverter


class ProviderType(Enum):
    """Enum for supported LLM provider types."""

    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    HUGGINGFACE = "huggingface"


class RoutingStrategy(Enum):
    """Enum for supported routing strategies."""

    COST_AWARE = "cost_aware"
    LATENCY_AWARE = "latency_aware"
    PARALLEL_PRIVACY = "parallel_privacy"
    SINGLE_PROVIDER = "single_provider"


class AIGateway:
    """Unified gateway for interacting with multiple LLM providers.

    This class provides a single interface for making requests to different
    LLM providers with advanced features like request routing, differential
    privacy, and comprehensive audit logging.

    Attributes:
        config_manager: Manages configuration for the gateway.
        audit_logger: Handles audit logging for all requests.
        api_key_manager: Securely manages API keys.
        router: Handles routing requests to appropriate providers.
        providers: Dictionary of instantiated provider clients.
        tee_server: Optional TEE model server integration.
    """

    def __init__(
        self,
        config_path: Optional[str] = None,
        enable_tee: bool = False,
        enable_coreml: bool = False,
        log_level: int = logging.INFO,
    ) -> None:
        """Initialize the AIGateway with the specified configuration.

        Args:
            config_path: Path to configuration file. If None, environment
                variables will be used.
            enable_tee: Whether to enable Trusted Execution Environment integration.
            enable_coreml: Whether to enable CoreML conversion for local models.
            log_level: Logging level for the gateway.
        """
        # Initialize configuration management
        self.config_manager = ConfigManager(config_path)

        # Set up logging
        self.audit_logger = AuditLogger(
            log_level=log_level,
            hipaa_compliant=self.config_manager.get("logging.hipaa_compliant", True),
        )

        # Initialize API key management
        self.api_key_manager = APIKeyManager()

        # Initialize routing
        routing_model_path = self.config_manager.get("routing.model_path")
        self.router = MLXRouter(model_path=routing_model_path)

        # Initialize providers
        self.providers = self._initialize_providers()

        # Initialize TEE if enabled
        self.tee_server = None
        if enable_tee:
            tee_config = self.config_manager.get("tee", {})
            self.tee_server = TEEModelServer(**tee_config)

        # Initialize CoreML converter if enabled
        self.coreml_converter = None
        if enable_coreml:
            self.coreml_converter = CoreMLConverter()

        self.audit_logger.log_initialization(
            enabled_providers=list(self.providers.keys()),
            enable_tee=enable_tee,
            enable_coreml=enable_coreml,
        )

    def _initialize_providers(self) -> Dict[ProviderType, BaseProvider]:
        """Initialize provider clients based on configuration.

        Returns:
            Dictionary mapping provider types to provider instances.
        """
        providers = {}

        # Initialize OpenAI if configured
        if self.config_manager.get("providers.openai.enabled", False):
            api_key = self.api_key_manager.get_key(ProviderType.OPENAI)
            providers[ProviderType.OPENAI] = OpenAIProvider(
                api_key=api_key,
                **self.config_manager.get("providers.openai.config", {}),
            )

        # Initialize Anthropic if configured
        if self.config_manager.get("providers.anthropic.enabled", False):
            api_key = self.api_key_manager.get_key(ProviderType.ANTHROPIC)
            providers[ProviderType.ANTHROPIC] = AnthropicProvider(
                api_key=api_key,
                **self.config_manager.get("providers.anthropic.config", {}),
            )

        # Initialize Google if configured
        if self.config_manager.get("providers.google.enabled", False):
            api_key = self.api_key_manager.get_key(ProviderType.GOOGLE)
            providers[ProviderType.GOOGLE] = GoogleProvider(
                api_key=api_key,
                **self.config_manager.get("providers.google.config", {}),
            )

        # Initialize HuggingFace if configured
        if self.config_manager.get("providers.huggingface.enabled", False):
            api_key = self.api_key_manager.get_key(ProviderType.HUGGINGFACE)
            providers[ProviderType.HUGGINGFACE] = HuggingFaceProvider(
                api_key=api_key,
                **self.config_manager.get("providers.huggingface.config", {}),
            )

        return providers

    def _get_strategy(self, strategy_type: RoutingStrategy):
        """Get the appropriate routing strategy based on the specified type.

        Args:
            strategy_type: The routing strategy to use.

        Returns:
            An instance of the specified routing strategy.
        """
        if strategy_type == RoutingStrategy.COST_AWARE:
            return CostAwareStrategy(self.providers)
        elif strategy_type == RoutingStrategy.LATENCY_AWARE:
            return LatencyAwareStrategy(self.providers)
        elif strategy_type == RoutingStrategy.PARALLEL_PRIVACY:
            return ParallelPrivacyStrategy(self.providers)
        else:
            raise ValueError(f"Unsupported routing strategy: {strategy_type}")

    async def completion(
        self,
        prompt: str,
        provider: Optional[ProviderType] = None,
        routing_strategy: RoutingStrategy = RoutingStrategy.COST_AWARE,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        use_tee: bool = False,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate a completion for the given prompt.

        Args:
            prompt: The prompt to generate a completion for.
            provider: Specific provider to use. If None, a provider will be
                selected based on the routing strategy.
            routing_strategy: Strategy to use for selecting a provider if
                provider is None.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            timeout: Request timeout in seconds.
            use_tee: Whether to use the TEE for this request.
            additional_params: Additional provider-specific parameters.

        Returns:
            The completion response.
        """
        request_id = self.audit_logger.log_request_start(
            prompt=prompt,
            provider=provider.value if provider else None,
            routing_strategy=routing_strategy.value,
            max_tokens=max_tokens,
            temperature=temperature,
            use_tee=use_tee,
        )

        try:
            # If provider is specified, use it directly
            if provider is not None:
                if provider not in self.providers:
                    raise ValueError(f"Provider {provider} is not configured")

                selected_provider = self.providers[provider]

                # If TEE is enabled and requested, use it
                if use_tee and self.tee_server:
                    response = await self.tee_server.process_request(
                        provider=selected_provider,
                        prompt=prompt,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        n=n,
                        stream=stream,
                        stop=stop,
                        timeout=timeout,
                        additional_params=additional_params or {},
                    )
                else:
                    response = await selected_provider.completion(
                        prompt=prompt,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        n=n,
                        stream=stream,
                        stop=stop,
                        timeout=timeout,
                        **additional_params or {},
                    )
            else:
                # Use routing strategy to select provider
                if routing_strategy == RoutingStrategy.SINGLE_PROVIDER:
                    # Use MLX router to select a single provider
                    selected_provider_type = await self.router.route_request(prompt)
                    selected_provider = self.providers[selected_provider_type]

                    response = await selected_provider.completion(
                        prompt=prompt,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        n=n,
                        stream=stream,
                        stop=stop,
                        timeout=timeout,
                        **additional_params or {},
                    )
                else:
                    # Use the specified strategy
                    strategy = self._get_strategy(routing_strategy)
                    response = await strategy.execute(
                        prompt=prompt,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        n=n,
                        stream=stream,
                        stop=stop,
                        timeout=timeout,
                        additional_params=additional_params or {},
                    )

            self.audit_logger.log_request_success(request_id=request_id, response=response)
            return response

        except Exception as e:
            self.audit_logger.log_request_error(request_id=request_id, error=str(e))
            raise

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        provider: Optional[ProviderType] = None,
        routing_strategy: RoutingStrategy = RoutingStrategy.COST_AWARE,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        use_tee: bool = False,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Generate a chat completion for the given messages.

        Args:
            messages: List of chat messages, each with 'role' and 'content'.
            provider: Specific provider to use. If None, a provider will be
                selected based on the routing strategy.
            routing_strategy: Strategy to use for selecting a provider if
                provider is None.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            timeout: Request timeout in seconds.
            use_tee: Whether to use the TEE for this request.
            additional_params: Additional provider-specific parameters.

        Returns:
            The chat completion response.
        """
        request_id = self.audit_logger.log_request_start(
            messages=messages,
            provider=provider.value if provider else None,
            routing_strategy=routing_strategy.value,
            max_tokens=max_tokens,
            temperature=temperature,
            use_tee=use_tee,
        )

        try:
            # Similar implementation as completion but for chat interfaces
            if provider is not None:
                if provider not in self.providers:
                    raise ValueError(f"Provider {provider} is not configured")

                selected_provider = self.providers[provider]

                if use_tee and self.tee_server:
                    response = await self.tee_server.process_chat_request(
                        provider=selected_provider,
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        n=n,
                        stream=stream,
                        stop=stop,
                        timeout=timeout,
                        additional_params=additional_params or {},
                    )
                else:
                    response = await selected_provider.chat_completion(
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        n=n,
                        stream=stream,
                        stop=stop,
                        timeout=timeout,
                        **additional_params or {},
                    )
            else:
                # Use routing strategy to select provider
                if routing_strategy == RoutingStrategy.SINGLE_PROVIDER:
                    # For chat, we use the last message content for routing
                    last_message = messages[-1]["content"]
                    selected_provider_type = await self.router.route_request(last_message)
                    selected_provider = self.providers[selected_provider_type]

                    response = await selected_provider.chat_completion(
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        n=n,
                        stream=stream,
                        stop=stop,
                        timeout=timeout,
                        **additional_params or {},
                    )
                else:
                    # Use the specified strategy
                    strategy = self._get_strategy(routing_strategy)
                    response = await strategy.execute_chat(
                        messages=messages,
                        max_tokens=max_tokens,
                        temperature=temperature,
                        top_p=top_p,
                        n=n,
                        stream=stream,
                        stop=stop,
                        timeout=timeout,
                        additional_params=additional_params or {},
                    )

            self.audit_logger.log_request_success(request_id=request_id, response=response)
            return response

        except Exception as e:
            self.audit_logger.log_request_error(request_id=request_id, error=str(e))
            raise
