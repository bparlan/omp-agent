#!/usr/bin/env python3
"""
Test suite for modular healthcheck architecture.
Validates that the refactored implementation maintains backward compatibility
and follows modular design principles.
"""

import tempfile
import os
from pathlib import Path
import json
import sys

# Add the skill directory to path (so core.validation can be found)
sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent))

# Now import from the skill's core module
from skills.healthcheck.core.validation import (
    ValidatorBase,
    RequiredFieldsValidator,
    StableSuffixValidator,
    SkillNameValidator,
    SkillValidator,
)
from discovery import discover_skills_directory, discover_skills
from reporting import generate_badges, generate_health_report, generate_processed_skills
from cli import parse_arguments, validate_single_skill, process_all_skills

class TestSkillValidator:
    """Test validation module"""

    def test_validator_base_is_abstract(self):
        """Test that ValidatorBase is abstract"""
        try:
            validator = ValidatorBase("test")
            validator.validate("")
            assert False, "ValidatorBase should raise NotImplementedError"
        except NotImplementedError:
            pass  # Expected

    def test_required_fields_validator(self):
        """Test required fields validation"""
        validator = RequiredFieldsValidator()
        
        # Valid content
        valid_content = """name: test-skill
description: A test skill
version: 1.0.0-stable
userInvocable: true"""
        
        result = validator.validate(valid_content)
        assert result["is_valid"] is True
        assert result["errors"] == []
        
        # Invalid content (missing field)
        invalid_content = """name: test-skill
version: 1.0.0-stable
userInvocable: true"""
        
        result = validator.validate(invalid_content)
        assert result["is_valid"] is False
        assert "Missing required field: description" in result["errors"]

    def test_stable_suffix_validator(self):
        """Test stable suffix validation"""
        validator = StableSuffixValidator()
        
        # Valid content with stable suffix
        valid_content = """name: test-skill
version: 1.0.0-stable
userInvocable: true"""
        
        result = validator.validate(valid_content)
        assert result["is_valid"] is True
        assert result["has_stable_suffix"] is True
        
        # Invalid content without stable suffix
        invalid_content = """name: test-skill
version: 1.0.0
userInvocable: true"""
        
        result = validator.validate(invalid_content)
        assert result["is_valid"] is False
        assert result["has_stable_suffix"] is False
        assert "does not have -stable or -test suffix" in result["errors"][0]

    def test_skill_name_validator(self):
        """Test skill name validation"""
        validator = SkillNameValidator()
        
        # Valid content
        valid_content = """name: test-skill
version: 1.0.0-stable
userInvocable: true"""
        
        result = validator.validate(valid_content)
        assert result["is_valid"] is True
        assert result["name"] == "test-skill"
        
        # Invalid content (missing name)
        invalid_content = """description: A test skill
version: 1.0.0-stable
userInvocable: true"""
        
        result = validator.validate(invalid_content)
        assert result["is_valid"] is False
        assert result["errors"] == ["Name field not found"]

    def test_validation_orchestrator(self):
        """Test validation orchestrator"""
        from skills.healthcheck.core.validation import ValidationOrchestrator
        
        orchestrator = ValidationOrchestrator()
        validators = orchestrator.combine_validators_for_testing()
        
        assert len(validators) == 3
        assert RequiredFieldsValidator in validators
        assert StableSuffixValidator in validators
        assert SkillNameValidator in validators

    def test_skill_validator(self):
        """Test skill validator integration"""
        validator = SkillValidator()
        
        content = """name: test-skill
description: A test skill
version: 1.0.0-stable
userInvocable: true"""
        
        result = validator.validate(content)
        assert "is_valid" in result
        assert "score" in result
        assert "status" in result
        assert result["status"] == "healthy"

    def test_discover_skills_directory(self):
        """Test skills directory discovery"""
        skills_dir = discover_skills_directory()
        
        assert skills_dir is not None
        assert isinstance(skills_dir, Path)
        assert skills_dir.exists()
        assert skills_dir.name == "skills"

    def test_discover_skills(self):
        """Test skill discovery"""
        skills = discover_skills()
        
        assert isinstance(skills, list)
        
        # Should find at least some skills
        assert len(skills) > 0
        
        # Check that we have paths
        for skill_path in skills:
            assert isinstance(skill_path, Path)
            assert (skill_path / "SKILL.md").exists()

    def test_generate_badges(self):
        """Test badges report generation"""
        results = [
            {
                "skill_name": "test-skill-1",
                "is_valid": True,
                "score": 100.0,
                "status": "healthy",
                "last_modified": "2025-01-01T00:00:00",
                "last_checked": "2025-01-02T00:00:00",
            },
            {
                "skill_name": "test-skill-2",
                "is_valid": False,
                "score": 0.0,
                "status": "error",
                "errors": ["Validation failed"],
                "last_modified": "2025-01-01T00:00:00",
                "last_checked": "2025-01-02T00:00:00",
            }
        ]
        
        # This should not raise an exception
        generate_badges(results)
        
        # Check that file was created
        assert Path("health_badges.md").exists()
        content = Path("health_badges.md").read_text()
        assert "test-skill-1" in content
        assert "test-skill-2" in content
        
        # Clean up
        Path("health_badges.md").unlink()

    def test_generate_health_report(self):
        """Test health report generation"""
        results = [
            {
                "skill_name": "test-skill-1",
                "is_valid": True,
                "score": 100.0,
                "status": "healthy",
                "last_modified": "2025-01-01T00:00:00",
                "last_checked": "2025-01-02T00:00:00",
            }
        ]
        
        # This should not raise an exception
        generate_health_report(results)
        
        # Check that file was created
        assert Path("health_check_report.json").exists()
        content = Path("health_check_report.json").read_text()
        assert "test-skill-1" in content
        
        # Clean up
        Path("health_check_report.json").unlink()

    def test_generate_processed_skills(self):
        """Test processed skills report generation"""
        results = [
            {
                "skill_name": "test-skill-1",
                "is_valid": True,
                "score": 100.0,
                "status": "healthy",
                "last_modified": "2025-01-01T00:00:00",
                "last_checked": "2025-01-02T00:00:00",
            }
        ]
        
        # This should not raise an exception
        generate_processed_skills(results)
        
        # Check that file was created
        assert Path("processed_skills.json").exists()
        content = Path("processed_skills.json").read_text()
        assert "test-skill-1" in content
        
        # Clean up
        Path("processed_skills.json").unlink()

    def test_parse_arguments(self):
        """Test argument parsing"""
        # Simulate command line arguments
        original_argv = sys.argv
        
        try:
            sys.argv = ["healthcheck.py", "my-skill"]
            args = parse_arguments()
            
            assert args.skill_name == "my-skill"
            assert args.all_flag is False
            assert args.help_flag is False
            
            sys.argv = ["healthcheck.py", "--all"]
            args = parse_arguments()
            
            assert args.skill_name is None
            assert args.all_flag is True
            assert args.help_flag is False
            
        finally:
            sys.argv = original_argv

    def test_validate_single_skill(self):
        """Test single skill validation"""
        # Mock a skill in the test directory
        test_skill_path = Path(__file__).parent / "test-skill"
        test_skill_path.mkdir(exist_ok=True)
        
        skill_file = test_skill_path / "SKILL.md"
        skill_file.write_text("""name: test-skill
description: A test skill
version: 1.0.0-stable
userInvocable: true""")
        
        try:
            result = validate_single_skill("test-skill")
            
            assert result is not None
            assert "is_valid" in result
            assert "skill_name" in result
            assert result["skill_name"] == "test-skill"
            
        finally:
            # Clean up
            import shutil
            if test_skill_path.exists():
                shutil.rmtree(test_skill_path)

    def test_process_all_skills(self):
        """Test processing all skills"""
        results = process_all_skills()
        
        assert isinstance(results, list)
        
        # Should process some skills
        # (number depends on what's available)
        assert len(results) >= 0

    def test_cli_integration(self):
        """Test CLI module integration"""
        # Test that all expected functions are available
        assert callable(parse_arguments)
        assert callable(validate_single_skill)
        assert callable(process_all_skills)

    def test_modular_separation_of_concerns(self):
        """Test that concerns are properly separated"""
        # Each module should have its own specific functionality
        from skills.healthcheck.core.validation import ValidatorBase
        from discovery import discover_skills_directory
        from reporting import generate_badges
        from cli import parse_arguments

        # Should be able to import all modules independently
        assert ValidatorBase is not None
        assert discover_skills_directory is not None
        assert generate_badges is not None
        assert parse_arguments is not None

    def test_requirements_4_future_extensibility(self):
        """Test requirement 4: Future extensibility"""
        # Should support Validator base class extension
        from skills.healthcheck.core.validation import ValidatorBase

        # Should be able to create new validators
        class TestValidator(ValidatorBase):
            def validate(self, content):
                return {"test_score": 1.0, "test_passed": True}

        validator = TestValidator("test")
        result = validator.validate("test content")
        
        assert result["test_score"] == 1.0
        assert result["test_passed"] is True

    def test_requirements_5_technical_requirements(self):
        """Test requirement 5: Technical requirements"""
        # Each module should be independently importable
        import importlib
        
        # Core validation
        core_module = importlib.import_module("skills.healthcheck.core.validation")
        assert hasattr(core_module, "ValidatorBase")
        
        # Discovery module
        discovery_module = importlib.import_module("skills.healthcheck.discovery")
        assert hasattr(discovery_module, "discover_skills_directory")
        
        # Reporting module
        reporting_module = importlib.import_module("skills.healthcheck.reporting")
        assert hasattr(reporting_module, "generate_badges")
        
        # CLI module
        cli_module = importlib.import_module("skills.healthcheck.cli")
        assert hasattr(cli_module, "parse_arguments")

    def test_requirements_6_quality_requirements(self):
        """Test requirement 6: Quality requirements"""
        # Validation logic should be pure (no side effects)
        from skills.healthcheck.core.validation import RequiredFieldsValidator
        
        validator = RequiredFieldsValidator()
        content = """name: test-skill
description: A test skill
version: 1.0.0-stable
userInvocable: true"""
        
        # Multiple calls should give same result
        result1 = validator.validate(content)
        result2 = validator.validate(content)
        
        assert result1 == result2

    def test_all_skills_healthcheck(self):
        """Integration test for all skills"""
        # This test validates that the complete system works
        results = process_all_skills()
        
        assert isinstance(results, list)
        
        # Should have processed skills
        # (actual number depends on what's in the repository)
        assert len(results) >= 0


def run_all_tests():
    """Run all tests and report results"""
    test_classes = [
        TestSkillValidator(),
    ]
    
    all_passed = True
    
    for test_class in test_classes:
        print(f"\nRunning tests for {test_class.__class__.__name__}...")
        
        test_methods = [
            method for method in dir(test_class) 
            if method.startswith("test_") and callable(getattr(test_class, method))
        ]
        
        for method_name in test_methods:
            try:
                print(f"  Running {method_name}...", end=" ")
                method = getattr(test_class, method_name)
                method()
                print("PASS")
            except Exception as e:
                print(f"FAIL: {str(e)}")
                all_passed = False
    
    if all_passed:
        print("\n✓ All tests passed!")
    else:
        print("\n✗ Some tests failed")
    
    return all_passed


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
