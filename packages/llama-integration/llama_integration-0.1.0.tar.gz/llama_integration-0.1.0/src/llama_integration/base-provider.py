"""Base provider interface for LLM services.

This module defines the abstract base class that all provider implementations
must inherit from, ensuring a consistent interface across different LLM
providers.
"""

import abc
from typing import Any, Dict, List, Optional, Union


class BaseProvider(abc.ABC):
    """Abstract base class for LLM providers.

    All provider implementations must inherit from this class to ensure a
    consistent interface across different LLM providers.

    Attributes:
        api_key: API key for the provider.
        base_url: Base URL for API requests.
        timeout: Default timeout for requests in seconds.
        default_headers: Default headers to include in all requests.
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> None:
        """Initialize the provider with the given parameters.

        Args:
            api_key: API key for the provider.
            base_url: Base URL for API requests. If None, the default URL for
                the provider will be used.
            timeout: Default timeout for requests in seconds.
            **kwargs: Additional provider-specific parameters.
        """
        self.api_key = api_key
        self.base_url = base_url
        self.timeout = timeout or 60.0
        self.default_headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    @abc.abstractmethod
    async def completion(
        self,
        prompt: str,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate a completion for the given prompt.

        Args:
            prompt: The prompt to generate a completion for.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            timeout: Request timeout in seconds.
            **kwargs: Additional provider-specific parameters.

        Returns:
            The completion response.
        """
        pass

    @abc.abstractmethod
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        timeout: Optional[float] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Generate a chat completion for the given messages.

        Args:
            messages: List of chat messages, each with 'role' and 'content'.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            timeout: Request timeout in seconds.
            **kwargs: Additional provider-specific parameters.

        Returns:
            The chat completion response.
        """
        pass

    @abc.abstractmethod
    def prepare_payload(
        self,
        is_chat: bool,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        top_p: float = 1.0,
        n: int = 1,
        stream: bool = False,
        stop: Optional[Union[str, List[str]]] = None,
        **kwargs,
    ) -> Dict[str, Any]:
        """Prepare the payload for the API request.

        Args:
            is_chat: Whether this is a chat completion request.
            prompt: The prompt for completion requests.
            messages: The messages for chat completion requests.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            top_p: Nucleus sampling parameter.
            n: Number of completions to generate.
            stream: Whether to stream the response.
            stop: Sequences at which to stop generation.
            **kwargs: Additional provider-specific parameters.

        Returns:
            The prepared payload for the API request.
        """
        pass

    @abc.abstractmethod
    def parse_response(
        self,
        response: Dict[str, Any],
        is_chat: bool,
    ) -> Dict[str, Any]:
        """Parse the API response into a standardized format.

        Args:
            response: The raw API response.
            is_chat: Whether this is a chat completion response.

        Returns:
            The parsed response in a standardized format.
        """
        pass

    @property
    @abc.abstractmethod
    def cost_per_token(self) -> Dict[str, float]:
        """Get the cost per token for this provider.

        Returns:
            Dictionary with 'input' and 'output' token costs.
        """
        pass
