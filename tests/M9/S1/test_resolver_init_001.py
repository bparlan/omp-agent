#!/usr/bin/env python3
# {Verification IDs: VER-M9S1V-FR-RESOLVER_INIT-001}
# {Requirement IDs: FR-RESOLVER_INIT}
# Test Type: IMPLEMENTATION_CHECK

import sys
import os

sys.path.insert(0, os.path.join(os.getcwd()))

from core.artifacts.resolution import resolve_artifact


def test_resolver_api():
    data = resolve_artifact(identity="SPEC-M9S1", type="specification")

    assert isinstance(data, dict), "resolve_artifact must return a dictionary"
    assert "resolved" in data, "Resolver response missing 'resolved' field"
    assert data.get("resolved") in (True, False), "'resolved' must be boolean"
    assert "error" in data, "Resolver response missing 'error' field"

    if data.get("resolved") is True:
        artifact = data.get("artifact")
        assert (
            isinstance(artifact, dict) and artifact
        ), "Missing or invalid artifact details"
        print("PASS: Resolver API returned resolved artifact details")
    else:
        error = data.get("error")
        assert isinstance(error, dict), "Error must be a dictionary"
        assert error.get("type") == "ArtifactNotFoundError", "Unexpected error type"
        print("PASS: Resolver API returned structured ambiguity/not-found error")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(test_resolver_api())
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    except Exception as e:
        print("FAIL:", e)
        sys.exit(1)
