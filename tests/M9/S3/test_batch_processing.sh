#!/usr/bin/env bash
# {Verification IDs: VER-M9S3-FR-BATCH_PROCESSING-1}
# {Requirement IDs: FR-HEALTHCENTER-BATCH_PROCESSING}
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

if [[ ${STATUS} -ne 0 ]]; then
  echo "FAIL: healthcenter --all exited with ${STATUS}"
  exit 1
fi

skills=("health_badges" "health_check_report" "processed_skills" "skills-ledger")
for skill in "${skills[@]}"; do
  ARTIFACT="${ARTIFACT_DIR}/M9-health-check-${skill}.md"
  if [[ ! -f "${ARTIFACT}" ]]; then
    echo "FAIL: Missing batch artifact for ${skill} at ${ARTIFACT}"
    exit 1
  fi
done

echo "PASS: Batch processing created health-check artifacts for all skills"
exit 0
