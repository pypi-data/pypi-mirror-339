"""Tests for API key management.

This module contains tests for the API key manager and related security
components.
"""

import os
from unittest.mock import patch

import pytest
from llama_integrations.gateway import ProviderType
from llama_integrations.security.api_keys import APIKeyManager, SecretVault


@pytest.fixture
def mock_env_vars():
    """Fixture for setting up mock environment variables."""
    env_vars = {
        "OPENAI_API_KEY": "test-openai-key",
        "ANTHROPIC_API_KEY": "test-anthropic-key",
        "GOOGLE_API_KEY": "test-google-key",
        "HUGGINGFACE_API_KEY": "test-huggingface-key",
    }

    with patch.dict(os.environ, env_vars):
        yield


@pytest.fixture
def api_key_manager():
    """Fixture for an API key manager."""
    return APIKeyManager()


def test_get_key_from_environment(mock_env_vars, api_key_manager):
    """Test getting an API key from environment variables."""
    # Get a key for OpenAI
    openai_key = api_key_manager.get_key(ProviderType.OPENAI)

    # Check that the key is correct
    assert openai_key == "test-openai-key"

    # Get a key for Anthropic
    anthropic_key = api_key_manager.get_key(ProviderType.ANTHROPIC)

    # Check that the key is correct
    assert anthropic_key == "test-anthropic-key"


def test_key_caching(mock_env_vars, api_key_manager):
    """Test that API keys are cached."""
    # Get a key for OpenAI
    api_key_manager.get_key(ProviderType.OPENAI)

    # Check that the key is cached
    assert ProviderType.OPENAI in api_key_manager._keys
    assert api_key_manager._keys[ProviderType.OPENAI] == "test-openai-key"


def test_missing_key_raises_error(api_key_manager):
    """Test that a missing API key raises an error."""
    with pytest.raises(ValueError, match="API key for openai not found"):
        api_key_manager.get_key(ProviderType.OPENAI)


def test_clear_cache(mock_env_vars, api_key_manager):
    """Test clearing the API key cache."""
    # Get a key for OpenAI to populate the cache
    api_key_manager.get_key(ProviderType.OPENAI)

    # Clear the cache
    api_key_manager.clear_cache()

    # Check that the cache is empty
    assert not api_key_manager._keys


def test_rotate_keys(mock_env_vars, api_key_manager):
    """Test rotating API keys."""
    # Get a key for OpenAI to populate the cache
    api_key_manager.get_key(ProviderType.OPENAI)

    # Rotate keys
    api_key_manager.rotate_keys()

    # Check that the cache is empty
    assert not api_key_manager._keys


def test_secret_vault_initialization():
    """Test initializing a secret vault."""
    vault = SecretVault()

    # Check initial state
    assert vault.vault_path is None
    assert not vault.is_encrypted
    assert not vault._secrets


def test_secret_vault_set_get_secret():
    """Test setting and getting a secret in the vault."""
    vault = SecretVault()

    # Set a secret
    vault.set_secret("test-key", "test-value")

    # Get the secret
    value = vault.get_secret("test-key")

    # Check that the value is correct
    assert value == "test-value"


def test_secret_vault_delete_secret():
    """Test deleting a secret from the vault."""
    vault = SecretVault()

    # Set a secret
    vault.set_secret("test-key", "test-value")

    # Delete the secret
    vault.delete_secret("test-key")

    # Check that the secret is gone
    assert vault.get_secret("test-key") is None


def test_secret_vault_list_secrets():
    """Test listing secrets in the vault."""
    vault = SecretVault()

    # Set secrets
    vault.set_secret("key1", "value1")
    vault.set_secret("key2", "value2")

    # List secrets
    secrets = vault.list_secrets()

    # Check the secrets
    assert secrets == {"key1": "value1", "key2": "value2"}


def test_secret_vault_encrypt_decrypt():
    """Test encrypting and decrypting content in the vault."""
    vault = SecretVault(encryption_key="test-key")

    # Encrypt some content
    plaintext = "This is a test"
    ciphertext = vault._encrypt(plaintext)

    # Check that the ciphertext is different from the plaintext
    assert ciphertext != plaintext

    # Decrypt the ciphertext
    decrypted = vault._decrypt(ciphertext)

    # Check that the decrypted text matches the original plaintext
    assert decrypted == plaintext


if __name__ == "__main__":
    pytest.main()
