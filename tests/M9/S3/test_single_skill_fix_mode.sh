#!/usr/bin/env bash
# {Verification IDs: VER-M9S3-FR-SINGLE_SKILL-1}
# {Requirement IDs: FR-HEALTHCENTER-SINGLE_SKILL}
# Test Type: IMPLEMENTATION_CHECK

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
ARTIFACT_DIR="${REPO_ROOT}/milestones/M9"

mkdir -p "${ARTIFACT_DIR}"

cleanup_artifacts() {
  find "${ARTIFACT_DIR}" -maxdepth 1 -name 'M9-health-check-example_skill_noncompliant.md' -delete || true
}
trap cleanup_artifacts EXIT
cleanup_artifacts

set +e
"${REPO_ROOT}/skills/healthcenter/healthcenter.py" --skill example_skill_noncompliant --fix
STATUS=$?
set -e

if [[ ${STATUS} -eq 127 ]]; then
  echo "VALID_INITIAL_FAILURE: healthcenter skill not available yet"
  exit 127
fi

if [[ ${STATUS} -ne 0 ]]; then
  echo "FAIL: healthcenter --fix exited with ${STATUS}"
  exit 1
fi

ARTIFACT="${ARTIFACT_DIR}/M9-health-check-example_skill_noncompliant.md"
if [[ ! -f "${ARTIFACT}" ]]; then
  echo "FAIL: Missing health-check artifact for noncompliant skill at ${ARTIFACT}"
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

echo "PASS: Single skill --fix mode completed and artifact was created"
exit 0
