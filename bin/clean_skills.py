#!/usr/bin/env python3
import os
import re
import sys
from pathlib import Path


def clean_content(content: str) -> tuple[str, dict]:
    stats = {
        "brackets_removed": 0,
        "lines_removed": 0,
        "prefixes_stripped": 0,
        "backticks_fixed": 0,
    }

    # 1. Fix 4 backtick quotations (Rule 3)
    # Replaces exactly four backticks ```` with three backticks ```
    backtick_pattern = re.compile(r"(?<!`)````(?!`)")
    matches = backtick_pattern.findall(content)
    if matches:
        stats["backticks_fixed"] += len(matches)
        content = backtick_pattern.sub("```", content)

    # 2. Process line numbers (Rule 2)
    lines = content.splitlines()
    cleaned_lines = []
    for line in lines:
        # If the line consists only of a bracketed number (with optional whitespace)
        if re.match(r"^\s*\[\d+\]\s*$", line):
            stats["lines_removed"] += 1
            continue  # Skip/remove the line completely

        # If the line starts with a bracketed number followed by text (and is not a reference definition like "[97]: url")
        match = re.match(r"^\s*\[\d+\](?!\s*:)\s*(.*)$", line)
        if match:
            stats["prefixes_stripped"] += 1
            cleaned_lines.append(
                match.group(1)
            )  # Keep only the text after the line number
        else:
            cleaned_lines.append(line)
    content = "\n".join(cleaned_lines)

    # 3. Remove NotebookLM reference bracketed numbers (Rule 1)
    # Matches [7], [49], [154, 162] etc when NOT followed by ( or [ to protect links/reference links
    ref_pattern = re.compile(r"\s*\[\d+(?:\s*,\s*\d+)*\](?!\s*[\(\[])")
    matches = ref_pattern.findall(content)
    if matches:
        stats["brackets_removed"] += len(matches)
        content = ref_pattern.sub("", content)

    return content, stats


def clean_file(filepath: Path) -> bool:
    try:
        content = filepath.read_text(encoding="utf-8", errors="ignore")
        cleaned, stats = clean_content(content)

        # Check if any changes were made
        if cleaned != content:
            filepath.write_text(cleaned, encoding="utf-8")
            print(
                f"[HEALED] {filepath.name} -> Brackets removed: {stats['brackets_removed']}, "
                f"Lines removed: {stats['lines_removed']}, "
                f"Prefixes stripped: {stats['prefixes_stripped']}, "
                f"Backticks fixed: {stats['backticks_fixed']}"
            )
            return True
        else:
            print(f"[OK] {filepath.name} is already clean.")
            return False
    except Exception as e:
        print(f"[ERROR] Failed to clean {filepath.name}: {e}", file=sys.stderr)
        return False


def main():
    # Parse CLI target directories or fallback to standard folders
    targets = sys.argv[1:]
    if not targets:
        # Standard default search directories
        default_folders = [
            "./skills",
            "./milestones",
            "/workspace/artifacts",
            "./artifacts",
        ]
        targets = [f for f in default_folders if os.path.exists(f) and os.path.isdir(f)]
        if not targets:
            print(
                "[INFO] No default skill directories found. Scanning current directory recursively."
            )
            targets = ["."]

    print("=========================================================")
    print(" OMP AEF Skill and Document Health Repair Agent")
    print("=========================================================")

    processed_files = 0
    healed_files = 0

    for target in targets:
        target_path = Path(target).resolve()
        if not target_path.exists() or not target_path.is_dir():
            # Gracefully handle partial implementation folders without crashing (Rule 4)
            print(
                f"[SKIP] Directory {target} does not exist or is not a directory. Continuing..."
            )
            continue

        print(f"Scanning directory: {target_path}")
        # Recursively search for all .md files
        md_files = list(target_path.glob("**/*.md"))
        for file in md_files:
            # Skip hidden files or node_modules / .git
            if (
                any(part.startswith(".") for part in file.parts)
                or "node_modules" in file.parts
            ):
                continue
            processed_files += 1
            if clean_file(file):
                healed_files += 1

    print("=========================================================")
    print(" Healing Sweep Completed!")
    print(f" Processed: {processed_files} files, Healed: {healed_files} files.")
    print("=========================================================")


if __name__ == "__main__":
    main()
