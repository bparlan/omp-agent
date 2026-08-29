# Healthcheck Skill Modular Decomposition Requirements

## Overview
This document defines the provisional requirements for transforming the monolithic healthcheck.py script into a modular architecture while maintaining backward compatibility and enabling future extensibility.

## Current State Analysis

### Monolithic healthcheck.py (237 lines)
**Location:** `/Users/bparlan/devcode/aef/agent/skills/healthcheck/healthcheck.py`

**Current Components:**
1. **Discovery Logic** (`discover_skills_directory()`, `SKILLS_DIR`): Project-agnostic skill directory discovery
2. **Validation Logic** (`validate_skill_file()`): Core validation of SKILL.md files
3. **Skill Discovery** (`discover_skills()`): Finds skill directories and SKILL.md files
4. **Orchestration** (`run_health_check()`): Main execution flow, validation, reporting
5. **Reporting** (`generate_badges()`, `generate_health_report()`, `generate_processed_skills()`): Three output formats
6. **CLI Interface** (`main()`): Command-line argument parsing and entry point

**Current Features:**
- Validates SKILL.md frontmatter (name, version, description, tools, userInvocable)
- Checks for -stable suffix in version fields
- Supports both single-skill and --all batch processing modes
- Generates three report types: health_badges.md, health_check_report.json, processed_skills.json
- Maintains backward-compatible CLI interface

## Requirements Model

### 1. Modular Architecture Requirements

#### Core Components (5 Modules)
**Goal:** Decompose monolithic script into focused, single-responsibility modules

1. **core/validation.py** - Pure validation logic with Validator base classes
2. **discovery.py** - Skill discovery mechanisms with project root detection
3. **reporting.py** - All reporting functionality (badges, JSON reports, processed skills)
4. **cli.py** - CLI parsing and orchestration with argument handling
5. **main.py** - Clean entry point that imports and runs modules

#### Single Responsibility Principle
Each module must have exactly one reason to change:
- `validation.py`: Validation rules and scoring
- `discovery.py`: Skill directory detection and discovery
- `reporting.py`: Report generation and formatting
- `cli.py`: CLI argument parsing and user interaction
- `main.py`: Application orchestration and workflow coordination

### 2. Backward Compatibility Requirements

#### CLI Interface Preservation
**Requirement:** All existing CLI usage patterns must continue to work identically

- `python3 healthcheck.py [skill_name]` - Check specific skill
- `python3 healthcheck.py --all` - Process all skills in 3 batches
- `python3 healthcheck.py --help` - Show help

**Implementation Details:**
- Same command-line argument parsing behavior
- Same output format and order
- Same exit codes for success/failure
- Same error messages and formatting
- Same report file generation

#### Functional Equivalence
**Requirement:** All existing functionality must produce identical results
- Validation logic: Same scoring algorithm and status determination
- Discovery: Same skill detection patterns and fallback strategies
- Reporting: Same output formats and content structure
- Error handling: Same error types and messages

### 3. Single Skill vs Batch Processing Requirements

#### Single Skill Mode
**Requirement:** Must support checking individual skills
- Input: Specific skill name or path
- Output: Focused validation results for that skill only
- Behavior: Process only the specified skill

#### Batch Mode (--all flag)
**Requirement:** Must support processing all skills in systematic batches
- Input: --all flag
- Output: Comprehensive reports for all skills
- Behavior: Process skills in 3 systematic batches for maintainability

#### Batch Processing Details
- **Batch 1:** Core skills validation
- **Batch 2:** Extension skills validation
- **Batch 3:** Edge cases and error handling
- Processing must maintain identical validation logic across all batches

### 4. Future Extensibility Requirements

#### Plugin Architecture
**Requirement:** Enable easy addition of new validation rules and processors
- Validation rules: New Validator subclasses without modifying existing code
- Output formats: New report generators without modifying core modules
- Discovery strategies: New skill detection methods

#### Validation Rule Extension
**Requirement:** Support new validation rules via inheritance
```python
class NewValidator(ValidatorBase):
    def validate(self, content: str) -> Dict[str, Any]:
        # Custom validation logic
        pass
```

#### Output Format Extension
**Requirement:** Support new report formats
```python
class NewReportGenerator:
    def generate(self, results: List[Dict]) -> str:
        # Custom report format
        pass
```

### 5. Technical Requirements

#### Code Structure Requirements
- Each module must be independently importable
- No circular dependencies between modules
- Module interfaces must be clearly defined
- Each module must have comprehensive error handling

