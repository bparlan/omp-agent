#!/bin/bash
# Code Search wrapper for Oh My Pi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ "$1" = "--skeletons" ]; then
    python3 "$SCRIPT_DIR/code_indexer.py" --skeletons
elif [ "$1" = "--search" ]; then
    shift
    python3 "$SCRIPT_DIR/code_indexer.py" --search "$@"
elif [ "$1" = "--refresh" ]; then
    python3 "$SCRIPT_DIR/code_indexer.py"
else
    echo "Usage: $0 --skeletons | --search \"query\" | --refresh"
fi