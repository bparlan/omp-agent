# Healthcheck Skill Interface Contracts

## Executive Summary

This document defines the precise interface contracts between all healthcheck skill modules, resolving ambiguities and ensuring consistent behavior across the modular architecture. Interface contracts specify method signatures, data structures, dependencies, and behavioral expectations for each module component.

## Module Interface Overview

The healthcheck skill consists of 5 core modules with the following interface contracts:

| Module | Primary Purpose | Key Interface Methods | Dependencies | Responsibilities |
|--------|----------------|---------------------|-------------|------------------|
| **validation.py** | Pure validation logic | `validate_skill_file()`, `ValidationResult` | None | SKILL.md validation, scoring, status determination |
| **discovery.py** | Skill directory detection | `discover_skills()`, `get_skills_directory()` | None | Project root finding, skill location |
| **reporting.py** | Report generation | `generate_badges()`, `generate_health_report()`, `generate_processed_skills()` | Validation results | Report file creation, formatting |
| **cli.py** | CLI interface | `parse_arguments()`, `run_health_check()` | All modules | Argument parsing, user interaction |
| **main.py** | Orchestration | `main()`, `HealthCheckOrchestrator` | All modules | Workflow coordination, execution entry point |

## Detailed Interface Contracts

### 1. Validation Module Contract (`core/validation.py`)

#### Data Structures

```python
@dataclass
class ValidationResult:
    """Model for skill validation results - immutable data structure"""
    name: str                    # Skill name extracted from SKILL.md
    status: str                  # "healthy", "needs_review", "error"
    validation_score: float      # 0.0-1.0, percentage of passed checks
    has_stable_suffix: bool      # True if version contains "-stable"
    issues: List[str]            # List of validation issues found
    last_modified: str           # ISO timestamp of last file modification
    last_checked: str            # ISO timestamp of validation check
```

#### Method Contracts

```python
class ValidatorBase:
    """Base class for all validation rules - pure validation logic"""
    def __init__(self, name: str):
        self.name = name

    def validate(self, content: str, skill_path: Path) -> Dict[str, Any]:
        """Validate skill content - IMPLEMENTATION REQUIRED"""
        pass

    def get_score(self, content: str) -> float:
        """Get validation score - PURE FUNCTION"""
        result = self.validate(content)
        return result.get('validation_score', 0.0)
```

#### Concrete Validators

```python
class RequiredFieldsValidator(ValidatorBase):
    """Validates presence of required frontmatter fields"""
    def validate(self, content: str, skill_path: Path) -> Dict[str, Any]:
        """Validate required fields: name:, version:, description:, tools:, userInvocable:"""
        pass

class StableSuffixValidator(ValidatorBase):
    """Validates -stable suffix in version field"""
    def validate(self, content: str, skill_path: Path) -> Dict[str, Any]:
        """Check for '-stable' in version field"""
        pass

class SkillNameValidator(ValidatorBase):
    """Extracts and validates skill name from frontmatter"""
    def validate(self, content: str, skill_path: Path) -> Dict[str, Any]:
        """Extract skill name from 'name:' field"""
        pass
```

#### Core Orchestrator

```python
class ValidationOrchestrator:
    """Orchestrates multiple validators to produce final validation results"""
    def __init__(self):
        self.validators = [
            RequiredFieldsValidator(),
            StableSuffixValidator(),
            SkillNameValidator()
        ]

    def validate_skill_file(self, skill_path: Path) -> ValidationResult:
        """MAIN VALIDATION INTERFACE - PURE FUNCTION"""
        """Orchestrates validation of a single skill file"""
        pass

    def combine_validators_for_testing(self) -> List[ValidatorBase]:
        """Returns validators list for testing - PUBLIC API"""
        return self.validators
```

#### Public Function Interface