#### Testing Requirements
- Each module must be unit testable independently
- Validation logic must be pure functions (no side effects)
- Discovery logic must be deterministic and testable
- CLI module must be testable without actual execution

#### Performance Requirements
- Must maintain or improve performance compared to monolithic version
- Memory usage must be reasonable for large skill repositories
- Processing time must remain within acceptable limits

### 6. Quality Assurance Requirements

#### Code Quality
- Each module must follow established Python conventions
- Code must be well-documented with docstrings
- Type hints must be used throughout
- Error handling must be comprehensive

#### Validation Logic Requirements
- Validation rules must be decoupled from I/O operations
- Scoring algorithms must be deterministic
- Validation results must be consistent across runs
- Edge cases must be handled gracefully

#### Reporting Requirements
- All reports must be machine-readable and human-readable
- Report formats must be stable and documented
- Generated files must include timestamps and metadata
- Report content must be validated before generation

### 7. Migration Requirements

#### Phase 1: Core Module Extraction
**Priority:** Highest
- Extract validation logic from healthcheck.py to core/validation.py
- Preserve all existing validation rules and scoring
- Ensure validation logic is pure and testable

#### Phase 2: Discovery Module Creation
**Priority:** High
- Extract discovery logic from healthcheck.py to discovery.py
- Maintain all discovery strategies and fallbacks
- Ensure project-agnostic discovery works

#### Phase 3: Reporting Module Creation
**Priority:** High
- Extract all report generation to reporting.py
- Support all existing report formats
- Ensure reports are generated in same format

#### Phase 4: CLI Module Creation
**Priority:** Medium
- Extract CLI parsing and orchestration to cli.py
- Maintain all CLI options and behavior
- Ensure backward compatibility

#### Phase 5: Main Module Creation
**Priority:** Medium
- Create main.py as clean entry point
- Coordinate all modules
- Maintain workflow orchestration

#### Phase 6: Integration and Testing
**Priority:** Critical
- Ensure all modules work together
- Maintain backward compatibility
- Write comprehensive tests for each module
- Verify all existing functionality preserved

### 8. Success Criteria

#### Functional Requirements
- [ ] All existing CLI commands work identically
- [ ] All validation rules produce same results
- [ ] All report formats are identical
- [ ] Single-skill mode works correctly
- [ ] Batch processing (--all) works correctly
- [ ] Error handling is consistent

#### Architecture Requirements
- [ ] Each module has single responsibility
- [ ] No circular dependencies exist
- [ ] All modules are independently testable
- [ ] Validation logic is pure and decoupled
- [ ] Future extensibility is enabled

#### Quality Requirements
- [ ] Code follows Python conventions
- [ ] Comprehensive documentation exists
- [ ] Type hints are used throughout
- [ ] Error handling is robust
- [ ] Performance is maintained or improved

### 9. Non-Functional Requirements

#### Maintainability
- Modules must be easily modifiable
- Changes to one module must not affect others
- Code must be readable and well-structured
- Documentation must be comprehensive

#### Extensibility
- New validation rules must be easy to add
- New output formats must be easy to add
- New discovery strategies must be easy to add
- CLI extensions must be straightforward

#### Reliability
- All edge cases must be handled
- Error conditions must be properly managed
- Output must be validated before generation
- Processes must be robust against failures

## Implementation Roadmap

### Week 1: Core Module Extraction
1. Extract validation logic to core/validation.py
2. Refactor existing validation into Validator base classes
3. Ensure backward compatibility

### Week 2: Discovery Module Creation
1. Extract discovery logic to discovery.py
2. Create project-agnostic discovery strategies
3. Test discovery against various directory structures

### Week 3: Reporting Module Creation
1. Extract reporting logic to reporting.py
2. Create report generators for all formats
3. Ensure report formats are identical

### Week 4: CLI Module Creation
1. Extract CLI parsing to cli.py
2. Create CLI argument handling
3. Maintain backward-compatible interface

### Week 5: Integration and Testing
1. Create main.py as orchestrator
2. Integrate all modules
3. Write comprehensive tests
4. Verify backward compatibility

### Week 6: Validation and Deployment
1. Run all existing functionality
2. Verify all requirements are met
3. Deploy modular architecture
4. Monitor for issues

## Conclusion

This requirements model provides a comprehensive blueprint for transforming the monolithic healthcheck.py into a modular, maintainable, and extensible architecture while preserving all existing functionality. The modular design will enable future extensions, improve testability, and reduce cognitive complexity, while the strict backward compatibility requirements ensure no disruption to existing users.