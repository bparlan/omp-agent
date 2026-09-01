# Functional Requirements Analysis

## SPEC-M9S3 Functional Requirements Status

### FR-RESOLVER_IMPLEMENTATION
**Requirement**: CLI Executable Contract for artifact resolution
- **Interface Contract**: `python3 -m core.artifacts.resolve --identity <artifact_id> --type <artifact_type> --metadata-filter <json_filter> --strict <boolean>`
- **Current Status**: ❌ **GAP** - Function exists but missing CLI interface
- **Implementation Details**:
  - `resolve_artifact()` exists in `core/artifacts/resolution.py`
  - Signature matches: `resolve_artifact(identity=None, artifact_type=None, metadata_filter=None, strict=False)`
  - Missing: CLI executable `core/artifacts/resolve.py` or `__main__.py`
  - Missing: Argument parsing for CLI interface
- **Observable Boundary**: Process exit code and stdout JSON output

### FR-LEGACY_RESOLUTION_SUPPORT
**Requirement**: Legacy artifact support with `--strict false`
- **Interface Contract**: `python3 -m core.artifacts.resolve --strict false`
- **Current Status**: ❌ **GAP** - Logic exists but missing CLI interface
- **Implementation Details**:
  - Legacy support implemented via `strict=False` parameter in `resolve_artifact()`
  - `LEGACY_ARTIFACT_MAPPINGS` dictionary exists but empty
  - `_collect_candidates()` respects `strict` flag
  - Missing: CLI interface for legacy mode
- **Observable Boundary**: Process exit code and legacy artifact metadata in stdout

### FR-ARTIFACT_VALIDATION
**Requirement**: JSON schema validation of artifact metadata
- **Interface Contract**: JSON schema validation against canonical contract
- **Current Status**: ❌ **PARTIAL** - Function exists but missing public interface
- **Implementation Details**:
  - `validate_metadata()` exists in `core/validation.py`
  - Schema validation implemented with jsonschema
  - Missing: Public `validate_artifact()` function as per "Public Interfaces"
  - Schema contracts defined but not fully integrated
- **Observable Boundary**: JSON validation output with boolean validity flag

### FR-PROJECT_CONFIG_INTEGRATION
**Requirement**: Read/write `.omp/config.yml` with project configuration
- **Interface Contract**: Filesystem State Contract
- **Current Status**: ❌ **GAP** - No implementation exists
- **Implementation Details**:
  - No `core/config.py` file exists
  - No `load_project_config()` or `validate_config()` functions
  - Schema contract defined but not implemented
  - `.omp/config.yml` template missing
- **Observable Boundary**: File existence and JSON schema validation result

### FR-MODE_AWARE_BOOTSTRAP
**Requirement**: CLI executable with `--mode <framework|application>`
- **Interface Contract**: `bootstrap-project --mode <framework|application>`
- **Current Status**: ❌ **GAP** - Documentation exists but no CLI
- **Implementation Details**:
  - `skills/bootstrap-project/SKILL.md` exists but is skill documentation
  - No actual `bootstrap-project` CLI executable
  - Mode-aware behavior documented but not implemented
  - Framework vs application mode logic missing
- **Observable Boundary**: Directory structure and file contents after bootstrap

## Summary of Concrete Interface Contract Gaps

### **CLI Interfaces Missing (3/5)**
1. `python3 -m core.artifacts.resolve` - No module entry point
2. `bootstrap-project` - No CLI executable, only skill doc
3. `--strict false` legacy mode - No CLI interface

### **Public Interface Functions Missing (2/3)**
1. `validate_artifact(metadata)` - Only exists as `validate_metadata(artifact_path, schema)`
2. `load_project_config()` - No implementation exists
3. `validate_config(config)` - No implementation exists

### **Core Modules Missing (1/6)**
1. `core/config.py` - Configuration handling module

## Implementation Priority

### **Critical (Must Implement)**
1. **CLI executable `core/artifacts/resolve.py`** - FR-RESOLVER_IMPLEMENTATION
2. **`core/config.py`** - FR-PROJECT_CONFIG_INTEGRATION
3. **Public `validate_artifact()`** - FR-ARTIFACT_VALIDATION

### **Important (Should Implement)**
1. **CLI executable `bootstrap-project`** - FR-MODE_AWARE_BOOTSTRAP
2. **Legacy CLI interface** - FR-LEGACY_RESOLUTION_SUPPORT

## Artifacts Required for Concrete Interface Contracts

1. **core/artifacts/resolve.py** - CLI wrapper for resolve_artifact()
2. **core/config.py** - Project configuration handling
3. **core/artifacts/__init__.py** - Export validate_artifact()
4. **skills/bootstrap-project/bootstrap-project** - CLI executable
5. **tests/** - Test fixtures for legacy and canonical artifacts
6. **.omp/config.yml** - Configuration template