```python
def validate_skill_file(skill_path: Path) -> Dict[str, Any]:
    """PUBLIC VALIDATION FUNCTION - BACKWARD COMPATIBILITY"""
    """Legacy wrapper for backward compatibility - delegates to ValidationOrchestrator"""
    pass
```

#### Contract Specifications

- **Purity**: All validation methods must be pure (no I/O, no side effects)
- **Determinism**: Same input always produces same output
- **Error Handling**: Comprehensive exception handling with error status
- **Scoring**: Validation score 0.0-1.0, >=0.8 = healthy, <0.8 = needs_review
- **State**: No global state or mutable class attributes

### 2. Discovery Module Contract (`core/discovery.py`)

#### Data Structures

```python
from pathlib import Path
from typing import List, Optional, Dict, Any
```

#### Method Contracts

```python
def discover_skills_directory() -> Path:
    """PROJECT-AGNOSTIC DISCOVERY - PURE FUNCTION"""
    """Find skills directory using multiple strategies:
    1. Script parent directory (/script/parent/skills)
    2. OMP_PROJECT_ROOT environment variable
    3. skills-ledger.json upward search
    4. Current working directory fallback
    5. Script directory fallback
    """
    pass

def get_skills_directory() -> Path:
    """CACHED DISCOVERY - PERFORMANT"""
    """Returns cached skills directory - thread-safe singleton"""
    pass

def discover_skills() -> List[Path]:
    """SKILL DISCOVERY - FILE SYSTEM DEPENDENT"""
    """Find all SKILL.md files in discovered skills directory"""
    pass

def discover_skill_by_name(skill_name: str) -> Optional[Path]:
    """SPECIFIC SKILL DISCOVERY - LINEAR SEARCH"""
    """Find skill by name using parent directory name matching"""
    pass

def get_skills_summary() -> Dict[str, Any]:
    """SUMMARY INFORMATION - AGGREGATION"""
    """Get comprehensive summary of discovered skills"""
    pass
```

#### Contract Specifications

- **Deterministic**: Same directory structure always produces same results
- **Fallbacks**: All discovery strategies must be implemented
- **Caching**: `get_skills_directory()` should cache results
- **Error Handling**: Graceful handling of missing directories
- **Performance**: Linear search acceptable for typical repository sizes

### 3. Reporting Module Contract (`core/reporting.py`)

#### Method Contracts

```python
def generate_badges(results: List[ValidationResult]) -> None:
    """GENERATE health_badges.md - MARKDOWN REPORT"""
    """Generate markdown table with skill health status
    Output: skills_dir / "health_badges.md"
    Format: Markdown table with status emojis, scores, timestamps
    """
    pass

def generate_health_report(results: List[ValidationResult]) -> None:
    """GENERATE health_check_report.json - DETAILED JSON REPORT"""
    """Generate comprehensive JSON report with statistics
    Output: skills_dir / "health_check_report.json"
    Includes: timestamp, counts, detailed skill results
    """
    pass

def generate_processed_skills(results: List[ValidationResult]) -> None:
    """GENERATE processed_skills.json - NAME-MAPPED REPORT"""
    """Generate JSON mapping skill names to results
    Output: skills_dir / "processed_skills.json"
    Format: {skill_name: result_dict}
    """
    pass

def generate_skills_summary(results: List[ValidationResult]) -> Dict[str, Any]:
    """GENERATE SKILLS SUMMARY - AGGREGATION FUNCTION"""
    """Generate comprehensive summary dictionary
    Returns: {
        "summary": {...statistics...},
        "skills": results,
        "status_distribution": {...}
    }
    """
    pass
```

#### Contract Specifications

- **Output Format**: Specific file formats and naming conventions
- **Timestamp Inclusion**: All reports must include generation timestamps
- **Content Validation**: Report content must be valid (parsable JSON, markdown)
- **File Writing**: Uses Path.write_text() and json.dump() with indentation
- **Error Handling**: Graceful handling of write failures

### 4. CLI Module Contract (`cli.py`)

#### Method Contracts

