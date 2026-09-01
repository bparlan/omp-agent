# Broader System Awareness - AEF Skill Integration Guide

## Purpose
This document establishes comprehensive system awareness requirements for all AEF skills, ensuring they understand the broader engineering ecosystem while maintaining behavioral contract boundaries.

## Overview
AEF skills must balance two competing needs:
1. **Contract Compliance**: Strict adherence to behavioral contracts prohibiting certain investigation types
2. **System Integration**: Understanding the broader AEF ecosystem to generate implementable specifications

This guide defines the controlled investigation capabilities and system awareness boundaries for all skills.

## Core System Boundaries

### Prohibited Investigation Types (Contract-Inherited)

All AEF skills MUST NOT perform these investigation types:

#### 1. Binary Toolchain Analysis
- **Prohibited**: Scanning `bin/` directory contents
- **Prohibited**: Analyzing binary naming conventions
- **Prohibited**: Investigating exit code patterns
- **Prohibited**: Toolchain integration strategies

**Examples of Prohibited Actions:**
```bash
# ❌ NEVER DO:
- grep -r "def main" bin/
- find bin/ -name "*.js" | xargs node -c
- cat bin/config.js
```

#### 2. Architectural Design Investigation
- **Prohibited**: Toolchain cohesion analysis
- **Prohibited**: Naming convention discovery
- **Prohibited**: Design pattern identification
- **Prohibited**: Architecture planning

#### 3. Implementation Details Investigation
- **Prohibited**: Internal module data routing
- **Prohibited**: Algorithm analysis
- **Prohibited**: Performance optimization planning
- **Prohibited**: Debug logging implementation

### Allowed Investigation Types (Contract-Respected)

All AEF skills MAY perform these controlled investigation types:

#### 1. Milestone Integration Bindings Analysis
**Allowed Scope:**
- Required binaries, fixtures, interfaces from milestone Integration Bindings table
- Out of scope definitions from milestone
- Risk factors and assumptions from milestone
- Spec decomposition plan details

**Safe Investigation Commands:**
```bash
# ✅ ALLOWED:
# Extract integration bindings from milestone
grep -A 20 "## Integration Bindings" milestones/M{X}/M{X}.md

# Extract spec decomposition plan
grep -A 30 "## Spec Decomposition Plan" milestones/M{X}/M{X}.md
```

#### 2. Existing Module Interface Discovery
**Allowed Scope:**
- Public module exports and function signatures
- Class interfaces and method definitions
- Custom error classes and parameter types
- Existing fixture structures and dependencies

**Allowed Investigation Methods:**
- Use `lsp` tool for symbol-aware code intelligence
- Use `code-search` for semantic repository search
- Use `ast_edit` for pattern analysis (within allowed scope)

#### 3. System Architecture Understanding
**Allowed Scope:**
- Understanding canonical artifact system components
- Recognizing artifact validation API usage
- Identifying integration with M9 artifact validation
- Understanding milestone artifact identity requirements

#### 4. Template and Structure Validation
**Allowed Scope:**
- Required section structure from specification templates
- YAML frontmatter field formats and validation
- Required artifact naming conventions (SPEC-M{X}S{Y}.md)
- Template version compatibility requirements

## Enhanced Tooling Capabilities

### Standard AEF Skills Toolset
All AEF skills have access to core tools:
- `read`, `write`, `edit`, `bash` - Basic file operations
- `task` - Delegation capabilities
- `hub` - Peer messaging
- `ask` - Interactive handoff

### Enhanced Investigation Tools (Skill-Specific)

#### 1. `code-search`
**Purpose**: Semantic repository search for existing integration patterns
**Allowed Use Cases:**
- Discovering existing fixture structures
- Understanding existing test organization
- Identifying existing module interfaces
- Finding artifact system integration patterns

**Safe Investigation Scope:**
- Search within milestones/ and skills/ directories
- Search for pattern matching (e.g., `def.*fixture`, `class.*Fixture`)
- Search for interface definitions (e.g., `export.*interface`, `class.*Service`)

#### 2. `lsp`
**Purpose**: Symbol-aware code intelligence for interface discovery
**Allowed Use Cases:**
- Discovering existing public APIs
- Understanding module exports and signatures
- Identifying existing function definitions
- Exploring code structure without binary analysis

**Safe Investigation Scope:**
- Only investigate module interfaces and exports
- Only explore code definitions (not implementation details)
- Only search for patterns within existing milestone and skill directories

#### 3. `ast_edit`
**Purpose**: AST-aware pattern analysis for existing code structures
**Allowed Use Cases:**
- Analyze existing module structure
- Understand existing code organization
- Discover existing implementation patterns

**Safe Investigation Scope:**
- Only analyze existing code structure (not redesign)
- Only investigate patterns already present in repository
- Never propose new architectural patterns

