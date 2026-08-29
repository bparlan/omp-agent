# Healthcheck Skill Modular Decomposition Requirements Mapping

## Executive Summary

This document provides a comprehensive mapping of the modular decomposition requirements for the healthcheck skill, identifying conflicts, defining interface contracts, and establishing a clear implementation roadmap to resolve architectural ambiguities.

## Current Conflict Analysis

### Conflict 1: Duplicate Discovery Logic
**Files Conflicting**:
- `skills/healthcheck/discovery.py` (80 lines) - Direct implementation
- `skills/healthcheck/core/discovery.py` (132 lines) - Extended implementation

**Conflict Points**:
1. Different global variable names (`skills_dir` vs `skill_files`)
2. Different function signatures and implementations
3. Different test expectations

**Resolution**: Keep `skills/healthcheck/discovery.py` as primary, merge into core/ structure.

### Conflict 2: Duplicate Validation Logic
**Files Conflicting**:
- `skills/healthcheck/core/validation.py` (184 lines) - ValidatorBase pattern
- `skills/healthcheck/cli.py` (198 lines) - SkillValidator pattern
- `skills/healthcheck/main.py` (190 lines) - ValidationOrchestrator pattern

**Conflict Points**:
1. Different base classes (ValidatorBase vs Validator vs SkillValidator)
2. Different interfaces and return types
3. Conflicting test expectations

**Resolution**: Consolidate into single validation.py following ValidatorBase pattern.

### Conflict 3: Split CLI and Main Logic
**Files Conflicting**:
- `skills/healthcheck/cli.py` (198 lines) - Current main functionality
- `skills/healthcheck/main.py` (190 lines) - Orchestration wrapper

**Conflict Points**:
1. CLI logic embedded in cli.py vs main.py
2. Argument parsing duplicated
3. Test expectations conflict

**Resolution**: Consolidate CLI functionality into single cli.py, make main.py clean orchestrator.

## Interface Contract Specifications

### 1. Discovery Module Contract
```python
# Expected interface based on requirements
from pathlib import Path
from typing import List, Optional

def discover_skills_directory() -> Path:
    """Project-agnostic skill directory discovery"""
    pass

def get_skills_directory() -> Path:
    """Cached discovery result"""
    pass

def discover_skills() -> List[Path]:
    """Find all SKILL.md files"""
    pass

def discover_skill_by_name(skill_name: str) -> Optional[Path]:
    """Find specific skill by name"""
    pass
```

### 2. Validation Module Contract
```python
# Expected interface based on requirements
from pathlib import Path
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class ValidationResult:
    name: str
    status: str
    validation_score: float
    has_stable_suffix: bool
    issues: List[str]
    last_modified: str
    last_checked: str

class ValidatorBase:
    """Base validator class for skill validation rules"""
    pass

class RequiredFieldsValidator(ValidatorBase):
    pass

class StableSuffixValidator(ValidatorBase):
    pass

class SkillNameValidator(ValidatorBase):
    pass

class ValidationOrchestrator:
    """Orchestrates validation using multiple validators"""
    pass

def validate_skill_file(skill_path: Path) -> Dict[str, Any]:
    """Public validation interface"""
    pass
```

### 3. Reporting Module Contract
```python
# Expected interface based on requirements
from pathlib import Path
from typing import List, Dict, Any

def generate_badges(results: List[Dict[str, Any]]) -> None:
    """Generate health_badges.md"""
    pass

def generate_health_report(results: List[Dict[str, Any]]) -> None:
    """Generate health_check_report.json"""
    pass

def generate_processed_skills(results: List[Dict[str, Any]]) -> None:
    """Generate processed_skills.json"""
    pass
```

### 4. CLI Module Contract
```python
# Expected interface based on requirements
from typing import Dict, Any, Optional, List

def parse_arguments() -> Dict[str, Any]:
    """CLI argument parsing"""
    pass

def validate_single_skill(skill_name: str) -> Optional[Dict[str, Any]]:
    """Single skill validation"""
    pass

def process_all_skills() -> List[Dict[str, Any]]:
    """Batch processing of all skills"""
    pass

def run_health_check(skill_name: Optional[str] = None, all_flag: bool = False) -> List[Dict[str, Any]]:
    """Main health check orchestration"""
    pass
```

