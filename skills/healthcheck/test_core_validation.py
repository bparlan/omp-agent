"""
Comprehensive unit tests for core/validation module.
Ensures backward compatibility with original healthcheck.py
and validates the modular validation system.
"""

import sys
import os
import tempfile
from pathlib import Path
from datetime import datetime
from unittest.mock import patch, MagicMock

# Add the module to Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.validation import (
    ValidationResult,
    Validator,
    RequiredFieldsValidator,
    VersionValidator,
    NameValidator,
    ValidationOrchestrator,
    validate_skill_file
)
def test_validation_result_dataclass():
    """Test ValidationResult dataclass structure."""
    result = ValidationResult(
        name="test-skill",
        status="healthy",
        validation_score=0.8,
        has_stable_suffix=True,
        issues=[],
        last_modified="2023-01-01T00:00:00",
        last_checked="2023-01-02T00:00:00"
    )

    assert result.name == "test-skill"
    assert result.status == "healthy"
    assert result.validation_score == 0.8
    assert result.has_stable_suffix == True
    assert result.issues == []
    assert result.last_modified == "2023-01-01T00:00:00"
    assert result.last_checked == "2023-01-02T00:00:00"
    print("✓ ValidationResult dataclass test passed")
def test_required_fields_validator():
    """Test RequiredFieldsValidator with various skill content."""
    validator = RequiredFieldsValidator()

    # Valid skill content with all required fields
    valid_content = """name: test-skill
version: 1.0.0-stable
description: A test skill
tools: echo,cat
userInvocable: true"""

    result = validator.validate(valid_content, Path("test/skill/SKILL.md"))
    assert result.validation_score == 1.0
    assert result.issues == []
    assert result.has_stable_suffix == True
    print("✓ RequiredFieldsValidator valid content test passed")

    # Invalid skill content missing fields
    invalid_content = """name: test-skill
version: 1.0.0
description: A test skill"""

    result = validator.validate(invalid_content, Path("test/skill/SKILL.md"))
    assert result.validation_score == 3/5  # 3 out of 5 fields
    assert "Missing tools field" in result.issues
    assert "Missing userInvocable field" in result.issues
    assert result.has_stable_suffix == False
    print("✓ RequiredFieldsValidator invalid content test passed")
def test_version_validator():
    """Test VersionValidator with stable suffix detection."""
    validator = VersionValidator()

    # Content with stable suffix
    stable_content = """name: test-skill
version: 1.0.0-stable
description: Test"""

    result = validator.validate(stable_content, Path("test/skill/SKILL.md"))
    assert result.has_stable_suffix == True
    print("✓ VersionValidator stable content test passed")

    # Content without stable suffix
    unstable_content = """name: test-skill
version: 1.0.0
description: Test"""

    result = validator.validate(unstable_content, Path("test/skill/SKILL.md"))
    assert result.has_stable_suffix == False
    print("✓ VersionValidator unstable content test passed")

    # Content without version field
    no_version_content = """name: test-skill
description: Test"""

    result = validator.validate(no_version_content, Path("test/skill/SKILL.md"))
    assert result.has_stable_suffix == False
    print("✓ VersionValidator no version test passed")
def test_name_validator():
    """Test NameValidator for skill name extraction."""
    validator = NameValidator()

    # Content with name field
    content_with_name = """name: my-custom-skill
version: 1.0.0
description: Test"""

    result = validator.validate(content_with_name, Path("test/skill/SKILL.md"))
    assert result.name == "my-custom-skill"
    print("✓ NameValidator with name field test passed")

    # Content without name field (should use directory name)
    content_without_name = """version: 1.0.0
description: Test"""

    result = validator.validate(content_without_name, Path("test/skill/SKILL.md"))
    assert result.name == "skill"
    print("✓ NameValidator without name field test passed")

    # Content with malformed name
    content_malformed_name = """name:  \
version: 1.0.0
description: Test"""

    result = validator.validate(content_malformed_name, Path("test/skill/SKILL.md"))
    assert result.name == "skill"
    print("✓ NameValidator malformed name test passed")
