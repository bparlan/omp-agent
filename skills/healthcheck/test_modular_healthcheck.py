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
import subprocess

# Add the skill directory to path
sys.path.insert(0, str(Path(__file__).parent))

from core.validation import (
    ValidatorBase, RequiredFieldsValidator,
    StableSuffixValidator, SkillNameValidator, SkillValidator
)
from discovery import discover_skills_directory, discover_skills
from reporting import (
    generate_badges, generate_health_report, generate_processed_skills
)
from cli import parse_arguments, validate_single_skill, process_all_skills
from main import main
class TestSkillValidator:
    """Test validation module"""

    def test_validator_base_abstract(self):
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
        valid_content = """---
name: Test Skill
version: "1.0.0-stable"
description: A test skill
tools: [bash, python]
userInvocable: true
---
"""
        result = validator.validate(valid_content)
        assert result['validation_score'] == 1.0
        assert len(result['issues']) == 0
        assert result['passes_all'] == True

        # Invalid content (missing fields)
        invalid_content = "name: Test Skill\nversion: 1.0.0"
        result = validator.validate(invalid_content)
        assert result['validation_score'] < 1.0
        assert len(result['issues']) > 0
        assert result['passes_all'] == False

    def test_stable_suffix_validator(self):
        """Test stable suffix validation"""
        validator = StableSuffixValidator()

        # Valid content
        valid_content = "version: \"1.0.0-stable\""
        result = validator.validate(valid_content)
        assert result['has_stable_suffix'] == True
        assert result['passes'] == True

        # Invalid content
        invalid_content = "version: \"1.0.0\""
        result = validator.validate(invalid_content)
        assert result['has_stable_suffix'] == False
        assert result['passes'] == False

    def test_skill_name_validator(self):
        """Test skill name extraction"""
        validator = SkillNameValidator()

        # Valid content
        content = "name: My Awesome Skill"
        result = validator.validate(content)
        assert result['extracted_name'] == "My Awesome Skill"
        assert result['has_name'] == True

        # Invalid content
        content = "version: 1.0.0"
        result = validator.validate(content)
        assert result['extracted_name'] == ""
        assert result['has_name'] == False

    def test_skill_validator_integration(self):
        """Test SkillValidator integration"""
        validator = SkillValidator()

        # Create temporary SKILL.md file
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_file = Path(tmpdir) / "SKILL.md"
            skill_file.write_text("""---
name: Integration Test
version: "2.0.0-stable"
description: Test skill
tools: [python]
userInvocable: true
---""")

            result = validator.validate_skill_file(skill_file)
            assert result['name'] == "Integration Test"
            assert result['status'] == "healthy"
            assert result['validation_score'] == 1.0
            assert result['has_stable_suffix'] == True
            assert len(result['issues']) == 0

    def test_skill_validator_error_handling(self):
        """Test error handling in SkillValidator"""
        validator = SkillValidator()

        # Non-existent file
        non_existent = Path("/tmp/non_existent_skill.md")
        result = validator.validate_skill_file(non_existent)
        assert result['status'] == "error"
        assert len(result['issues']) > 0
class TestDiscoveryModule:
    """Test discovery module"""

    def test_discover_skills_directory(self):
        """Test skills directory discovery"""
        # This should find a skills directory somewhere
        skills_dir = discover_skills_directory()
        assert isinstance(skills_dir, Path)
        assert skills_dir.exists()

    def test_discover_skills(self):
        """Test skill discovery"""
        skills = discover_skills()
        # Should return a list of Path objects
        assert isinstance(skills, list)
        for skill in skills:
            assert isinstance(skill, Path)
            assert (skill.parent / "SKILL.md").exists()