#### 4. `inspector`
**Purpose**: Visual inspection QA for generated specification quality
**Allowed Use Cases:**
- Validate generated specification formatting
- Check for consistency and completeness
- Visual verification of spec structure

## System Integration Requirements

### 1. M9 Artifact Validation System Integration

**Canonical Artifact System Components:**
- `core/validation.py` - Artifact validation API
- `core/artifacts/metadata.py` - Frontmatter parsing
- `core/artifacts/registry.py` - Type registry and storage rules
- `core/artifacts/resolution.py` - Artifact resolution
- `core/artifacts/types.py` - Type definitions

**Integration Expectations:**

#### For Spec Generation Skills
When milestone references artifact validation:
- **Reference Canonical APIs**: Use `core/validation.py` validation contracts (`validate_metadata()`, `validate_artifact()`)
- **Integrate Frontmatter Parsing**: Reference `core/artifacts/metadata.py` for frontmatter requirements
- **Align with Artifact Registry**: Use `core/artifacts/registry.py` for type definitions and storage rules
- **Respect Resolution Model**: Use `core/artifacts/resolution.py` for artifact resolution contracts

#### For Implementation Skills
When implementing artifact validation:
- **Use Canonical Components**: Import from `core/artifacts/` and `core/validation.py` rather than reimplementing
- **Follow Validation API**: Implement `validate_metadata(artifact_path)` and `validate_artifact(metadata)` contracts
- **Integrate with Artifact Registry**: Use `ArtifactRegistry` for type management
- **Respect Storage Rules**: Follow storage and resolution rules from `core/artifacts/`

### 2. Milestone Integration Requirements

#### Spec Generation Skills
- **Extract Integration Bindings**: From milestone's Integration Bindings table
- **Understand Affected Modules**: Use `lsp` to discover existing module interfaces
- **Identify Fixture Dependencies**: Analyze existing test/fixture structures
- **Respect Traceability**: Maintain `derived_from` lineage in generated specs

#### Implementation Skills
- **Reference Generated Specs**: Use milestone integration bindings from spec
- **Maintain Module Boundaries**: Respect existing allowlist/denylist from spec
- **Follow Interface Contracts**: Implement exactly as specified in generated specs
- **Integrate with Existing Systems**: Use existing module interfaces where specified

### 3. Project Configuration Integration

#### Bootstrapping Skills
- **Respect Active Project Boundary**: Do not inject AEF-specific artifacts into application projects
- **Generate Appropriate Guidance**: Use project configuration to determine guidance needs
- **Maintain Mode Awareness**: Support framework and application modes appropriately
- **Preserve Existing Architecture**: Do not disrupt application-specific documentation patterns

#### Other Skills
- **Use Canonical Artifact System**: All artifact interactions go through `core/artifacts/`
- **Follow Project Configuration**: Respect `.omp/config.yml` schema and settings
- **Maintain Project Isolation**: Do not cross project boundaries unintentionally
- **Use Canonical Resolution**: Always resolve artifacts through `core/artifacts/resolution.py`

## Quality Gate Enhancements

### System-Aware Quality Gates

#### Mechanical Validation
- **Contract Compliance**: Verify FRs define observable boundaries (CLI, Schema, Filesystem)
- **Infrastructure Alignment**: Ensure requirements reference existing integration bindings
- **System Integration**: Validate specs against actual module interfaces and fixture structures

#### System Awareness Validation
- **Integration Binding Reference**: Generated specs must reference milestone integration bindings
- **Module Interface Compliance**: Requirements must align with existing module interfaces
- **Fixture Dependency Verification**: Specs must respect existing fixture structures
- **Artifact System Integration**: Specs must reference canonical artifact system contracts

#### Consistency Validation
- **Traceability Lineage**: Maintain `derived_from` linking to milestone ID
- **Template Compliance**: Include all required sections from specification template
- **System Consistency**: Specs must reference existing integration bindings and repository structure
- **Integration Binding Alignment**: Generated specs must align with actual repository structure

## Investigation Workflow Guidelines

### Step-by-Step Investigation Process

#### 1. Extract Milestone Information
```bash
# Extract integration bindings from milestone
grep -A 20 "## Integration Bindings" milestones/M{X}/M{X}.md

# Extract spec decomposition plan
grep -A 30 "## Spec Decomposition Plan" milestones/M{X}/M{X}.md

# Extract artifact system references from milestone
grep -i "artifact.*validation\|core.*validation" milestones/M{X}/M{X}.md
```

#### 2. Discover Existing Module Interfaces
Use `lsp` tool for safe module discovery:
- Discover existing public APIs
- Understand module exports and signatures
- Identify existing function definitions
- Explore existing fixture structures

