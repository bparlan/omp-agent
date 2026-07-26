#!/bin/sh
# ground-truth-check.sh — Read-only live-state verification utility
#
# Usage: ground-truth-check.sh <command> [args]
#
# Commands:
#   file-exists <path>     Check if a file exists (PASS/FAIL)
#   dir-exists <path>      Check if a directory exists (PASS/FAIL)
#   command-exists <name>  Check if a command is on PATH (PASS/FAIL)
#   file-contains <path> <pattern>  Check if file contains literal pattern (PASS/FAIL)
#   git-status [path]      Check git status of a directory (PASS/FAIL)
#
# Strictly read-only — no writes, no mutations, no side effects.
# POSIX shell, no dependencies beyond stdlib.

set -eu

usage() {
    cat <<'EOF'
Usage: ground-truth-check.sh <command> [args]

Commands:
  file-exists <path>       PASS if file exists, FAIL otherwise
  dir-exists <path>        PASS if directory exists, FAIL otherwise
  command-exists <name>    PASS if command is available on PATH, FAIL otherwise
  file-contains <path> <pattern>  PASS if file contains literal pattern, FAIL otherwise
  git-status [path]        Show git status (PASS/FAIL based on repo existence)

Returns exit code 0 on PASS, 1 on FAIL.
EOF
    exit 0
}

if [ $# -eq 0 ] || [ "$1" = "--help" ] || [ "$1" = "-h" ]; then
    usage
fi

CMD="$1"
shift

case "$CMD" in
    file-exists)
        if [ $# -ne 1 ]; then usage; fi
        if [ -f "$1" ]; then
            echo "PASS: file exists: $1"
            exit 0
        else
            echo "FAIL: file not found: $1"
            exit 1
        fi
        ;;
    dir-exists)
        if [ $# -ne 1 ]; then usage; fi
        if [ -d "$1" ]; then
            echo "PASS: directory exists: $1"
            exit 0
        else
            echo "FAIL: directory not found: $1"
            exit 1
        fi
        ;;
    command-exists)
        if [ $# -ne 1 ]; then usage; fi
        if command -v "$1" >/dev/null 2>&1; then
            echo "PASS: command available: $1"
            exit 0
        else
            echo "FAIL: command not found: $1"
            exit 1
        fi
        ;;
    file-contains)
        if [ $# -ne 2 ]; then usage; fi
        path="$1"
        pattern="$2"
        if [ ! -f "$path" ]; then
            echo "FAIL: file not found: $path"
            exit 1
        fi
        if grep -qF -- "$pattern" "$path" 2>/dev/null; then
            echo "PASS: file contains pattern: $path"
            exit 0
        else
            echo "FAIL: pattern not found in file: $path"
            exit 1
        fi
        ;;
    git-status)
        dir="${1:-.}"
        if [ ! -d "$dir" ]; then
            echo "FAIL: directory not found: $dir"
            exit 1
        fi
        if cd "$dir" 2>/dev/null && git status --short 2>/dev/null; then
            echo "PASS: git repository: $dir"
            exit 0
        else
            echo "FAIL: not a git repository: $dir"
            exit 1
        fi
        ;;
    *)
        echo "FAIL: unknown command: $CMD"
        usage
        ;;
esac
