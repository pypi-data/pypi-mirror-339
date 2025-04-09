"""Provider selection strategies for the LLM integration gateway.

This module implements various strategies for selecting LLM providers based
on different criteria such as cost, latency, and privacy.
"""

import abc
import asyncio
import logging
import time
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

from llama_integrations.gateway import ProviderType
from llama_integrations.providers.base import BaseProvider

logger = logging.getLogger(__name__)


class RoutingStrategy(abc.ABC):
    """Abstract base class for provider selection strategies.

    All routing strategies must inherit from this class to ensure a consistent
    interface.

    Attributes:
        providers: Dictionary mapping provider types to provider instances.
    """

    def __init__(self, providers: Dict[ProviderType, BaseProvider]) -> None:
        """Initialize the strategy with the given providers.

        Args:
            providers: Dictionary mapping provider types to provider instances.
        """
        self.providers = providers

    @abc.abstractmethod
    async def select_provider(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Tuple[ProviderType, BaseProvider]:
        """Select the most appropriate provider for the given request.

        Args:
            prompt: The prompt for completion requests.
            messages: The messages for chat completion requests.
            **kwargs: Additional parameters that may influence selection.

        Returns:
            Tuple of selected provider type and provider instance.
        """
        pass

    async def execute(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute the strategy and return the completion response.

        Args:
            prompt: The prompt to generate a completion for.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            timeout: Request timeout in seconds.
            additional_params: Additional provider-specific parameters.

        Returns:
            The completion response.
        """
        selected_type, selected_provider = await self.select_provider(prompt=prompt)

        logger.debug(
            "Selected provider %s using %s strategy", selected_type, self.__class__.__name__
        )

        return await selected_provider.completion(
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            stop=stop,
            timeout=timeout,
            **(additional_params or {}),
        )

    async def execute_chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute the strategy and return the chat completion response.

        Args:
            messages: List of chat messages, each with 'role' and 'content'.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            timeout: Request timeout in seconds.
            additional_params: Additional provider-specific parameters.

        Returns:
            The chat completion response.
        """
        last_message_content = messages[-1]["content"] if messages else ""
        selected_type, selected_provider = await self.select_provider(
            messages=messages, prompt=last_message_content
        )

        logger.debug(
            "Selected provider %s using %s strategy", selected_type, self.__class__.__name__
        )

        return await selected_provider.chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            stop=stop,
            timeout=timeout,
            **(additional_params or {}),
        )


class CostAwareStrategy(RoutingStrategy):
    """Strategy that selects the provider with the lowest cost.

    This strategy estimates the cost of using each provider for the given
    request and selects the one with the lowest estimated cost.
    """

    async def select_provider(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Tuple[ProviderType, BaseProvider]:
        """Select the provider with the lowest estimated cost.

        Args:
            prompt: The prompt for completion requests.
            messages: The messages for chat completion requests.
            **kwargs: Additional parameters that may influence selection.

        Returns:
            Tuple of selected provider type and provider instance.
        """
        if not self.providers:
            raise ValueError("No providers available")

        # Estimate input token count
        # In a production system, this would use a more accurate tokenizer
        if prompt:
            input_tokens = len(prompt.split()) // 3 + 10  # Rough estimate
        elif messages:
            input_tokens = sum(len(msg["content"].split()) for msg in messages) // 3 + 10
        else:
            input_tokens = 100  # Default estimate

        # Estimate output token count (max_tokens)
        output_tokens = kwargs.get("max_tokens", 1024)

        # Calculate estimated cost for each provider
        costs = {}
        for provider_type, provider in self.providers.items():
            token_costs = provider.cost_per_token
            estimated_cost = (
                input_tokens * token_costs["input"] + output_tokens * token_costs["output"]
            )
            costs[provider_type] = estimated_cost

        # Select the provider with the lowest cost
        selected_type = min(costs, key=costs.get)
        selected_provider = self.providers[selected_type]

        return selected_type, selected_provider


class LatencyAwareStrategy(RoutingStrategy):
    """Strategy that selects the provider with the lowest latency.

    This strategy maintains a running average of response times for each
    provider and selects the one with the lowest expected latency.
    """

    def __init__(self, providers: Dict[ProviderType, BaseProvider]) -> None:
        """Initialize the latency-aware strategy.

        Args:
            providers: Dictionary mapping provider types to provider instances.
        """
        super().__init__(providers)

        # Initialize latency tracking
        self.latency_history: Dict[ProviderType, List[float]] = {
            provider_type: [] for provider_type in providers
        }
        self.latency_averages: Dict[ProviderType, float] = {
            provider_type: 1.0 for provider_type in providers
        }
        self.history_size = 10

    def update_latency(self, provider_type: ProviderType, latency: float) -> None:
        """Update the latency history for a provider.

        Args:
            provider_type: The provider type.
            latency: The measured latency in seconds.
        """
        history = self.latency_history[provider_type]
        history.append(latency)

        # Keep only the most recent measurements
        if len(history) > self.history_size:
            history = history[-self.history_size :]
            self.latency_history[provider_type] = history

        # Update the running average
        self.latency_averages[provider_type] = sum(history) / len(history)

    async def select_provider(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Tuple[ProviderType, BaseProvider]:
        """Select the provider with the lowest expected latency.

        Args:
            prompt: The prompt for completion requests.
            messages: The messages for chat completion requests.
            **kwargs: Additional parameters that may influence selection.

        Returns:
            Tuple of selected provider type and provider instance.
        """
        if not self.providers:
            raise ValueError("No providers available")

        # Select the provider with the lowest average latency
        selected_type = min(self.latency_averages, key=self.latency_averages.get)
        selected_provider = self.providers[selected_type]

        return selected_type, selected_provider

    async def execute(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute the strategy with latency measurement.

        Args:
            prompt: The prompt to generate a completion for.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            timeout: Request timeout in seconds.
            additional_params: Additional provider-specific parameters.

        Returns:
            The completion response.
        """
        selected_type, selected_provider = await self.select_provider(prompt=prompt)

        logger.debug("Selected provider %s using latency-aware strategy", selected_type)

        # Measure latency
        start_time = time.time()

        try:
            response = await selected_provider.completion(
                prompt=prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stream=stream,
                stop=stop,
                timeout=timeout,
                **(additional_params or {}),
            )

            # Update latency metrics
            latency = time.time() - start_time
            self.update_latency(selected_type, latency)

            return response
        except Exception as e:
            # If an error occurs, penalize the provider by adding a high latency
            self.update_latency(selected_type, timeout or 30.0)
            raise

    async def execute_chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute the strategy with latency measurement for chat.

        Args:
            messages: List of chat messages, each with 'role' and 'content'.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            timeout: Request timeout in seconds.
            additional_params: Additional provider-specific parameters.

        Returns:
            The chat completion response.
        """
        last_message_content = messages[-1]["content"] if messages else ""
        selected_type, selected_provider = await self.select_provider(
            messages=messages, prompt=last_message_content
        )

        logger.debug("Selected provider %s using latency-aware strategy", selected_type)

        # Measure latency
        start_time = time.time()

        try:
            response = await selected_provider.chat_completion(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stream=stream,
                stop=stop,
                timeout=timeout,
                **(additional_params or {}),
            )

            # Update latency metrics
            latency = time.time() - start_time
            self.update_latency(selected_type, latency)

            return response
        except Exception as e:
            # If an error occurs, penalize the provider by adding a high latency
            self.update_latency(selected_type, timeout or 30.0)
            raise


class ParallelPrivacyStrategy(RoutingStrategy):
    """Strategy that queries multiple providers in parallel with privacy protection.

    This strategy sends requests to multiple providers simultaneously and
    applies differential privacy techniques to protect user data.
    """

    async def select_provider(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        **kwargs,
    ) -> Tuple[ProviderType, BaseProvider]:
        """This method is not used in the parallel strategy.

        The parallel strategy queries multiple providers simultaneously,
        so it doesn't select a single provider.

        Args:
            prompt: The prompt for completion requests.
            messages: The messages for chat completion requests.
            **kwargs: Additional parameters that may influence selection.

        Returns:
            A placeholder tuple with the first provider.
        """
        if not self.providers:
            raise ValueError("No providers available")

        # Return the first provider as a placeholder
        provider_type = next(iter(self.providers))
        return provider_type, self.providers[provider_type]

    async def execute(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute parallel queries with privacy protection.

        Args:
            prompt: The prompt to generate a completion for.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            timeout: Request timeout in seconds.
            additional_params: Additional provider-specific parameters.

        Returns:
            A merged response from all providers.
        """
        if not self.providers:
            raise ValueError("No providers available")

        # Apply differential privacy to the prompt
        # This is a simplified implementation for demonstration
        privacies = await asyncio.gather(
            *[
                self._query_with_privacy(
                    provider_type,
                    provider,
                    prompt,
                    max_tokens,
                    temperature,
                    top_p,
                    n,
                    stream,
                    stop,
                    timeout,
                    additional_params,
                )
                for provider_type, provider in self.providers.items()
            ]
        )

        # For simplicity, return the first successful response
        for response in privacies:
            if response:
                return response

        raise ValueError("All parallel queries failed")

    async def execute_chat(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        additional_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Execute parallel queries with privacy protection for chat.

        Args:
            messages: List of chat messages, each with 'role' and 'content'.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Top-p sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Stop sequences.
            timeout: Request timeout.
            additional_params: Additional provider-specific parameters.

        Returns:
            A dictionary containing the aggregated response or error information.
        """
        # Placeholder implementation
        logger.info("Executing parallel privacy chat strategy")

        # Logic to split/mask messages and query multiple providers would go here
        # For now, just pick the first provider as a placeholder
        first_provider_type = list(self.providers.keys())[0]
        selected_provider = self.providers[first_provider_type]

        try:
            response = await selected_provider.chat(
                messages=messages,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stream=stream,
                stop=stop,
                timeout=timeout,
                **additional_params if additional_params else {},
            )
            response["provider"] = first_provider_type.value
            return response
        except Exception as e:
            logger.error(f"Parallel privacy chat execution failed: {e}")
            raise
