"""Audit logging implementation with HIPAA-compliant masking.

This module implements comprehensive audit logging for all LLM requests
and responses, with HIPAA-compliant masking of sensitive information.
"""

import datetime
import json
import logging
import os
import uuid
from typing import Any, Dict, List, Optional, Union

from llama_integrations.logging.masking import HIPAAMasker

logger = logging.getLogger(__name__)


class AuditLogger:
    """Comprehensive audit logger for LLM requests and responses.

    This class implements logging for all LLM requests and responses,
    with optional HIPAA-compliant masking of sensitive information.

    Attributes:
        log_dir: Directory for audit log files.
        hipaa_compliant: Whether to apply HIPAA-compliant masking.
        masker: HIPAA-compliant masker instance.
        logger: Logger instance.
    """

    def __init__(
        self,
        log_dir: Optional[str] = None,
        hipaa_compliant: bool = True,
        log_level: int = logging.INFO,
        log_format: Optional[str] = None,
    ):
        """Initialize the audit logger.

        Args:
            log_dir: Directory for audit log files. If None, logs will be
                written to stdout only.
            hipaa_compliant: Whether to apply HIPAA-compliant masking.
            log_level: Logging level.
            log_format: Log format string.
        """
        self.log_dir = log_dir
        self.hipaa_compliant = hipaa_compliant

        # Initialize the masker if HIPAA compliance is required
        self.masker = HIPAAMasker() if hipaa_compliant else None

        # Configure logging
        self.logger = logging.getLogger("llama_integrations.audit")
        self.logger.setLevel(log_level)

        # Create log directory if needed
        if log_dir:
            os.makedirs(log_dir, exist_ok=True)

            # Add file handler
            file_handler = logging.FileHandler(
                os.path.join(log_dir, f"audit_{datetime.datetime.now().strftime('%Y%m%d')}.log")
            )
            file_handler.setLevel(log_level)

            # Set formatter
            formatter = logging.Formatter(
                log_format or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            file_handler.setFormatter(formatter)

            self.logger.addHandler(file_handler)

    def log_initialization(
        self,
        enabled_providers: List[str],
        enable_tee: bool,
        enable_coreml: bool,
    ) -> None:
        """Log initialization of the gateway.

        Args:
            enabled_providers: List of enabled provider names.
            enable_tee: Whether TEE integration is enabled.
            enable_coreml: Whether CoreML conversion is enabled.
        """
        self.logger.info(
            "Gateway initialized with providers: %s, TEE: %s, CoreML: %s",
            enabled_providers,
            enable_tee,
            enable_coreml,
        )

    def log_request_start(
        self,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
        provider: Optional[str] = None,
        routing_strategy: Optional[str] = None,
        max_tokens: int = 1024,
        temperature: float = 0.7,
        use_tee: bool = False,
    ) -> str:
        """Log the start of a request.

        Args:
            prompt: The prompt for completion requests.
            messages: The messages for chat completion requests.
            provider: The provider name if specified.
            routing_strategy: The routing strategy name if used.
            max_tokens: Maximum number of tokens to generate.
            temperature: Sampling temperature.
            use_tee: Whether TEE is used for this request.

        Returns:
            Request ID.
        """
        request_id = str(uuid.uuid4())

        # Apply HIPAA masking if needed
        masked_prompt = None
        masked_messages = None

        if prompt and self.hipaa_compliant and self.masker:
            masked_prompt = self.masker.mask_text(prompt)
        else:
            masked_prompt = prompt

        if messages and self.hipaa_compliant and self.masker:
            masked_messages = []
            for message in messages:
                masked_message = self.masker.mask(message)
                masked_messages.append(masked_message)
            messages = masked_messages
