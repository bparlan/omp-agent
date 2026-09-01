#!/usr/bin/env python3
"""
Custom error classes for artifact system - FR-RESOLVER_IMPLEMENTATION

Implements custom error classes for artifact system operations.
Public interfaces: ArtifactSystemError, ConfigurationError, ValidationError
"""

from typing import List, Any, Optional, Dict
from dataclasses import dataclass, field


@dataclass
class ArtifactSystemError(Exception):
    """Base error class for artifact system errors."""

    error_code: str = "ARTIFACT_SYSTEM_ERROR"
    details: Optional[str] = None

    def __str__(self) -> str:
        return f"ArtifactSystemError: {self.details}"


@dataclass
class ConfigurationError(Exception):
    """Error raised for configuration failures."""

    error_code: str = "CONFIG_ERROR"
    missing_fields: List[str] = field(default_factory=list)
    invalid_values: Dict[str, Any] = field(default_factory=dict)

    def __str__(self) -> str:
        parts = ["ConfigurationError"]
        if self.missing_fields:
            parts.append(f"missing_fields={self.missing_fields}")
        if self.invalid_values:
            parts.append(f"invalid_values={self.invalid_values}")
        return ": ".join(parts)


@dataclass
class ValidationError(Exception):
    """Error raised for metadata validation failures."""

    error_code: str = "VALIDATION_ERROR"
    artifact_identity: Optional[str] = None
    errors: List[str] = field(default_factory=list)
    missing_fields: List[str] = field(default_factory=list)

    def __str__(self) -> str:
        parts = ["ValidationError"]
        if self.artifact_identity:
            parts.append(f"artifact={self.artifact_identity}")
        if self.missing_fields:
            parts.append(f"missing_fields={self.missing_fields}")
        if self.errors:
            parts.append(f"errors={self.errors}")
        return ": ".join(parts)