#### 3. Analyze Artifact System Integration
Use `code-search` for artifact system analysis:
- Find references to `core/validation.py`
- Discover `core/artifacts/` usage patterns
- Identify `ArtifactRegistry` integration
- Find `validate_metadata()` and `validate_artifact()` contracts

#### 4. Validate Generated Specifications
After spec generation:
- Verify integration binding references
- Validate module interface alignment
- Check fixture dependency compliance
- Confirm artifact system integration

## Failure Conditions (Enhanced)

### System-Aware HALT Conditions

#### Integration Failure HALT Conditions
- **Milestone Binding Empty**: Integration bindings table empty AND spec decomposition plan references binaries not in bin/
- **System Alignment Failure**: Generated spec does not reference existing integration bindings or module interfaces
- **Integration Compliance Failure**: Specification contracts do not respect existing fixture dependencies or module boundaries

#### System Awareness Failure HALT Conditions
- **Module Interface Omission**: Generated spec does not define public module interfaces
- **Fixture Structure Ignorance**: Generated spec does not reference existing fixture structures
- **Artifact System Misalignment**: Generated spec does not reference canonical artifact system contracts
- **Integration Binding Mismatch**: Generated spec does not align with actual repository structure

## Skill-Specific Integration Requirements

### 1. `generate-spec` Skill Integration

#### System-Aware Generation Requirements
- Use `code-search` and `lsp` for integration binding discovery
- Analyze existing module interfaces for affected modules list
- Validate fixture structures for fixture dependencies
- Reference canonical artifact validation APIs where applicable

#### Integration Verification
- Verify generated spec references existing milestone integration bindings
- Confirm spec contracts respect existing module interfaces
- Ensure spec requirements align with existing fixture structures
- Validate spec references canonical artifact system contracts

### 2. `implement-specification` Skill Integration

#### Implementation Integration Requirements
- **Use Canonical Components**: Import from `core/artifacts/` and `core/validation.py`
- **Follow Generated Contracts**: Implement exactly as specified in generated specs
- **Maintain Existing Interfaces**: Respect existing module exports and signatures
- **Integrate with Artifact System**: Use canonical validation and resolution APIs

#### Implementation Validation
- Verify implementation matches generated spec requirements
- Confirm implementation respects existing module boundaries
- Ensure implementation aligns with fixture dependencies
- Validate implementation uses canonical artifact system contracts

### 3. `generate-verification` Skill Integration

#### Verification Integration Requirements
- **Understand Generated Contracts**: Use spec FRs for verification generation
- **Respect Module Boundaries**: Verify against existing module interfaces
- **Validate Fixture Dependencies**: Ensure verification covers existing fixture structures
- **Align with Artifact System**: Verify against canonical artifact validation contracts

### 4. `evaluate-implementation` Skill Integration

#### Evaluation Integration Requirements
- **Use Canonical Validation**: Use `core/validation.py` for artifact validation
- **Follow Generated Contracts**: Evaluate implementation against generated spec
- **Respect Existing Integration**: Ensure evaluation aligns with existing milestone bindings
- **Validate System Integration**: Confirm implementation integration with canonical artifact system

## Implementation Checklist

### For All Skills
- [ ] Use only allowed investigation types (respect behavioral contract)
- [ ] Reference milestone integration bindings when needed
- [ ] Use `lsp` and `code-search` for module interface discovery
- [ ] Validate generated specs against existing repository structure
- [ ] Reference canonical artifact system contracts where applicable
- [ ] Respect existing module boundaries and fixture structures
- [ ] Maintain proper traceability (`derived_from` lineage)
- [ ] Use canonical components (`core/artifacts/`, `core/validation.py`)

### For Spec Generation Skills
- [ ] Extract integration bindings from milestone
- [ ] Discover affected modules using `lsp`
- [ ] Analyze fixture structures using `code-search`
- [ ] Reference canonical artifact validation APIs
- [ ] Generate specs that align with existing repository structure
- [ ] Ensure specs respect existing module interfaces

### For Implementation Skills
- [ ] Use canonical components for artifact system integration
- [ ] Implement exactly as specified in generated specs
- [ ] Respect existing module boundaries
- [ ] Validate implementation against generated spec requirements
- [ ] Ensure proper integration with artifact validation system

## Conclusion

Broader system awareness enables AEF skills to generate and implement specifications that truly integrate with the existing AEF ecosystem while maintaining strict adherence to behavioral contracts. By allowing controlled investigation of milestone integration bindings, existing module interfaces, and fixture structures, skills can produce specifications that are both mechanically verifiable and system-aligned.

The key is balancing contract compliance with the need to understand the broader system - skills must investigate evidence that is already available in the milestone and repository, but must never independently discover or analyze binary systems, toolchain details, or architectural designs.
