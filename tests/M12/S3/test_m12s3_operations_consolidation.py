#!/usr/bin/env python3
# {Verification IDs: VI-M12S3-4}
# {Requirement IDs: FR-OPERATIONS_CONSOLIDATION_ARTIFACT}
# Test Type: INTEGRITY_CHECK

import sys
from pathlib import Path

REPO_ROOT = next(
    (p for p in Path(__file__).resolve().parents if (p / 'AGENTS.md').exists() or (p / '.git').exists()),
    Path(__file__).resolve().parents[4],
)
ARTIFACT_TYPES = REPO_ROOT / 'core' / 'artifacts' / 'artifact_types.py'

def fail(msg):
    print(f'FAIL: {msg}')
    sys.exit(1)

def pass_(msg):
    print(f'PASS: {msg}')

def main():
    if not ARTIFACT_TYPES.exists():
        fail(f'{ARTIFACT_TYPES}: file does not exist')

    content = ARTIFACT_TYPES.read_text()

    if 'operations-consolidation' not in content:
        fail(f'{ARTIFACT_TYPES}: operations-consolidation type not registered')

    if 'canonical_storage_location' not in content.lower():
        fail(f'{ARTIFACT_TYPES}: canonical_storage_location not defined for operations-consolidation')

    required_fields = ['machine_identifier', 'canonical_storage_location', 'required_metadata', 'allowed_relationships']
    missing = [field for field in required_fields if field not in content.lower()]
    if missing:
        fail(f'{ARTIFACT_TYPES}: missing required type fields: {missing}')

    pass_('Operations-consolidation artifact type properly registered')

if __name__ == '__main__':
    main()