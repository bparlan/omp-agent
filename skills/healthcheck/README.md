# Healthcheck Skill

## Overview
AEF-OMP skill for validating skill SKILL.md files and checking -stable suffix in versions.

## Architecture
The healthcheck skill has been refactored from a monolithic 237-line script into a modular architecture for better maintainability and agentic efficiency:

1. **core/validation.py** - Pure validation logic with Validator base classes and validation orchestrators
2. **discovery.py** - Skill discovery mechanisms with project root detection
3. **reporting.py** - All reporting functionality (badges, JSON reports, processed skills)
4. **cli.py** - CLI parsing and orchestration with argument handling
5. **main.py** - Entry point that imports and runs modules

## Features
- Validates SKILL.md frontmatter (name, version, description, tools, userInvocable fields)
- Checks for -stable suffix in version fields
- Detects malformed frontmatter and formatting issues
- Supports both single-skill and batch processing modes
- Generates multiple output formats (Markdown badges, JSON reports, processed skills)
- Maintains backward-compatible CLI interface

## Usage
```bash
python3 healthcheck.py [skill_name]           # Check specific skill
python3 healthcheck.py --all                 # Process all skills in 3 batches
python3 healthcheck.py --help                # Show help
```

## Validation Rules
The skill validates the following:
- Required frontmatter fields are present
- Version fields have -stable suffix
- Frontmatter delimiters are properly formatted
- Description field follows naming conventions
- Backtick fencing is properly formatted

## Output
The healthcheck generates three types of reports:
1. **health_badges.md** - Table with skill status and validation scores
2. **health_check_report.json** - Detailed JSON report with all skills
3. **processed_skills.json** - Name-to-result mapping for easy access

## Testing
Each module is independently testable:
- Validation tests in core/validation.py
- Discovery tests in discovery.py
- Report generation tests in reporting.py
- CLI argument parsing tests in cli.py

## Future Extensions
The modular architecture enables easy extension:
- Add new validation rules by extending Validator base class
- Support new output formats in reporting.py
- Add new discovery strategies in discovery.py
- Extend CLI options in cli.py