class TestReportingModule:
    """Test reporting module"""

    def setup_method(self):
        """Setup for each test"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_results = [
            {
                "name": "Test Skill 1",
                "status": "healthy",
                "validation_score": 0.8,
                "has_stable_suffix": True,
                "issues": [],
                "last_modified": "2024-01-01T00:00:00",
                "last_checked": "2024-01-01T00:00:00"
            },
            {
                "name": "Test Skill 2",
                "status": "needs_review",
                "validation_score": 0.6,
                "has_stable_suffix": False,
                "issues": ["Missing tools field"],
                "last_modified": "2024-01-01T00:00:00",
                "last_checked": "2024-01-01T00:00:00"
            }
        ]

    def test_generate_badges(self):
        """Test badges generation"""
        os.environ['OMP_PROJECT_ROOT'] = self.temp_dir

        try:
            # Change to temp directory
            original_cwd = os.getcwd()
            os.chdir(self.temp_dir)

            # Generate badges
            generate_badges(self.test_results)

            # Verify file was created
            badges_file = Path(self.temp_dir) / "health_badges.md"
            assert badges_file.exists()

            content = badges_file.read_text()
            assert "Test Skill 1" in content
            assert "Test Skill 2" in content
            assert "healthy" in content
            assert "needs_review" in content

        finally:
            os.chdir(original_cwd)
            del os.environ['OMP_PROJECT_ROOT']

    def test_generate_health_report(self):
        """Test health report generation"""
        os.environ['OMP_PROJECT_ROOT'] = self.temp_dir

        try:
            original_cwd = os.getcwd()
            os.chdir(self.temp_dir)

            generate_health_report(self.test_results)

            health_file = Path(self.temp_dir) / "health_check_report.json"
            assert health_file.exists()

            with open(health_file) as f:
                report = json.load(f)

            assert report['total_skills'] == 2
            assert report['healthy_count'] == 1
            assert report['needs_review_count'] == 1
            assert report['error_count'] == 0

        finally:
            os.chdir(original_cwd)
            del os.environ['OMP_PROJECT_ROOT']

    def test_generate_processed_skills(self):
        """Test processed skills generation"""
        os.environ['OMP_PROJECT_ROOT'] = self.temp_dir

        try:
            original_cwd = os.getcwd()
            os.chdir(self.temp_dir)

            generate_processed_skills(self.test_results)

            processed_file = Path(self.temp_dir) / "processed_skills.json"
            assert processed_file.exists()

            with open(processed_file) as f:
                processed = json.load(f)

            assert "Test Skill 1" in processed
            assert "Test Skill 2" in processed
            assert processed["Test Skill 1"]["status"] == "healthy"
            assert processed["Test Skill 2"]["status"] == "needs_review"

        finally:
            os.chdir(original_cwd)
            del os.environ['OMP_PROJECT_ROOT']
class TestCLIModule:
    """Test CLI module"""

    def test_parse_arguments(self):
        """Test argument parsing"""
        # Test help flag
        original_argv = sys.argv
        try:
            sys.argv = ['healthcheck.py', '--help']
            args = parse_arguments()
            assert args.help == True
            assert args.skill_name is None
            assert args.all == False

            sys.argv = ['healthcheck.py', 'test_skill']
            args = parse_arguments()
            assert args.skill_name == "test_skill"
            assert args.help == False
            assert args.all == False

            sys.argv = ['healthcheck.py', '--all']
            args = parse_arguments()
            assert args.all == True
            assert args.skill_name is None

        finally:
            sys.argv = original_argv

    def test_argument_parsing_edge_cases(self):
        """Test edge cases in argument parsing"""
        original_argv = sys.argv
        try:
            # Test no arguments
            sys.argv = ['healthcheck.py']
            args = parse_arguments()
            assert args.skill_name is None
            assert args.all == False
            assert args.help == False

            # Test both skill name and --all (should prioritize skill name)
            sys.argv = ['healthcheck.py', 'test_skill', '--all']
            args = parse_arguments()
            assert args.skill_name == "test_skill"
            assert args.all == True  # Both are set, --all takes effect

        finally:
            sys.argv = original_argv
class TestIntegration:
    """Integration tests for modular healthcheck"""

    def test_cli_integration(self):
        """Test CLI integration"""
        # Test that modules can be imported and used together
        from core.validation import SkillValidator
        from discovery import discover_skills
        from reporting import generate_badges, generate_health_report

        # Create a temporary skill
        with tempfile.TemporaryDirectory() as tmpdir:
            os.environ['OMP_PROJECT_ROOT'] = tmpdir

            try:
                # Create a test skill directory
                skill_dir = Path(tmpdir) / "test_skill"
                skill_dir.mkdir()

                skill_file = skill_dir / "SKILL.md"
                skill_file.write_text("""---
