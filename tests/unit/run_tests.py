import os
import sys
import subprocess

# Add current directory to PYTHONPATH
sys.path.insert(0, "/Users/bparlan/devcode/aef/agent")


def run_test(test_name):
    test_path = f"tests/M9/S1/{test_name}"

    if test_name.endswith(".py"):
        cmd = [sys.executable, test_path]
        env = os.environ.copy()
        env["PYTHONPATH"] = "/Users/bparlan/devcode/aef/agent:" + env.get(
            "PYTHONPATH", ""
        )
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)
    else:
        cmd = ["bash", test_path]
        env = os.environ.copy()
        env["PYTHONPATH"] = "/Users/bparlan/devcode/aef/agent:" + env.get(
            "PYTHONPATH", ""
        )
        result = subprocess.run(cmd, capture_output=True, text=True, env=env)

    return result.returncode == 0, result.stdout, result.stderr


# Tests from ledger
tests = [
    "test_vi1_validate_missing_keys.py",
    "test_vi2_ambiguous_resolution.py",
    "test_vi3_artifact_creation.sh",
    "test_vi4_invalid_artifact_failure.sh",
    "test_vi5_milestone_explicit_identity.py",
    "test_vi6_relationship_fields.py",
    "test_vi7_legacy_strict_flag.py",
    "test_vi8_type_consistency.py",
    "test_vi9_verify_metadata_cli.py",
    "test_vi9b_verify_traceability_cli.py",
    "test_vi10_performance_threshold.sh",
    "test_vi11_generated_test_canonical_reference.py",
    "test_vi12_legacy_migration_safety.py",
]

results = []
for test in tests:
    print(f"Running {test}...")
    success, stdout, stderr = run_test(test)
    print(f"Success: {success}")
    if not success:
        print(f"Stdout: {stdout[:200]}...")
        print(f"Stderr: {stderr[:200]}...")
    print()
