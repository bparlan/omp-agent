# Healthcheck Skill Modular Structure

## Overview

This document defines the final consolidated modular structure for the healthcheck skill, implementing the requirements mapping and resolving all architectural ambiguities.

## Final 5-Module Architecture

```
skills/healthcheck/
├── core/
│   ├── validation.py      # 176 lines - Pure validation logic
│   ├── discovery.py      # 132 lines - Discovery logic
│   └── reporting.py      # 228 lines - Reporting logic
│
├── cli.py               # 193 lines - CLI interface
└── main.py              # Clean orchestrator
```

## Module Details

### 1. Core/Validation.py
**Purpose**: Pure validation logic with Validator base classes and validation orchestrators
**Lines**: 176
**Responsibility**: SKILL.md validation, scoring, status determination
**Interface**: `ValidationOrchestrator.validate_skill_file()`

### 2. Core/Discovery.py
**Purpose**: Project-agnostic skill directory detection and discovery
**Lines**: 132
**Responsibility**: Project root finding, skill location
**Interface**: `discover_skills()`, `get_skills_directory()`

### 3. Core/Reporting.py
**Purpose**: All reporting functionality (badges, JSON reports, processed skills)
**Lines**: 228
**Responsibility**: Report generation and formatting
**Interface**: `generate_badges()`, `generate_health_report()`, `generate_processed_skills()`

### 4. CLI.py
**Purpose**: CLI parsing and orchestration with argument handling
**Lines**: 193
**Responsibility**: CLI interface and user interaction
**Interface**: `parse_arguments()`, `run_health_check()`

### 5. Main.py
**Purpose**: Clean entry point that imports and runs modules
**Lines**: 190
**Responsibility**: Application orchestration and workflow coordination
**Interface**: `main()`, `HealthCheckOrchestrator` coordination

## Consolidation Actions Required

### Phase 1: Remove Duplicate Files

**Files to delete**:
1. `skills/healthcheck/discovery.py` (80 lines) - Duplicate of core/discovery.py
2. `skills/healthcheck/healthcheck.py` (21 lines) - Legacy wrapper, keep as-is
3. `skills/healthcheck/healthcheck_modular/` (empty directory) - Remove entirely
4. Any other duplicate files in subdirectory listings

**Files to keep**:
- `skills/healthcheck/core/validation.py` (176 lines) - Single validation implementation
- `skills/healthcheck/core/discovery.py` (132 lines) - Single discovery implementation
- `skills/healthcheck/core/reporting.py` (228 lines) - Single reporting implementation
- `skills/healthcheck/cli.py` (193 lines) - Main CLI interface
- `skills/healthcheck/main.py` (190 lines) - Clean orchestrator

### Phase 2: Update Imports

**Current problematic imports**:
```python
# In core/validation.py
sys.path.insert(0, str(Path(__file__).parent))
from core.validation import ...

# In cli.py
from discovery import get_skills_directory
from core.validation import SkillValidator
from reporting import generate_badges, generate_health_report, generate_processed_skills
```

**Required updates**:
- All imports must reference correct paths
- Remove unnecessary path manipulation
- Use relative imports where possible

### Phase 3: Interface Contract Compliance

**Validation Module Contract**:
```python
# Expected interface after consolidation
from pathlib import Path
from typing import Dict, Any

class ValidationOrchestrator:
    def validate_skill_file(self, skill_path: Path) -> Dict[str, Any]:
        pass

class ValidatorBase:
    def validate(self, content: str, skill_path: Path) -> Dict[str, Any]:
        pass
```

**Discovery Module Contract**:
```python
# Expected interface after consolidation
from pathlib import Path
from typing import List, Optional

def discover_skills_directory() -> Path:
    pass

def discover_skills() -> List[Path]:
    pass
```

**Reporting Module Contract**:
```python
# Expected interface after consolidation
from pathlib import Path
from typing import List, Dict, Any

def generate_badges(results: List[Dict[str, Any]]) -> None:
    pass
```

**CLI Module Contract**:
```python
# Expected interface after consolidation
from typing import Optional, List, Dict, Any

def parse_arguments() -> Dict[str, Any]:
    pass

def run_health_check(skill_name: Optional[str] = None, all_flag: bool = False) -> List[Dict[str, Any]]:
    pass
```

### Phase 4: Test Suite Updates

**test_modular_healthcheck.py expectations**:
- Checks for existence of: `core/validation.py`, `discovery.py`, `reporting.py`, `cli.py`, `main.py`
- Tests CLI interface with exact patterns
- Tests Validator base class extensibility
- Tests module importability

**Required test updates**:
- Update module paths in test imports
- Verify CLI interface matches test expectations
- Ensure all contract requirements met

## File Structure After Consolidation

### Core Module Structure

**Core/Validation.py**:
- `ValidationResult` dataclass (immutable data structure)
- `ValidatorBase` abstract base class
- `RequiredFieldsValidator` implementation
- `StableSuffixValidator` implementation
- `SkillNameValidator` implementation
- `ValidationOrchestrator` class
- `validate_skill_file()` public function

**Core/Discovery.py**:
- `discover_skills_directory()` function
- `get_skills_directory()` function (cached)
- `discover_skills()` function
- `discover_skill_by_name()` function
- `get_skills_summary()` function

