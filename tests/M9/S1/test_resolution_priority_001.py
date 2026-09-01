#!/usr/bin/env python3
# {Verification IDs: VER-M9S1V-NFR-RESOLUTION_PRIORITY-001}
# {Requirement IDs: NFR-RESOLUTION_PRIORITY}
# Test Type: IMPLEMENTATION_CHECK

import sys
import os

sys.path.insert(0, os.path.join(os.getcwd()))

from core.artifacts.resolution import resolve_artifact


def test_resolution_priority():
    data = resolve_artifact(identity="SPEC-M9S1", type="specification", strict=False)

    assert isinstance(data, dict), "resolve_artifact must return a dictionary"
    assert "resolved" in data, "Resolver response missing 'resolved' field"

    if data.get("resolved") is True:
        artifact = data.get("artifact")
        assert (
            isinstance(artifact, dict) and artifact
        ), "Missing or invalid artifact details"
        print("PASS: Resolver returned canonical artifact details")
    else:
        error = data.get("error")
        assert isinstance(error, dict), "Error must be a dictionary"
        assert "type" in error, "Error missing 'type' field"
        assert "options" not in error or isinstance(
            error.get("options"), list
        ), "If present, options must be a list"
        print("PASS: Resolver returned structured error when no artifact matches")

    return 0


if __name__ == "__main__":
    try:
        sys.exit(test_resolution_priority())
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    except Exception as e:
        print("FAIL:", e)
        sys.exit(1)