```python
def parse_arguments() -> argparse.Namespace:
    """ARGUMENT PARSING - ARGUMENT PARSING LIBRARY"""
    """Parse command-line arguments using argparse
    Supported arguments:
    - positional skill_name: optional skill name to validate
    - --all flag: batch process all skills
    - --help flag: display help information

    Returns: argparse.Namespace with attributes:
    - skill_name: Optional[str]
    - all: bool
    - help: bool
    """
    pass

def validate_single_skill(skill_name: str) -> Optional[Dict[str, Any]]:
    """SINGLE SKILL VALIDATION - ORCHESTRATION"""
    """Validate specific skill by name
    Returns: ValidationResult dict or None if skill not found
    """
    pass

def process_all_skills() -> List[Dict[str, Any]]:
    """BATCH PROCESSING - 3-BATCH SYSTEM"""
    """Process all skills in 3 systematic batches:
    - Batch 1: Core skills
    - Batch 2: Extension skills
    - Batch 3: Edge cases and error handling

    Returns: List of all validation results
    """
    pass

def run_health_check(skill_name: Optional[str] = None, all_flag: bool = False) -> List[Dict[str, Any]]:
    """MAIN EXECUTION - DELEGATION"""
    """Main health check orchestration
    Coordinates discovery, validation, and reporting
    """
    pass

def show_help() -> None:
    """HELP DISPLAY - USER INFORMATION"""
    """Display comprehensive help information
    Shows usage examples, available options, output formats
    """
    pass
```

#### Contract Specifications

- **CLI Interface**: Must support exact patterns from requirements.md
- **Argument Parsing**: Uses standard argparse with proper error handling
- **Output Formatting**: Console output follows established formats
- **Help System**: Comprehensive help with examples and descriptions
- **Error Handling**: User-friendly error messages and exit codes

### 5. Main Module Contract (`main.py`)

#### Method Contracts

```python
class HealthCheckOrchestrator:
    """ORCHESTRATION COORDINATOR - WORKFLOW MANAGEMENT"""
    def __init__(self):
        self.validation_orchestrator = ValidationOrchestrator()
        self.results = []

    def run_skill_validation(self, skill_path: Path) -> ValidationResult:
        """SINGLE SKILL VALIDATION - ORCHESTRATION"""
        """Validate skill using modular validation system
        Returns: ValidationResult from validation orchestrator
        """
        pass

    def run_all_skills(self) -> list:
        """ALL SKILLS VALIDATION - BATCH ORCHESTRATION"""
        """Validate all discovered skills
        Returns: List of ValidationResult objects
        """
        pass

    def run_single_skill(self, skill_name: str = None, skill_path: str = None) -> list:
        """SINGLE SKILL BY PATH - FLEXIBLE TARGETING"""
        """Validate single skill by name or path
        Returns: List containing single ValidationResult or empty list
        """
        pass

    def generate_all_reports(self, results: list):
        """REPORT GENERATION - COORDINATION"""
        """Generate all reports using modular reporting system
        Coordinates with reporting module for all output formats
        """
        pass

    def run_batch_validation(self):
        """3-BATCH EXECUTION - SYSTEMATIC PROCESSING"""
        """Execute batch validation in 3 systematic batches
        Orchestrates the 3-batch processing system
        """
        pass

    def run(self, mode: str = "all", skill_name: str = None, skill_path: str = None):
        """MAIN EXECUTION - HIGH-LEVEL COORDINATION"""
        """Main execution method - coordinates all modules
        Handles mode selection, execution, and reporting
        """
        pass
```

#### Public Function Interface

```python
def legacy_healthcheck_main() -> int:
    """LEGACY MAIN - BACKWARD COMPATIBILITY"""
    """Legacy main function for backward compatibility
    Maintains exact behavior of original healthcheck.py
    """
    pass

def main() -> int:
    """MODERN MAIN - ENTRY POINT"""
    """Main entry point - delegates to legacy for compatibility
    Can be extended for new functionality
    """
    pass
```

