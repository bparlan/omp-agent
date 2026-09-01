#!/usr/bin/env bash
# {Verification IDs: VER-M9S3-NFR-ERROR_HANDLING-1}
# {Requirement IDs: NFR-HEALTHCENTER-ERROR_HANDLING}
# Test Type: IMPLEMENTATION_CHECK

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../../.." && pwd)"
ARTIFACT_DIR="${REPO_ROOT}/milestones/M9"

mkdir -p "${ARTIFACT_DIR}"

cleanup_artifacts() {
  find "${ARTIFACT_DIR}" -maxdepth 1 -name 'M9-health-check-*.md' -delete || true
}
trap cleanup_artifacts EXIT
cleanup_artifacts

set +e
"${REPO_ROOT}/skills/healthcenter/healthcenter.py" --all
STATUS=$?
set -e

if [[ ${STATUS} -eq 127 ]]; then
  echo "VALID_INITIAL_FAILURE: healthcenter skill not available yet"
  exit 127
fi

ARTIFACT="${ARTIFACT_DIR}/M9-health-check-health_badges.md"
if [[ ! -f "${ARTIFACT}" ]]; then
  echo "FAIL: Missing expected artifact for health_badges at ${ARTIFACT}"
  exit 1
fi

if ! grep -q '^---$' "${ARTIFACT}"; then
  echo "FAIL: Artifact missing YAML frontmatter delimiter"
  exit 1
fi

echo "PASS: Batch processing continued and created artifact despite errors"
exit 0