### 5. Main Module Contract
```python
# Expected interface based on requirements
def main() -> int:
    """Entry point and orchestrator"""
    pass
```

## Structured Implementation Plan

### Phase 1: Code Consolidation (Week 1)

**Actions**:
1. Remove duplicate files:
   - Delete `skills/healthcheck/discovery.py` (keep core/discovery.py)
   - Delete `skills/healthcheck/core/cli.py` (keep cli.py)
   - Delete `skills/healthcheck/healthcheck.py` (keep as legacy wrapper)
   - Delete `skills/healthcheck/healthcheck_modular/` (empty)

2. Consolidate core modules into `skills/healthcheck/core/`:
   ```
   skills/healthcheck/
   ├── core/
   │   ├── validation.py      # Single validation implementation
   │   ├── discovery.py      # Single discovery implementation
   │   └── reporting.py      # Single reporting implementation
   │
   ├── cli.py               # Consolidated CLI interface
   └── main.py              # Clean orchestrator
   ```

3. Update imports in all modules to use correct paths

**Success Criteria**:
- Exactly 5 core modules exist
- No duplicate functionality
- All imports resolved
- Tests pass

### Phase 2: Interface Contract Enforcement (Week 2)

**Actions**:
1. Update validation.py to follow ValidatorBase pattern
2. Ensure validation.py is pure (no side effects)
3. Implement strict interface contracts in each module
4. Add comprehensive type hints
5. Update test expectations to match new contracts

**Interface Contract Enforcement**:
```python
# Example: Pure validation function validation.py
from pathlib import Path
from typing import Dict, Any

def validate_skill_file(skill_path: Path) -> Dict[str, Any]:
    """Pure validation - no I/O operations"""
    # Read file content
    content = skill_path.read_text()

    # Pure validation logic (no writes, no system calls)
    score = calculate_validation_score(content)
    has_stable = "-stable" in content.lower()

    return {
        "name": extract_skill_name(content),
        "status": "healthy" if score >= 0.8 else "needs_review",
        "validation_score": score,
        "has_stable_suffix": has_stable,
        "issues": find_issues(content),
        "last_modified": get_last_modified(skill_path),
        "last_checked": get_current_timestamp()
    }
```

### Phase 3: Backward Compatibility Preservation (Week 3)

**Actions**:
1. Maintain exact CLI interface:
   - `python3 healthcheck.py [skill_name]`
   - `python3 healthcheck.py --all`
   - `python3 healthcheck.py --help`

2. Preserve exact output formats and ordering
3. Maintain same exit codes and error messages
4. Ensure all three report files are generated
5. Keep 3-batch processing behavior

**CLI Interface Preservation**:
```python
# From test_modular_healthcheck.py - must pass
from cli import parse_arguments

sys.argv = ['healthcheck.py', 'my_skill']
args = parse_arguments()
assert args.skill_name == "my_skill"

sys.argv = ['healthcheck.py', '--all']
args = parse_arguments()
assert args.all == True

sys.argv = ['healthcheck.py', '--help']
args = parse_arguments()
assert args.help == True
```

### Phase 4: Testing Strategy Alignment (Week 4)

**Actions**:
1. Update test_modular_healthcheck.py to test new consolidated structure
2. Ensure all test requirements are met:
   - Modules independently importable
   - Validator base class extensible
   - Validation logic pure
   - CLI interface preserved
   - Both single-skill and batch processing work

3. Create comprehensive unit tests for each module
4. Add integration tests for module interactions

**Testing Strategy Updates**:
```python
# Updated test expectations from test_modular_healthcheck.py

# Requirement 1: Modular architecture
required_modules = [
    "core/validation.py",    # Single file
    "discovery.py",          # From core/
    "reporting.py",          # From core/
    "cli.py",                # Main cli.py
    "main.py"                # Clean orchestrator
]

# Requirement 2: Backward compatibility
# CLI interface must match exact test expectations

# Requirement 3: Extensibility
# ValidatorBase must be importable from core.validation

# Requirement 4: Technical structure
# All modules must be independently importable
```

