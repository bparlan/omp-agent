#!/usr/bin/env python3
# {Verification IDs: VER-M9S1V-FR-LEGACY_COMPAT-001}
# {Requirement IDs: FR-LEGACY_COMPAT}
# Test Type: IMPLEMENTATION_CHECK

import os
import sys

sys.path.insert(0, os.path.join(os.getcwd()))

from core.artifacts.resolution import LEGACY_ARTIFACT_MAPPINGS, _is_canonical_artifact

def test_legacy_compat():
    # LEGACY_ARTIFACT_MAPPINGS exists and is a dict
    assert isinstance(LEGACY_ARTIFACT_MAPPINGS, dict), "LEGACY_ARTIFACT_MAPPINGS must be a dictionary"

    valid_path = os.path.join('tests', 'fixtures', 'synthetic_metadata_valid', 'valid_artifact.md')
    legacy_path = os.path.join('tests', 'fixtures', 'legacy_artifacts', 'LEG-001.md')

    # _is_canonical_artifact should be callable
    assert callable(_is_canonical_artifact), "_is_canonical_artifact is not callable"

    # Call with valid and legacy artifact paths
    valid_result = _is_canonical_artifact(valid_path)
    legacy_result = _is_canonical_artifact(legacy_path)

    assert isinstance(valid_result, bool), "_is_canonical_artifact must return bool"
    assert isinstance(legacy_result, bool), "_is_canonical_artifact must return bool"

    print("PASS: Legacy compatibility structures present and _is_canonical_artifact is callable")
    return 0

if __name__ == '__main__':
    try:
        sys.exit(test_legacy_compat())
    except AssertionError as e:
        print("FAIL:", e)
        sys.exit(1)
    except Exception as e:
        print("FAIL:", e)
        sys.exit(1)