**Core/Reporting.py**:
- `generate_badges()` function
- `generate_health_report()` function
- `generate_processed_skills()` function
- `generate_skills_summary()` function

### Non-Core Module Structure

**CLI.py**:
- `parse_arguments()` function
- `validate_single_skill()` function
- `process_all_skills()` function
- `run_health_check()` function
- `show_help()` function

**Main.py**:
- `HealthCheckOrchestrator` class
- `legacy_healthcheck_main()` function
- `main()` function (entry point)

## Dependency Management

### Allowed Dependencies (Unidirectional)

```
main.py → cli.py
main.py → discovery.py
main.py → validation.py
main.py → reporting.py

cli.py → discovery.py
cli.py → validation.py
cli.py → reporting.py

discovery.py → validation.py (for skill name extraction)
validation.py → None (pure function)
reporting.py → None (pure function)
```

### Dependency Elimination

**Current problematic dependencies**:
- `cli.py` importing from `discovery.py` (should be `core.discovery`)
- `cli.py` importing from `core.validation` (correct)
- `cli.py` importing from `reporting` (should be `core.reporting`)

**Required fixes**:
- Update all imports to use correct module paths
- Remove any circular dependencies
- Ensure dependency direction is strictly unidirectional

## Interface Contract Enforcement

### Validation Module Purity Requirements

**Must be pure functions** (no side effects):
- `validate_skill_file(skill_path: Path) -> Dict[str, Any]`
- All validator methods (`validate(content: str, skill_path: Path)`)
- No `write_text()`, `open()`, `sys.stdout`, `os.environ` calls

**Current status check**:
```python
# From test_modular_healthcheck.py
assert "write_text" not in source
assert "open(" not in source
assert "os." not in source or "os.environ" not in source
assert "sys." not in source or "sys.argv" not in source
```

### Discovery Module Determinism Requirements

**Must be deterministic**:
- Same input → same output
- No reliance on external state
- File system access only through parameters

### Reporting Module Output Requirements

**Must generate valid output**:
- JSON reports must be parsable
- Markdown reports must have proper format
- Files must include timestamps

## Backward Compatibility Preservation

### CLI Interface Requirements

**Exact patterns from requirements**:
```bash
python3 healthcheck.py [skill_name]           # Single skill
python3 healthcheck.py --all                 # Batch processing
python3 healthcheck.py --help                # Help
```

**Expected behavior**:
- Same argument parsing logic
- Same output formatting
- Same exit codes
- Same error messages

### Functional Requirements

**Must preserve all existing functionality**:
- SKILL.md validation (name, version, description, tools, userInvocable)
- -stable suffix checking in version fields
- 3-batch processing system
- Three report file generation
- Error handling consistency

## Implementation Timeline

### Week 1: Consolidation Phase (Days 1-7)
**Goal**: Remove duplicates and establish clean structure

**Actions**:
1. Remove duplicate files (discovery.py, healthcheck_modular/)
2. Update imports across all modules
3. Verify interface contracts
4. Run basic functionality tests

**Success Metrics**:
- Exactly 5 core modules exist
- All imports resolved
- Basic functionality preserved

### Week 2: Interface Compliance Phase (Days 8-14)
**Goal**: Enforce interface contracts and type safety

**Actions**:
1. Update validation.py to be pure functions
2. Ensure all method signatures match contracts
3. Add comprehensive type hints
4. Update test expectations

**Success Metrics**:
- All modules independently importable
- Validation logic is pure
- CLI interface tests pass

### Week 3: Compatibility Phase (Days 15-21)
**Goal**: Preserve 100% backward compatibility

**Actions**:
1. Verify exact CLI interface preservation
2. Test all output formats
3. Validate 3-batch processing
4. Run comprehensive compatibility tests

**Success Metrics**:
- All CLI test patterns pass
- All report formats identical
- Functional equivalence verified

### Week 4: Validation Phase (Days 22-28)
**Goal**: Full system validation and deployment

**Actions**:
1. Run complete test suite
2. Performance benchmarking
3. Edge case testing
4. Final deployment validation

**Success Metrics**:
- All tests pass
- Architecture meets all requirements
- Ready for production deployment

## Current Status

**Analysis Complete**: ✅
**Documentation Created**: ✅ (3 comprehensive deliverables)
**Architecture Defined**: ✅ (Clean 5-module structure)
**Interface Contracts Established**: ✅ (Detailed contracts for all modules)

**Ready for Phase 1 Implementation**: Code consolidation and structure cleanup begins next week.

## Conclusion

The healthcheck skill modular decomposition task has progressed through the analysis phase with comprehensive deliverables. The final consolidated structure will eliminate all ambiguities and conflicts while preserving 100% backward compatibility.

The 5-module architecture provides:
- **Clear separation of concerns** (Single responsibility per module)
- **Strong interface contracts** (Well-defined module boundaries)
- **Independent testability** (Each module can be tested in isolation)
- **Future extensibility** (Plugin architecture enabled)
- **Maintainable code** (Reduced cognitive complexity)

Ready for immediate implementation following the structured roadmap.