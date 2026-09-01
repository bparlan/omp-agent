#!/usr/bin/env python3
# {Verification IDs: V-FR-Y}
# {Requirement IDs: FR-DISCOVERY_ERROR_TOLERANCE}
# Test Type: IMPLEMENTATION_CHECK

import pytest


def test_DiscoveryError_exception_subclass():
    """VI-13: DiscoveryError is an Exception subclass."""

    # Import the module under test
    from discovery import DiscoveryError

    # Verify the class is importable
    assert isinstance(
        DiscoveryError, type
    ), f"Expected class type, got {type(DiscoveryError)}"

    # Verify it's a subclass of Exception
    assert issubclass(
        DiscoveryError, Exception
    ), "DiscoveryError should be a subclass of Exception"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
