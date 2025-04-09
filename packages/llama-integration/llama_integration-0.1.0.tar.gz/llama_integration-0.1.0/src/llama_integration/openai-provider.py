"""OpenAI provider implementation.

This module implements the OpenAI provider for the LLM integration gateway.
"""

from typing import Any, Dict, List, Optional, Union

import aiohttp
from llama_integrations.providers.base import BaseProvider


class OpenAIProvider(BaseProvider):
    """OpenAI API provider implementation.

    This class implements the BaseProvider interface for the OpenAI API.

    Attributes:
        api_key: OpenAI API key.
        base_url: Base URL for API requests.
        timeout: Default timeout for requests in seconds.
        default_headers: Default headers to include in all requests.
        model: Default model to use for requests.
    """

    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        timeout: Optional[float] = None,
        model: str = "gpt-4o",
        organization_id: Optional[str] = None,
        **kwargs,
    ) -> None:
        """Initialize the OpenAI provider.

        Args:
            api_key: OpenAI API key.
            base_url: Base URL for API requests. If None, the default OpenAI
                API URL will be used.
            timeout: Default timeout for requests in seconds.
            model: Default model to use for requests.
            organization_id: OpenAI organization ID.
            **kwargs: Additional provider-specific parameters.
        """
        super().__init__(api_key, base_url, timeout, **kwargs)

        self.base_url = base_url or "https://api.openai.com/v1"
        self.model = model

        # Add organization ID to headers if provided
        if organization_id:
            self.default_headers["OpenAI-Organization"] = organization_id

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
        """Generate a completion using the OpenAI API.

        Note: OpenAI has deprecated the completions endpoint in favor of chat
        completions. This method implements a compatibility layer.

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
        # Convert to chat format for compatibility
        messages = [{"role": "user", "content": prompt}]

        # Use chat completion internally
        response = await self.chat_completion(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            stop=stop,
            timeout=timeout,
            **kwargs,
        )

        # Convert chat response to completion format
        if "choices" in response and response["choices"]:
            for choice in response["choices"]:
                if "message" in choice:
                    choice["text"] = choice["message"]["content"]
                    del choice["message"]

        return response

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
        """Generate a chat completion using the OpenAI API.

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
        timeout = timeout or self.timeout

        # Prepare payload
        payload = self.prepare_payload(
            is_chat=True,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            n=n,
            stream=stream,
            stop=stop,
            **kwargs,
        )

        # Use the pre-configured aiohttp ClientSession to make requests
        async with aiohttp.ClientSession() as session:
            url = f"{self.base_url}/chat/completions"

            async with session.post(
                url, headers=self.default_headers, json=payload, timeout=timeout
            ) as response:
                # Check for errors
                if response.status != 200:
                    error_text = await response.text()
                    raise ValueError(f"Error from OpenAI API: {error_text}")

                # Parse response
                response_json = await response.json()

        # Add request metadata
        response_json["provider"] = "openai"
        response_json["model"] = payload.get("model", self.model)

        # Standardize response format
        return self.parse_response(response_json, is_chat=True)

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
        pass
