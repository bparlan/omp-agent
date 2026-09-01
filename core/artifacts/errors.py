from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AmbiguousResolutionError(Exception):
    """Raised when multiple artifacts match a resolution query."""

    matching_artifacts: List[str] = field(default_factory=list)
    match_criteria: Dict[str, Any] = field(default_factory=dict)
    user_instruction: str = ""

    def __str__(self) -> str:
        return (
            f"AmbiguousResolutionError: {len(self.matching_artifacts)} artifacts matched "
            f"criteria {self.match_criteria}. {self.user_instruction}"
        )


@dataclass
class ValidationError(Exception):
    """Raised when artifact metadata validation fails."""

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


@dataclass
class ArtifactNotFoundError(Exception):
    """Raised when artifact resolution finds no matching artifact."""

    identity: Optional[str] = None
    attempted_path: str = ""
    failure_reason: str = ""

    def __str__(self) -> str:
        return (
            f"ArtifactNotFoundError: identity={self.identity}, "
            f"path={self.attempted_path}, reason={self.failure_reason}"
        )
