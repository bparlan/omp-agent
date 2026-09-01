#!/usr/bin/env python3
# {Verification IDs: VER-M9S3V1-FR6}
# {Requirement IDs: FR-HEALTHCENTER-STORAGE_COMPLIANCE}
# Test Type: PYTHON_TEST

import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT.parent))

def test_storage_compliance_python_api():
    """Test FR6: Storage Compliance using Python API"""
    
    # Import the artifact registry function
    try:
        from core.artifacts.registry import ArtifactRegistry, get_registry
        print("✓ core.artifacts.registry imported successfully")
    except ImportError as e:
        print(f"VALID_INITIAL_FAILURE: core.artifacts.registry not available: {e}")
        sys.exit(127)
    
    # Get the global registry instance
    registry = get_registry()
    assert registry is not None, "Registry instance should not be None"
    
    # Test data based on verification protocol
    artifact_type_name = "health-check"
    expected_storage_pattern = "{milestone_id}/health-checks/{skill_id}-HC-{N}.md"
    expected_pattern = "M9/health-checks/{skill_id}-HC-{N}.md"
    
    # Test 1: Verify storage rule retrieval
    print("Testing storage rule retrieval...")
    try:
        storage_rule = registry.get_type(artifact_type_name)
        print(f"✓ Storage rule retrieved: {storage_rule}")
        
        assert storage_rule is not None, "Storage rule should not be None"
        
        # Verify storage rule structure
        assert "pattern" in storage_rule.storage_rule, "Storage rule should contain pattern"
        assert "naming_conventions" in storage_rule.storage_rule, "Storage rule should contain naming conventions"
        
    except AttributeError as e:
        print(f"VALID_INITIAL_FAILURE: get_type not available: {e}")
        sys.exit(127)
    
    # Test 2: Verify storage pattern matches expected format
    print("Testing storage pattern format...")
    
    # Extract actual pattern from storage rule
    actual_pattern = storage_rule.storage_rule.get("pattern", "")
    assert actual_pattern == expected_pattern, f"Storage pattern mismatch. Expected: {expected_pattern}, Got: {actual_pattern}"
    
    # Test 3: Verify pattern uses correct placeholders
    assert "{milestone_id}" in actual_pattern, "Pattern should contain milestone_id placeholder"
    assert "{skill_id}" in actual_pattern, "Pattern should contain skill_id placeholder"
    assert "{N}" in actual_pattern, "Pattern should contain N placeholder"
    
    # Test 4: Verify naming conventions structure
    naming_conventions = storage_rule.storage_rule.get("naming_conventions", {})
    assert isinstance(naming_conventions, dict), "Naming conventions should be a dict"
    
    # Expected naming conventions components
    expected_conventions = [
        "milestone_id_prefix", "skill_id_prefix", "health_check_suffix", "numbering_scheme"
    ]
    
    for convention in expected_conventions:
        assert convention in naming_conventions, f"Naming convention '{convention}' should be present"
    
    # Test 5: Verify concrete instance path construction
    test_milestone_id = "M9"
    test_skill_id = "healthcenter"
    test_artifact_number = "1"
    
    # Simulate pattern substitution
    constructed_path = actual_pattern.replace("{milestone_id}", test_milestone_id)
    constructed_path = constructed_path.replace("{skill_id}", test_skill_id)
    constructed_path = constructed_path.replace("{N}", test_artifact_number)
    
    expected_constructed_path = "M9/health-checks/healthcenter-HC-1.md"
    assert constructed_path == expected_constructed_path, f"Path construction incorrect. Expected: {expected_constructed_path}, Got: {constructed_path}"
    
    # Test 6: Verify storage rule consistency
    # Storage rule should be consistent with registered type
    assert storage_rule.name == artifact_type_name, "Storage rule type should match artifact type"
    
    # Test 7: Verify storage rule accessibility
    # The storage rule should be retrievable consistently
    storage_rule_again = registry.get_type(artifact_type_name)
    assert storage_rule_again is not None, "Storage rule should be accessible"
    assert storage_rule.storage_rule == storage_rule_again.storage_rule, "Storage rule should be consistent across retrievals"
    
    print("✓ All storage compliance assertions passed")
    sys.exit(0)

if __name__ == "__main__":
    test_storage_compliance_python_api()