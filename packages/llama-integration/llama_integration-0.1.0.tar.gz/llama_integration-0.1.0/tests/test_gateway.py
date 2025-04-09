"""Tests for the AIGateway component.

This module contains tests for the AIGateway component, including provider
selection, request handling, and error handling.
"""

import asyncio
import os
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from llama_integrations.gateway import AIGateway, ProviderType, RoutingStrategy
from llama_integrations.providers.base import BaseProvider


@pytest.fixture
def mock_config_manager():
    """Fixture for a mock ConfigManager."""
    mock_config = MagicMock()
    mock_config.get.return_value = {"enabled": True, "config": {}}
    return mock_config


@pytest.fixture
def mock_provider():
    """Fixture for a mock provider."""
    mock = AsyncMock(spec=BaseProvider)

    # Mock completion method
    mock.completion.return_value = {
        "choices": [
            {
                "text": "This is a test response",
                "index": 0,
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
        "provider": "test",
        "model": "test-model",
    }

    # Mock chat completion method
    mock.chat_completion.return_value = {
        "choices": [
            {
                "message": {
                    "role": "assistant",
                    "content": "This is a test response",
                },
                "index": 0,
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 20,
            "total_tokens": 30,
        },
        "provider": "test",
        "model": "test-model",
    }

    # Mock cost per token property
    mock.cost_per_token = {"input": 0.00001, "output": 0.00003}

    return mock


@pytest.fixture
def mock_router():
    """Fixture for a mock MLXRouter."""
    mock = AsyncMock()
    mock.route_request.return_value = ProviderType.OPENAI
    return mock


@pytest.fixture
def mock_gateway(mock_config_manager, mock_provider, mock_router):
    """Fixture for a mock AIGateway."""
    with patch("llama_integrations.gateway.ConfigManager", return_value=mock_config_manager), patch(
        "llama_integrations.gateway.APIKeyManager"
    ), patch("llama_integrations.gateway.AuditLogger"), patch(
        "llama_integrations.gateway.MLXRouter", return_value=mock_router
    ):

        gateway = AIGateway()

        # Set up mock providers
        gateway.providers = {
            ProviderType.OPENAI: mock_provider,
            ProviderType.ANTHROPIC: mock_provider,
        }

        yield gateway


@pytest.mark.asyncio
async def test_completion_with_specific_provider(mock_gateway, mock_provider):
    """Test completion with a specific provider."""
    response = await mock_gateway.completion(
        prompt="Test prompt",
        provider=ProviderType.OPENAI,
        max_tokens=100,
        temperature=0.7,
    )

    # Check that the provider's completion method was called with the correct arguments
    mock_provider.completion.assert_called_once_with(
        prompt="Test prompt",
        max_tokens=100,
        temperature=0.7,
        top_p=1.0,
        n=1,
        stream=False,
        stop=None,
        timeout=None,
    )

    # Check that the response is as expected
    assert response["choices"][0]["text"] == "This is a test response"
    assert response["provider"] == "test"
    assert response["model"] == "test-model"


@pytest.mark.asyncio
async def test_chat_completion_with_specific_provider(mock_gateway, mock_provider):
    """Test chat completion with a specific provider."""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"},
    ]

    response = await mock_gateway.chat_completion(
        messages=messages,
        provider=ProviderType.OPENAI,
        max_tokens=100,
        temperature=0.7,
    )

    # Check that the provider's chat completion method was called with the correct arguments
    mock_provider.chat_completion.assert_called_once_with(
        messages=messages,
        max_tokens=100,
        temperature=0.7,
        top_p=1.0,
        n=1,
        stream=False,
        stop=None,
        timeout=None,
    )

    # Check that the response is as expected
    assert response["choices"][0]["message"]["content"] == "This is a test response"
    assert response["provider"] == "test"
    assert response["model"] == "test-model"


@pytest.mark.asyncio
async def test_completion_with_routing_strategy(mock_gateway, mock_provider, mock_router):
    """Test completion with a routing strategy."""
    response = await mock_gateway.completion(
        prompt="Test prompt",
        routing_strategy=RoutingStrategy.SINGLE_PROVIDER,
        max_tokens=100,
        temperature=0.7,
    )

    # Check that the router was called
    mock_router.route_request.assert_called_once_with("Test prompt")

    # Check that the provider's completion method was called
    mock_provider.completion.assert_called_once()

    # Check that the response is as expected
    assert response["choices"][0]["text"] == "This is a test response"


@pytest.mark.asyncio
async def test_completion_with_cost_aware_strategy(mock_gateway, mock_provider):
    """Test completion with the cost-aware strategy"""
    mock_provider.name = "provider-b"
    mock_provider.cost_per_token = 0.0001

    response = await mock_gateway.completion(
        prompt="Test prompt",
        provider=ProviderType.OPENAI,
        max_tokens=100,
        temperature=0.7,
    )

    # Check that the provider's completion method was called with the correct arguments
    mock_provider.completion.assert_called_once_with(
        prompt="Test prompt",
        max_tokens=100,
        temperature=0.7,
        top_p=1.0,
        n=1,
        stream=False,
        stop=None,
        timeout=None,
    )

    # Check that the response is as expected
    assert response["choices"][0]["text"] == "This is a test response"
    assert response["provider"] == "test"
    assert response["model"] == "test-model"
