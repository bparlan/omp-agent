#!/usr/bin/env python3
# {Verification IDs: VI-M12S3-5}
# {Requirement IDs: FR-END_TO_END_CIRCULATION_VALIDATION}
# Test Type: IMPLEMENTATION_CHECK

import sys
from pathlib import Path

REPO_ROOT = next(
    (p for p in Path(__file__).resolve().parents if (p / 'AGENTS.md').exists() or (p / '.git').exists()),
    Path(__file__).resolve().parents[4],
)

VALIDATION_SCRIPT = REPO_ROOT / 'bin' / 'validate-circulation.sh'

def fail(msg):
    print(f'FAIL: {msg}')
    sys.exit(1)

def pass_(msg):
    print(f'PASS: {msg}')

def main():
    if not VALIDATION_SCRIPT.exists():
        fail(f'{VALIDATION_SCRIPT}: Validation script does not exist')

    if not VALIDATION_SCRIPT.is_file():
        fail(f'{VALIDATION_SCRIPT}: Not a file')

    content = VALIDATION_SCRIPT.read_text()
    if len(content.strip()) == 0:
        fail(f'{VALIDATION_SCRIPT}: File is empty')

    if 'AGENTS.md' not in content:
        fail(f'{VALIDATION_SCRIPT}: Does not reference AGENTS.md')

    if '# Validate Circulation' not in content:
        fail(f'{VALIDATION_SCRIPT}: Does not contain expected content')

    pass_('End-to-end circulation validation script exists and contains required content')

if __name__ == '__main__':
    main()