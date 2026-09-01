#!/usr/bin/env python3
# {Verification IDs: VER-M9S3-NFR-BACKWARD_COMPATIBILITY-1}
# {Requirement IDs: NFR-HEALTHCENTER-BACKWARD_COMPATIBILITY}
# Test Type: IMPLEMENTATION_CHECK

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))


def main():
    legacy_dirs = [
        REPO_ROOT / "skills" / "healthcheck",
        REPO_ROOT / "skills" / "health-monitoring",
    ]
    missing = [str(p) for p in legacy_dirs if not p.exists()]
    if missing:
        print("PASS: Legacy health directories have been removed")
        sys.exit(0)

    print("FAIL: Legacy health directories still exist")
    sys.exit(1)


if __name__ == "__main__":
    main()