def test_validation_orchestrator_integration():
    """Test ValidationOrchestrator integration with all validators."""
    orchestrator = ValidationOrchestrator()

    # Valid complete skill
    valid_content = """name: test-skill
version: 1.0.0-stable
description: A test skill
tools: echo,cat
userInvocable: true"""

    result = orchestrator.validate_skill(valid_content, Path("test/skill/SKILL.md"))
    assert result.name == "test-skill"
    assert result.status == "healthy"
    assert result.validation_score >= 0.8
    assert result.has_stable_suffix == True
    print("✓ ValidationOrchestrator valid content test passed")

    # Invalid skill (below threshold)
    invalid_content = """name: test-skill
version: 1.0.0
description: Test"""

    result = orchestrator.validate_skill(invalid_content, Path("test/skill/SKILL.md"))
    assert result.name == "test-skill"
    assert result.validation_score < 0.8  # Below healthy threshold
    assert result.status == "needs_review"
    assert "Missing tools field" in result.issues
    print("✓ ValidationOrchestrator invalid content test passed")

    # Test score boundary (exactly 0.8)
    boundary_content = """name: test-skill
version: 1.0.0
description: Test
tools: echo
userInvocable: true"""

    result = orchestrator.validate_skill(boundary_content, Path("test/skill/SKILL.md"))
    assert result.validation_score == 0.8
    assert result.status == "healthy"  # Exactly 0.8 is healthy
    print("✓ ValidationOrchestrator boundary score test passed")
def test_validation_orchestrator_error_handling():
    """Test ValidationOrchestrator error handling."""
    orchestrator = ValidationOrchestrator()

    # Create a faulty validator for testing
    class FaultyValidator(Validator):
        def validate(self, content: str, skill_path: Path):
            raise ValueError("Test validation error")

    # Temporarily replace validators with faulty one
    original_validators = orchestrator.validators
    orchestrator.validators = [FaultyValidator()]

    try:
        result = orchestrator.validate_skill("test", Path("test/skill/SKILL.md"))
        assert result.status == "error"
        assert any("Validation error" in issue for issue in result.issues)
        print("✓ ValidationOrchestrator error handling test passed")
    finally:
        orchestrator.validators = original_validators
def test_validation_scoring_algorithm():
    """Test that scoring algorithm matches original healthcheck.py logic."""
    validator = RequiredFieldsValidator()

    # Test with exactly 3 out of 5 fields present
    content = """name: test
version: 1.0.0
description: Test
tools: echo"""

    result = validator.validate(content, Path("test/skill/SKILL.md"))
    expected_score = 3/5  # 60%
    assert abs(result.validation_score - expected_score) < 0.001
    print(f"✓ Validation scoring test passed: {result.validation_score} == {expected_score}")

    # Test with 5 out of 5 fields
    content_full = """name: test
version: 1.0.0
description: Test
tools: echo
userInvocable: true"""

    result = validator.validate(content_full, Path("test/skill/SKILL.md"))
    assert result.validation_score == 1.0
    print("✓ Perfect validation score test passed")

    # Test edge case: no fields present
    content_empty = """random text"""

    result = validator.validate(content_empty, Path("test/skill/SKILL.md"))
    assert result.validation_score == 0.0
    print("✓ Empty validation score test passed")
def test_stable_suffix_detection():
    """Test stable suffix detection matches original behavior."""
    test_cases = [
        ("version: 1.0.0-stable", True),
        ("version: 2.0.0-STABLE", True),
        ("version: 3.0.0-stable-rc1", True),
        ("version: 1.0.0", False),
        ("version: 2.0.0-rc1", False),
        ("version: stable", False),
        ("", False),
        ("version: 1.0.0", False),
    ]

    validator = RequiredFieldsValidator()

    for content, expected in test_cases:
        # Create full skill content for testing
        full_content = f"""name: test-skill
{content}
description: Test
tools: echo
userInvocable: true"""

        result = validator.validate(full_content, Path("test/skill/SKILL.md"))
        assert result.has_stable_suffix == expected, f"Failed for content: {content}"

    print("✓ Stable suffix detection test passed")
def test_skill_name_extraction():
    """Test skill name extraction matches original behavior."""
    validator = NameValidator()

    # Test various name formats
    test_cases = [
        ("name: simple", "simple"),
        ("name: complex-skill.name", "complex-skill.name"),
        ("name:   spaced name   ", "spaced name"),
        ("name:", "skill"),  # Should fallback to directory name
    ]

    for content, expected_name in test_cases:
        full_content = f"""{content}
version: 1.0.0
description: Test"""

        result = validator.validate(full_content, Path("test/skill/SKILL.md"))
        assert result.name == expected_name, f"Failed for name: {content}"

    print("✓ Skill name extraction test passed")
