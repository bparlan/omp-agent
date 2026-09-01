#!/usr/bin/env python3
# {Verification IDs: VI-M12S3-3}
# {Requirement IDs: FR-EVENT_DRIVEN_WATCH_TRIGGER}
# Test Type: SPECIFICATION_CHECK

import sys
from pathlib import Path

REPO_ROOT = next(
    (p for p in Path(__file__).resolve().parents if (p / 'AGENTS.md').exists() or (p / '.git').exists()),
    Path(__file__).resolve().parents[4],
)
DOCS_SKILL = REPO_ROOT / 'skills' / 'manage-docs' / 'SKILL.md'

def fail(msg):
    print(f'FAIL: {msg}')
    sys.exit(1)

def pass_(msg):
    print(f'PASS: {msg}')

def main():
    if not DOCS_SKILL.exists():
        fail(f'{DOCS_SKILL}: file does not exist')
    
    content = DOCS_SKILL.read_text()
    
    # Check for manual trigger procedure documentation
    manual_trigger_indicators = [
        'manual trigger',
        'manual trigger procedure',
        'trigger procedure',
        'scan output format',
        'opt-in activation',
        'auto-scan disabled by default'
    ]
    
    found = False
    for indicator in manual_trigger_indicators:
        if indicator.lower() in content.lower():
            found = True
            break
    
    if not found:
        fail(f'{DOCS_SKILL}: no manual trigger procedure documented')
    
    # Check that auto-scan is disabled by default (not enabled by default)
    if 'auto-scan enabled by default' in content.lower():
        fail(f'{DOCS_SKILL}: auto-scan is enabled by default (must be disabled)')
    
    pass_('Event-driven watch trigger properly specified')

if __name__ == '__main__':
    main()