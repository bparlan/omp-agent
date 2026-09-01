#!/usr/bin/env bash
# {Verification IDs: VER-M9S3-FR-ARTIFACT_CREATION-1}
# {Requirement IDs: FR-HEALTHCENTER-ARTIFACT_CREATION}
# Test Type: IMPLEMENTATION_CHECK

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
FIXTURE_SKILL="${REPO_ROOT}/tests/fixtures/skills/example_skill"
ARTIFACT_DIR="${REPO_ROOT}/milestones/M9"

if [[ ! -d "${FIXTURE_SKILL}" ]]; then
  echo "FAIL: Missing fixture skill at ${FIXTURE_SKILL}"
  exit 1
fi

mkdir -p "${ARTIFACT_DIR}"

# Clean previous artifacts for deterministic run
find "${ARTIFACT_DIR}" -maxdepth 1 -name 'M9-health-check-example_skill.md' -delete || true

set +e
"${REPO_ROOT}/skills/healthcenter/healthcenter.py" --skill example_skill
STATUS=$?
set -e

if [[ ${STATUS} -eq 127 ]]; then
  echo "VALID_INITIAL_FAILURE: healthcenter skill not available yet"
  exit 127
fi

if [[ ${STATUS} -ne 0 ]]; then
  echo "FAIL: healthcenter exited with ${STATUS}"
  exit 1
fi

ARTIFACT="${ARTIFACT_DIR}/M9-health-check-example_skill.md"
if [[ ! -f "${ARTIFACT}" ]]; then
  echo "FAIL: Missing health-check artifact at ${ARTIFACT}"
  exit 1
fi

if ! grep -q '^---$' "${ARTIFACT}"; then
  echo "FAIL: Artifact missing YAML frontmatter delimiter"
  exit 1
fi

if ! grep -q '^type: health-check$' "${ARTIFACT}"; then
  echo "FAIL: Artifact frontmatter missing required type field"
  exit 1
fi

echo "PASS: Single skill health-check artifact created successfully"
exit 0