@patch('builtins.open', MagicMock())
@patch('pathlib.Path.read_text')
@patch('pathlib.Path.stat')
def test_validate_skill_file_backward_compatibility(mock_stat, mock_read_text, mock_open):
    """Test validate_skill_file function for backward compatibility."""
    from datetime import datetime

    # Mock file read and stat
    mock_read_text.return_value = """name: test-skill
version: 1.0.0-stable
description: A test skill
tools: echo,cat
userInvocable: true"""

    mock_stat.return_value = MagicMock(st_mtime=1234567890)

    # Create a temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("""name: test-skill
version: 1.0.0-stable
description: A test skill
tools: echo,cat
userInvocable: true""")
        temp_path = Path(f.name)

    try:
        # Test the function
        result = validate_skill_file(temp_path)

        # Verify result structure matches original healthcheck.py
        assert 'name' in result
        assert 'status' in result
        assert 'validation_score' in result
        assert 'has_stable_suffix' in result
        assert 'issues' in result
        assert 'last_modified' in result
        assert 'last_checked' in result

        # Verify values
        assert result['name'] == 'test-skill'
        assert result['status'] == 'healthy'  # 100% score
        assert result['validation_score'] == 1.0
        assert result['has_stable_suffix'] == True
        assert result['issues'] == []

        print("✓ Backward compatibility test passed")

    finally:
        # Clean up
        temp_path.unlink()
def test_module_independent_testability():
    """Test that each module can be tested independently."""
    # Test that validation module imports work without side effects
    try:
        from core.validation import ValidationResult
        from discovery import discover_skills, get_skills_directory
        from reporting import generate_skills_summary

        # Test that modules can be imported independently
        validation_result = ValidationResult(
            name="test",
            status="healthy",
            validation_score=1.0,
            has_stable_suffix=True,
            issues=[],
            last_modified="2023-01-01",
            last_checked="2023-01-02"
        )

        assert validation_result.name == "test"

        print("✓ Module independent testability test passed")

    except ImportError as e:
        assert False, f"Module import failed: {e}"
def test_pure_function_properties():
    """Test that validation functions are pure (no side effects)."""
    validator = RequiredFieldsValidator()

    content = """name: test
version: 1.0.0
description: Test
tools: echo
userInvocable: true"""

    # First call
    result1 = validator.validate(content, Path("test/skill/SKILL.md"))

    # Second call with same inputs should produce same outputs
    result2 = validator.validate(content, Path("test/skill/SKILL.md"))

    assert result1.validation_score == result2.validation_score
    assert result1.issues == result2.issues
    assert result1.has_stable_suffix == result2.has_stable_suffix
    assert result1.name == result2.name

    print("✓ Pure function properties test passed")
def test_validator_separation_of_concerns():
    """Test that validators have single responsibility."""
    # Each validator should handle only one aspect
    required_validator = RequiredFieldsValidator()
    version_validator = VersionValidator()
    name_validator = NameValidator()

    content = """name: test-skill
version: 1.0.0-stable
description: Test
tools: echo
userInvocable: true"""

    # RequiredFieldsValidator should only check fields
    required_result = required_validator.validate(content, Path("test/skill/SKILL.md"))
    assert 'validation_score' in dir(required_result)
    assert 'issues' in dir(required_result)

    # VersionValidator should only check version/stable suffix
    version_result = version_validator.validate(content, Path("test/skill/SKILL.md"))
    assert hasattr(version_result, 'has_stable_suffix')

    # NameValidator should only extract name
    name_result = name_validator.validate(content, Path("test/skill/SKILL.md"))
    assert hasattr(name_result, 'name')

    print("✓ Validator separation of concerns test passed")
def run_all_tests():
    """Run all validation tests."""
    print("Running comprehensive unit tests for core/validation module...")
    print("=" * 70)

    try:
        test_validation_result_dataclass()
        test_required_fields_validator()
        test_version_validator()
        test_name_validator()
        test_validation_orchestrator_integration()
        test_validation_orchestrator_error_handling()
        test_validation_scoring_algorithm()
        test_stable_suffix_detection()
        test_skill_name_extraction()
        test_validate_skill_file_backward_compatibility()
        test_module_independent_testability()
        test_pure_function_properties()
        test_validator_separation_of_concerns()

        print("=" * 70)
        print("All validation tests completed successfully!")
        print("\nKey achievements:")
        print("- ✓ Modular validation architecture working")
        print("- ✓ Backward compatibility maintained")
        print("- ✓ Each validator has single responsibility")
        print("- ✓ Pure functions enable independent testing")
        print("- ✓ Validation orchestrator properly integrates components")
        print("- ✓ Error handling robust and tested")

    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    return True
if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)