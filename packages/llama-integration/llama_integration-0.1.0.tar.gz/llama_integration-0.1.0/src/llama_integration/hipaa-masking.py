"""HIPAA-compliant masking for sensitive information.

This module implements masking of sensitive information in accordance with
HIPAA (Health Insurance Portability and Accountability Act) requirements.
"""

import re
from typing import Dict, List, Optional, Pattern, Union


class HIPAAMasker:
    """HIPAA-compliant masker for sensitive information.

    This class implements masking of protected health information (PHI)
    in accordance with HIPAA requirements.

    Attributes:
        patterns: Dictionary of regex patterns for different PHI types.
        replacements: Dictionary of replacement strings for different PHI types.
    """

    def __init__(self):
        """Initialize the HIPAA masker with default patterns."""
        # Define regex patterns for different PHI types
        self.patterns: Dict[str, Pattern] = {
            # Patient names
            "names": re.compile(r"\b[A-Z][a-z]+ [A-Z][a-z]+\b"),
            # Medical record numbers (MRN)
            "mrn": re.compile(
                r"\b(?:MRN|Medical Record Number|Record Number|Record #|#):?\s*([A-Za-z0-9-]+)\b"
            ),
            # Social Security Numbers (SSN)
            "ssn": re.compile(r"\b(?:\d{3}-\d{2}-\d{4}|\d{9})\b"),
            # Dates related to an individual
            "dates": re.compile(
                r"\b(?:0?[1-9]|1[0-2])[/-](?:0?[1-9]|[12]\d|3[01])[/-](?:19|20)\d{2}\b"
            ),
            # Phone numbers
            "phone": re.compile(r"\b(?:\+?1[-.\s]?)?(?:\(?\d{3}\)?[-.\s]?)\d{3}[-.\s]?\d{4}\b"),
            # Email addresses
            "email": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"),
            # Addresses
            "address": re.compile(
                r"\b\d+\s+[A-Za-z0-9\s,]+(?:Avenue|Lane|Road|Boulevard|Drive|Street|Ave|Ln|Rd|Blvd|Dr|St)\.?\s*,\s*[A-Za-z\s]+,\s*[A-Z]{2}\s*\d{5}(?:-\d{4})?\b"
            ),
            # IP addresses
            "ip": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
            # URLs
            "url": re.compile(r'https?://[^\s<>"]+|www\.[^\s<>"]+'),
            # Medical device identifiers
            "device": re.compile(
                r"\b(?:Device ID|Serial Number|Model Number):?\s*([A-Za-z0-9-]+)\b"
            ),
            # Health plan beneficiary numbers
            "beneficiary": re.compile(
                r"\b(?:Beneficiary|Member|Group|Policy)\s*(?:ID|Number|#):?\s*([A-Za-z0-9-]+)\b"
            ),
            # Account numbers
            "account": re.compile(r"\b(?:Account|Acct)\s*(?:ID|Number|#):?\s*([A-Za-z0-9-]+)\b"),
            # Certificate/license numbers
            "certificate": re.compile(
                r"\b(?:Certificate|License|Cert)\s*(?:ID|Number|#):?\s*([A-Za-z0-9-]+)\b"
            ),
            # Vehicle identifiers
            "vehicle": re.compile(r"\b(?:VIN|Vehicle|License Plate):?\s*([A-Za-z0-9-]+)\b"),
            # Biometric identifiers
            "biometric": re.compile(
                r"\b(?:Fingerprint|Retinal|Iris|Voice|Face|DNA|Biometric)\s*(?:ID|Scan|Print|Sample|Template):?\s*([A-Za-z0-9-]+)\b"
            ),
            # Common medical terms and conditions
            "medical_terms": re.compile(
                r"\b(?:diagnosed with|suffers from|treatment for|medication for|prescribed|dose of)\s+([A-Za-z0-9\s]+)\b",
                re.IGNORECASE,
            ),
        }

        # Define replacement strings for different PHI types
        self.replacements = {
            "names": "[NAME]",
            "mrn": "[MRN]",
            "ssn": "[SSN]",
            "dates": "[DATE]",
            "phone": "[PHONE]",
            "email": "[EMAIL]",
            "address": "[ADDRESS]",
            "ip": "[IP]",
            "url": "[URL]",
            "device": "[DEVICE-ID]",
            "beneficiary": "[BENEFICIARY-ID]",
            "account": "[ACCOUNT-ID]",
            "certificate": "[CERTIFICATE-ID]",
            "vehicle": "[VEHICLE-ID]",
            "biometric": "[BIOMETRIC-ID]",
            "medical_terms": "[MEDICAL-CONDITION]",
        }

    def mask_text(self, text: str) -> str:
        """Apply HIPAA-compliant masking to text.

        Args:
            text: Text to mask.

        Returns:
            Masked text.
        """
        if not text:
            return text

        masked_text = text

        # Apply each pattern in sequence
        for phi_type, pattern in self.patterns.items():
            replacement = self.replacements.get(phi_type, f"[{phi_type.upper()}]")
            masked_text = pattern.sub(replacement, masked_text)

        return masked_text

    def add_pattern(
        self,
        phi_type: str,
        pattern: Union[str, Pattern],
        replacement: Optional[str] = None,
    ) -> None:
        """Add a custom pattern for masking.

        Args:
            phi_type: Type of PHI to mask.
            pattern: Regex pattern as string or compiled Pattern.
            replacement: Replacement string. If None, a default will be used.
        """
        if isinstance(pattern, str):
            pattern = re.compile(pattern)

        self.patterns[phi_type] = pattern

        if replacement:
            self.replacements[phi_type] = replacement
        else:
            self.replacements[phi_type] = f"[{phi_type.upper()}]"

    def remove_pattern(self, phi_type: str) -> None:
        """Remove a pattern from masking.

        Args:
            phi_type: Type of PHI to remove.
        """
        if phi_type in self.patterns:
            del self.patterns[phi_type]

        if phi_type in self.replacements:
            del self.replacements[phi_type]

    def mask_json(self, json_obj: Union[Dict, List]) -> Union[Dict, List]:
        """Recursively mask PHI in a JSON object.

        Args:
            json_obj: JSON object to mask.

        Returns:
            Masked JSON object.
        """
        if isinstance(json_obj, dict):
            return {k: self.mask_json(v) for k, v in json_obj.items()}
        elif isinstance(json_obj, list):
            return [self.mask_json(item) for item in json_obj]
        elif isinstance(json_obj, str):
            return self.mask_text(json_obj)
        else:
            return json_obj
