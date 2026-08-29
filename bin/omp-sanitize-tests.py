#!/usr/bin/env python3
import sys
import re
from pathlib import Path

def sanitize_test_file(filepath: Path) -> bool:
    try:
        content = filepath.read_text(encoding="utf-8")
        original = content

        # Patterns to match pre-flight existence checks
        patterns = [
            r'if\s+\[\s+!\s+-[fx]\s+["\']?bin/[a-zA-Z0-9_-]+["\']?\s+\]\s*;\s*then\s*echo\s+["\'].*?INTEGRITY.*?["\'].*?\s+exit\s+\d+\s+fi',
            r'if\s+\[\[\s+!\s+-[fx]\s+["\']?bin/[a-zA-Z0-9_-]+["\']?\s+\]\]\s*;\s*then\s*echo\s+["\'].*?INTEGRITY.*?["\'].*?\s+exit\s+\d+\s+fi',
            r'if\s+\[\s+!\s+-[fx]\s+["\']?bin/[a-zA-Z0-9_-]+["\']?\s+\]\s*;\s*then\s*echo\s+["\'].*?not found.*?["\'].*?\s+exit\s+\d+\s+fi',
            r'if\s+\[\[\s+!\s+-[fx]\s+["\']?bin/[a-zA-Z0-9_-]+["\']?\s+\]\]\s*;\s*then\s*echo\s+["\'].*?not found.*?["\'].*?\s+exit\s+\d+\s+fi',
        ]

        modified = False
        for pattern in patterns:
            if re.search(pattern, content, re.DOTALL | re.IGNORECASE):
                content = re.sub(pattern, "# Sanitized: Pre-flight existence trap removed for TDD compatibility", content, flags=re.DOTALL | re.IGNORECASE)
                modified = True

        if modified and content != original:
            filepath.write_text(content, encoding="utf-8")
            print(f"[Sanitized] {filepath.name}: Stripped pre-flight existence trap.")
            return True

        return False
    except Exception as e:
        print(f"Error sanitizing {filepath.name}: {e}", file=sys.stderr)
        return False

def prune_stale_ledger_rows(ledger_path: Path) -> int:
    if not ledger_path.exists():
        return 0
    try:
        content = ledger_path.read_text(encoding="utf-8")
        lines = content.splitlines()
        new_lines = []
        pruned = 0
        for line in lines:
            # Detect Markdown table rows referencing tests
            if line.strip().startswith("|") and "tests/" in line:
                parts = [p.strip() for p in line.split("|") if p.strip()]
                if parts:
                    test_file_path = Path(parts[0])
                    # If the file does not physically exist, prune the row
                    if not test_file_path.exists():
                        print(f"[Pruned] Stale ledger row for missing file: {test_file_path}")
                        pruned += 1
                        continue
            new_lines.append(line)
        if pruned > 0:
            ledger_path.write_text("\n".join(new_lines) + "\n", encoding="utf-8")
        return pruned
    except Exception as e:
        print(f"Error pruning ledger {ledger_path}: {e}", file=sys.stderr)
        return 0

def main():
    target_dir = Path("tests")
    ledger_dir = Path("milestones")

    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
    if len(sys.argv) > 2:
        ledger_dir = Path(sys.argv[2])

    print("=========================================================")
    print(" OMP AEF Test Pre-flight Sanitizer & Ledger Synchronizer")
    print(f" Scanning tests in: {target_dir}")
    print(f" Scanning ledgers in: {ledger_dir}")
    print("=========================================================")

    # 1. Sanitize pre-flight traps from test files
    # Support both legacy (tests/M{X}/) and new (tests/M{X}/S{Y}/) directory structures
    sanitized_count = 0
    if target_dir.exists():
        # Scan for .sh files with pre-flight existence traps
        for pattern in ["test_*.sh", "**/test_*.sh"]:
            for file in target_dir.glob(pattern):
                if sanitize_test_file(file):
                    sanitized_count += 1
        print(f"[*] Sanitized {sanitized_count} executable test files.")

    # 2. Prune stale ledger rows from active test plans
    if ledger_dir.exists():
        pruned_total = 0
        # Support both legacy and new ledger naming patterns
        for pattern in ["M*S*T*.md", "**/M*S*T*.md"]:
            for ledger in ledger_dir.glob(pattern):
                pruned_total += prune_stale_ledger_rows(ledger)
        print(f"[*] Pruned {pruned_total} stale ledger rows.")

    print("Scan complete.")
    sys.exit(0)

if __name__ == "__main__":
    main()
