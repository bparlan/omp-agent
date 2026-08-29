#!/usr/bin/env python3
import os
import sys
import tempfile

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
CORE_PATH = os.path.join(REPO_ROOT, "core")

if CORE_PATH not in sys.path:
    sys.path.insert(0, CORE_PATH)

from core.artifacts.resolution import resolve_artifact, ARTIFACTS_BASE_DIR, _is_canonical_artifact

original_base = ARTIFACTS_BASE_DIR
with tempfile.TemporaryDirectory() as tmpdir:
    try:
        import core.artifacts.resolution as resolution_mod
        resolution_mod.ARTIFACTS_BASE_DIR = os.path.join(tmpdir, "milestones")
        os.makedirs(resolution_mod.ARTIFACTS_BASE_DIR)

        # Create a canonical artifact
        canonical_dir = os.path.join(resolution_mod.ARTIFACTS_BASE_DIR, "M9")
        os.makedirs(canonical_dir)
        canonical_path = os.path.join(canonical_dir, "canonical_m9.md")

        with open(canonical_path, 'w', encoding='utf-8') as f:
            f.write("---\n")
            f.write("id: canonical_m9\n")
            f.write("type: test\n")
            f.write("---\n")
            f.write("This is a canonical artifact with identity.\n")

        print(f"Created canonical artifact at: {canonical_path}")
        print(f"_is_canonical_artifact result: {_is_canonical_artifact(canonical_path)}")

        result = resolve_artifact(identity="canonical_m9", strict=True)
        print(f"Resolution result: {result}")

    finally:
        resolution_mod.ARTIFACTS_BASE_DIR = original_base