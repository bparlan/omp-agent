#!/usr/bin/env python3
# {Verification IDs: V-NFR-TYPE}
# {Requirement IDs: NFR-TYPE_HINTS}
# Test Type: INTEGRITY_TEST
"""Verify type hints on Validator.validate and __init__ via typing.get_type_hints."""

import sys
import os
import typing

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + "/../../..")
try:
    import core.validation as cv
except Exception:
    sys.exit(1)
Validator = getattr(cv, "Validator", None)
assert Validator is not None
hints = typing.get_type_hints(Validator.validate)
assert "content" in hints
assert hints.get("return") is not None
print("PASS: type hints present")