## Conflict Resolution Matrix

| Conflict | Location | Impact | Resolution |
|----------|----------|--------|------------|
| Duplicate discovery logic | discovery.py vs core/discovery.py | Medium | Keep core/discovery.py, remove discovery.py |
| Validation pattern conflicts | validation.py vs cli.py vs main.py | High | Consolidate into single validation.py (ValidatorBase) |
| CLI/main separation | cli.py vs main.py | Medium | Consolidate CLI into cli.py, clean main.py |
| Empty modular directory | healthcheck_modular/ | Low | Remove (no content) |
| Duplicate validation functions | healthcheck.py vs others | High | Remove healthcheck.py, keep as legacy wrapper |

## Critical Dependencies Analysis

### Required Dependencies for Each Module

1. **validation.py**: None (pure validation logic)
2. **discovery.py**: file system access (Path operations)
3. **reporting.py**: file system access + validation results
4. **cli.py**: all modules + sys.argv
5. **main.py**: all modules + orchestrator logic

### Circular Dependency Prevention

```python
# Allowed dependencies (unidirectional):
main.py → cli.py
main.py → discovery.py
main.py → validation.py
main.py → reporting.py

cli.py → discovery.py
cli.py → validation.py
cli.py → reporting.py

discovery.py → validation.py  (for skill name extraction)
validation.py → None
reporting.py → None
```

## Success Metrics

### Architecture Success Metrics
- **Module Count**: Exactly 5 core modules
- **Dependency Count**: Each module has max 2 direct dependencies
- **Cyclomatic Complexity**: Each module < 20
- **Test Coverage**: Each module > 80% tested

### Compatibility Success Metrics
- **CLI Interface**: 100% backward compatible (all test cases pass)
- **Functional Equivalence**: Identical validation results
- **Output Formats**: All three report types identical
- **Error Handling**: Same error types and messages

### Quality Success Metrics
- **Type Safety**: Comprehensive type hints in all modules
- **Documentation**: Docstrings for all public functions
- **Code Structure**: Single responsibility per module
- **Maintainability**: Easy to modify and extend

## Implementation Timeline

### Week 1: Consolidation Phase
- Days 1-2: Remove duplicate files and consolidate structure
- Days 3-4: Update imports and resolve dependency issues
- Days 5-6: Basic functionality testing
- Day 7: Initial test run

### Week 2: Contract Enforcement Phase
- Days 8-10: Implement interface contracts and type safety
- Days 11-12: Ensure validation logic purity
- Days 13-14: Documentation and code review
- Day 15: Integration testing

### Week 3: Compatibility Phase
- Days 16-18: Preserve CLI interface and backward compatibility
- Days 19-20: Ensure exact output format preservation
- Days 21-22: Error handling consistency
- Days 23-24: Final compatibility testing

### Week 4: Validation Phase
- Days 25-27: Run comprehensive test suite
- Days 28-29: Performance and edge case testing
- Days 30-31: Documentation updates
- Day 32: Final deployment validation

## Conclusion

This requirements mapping provides a clear path to resolve the healthcheck skill's modular decomposition ambiguities. By:

1. **Consolidating duplicate code** into a clean 5-module architecture
2. **Enforcing strict interface contracts** to ensure maintainability
3. **Preserving backward compatibility** to prevent disruption
4. **Implementing comprehensive testing** to ensure quality

The healthcheck skill will achieve a robust, maintainable, and extensible modular architecture while maintaining all existing functionality. The structured approach minimizes risk and provides clear milestones for successful completion.

**Key Risk Mitigation**:
- Code deduplication eliminates functionality conflicts
- Interface contracts prevent integration issues
- Backward compatibility preserves existing user workflows
- Comprehensive testing ensures quality and reliability
- Clear timeline provides accountability and progress tracking

The solution is ready for immediate implementation following this structured roadmap.