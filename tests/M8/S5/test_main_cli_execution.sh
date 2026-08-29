#!/bin/bash
# V-001 V-002
# FR-MAIN_ORCHESTRATION FR-MAIN_BACKWARD_COMPAT
# Test Type: IMPLEMENTATION_CHECK

set -euo pipefail

MAIN_PY="main.py"

echo "==> Testing $MAIN_PY --help"
python3 "$MAIN_PY" --help

echo "==> Testing $MAIN_PY (no args)"
python3 "$MAIN_PY"

echo "==> Testing $MAIN_PY --all"
python3 "$MAIN_PY" --all

echo "==> Testing $MAIN_PY <skill_name>"
python3 "$MAIN_PY" healthcheck

echo "==> All CLI execution tests passed"