name: Integration Test Skill
version: "1.5.0-stable"
description: This is a test skill for integration testing
tools: [python, bash]
userInvocable: true
---""")

                # Test validation
                validator = SkillValidator()
                result = validator.validate_skill_file(skill_file)
                assert result['status'] == "healthy"
                assert result['validation_score'] == 1.0
                assert result['has_stable_suffix'] == True

                # Test skill discovery
                skills = discover_skills()
                assert len(skills) >= 1
                skill_names = [s.parent.name for s in skills]
                assert "test_skill" in skill_names

                # Test report generation
                generate_badges([result])
                generate_health_report([result])

                badges_file = Path(tmpdir) / "health_badges.md"
                health_file = Path(tmpdir) / "health_check_report.json"

                assert badges_file.exists()
                assert health_file.exists()

                # Verify report content
                with open(health_file) as f:
                    report = json.load(f)
                assert report['healthy_count'] == 1

            finally:
                del os.environ['OMP_PROJECT_ROOT']

    def test_backward_compatibility(self):
        """Test that modular implementation maintains backward compatibility"""
        # Test that the original healthcheck.py can be imported and run
        original_healthcheck = Path(__file__).parent / "healthcheck.py"
        assert original_healthcheck.exists()

        # The original healthcheck.py should delegate to main.py
        # We can't easily test the full execution without mocking,
        # but we can verify the import structure
        import importlib.util
        spec = importlib.util.spec_from_file_location("healthcheck", str(original_healthcheck))
        module = importlib.util.module_from_spec(spec)

        # Should not raise import errors
        spec.loader.exec_module(module)

        # Should have main function
        assert hasattr(module, 'main')
        assert callable(module.main)

    def test_modular_separation_of_concerns(self):
        """Test that concerns are properly separated"""
        # Each module should have its own specific functionality
        from core.validation import ValidatorBase
        from discovery import discover_skills_directory
        from reporting import generate_badges
        from cli import parse_arguments

        # Should be able to import all modules independently
        assert ValidatorBase is not None
        assert discover_skills_directory is not None
        assert generate_badges is not None
        assert parse_arguments is not None

        # Modules should not have unexpected dependencies
        import inspect

        # Core validation should only import basic modules
        validation_source = inspect.getsource(ValidatorBase)
        assert "discovery" not in validation_source
        assert "reporting" not in validation_source
        assert "cli" not in validation_source

        # Discovery should not import validation/reporting
        discovery_source = inspect.getsource(discover_skills_directory)
        assert "validator" not in discovery_source.lower()
        assert "report" not in discovery_source.lower()

        # Reporting should not import CLI
        reporting_source = inspect.getsource(generate_badges)
        assert "cli" not in reporting_source.lower()

        # CLI should import the other modules
        cli_source = inspect.getsource(parse_arguments)
        assert "discovery" in cli_source or "from discovery" in cli_source
class TestRequirementsCompliance:
    """Test compliance with modular decomposition requirements"""

    def test_requirements_1_modular_architecture(self):
        """Test requirement 1: Modular architecture with 5 core components"""
        skill_dir = Path(__file__).parent

        # Check all required modules exist
        required_modules = [
            "core/validation.py",
            "discovery.py",
            "reporting.py",
            "cli.py",
            "main.py"
        ]

        for module in required_modules:
            module_path = skill_dir / module
            assert module_path.exists(), f"Required module {module} not found"
            assert module_path.is_file(), f"Required module {module} is not a file"

        # Check that original healthcheck.py delegates to main.py
        healthcheck_py = skill_dir / "healthcheck.py"
        assert healthcheck_py.exists()

        # Should import main and delegate
        content = healthcheck_py.read_text()
        assert "from main import main" in content
        assert "modular_main()" in content

    def test_requirements_2_backward_compatibility(self):
        """Test requirement 2: Backward compatibility"""
        # CLI interface should be preserved
        from cli import parse_arguments

        original_argv = sys.argv
        try:
            # Test original CLI patterns
            sys.argv = ['healthcheck.py', 'my_skill']
            args = parse_arguments()
            assert args.skill_name == "my_skill"

            sys.argv = ['healthcheck.py', '--all']
            args = parse_arguments()
            assert args.all == True

            sys.argv = ['healthcheck.py', '--help']
            args = parse_arguments()
            assert args.help == True

        finally:
            sys.argv = original_argv

    def test_requirements_3_single_batch_modes(self):
        """Test requirement 3: Single skill and batch processing modes"""
        # Should support both modes
        from cli import validate_single_skill, process_all_skills

        # Both functions should exist
        assert callable(validate_single_skill)
        assert callable(process_all_skills)

        # Process all skills should handle empty results gracefully
        results = process_all_skills()
        assert isinstance(results, list)

    def test_requirements_4_future_extensibility(self):
        """Test requirement 4: Future extensibility"""
        # Should support Validator base class extension
        from core.validation import ValidatorBase

        # Should be able to create new validators
        class TestValidator(ValidatorBase):
            def validate(self, content):
                return {'test_score': 1.0, 'test_passed': True}

        validator = TestValidator("test")
        result = validator.validate("test content")
        assert result['test_score'] == 1.0
        assert result['test_passed'] == True

        # Should support plugin architecture
        from cli import run_health_check
        assert callable(run_health_check)

    def test_requirements_5_technical_structure(self):
        """Test requirement 5: Technical structure"""
        skill_dir = Path(__file__).parent

        # Each module should be independently importable
        import importlib.util

        modules_to_test = [
            "core.validation",
            "discovery",
            "reporting",
            "cli",
            "main"
        ]

        for module_name in modules_to_test:
            try:
                # Try to import each module
                module_path = skill_dir / f"{module_name.replace('.', '/')}.py"
                spec = importlib.util.spec_from_file_location(module_name, str(module_path))
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                assert module is not None
            except Exception as e:
                raise AssertionError(f"Could not import module {module_name}: {e}")

    def test_requirements_6_quality_assurance(self):
        """Test requirement 6: Quality assurance"""
        from core.validation import SkillValidator

        # Each module should be testable
        validator = SkillValidator()
        assert hasattr(validator, 'validate_skill_file')
        assert hasattr(validator, 'combine_validators_for_testing')

        # Validation logic should be pure (no side effects)
        import inspect
        source = inspect.getsource(SkillValidator.validate_skill_file)

        # Should not modify file system during validation
        assert "write_text" not in source
        assert "open(" not in source

        # Should not have external dependencies
        assert "os." not in source or "os.environ" not in source
        assert "sys." not in source or "sys.argv" not in source
def run_all_tests():
    """Run all tests and report results"""
    print("Running modular healthcheck tests...")
    print("=" * 50)

    # Collect all test classes
    test_classes = [
        TestSkillValidator,
        TestDiscoveryModule,
        TestReportingModule,
        TestCLIModule,
        TestIntegration,
        TestRequirementsCompliance
    ]

    total_tests = 0
    passed_tests = 0
    failed_tests = 0

    for test_class in test_classes:
        print(f"\nRunning {test_class.__name__}...")
        test_instance = test_class()

        for method_name in dir(test_instance):
            if method_name.startswith('test_'):
                total_tests += 1
                try:
                    method = getattr(test_instance, method_name)
                    method()
                    print(f"  ✓ {method_name}")
                    passed_tests += 1
                except Exception as e:
                    print(f"  ✗ {method_name}: {e}")
                    failed_tests += 1

    print("\n" + "=" * 50)
    print(f"Test Results: {passed_tests}/{total_tests} passed, {failed_tests} failed")

    if failed_tests > 0:
        print(f"\nFAILED TESTS:")
        return False
    else:
        print(f"\nALL TESTS PASSED!")
        return True
if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)