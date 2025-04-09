"""Tests for provider selection strategies.

This module contains tests for the provider selection strategies,
including cost-aware, latency-aware, and parallel privacy strategies.
"""

from unittest.mock import AsyncMock, patch

import pytest
from llama_integrations.gateway import ProviderType
from llama_integrations.providers.base import BaseProvider
from llama_integrations.routing.strategies import (
    CostAwareStrategy,
    LatencyAwareStrategy,
    ParallelPrivacyStrategy,
)


@pytest.fixture
def mock_providers():
    """Fixture for mock providers with different costs."""
    openai_provider = AsyncMock(spec=BaseProvider)
    openai_provider.cost_per_token = {
        "input": 0.00010,
        "output": 0.00030,
    }  # More expensive

    anthropic_provider = AsyncMock(spec=BaseProvider)
    anthropic_provider.cost_per_token = {
        "input": 0.00005,
        "output": 0.00015,
    }  # Less expensive

    google_provider = AsyncMock(spec=BaseProvider)
    google_provider.cost_per_token = {
        "input": 0.00008,
        "output": 0.00025,
    }  # Medium expense

    return {
        ProviderType.OPENAI: openai_provider,
        ProviderType.ANTHROPIC: anthropic_provider,
        ProviderType.GOOGLE: google_provider,
    }


@pytest.mark.asyncio
async def test_cost_aware_strategy_selects_cheapest_provider(mock_providers):
    """Test that the cost-aware strategy selects the cheapest provider."""
    strategy = CostAwareStrategy(mock_providers)

    # Select provider for a request
    provider_type, provider = await strategy.select_provider(
        prompt="This is a test prompt with multiple tokens",
    )

    # Check that the cheapest provider (Anthropic) was selected
    assert provider_type == ProviderType.ANTHROPIC
    assert provider == mock_providers[ProviderType.ANTHROPIC]


@pytest.mark.asyncio
async def test_cost_aware_strategy_executes_with_selected_provider(mock_providers):
    """Test that the cost-aware strategy executes with the selected provider."""
    strategy = CostAwareStrategy(mock_providers)

    # Execute the strategy
    await strategy.execute(
        prompt="This is a test prompt",
        max_tokens=100,
        temperature=0.7,
    )

    # Check that only the cheapest provider's completion method was called
    mock_providers[ProviderType.ANTHROPIC].completion.assert_called_once()
    mock_providers[ProviderType.OPENAI].completion.assert_not_called()
    mock_providers[ProviderType.GOOGLE].completion.assert_not_called()


@pytest.fixture
def mock_providers_with_latency():
    """Fixture for mock providers with latency history."""
    openai_provider = AsyncMock(spec=BaseProvider)
    anthropic_provider = AsyncMock(spec=BaseProvider)
    google_provider = AsyncMock(spec=BaseProvider)

    return {
        ProviderType.OPENAI: openai_provider,
        ProviderType.ANTHROPIC: anthropic_provider,
        ProviderType.GOOGLE: google_provider,
    }


@pytest.mark.asyncio
async def test_latency_aware_strategy_selects_fastest_provider(
    mock_providers_with_latency,
):
    """Test that the latency-aware strategy selects the fastest provider."""
    strategy = LatencyAwareStrategy(mock_providers_with_latency)

    # Set up latency history
    strategy.latency_averages = {
        ProviderType.OPENAI: 1.5,  # Slow
        ProviderType.ANTHROPIC: 0.8,  # Medium
        ProviderType.GOOGLE: 0.5,  # Fast
    }

    # Select provider for a request
    provider_type, provider = await strategy.select_provider()

    # Check that the fastest provider (Google) was selected
    assert provider_type == ProviderType.GOOGLE
    assert provider == mock_providers_with_latency[ProviderType.GOOGLE]


@pytest.mark.asyncio
async def test_latency_aware_strategy_updates_latency_after_completion(
    mock_providers_with_latency,
):
    """Test that the latency-aware strategy updates latency after completion."""
    strategy = LatencyAwareStrategy(mock_providers_with_latency)

    # Set up initial latency history
    strategy.latency_averages = {
        ProviderType.OPENAI: 1.5,
        ProviderType.ANTHROPIC: 0.8,
        ProviderType.GOOGLE: 0.5,
    }

    # Mock the select_provider method to always return Google
    strategy.select_provider = AsyncMock(
        return_value=(
            ProviderType.GOOGLE,
            mock_providers_with_latency[ProviderType.GOOGLE],
        )
    )

    # Mock the time.time function to simulate latency
    with patch("llama_integrations.routing.strategies.time") as mock_time:
        mock_time.time.side_effect = [0, 1.2]  # Start time, end time (1.2s latency)

        # Execute the strategy
        await strategy.execute(
            prompt="This is a test prompt",
            max_tokens=100,
        )

        # Check that the latency was updated
        assert ProviderType.GOOGLE in strategy.latency_history
        assert strategy.latency_history[ProviderType.GOOGLE][-1] == 1.2


@pytest.mark.asyncio
async def test_parallel_privacy_strategy_queries_all_providers(mock_providers):
    """Test that the parallel privacy strategy queries all providers."""
    strategy = ParallelPrivacyStrategy(mock_providers)

    # Mock the _query_with_privacy method to return successful responses
    strategy._query_with_privacy = AsyncMock(
        return_value={
            "choices": [{"text": "This is a privacy-protected response"}],
        }
    )

    # Execute the strategy
    response = await strategy.execute(
        prompt="Sensitive data: SSN 123-45-6789",
        max_tokens=100,
    )

    # Check that _query_with_privacy was called for each provider
    assert strategy._query_with_privacy.call_count == len(mock_providers)

    # Check that the response is as expected
    assert response["choices"][0]["text"] == "This is a privacy-protected response"


@pytest.mark.asyncio
async def test_parallel_privacy_applies_privacy_protection(mock_providers):
    """Test that the parallel privacy strategy applies privacy protection."""
    strategy = ParallelPrivacyStrategy(mock_providers)

    # Test the _apply_differential_privacy method
    sensitive_text = "My SSN is 123-45-6789 and my email is user@example.com"
    protected_text = strategy._apply_differential_privacy(sensitive_text)

    # Check that sensitive information was masked
    assert "123-45-6789" not in protected_text
    assert "user@example.com" not in protected_text
    assert "[SSN]" in protected_text
    assert "[EMAIL]" in protected_text


if __name__ == "__main__":
    pytest.main()