#### Contract Specifications

- **Orchestration**: Coordinates all modules without direct implementation
- **State Management**: Maintains execution state and results
- **Workflow Control**: Manages execution flow and error handling
- **Backward Compatibility**: Supports legacy execution path
- **Extensibility**: Easy to add new workflows and processing modes

## Interface Contract Compliance Matrix

| Contract | Validation | Discovery | Reporting | CLI | Main |
|----------|------------|-----------|-----------|-----|------|
| **Method Signatures** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Return Types** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Parameter Types** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Error Handling** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Data Structure Compatibility** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Pure Function Requirements** | ✓ | ✓ | ✗ | ✗ | ✗ |
| **Performance Requirements** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Testing Requirements** | ✓ | ✓ | ✓ | ✓ | ✓ |
| **Backward Compatibility** | ✓ | ✓ | ✓ | ✓ | ✓ |

## Dependency Graph

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  main.py    │───▶│   cli.py    │───▶│ validation │───▶│discovery.py│
│(orchestrator)│   │(CLI interface) │   │(validation) │   │(discovery) │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
                                   │                    │
                                   ▼                    ▼
                               ┌─────────────┐    ┌─────────────┐
                               │ reporting   │◀───│validation   │
                               │(reporting) │    │(results)    │
                               └─────────────┘    └─────────────┘
```

## Interface Contract Violations and Resolutions

### Violation 1: Duplicate Validation Logic
**Location**: `skills/healthcheck/core/validation.py` vs `skills/healthcheck/cli.py`
**Issue**: Both have `validate_skill_file()` but different implementations
**Resolution**: Keep `skills/healthcheck/core/validation.py` as single source of truth, make `cli.py` delegate to it

### Violation 2: Duplicate Discovery Logic
**Location**: `skills/healthcheck/discovery.py` vs `skills/healthcheck/core/discovery.py`
**Issue**: Different implementations and signatures
**Resolution**: Keep `skills/healthcheck/core/discovery.py`, delete `skills/healthcheck/discovery.py`

### Violation 3: Mixed Responsibilities
**Location**: `skills/healthcheck/main.py` contains both orchestration and legacy logic
**Issue**: Single module has multiple responsibilities
**Resolution**: Split into `orchestrator.py` (pure orchestration) and `main.py` (entry point)

## Interface Contract Enforcement Protocol

### Phase 1: Contract Definition (Week 1)
1. All modules implement interface contracts
2. Type hints fully applied
3. Method signatures match contracts exactly
4. Documentation updated to reflect contracts

### Phase 2: Contract Compliance (Week 2)
1. Static analysis for interface compliance
2. Interface contract tests added to test suite
3. Contract violations fixed
4. Integration testing of interface contracts

### Phase 3: Contract Maintenance (Ongoing)
1. Interface contracts versioned with each major release
2. Breaking changes require version bump
3. Contract evolution plan for future enhancements
4. Regular interface contract reviews

## Interface Contract Testing Strategy

### Unit Testing
- Each module independently tested
- Mock dependencies where appropriate
- Interface contract violations caught early

### Integration Testing
- Module interactions tested
- Interface contracts exercised end-to-end
- Error conditions tested

### Contract Testing
- Interface compliance tests
- Version compatibility tests
- Backward compatibility verification

## Conclusion

Interface contracts provide the foundation for a maintainable, extensible, and testable modular architecture. By strictly defining and enforcing these contracts:

1. **Eliminates ambiguity** in module responsibilities and interfaces
2. **Enforces consistency** across all implementations
3. **Enables independent testing** of each module
4. **Prevents integration issues** through clear dependency definitions
5. **Facilitates future extensions** through well-defined interfaces

The interface contracts serve as the architectural backbone that ensures the healthcheck skill remains maintainable, testable, and extensible while preserving all existing functionality.