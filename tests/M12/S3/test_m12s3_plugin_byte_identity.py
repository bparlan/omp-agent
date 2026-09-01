#!/usr/bin/env python3
# {Verification IDs: VI-M12S3-6}
# {Requirement IDs: NFR-SCOPE_BOUNDARY_DOCS_ONLY}
# Test Type: INTEGRITY_CHECK

import sys
import hashlib
from pathlib import Path

def fail(msg):
    print(f'FAIL: {msg}')
    sys.exit(1)

def pass_(msg):
    print(f'PASS: {msg}')

def main():
    # Define source and plugin skill paths
    REPO_ROOT = next(
        (p for p in Path(__file__).resolve().parents if (p / 'AGENTS.md').exists() or (p / '.git').exists()),
        Path(__file__).resolve().parents[4],
    )
    
    DEV_SOURCE = REPO_ROOT / 'skills' / 'manage-development' / 'SKILL.md'
    DEV_PLUGIN = Path('/Users/bparlan/.omp/plugins/node_modules/omp-aef/skills/manage-development/SKILL.md')
    
    DOCS_SOURCE = REPO_ROOT / 'skills' / 'manage-docs' / 'SKILL.md'
    DOCS_PLUGIN = Path('/Users/bparlan/.omp/plugins/node_modules/omp-aef/skills/manage-docs/SKILL.md')
    
    # Check if all files exist
    for path, desc in [(DEV_SOURCE, 'manage-development source'),
                      (DEV_PLUGIN, 'manage-development plugin'),
                      (DOCS_SOURCE, 'manage-docs source'),
                      (DOCS_PLUGIN, 'manage-docs plugin')]:
        if not path.exists():
            fail(f'{desc} file does not exist: {path}')
    
    # Compute hashes and compare
    def compute_hash(path):
        with open(path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    
    dev_source_hash = compute_hash(DEV_SOURCE)
    dev_plugin_hash = compute_hash(DEV_PLUGIN)
    
    docs_source_hash = compute_hash(DOCS_SOURCE)
    docs_plugin_hash = compute_hash(DOCS_PLUGIN)
    
    # Verify byte identity
    if dev_source_hash != dev_plugin_hash:
        fail(f'manage-development skill file hash mismatch: source={dev_source_hash}, plugin={dev_plugin_hash}')
    
    if docs_source_hash != docs_plugin_hash:
        fail(f'manage-docs skill file hash mismatch: source={docs_source_hash}, plugin={docs_plugin_hash}')
    
    pass_('Plugin copies are byte-identical to source skill files')

if __name__ == '__main__':
    main()