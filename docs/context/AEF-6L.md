# AEF 6-Layer Substrate Architecture Context Document

## Overview

This document provides the technical foundation for implementing the AEF (Agentic Engineering Framework) 6-layer substrate architecture. It establishes the language-agnostic developer substrate that enables the AEF to operate across radically different project types without assuming technology stack.

**Status**: Technical specification for M10+ implementation
**Derived From**: `docs/ingest/aef-6layer-substrate.md`
**Current State**: M10 implementation completed (`M10CLOSE-1.md`), now extending with substrate architecture

---

## Executive Architecture Summary

The AEF 6-layer substrate separates concerns into six distinct layers:

```
LAYER 1: Environment / Reproducibility
│
LAYER 2: Universal Command Execution
│
LAYER 3: Universal Code Quality
│
LAYER 4: Modern Universal Developer Tooling
│
LAYER 5: Agent-Oriented Code Intelligence
│
LAYER 6: Verification and Security
```

**Strategic Decision**: Rust belongs in the execution substrate (Layer 1-3), not the control plane (currently Python).

---

## Current AEF State vs. Required Substrate

### M10 Implementation Status (`M10CLOSE-1.md`)
- ✅ **Complete**: `bin/omp-discover` CLI tool
- ✅ **Complete**: Project-agnostic artifact discovery
- ✅ **Complete**: Interface contract specifications
- ✅ **Complete**: Verification protocol setup
- ✅ **Complete**: Test generation framework

### Substrate Architecture Gaps (6-Layer)
1. ❌ **Environment Reproducibility**: No language-agnostic environment management
2. ❌ **Universal Command Execution**: Ad-hoc Python subprocess calls
3. ❌ **Universal Code Quality**: Technology-specific tools (pytest/cargo test/vitest)
4. ❌ **Universal Developer Tooling**: No standardized tool set
5. ❌ **Agent-Oriented Intelligence**: Limited cross-language code understanding
6. ❌ **Verification Layer**: Reactive rather than proactive verification

---

## Layer 1: Environment / Reproducibility

### Technical Requirements
**Goal**: Deterministic environment management across all project types

#### Core Component: `mise`
```bash
# Installation (recommended for all environments)
brew install mise
# OR
sh -ci "$(curl -fsSL https://mise.run)"

# Usage
mise install python@3.11
mise install node@20
mise install rust@stable
mise install go@1.22
mise install deno@2.0

# Project environment
mise use -f python@3.11
```

#### Environment Configuration File
```yaml
# .mise.toml
env_prefix = "project_"

tool "python" {
  version = "3.11.9"
}

tool "node" {
  version = "20.14.0"
}

tool "rust" {
  version = "stable"
}
```

#### AEF Integration Points
- **Agent Runtime**: Environment detection before task execution
- **Workspace Isolation**: Per-project environment configuration
- **Reproducibility**: Deterministic tool versions across all agents
- **Cross-Language Support**: Unified management of Python/Node/Rust/Go/Deno

#### Technical Implementation
```rust
// Example: Environment detection for AEF agents
pub struct EnvironmentDetector {
    project_root: PathBuf,
    mise_path: PathBuf,
}

impl EnvironmentDetector {
    pub async fn detect_environment(&self) -> Result<ProjectEnvironment> {
        // Check for .mise.toml
        // Parse tool configurations
        // Return deterministic environment spec
    }
}
```

---

## Layer 2: Universal Command Execution

### Technical Requirements
**Goal**: Abstract command execution across all programming language ecosystems

#### Core Components

##### `just` Command Orchestration
```yaml
# .justfile
fmt:
    {{ rustfmt }}
    {{ python -m black }}
    {{ npx eslint }}

lint:
    {{ rustc -- -D warnings }}
    {{ pylint }}
    {{ npm run lint }}

build:
    {{ cargo build --release }}
    {{ python -m pip install -e . }}
    {{ npm run build }}

verify:
    {{ ./bin/omp-discover }}
    {{ cargo test }}
    {{ pytest }}
    {{ npm run test }}
```

##### Universal Execution Interface
```rust
// Execution abstraction for all language ecosystems
pub struct UniversalExecutor {
    workspace_root: PathBuf,
    environment: ProjectEnvironment,
}

impl UniversalExecutor {
    pub async fn execute(&self, command: CommandSpec) -> Result<ExecutionResult> {
        match command.language.as_str() {
            "rust" => self.execute_rust(command).await,
            "python" => self.execute_python(command).await,
            "typescript" => self.execute_typescript(command).await,
            _ => self.execute_universal_shell(command).await,
        }
    }

    fn execute_universal_shell(&self, command: CommandSpec) -> Result<ExecutionResult> {
        // Use `just` for human-readable command execution
        // Capture stdout, stderr, exit_code, duration
        // Extract file changes and artifacts
    }
}
```

#### Universal Command Specifications
```rust
pub struct CommandSpec {
    pub command: String,                    // Human-readable command name
    pub args: Vec<String>,                  // Arguments
    pub language: String,                   // Target language ecosystem
    pub timeout: Duration,                  // Execution timeout
    pub env_vars: HashMap<String, String>,  // Environment variables
    pub working_directory: Option<PathBuf>, // Specific working dir
}

pub struct ExecutionResult {
    pub stdout: String,                     // Captured stdout
    pub stderr: String,                     // Captured stderr
    pub exit_code: i32,                     // Exit status
    pub duration: Duration,                  // Execution time
    pub files_changed: Vec<PathBuf>,        // Files modified
    pub artifacts: Vec<Artifact>,           // Generated artifacts
}
```

---

## Layer 3: Universal Code Quality

### Technical Requirements
**Goal**: Abstract quality checks across all programming language ecosystems

#### Quality Capability Specification
```yaml
# quality.yml
capabilities:
  format:
    rust:
      command: "rustfmt --config-path rustfmt.toml"
      files: "**/*.rs"
    python:
      command: "black --check"
      files: "**/*.py"
    typescript:
      command: "npx prettier --check"
      files: "**/*.{ts,tsx,js,jsx}"

  lint:
    rust:
      command: "clippy -- -D warnings"
      files: "**/*.rs"
    python:
      command: "pylint --rcfile=.pylintrc"
      files: "**/*.py"
    typescript:
      command: "npx eslint"
      files: "**/*.{ts,tsx,js,jsx}"

  typecheck:
    python:
      command: "mypy --config-file mypy.ini"
      files: "**/*.py"
    typescript:
      command: "tsc --noEmit"
      files: "**/*.{ts,tsx}"

  test:
    rust:
      command: "nextest run"
      files: "**/*_{test,spec}.rs"
    python:
      command: "pytest"
      files: "**/*test*.py"
    typescript:
      command: "vitest run"
      files: "**/*.test.{ts,tsx}"

  build:
    rust:
      command: "cargo build"
    python:
      command: "python -m pip install -e ."
    typescript:
      command: "npm run build"

  security:
    command: "semgrep --config=auto"
    files: "**/*.{js,ts,tsx,jsx,py,rs,go}"

  benchmark:
    rust:
      command: "criterion bench"
    python:
      command: "python -m pytest --benchmark"
    typescript:
      command: "npm run benchmark"
```

#### Quality Controller Interface
```rust
pub struct QualityController {
    config_path: PathBuf,
    workspace_root: PathBuf,
}

impl QualityController {
    pub async fn execute_capability(&self, capability: &str, target: &str) -> Result<QualityResult> {
        let quality_config = self.load_quality_config().await?
        let capability_spec = quality_config.capabilities.get(capability)
            .ok_or(QualityError::UnknownCapability(capability))?

        match target {
            "rust" => self.execute_rust_quality(capability_spec, capability).await,
            "python" => self.execute_python_quality(capability_spec, capability).await,
            "typescript" => self.execute_typescript_quality(capability_spec, capability).await,
            _ => self.execute_generic_quality(capability_spec, capability).await,
        }
    }

    fn execute_generic_quality(&self, spec: &QualityCapability, capability: &str) -> Result<QualityResult> {
        // Execute via universal command execution layer
        // Uses `just` for cross-language capability execution
    }
}
```

---

## Layer 4: Modern Universal Developer Tooling

### Technical Requirements
**Goal**: Provide universal command-line tools for all development workflows

#### Core Tool Specifications

##### File System Discovery
```bash
# ripgrep (rg) - Universal text search
rg "pattern" --type-not binary --type-not archive
rg "TODO|FIXME" --heading --line-number

# fd - Better filesystem discovery
fd "*.rs" --type f | head -20
fd "test_" --type d --exec echo "{} contains tests"
```

##### JSON/YAML Manipulation
```bash
# jq - Essential JSON manipulation
jq '.project.name' package.json
jq '.dependencies | keys' package-lock.json
jq '.env[] | select(.development == true)' .env.example

# yq - Essential YAML manipulation
yq eval '.tool.python.version' pyproject.toml
yq eval '.dependencies[] | select(.name == "serde")' Cargo.toml
```

##### Terminal Ergonomics
```bash
# fzf - Universal fuzzy finder
fzf --multi --preview 'cat {}'
fzf --prompt 'Themes> ' --expect 'enter,ctrl-d' $(ls themes/*)

# git - Version control foundation
function aef_git() {
    git ${@:-status}
}

# Custom AEF Git wrapper
export PATH="$PATH:/workspace/aef/bin"
```

#### Tool Integration Architecture
```rust
pub struct DeveloperToolchain {
    tools: HashMap<String, ToolSpec>,
    workspace_root: PathBuf,
}

impl DeveloperToolchain {
    pub async fn discover_files(&self, pattern: &str) -> Result<Vec<PathBuf>> {
        // Uses `fd` for filesystem discovery
        // Respects `.gitignore` and project conventions
    }

    pub async fn search_content(&self, query: &str, filters: &[&str]) -> Result<Vec<SearchResult>> {
        // Uses `rg` for content search
        // Supports multiple file types and exclusions
    }

    pub async fn parse_data(&self, data: &str, format: DataFormat) -> Result<serde_json::Value> {
        // Uses `jq`/`yq` for JSON/YAML parsing
        // Provides unified interface across data formats
    }
}
```

---

## Layer 5: Agent-Oriented Code Intelligence

### Technical Requirements
**Goal**: Enable agents to understand and work with any codebase regardless of technology

#### Code Intelligence Components

##### Language-Agnostic AST Analysis
```rust
pub struct CodeIntelligence {
    parsers: HashMap<String, LanguageParser>,
    workspace_root: PathBuf,
}

impl CodeIntelligence {
    pub async fn analyze_file(&self, file_path: &Path) -> Result<FileAnalysis> {
        let language = self.detect_language(file_path).await?
        match language.as_str() {
            "rust" => self.analyze_rust(file_path).await,
            "python" => self.analyze_python(file_path).await,
            "typescript" => self.analyze_typescript(file_path).await,
            "yaml" | "json" => self.analyze_structured(file_path).await,
            _ => Err(CodeIntelligenceError::UnsupportedLanguage(language)),
        }
    }

    async fn analyze_typescript(&self, file_path: &Path) -> Result<FileAnalysis> {
        // Uses tree-sitter for TypeScript AST parsing
        // Extracts exports, imports, types, interfaces
    }
}
```

##### Semantic Symbol Resolution
```rust
pub struct SymbolResolver {
    cache: LruCache<String, SymbolInfo>,
    workspace_root: PathBuf,
}

impl SymbolResolver {
    pub async fn resolve_symbol(&self, symbol_name: &str) -> Result<Vec<SymbolLocation>> {
        // Cross-file symbol resolution
        // Supports shadowing, re-exports, type aliases
        // Returns callsite locations for modifications
    }

    pub async fn get_definition(&self, symbol_name: &str) -> Result<DefinitionNode> {
        // Returns AST node with location
        // Enables refactoring across files
    }
}
```

#### Tree-Sitter Integration
```rust
// Critical for language-agnostic code analysis
use tree_sitter::{Parser, Language};

pub struct TreeSitterManager {
    rust_language: Language,
    python_language: Language,
    typescript_language: Language,
    parsers: HashMap<String, Parser>,
}

impl TreeSitterManager {
    pub fn new() -> Result<Self> {
        let mut rust_parser = Parser::new();
        rust_parser.set_language(tree_sitter_rust::LANGUAGE.into())?;

        let mut python_parser = Parser::new();
        python_parser.set_language(tree_sitter_python::LANGUAGE.into())?;

        let mut typescript_parser = Parser::new();
        typescript_parser.set_language(tree_sitter_typescript::LANGUAGE_TYPESCRIPT.into())?;

        Ok(Self {
            rust_language: tree_sitter_rust::LANGUAGE.into(),
            python_language: tree_sitter_python::LANGUAGE.into(),
            typescript_language: tree_sitter_typescript::LANGUAGE_TYPESCRIPT.into(),
            parsers: btreemap! {
                "rust".to_string() => rust_parser,
                "python".to_string() => python_parser,
                "typescript".to_string() => typescript_parser,
            },
        })
    }
}
```

---

## Layer 6: Verification and Security

### Technical Requirements
**Goal**: Proactive verification and security framework across all project types

#### Universal Verification Framework
```rust
pub struct VerificationEngine {
    security_scanners: Vec<Box<dyn SecurityScanner>>,
    verification_rules: Vec<VerificationRule>,
    workspace_root: PathBuf,
}

impl VerificationEngine {
    pub async fn run_security_scan(&self) -> Result<SecurityReport> {
        let mut report = SecurityReport::new();

        for scanner in &self.security_scanners {
            let scan_result = scanner.scan(&self.workspace_root).await?;
            report.merge(scan_result);
        }

        Ok(report)
    }

    pub async fn verify_compliance(&self, rules: &[VerificationRule]) -> Result<ComplianceReport> {
        // Run verification against project artifacts
        // Report violations and suggestions
        // Generate remediation plans
    }
}
```

#### Security Scanner Integration
```rust
// Semgrep security scanning
pub struct SemgrepScanner;

impl SecurityScanner for SemgrepScanner {
    async fn scan(&self, workspace: &Path) -> Result<SecurityReport> {
        let mut report = SecurityReport::new();

        // Execute semgrep with auto rules
        let output = Command::new("semgrep")
            .args(["--config=auto", "--json", workspace.to_str().unwrap()])
            .output()
            .await?;

        let findings: Vec<SemgrepFinding> = serde_json::from_slice(&output.stdout)?;

        for finding in findings {
            report.add_violation(Violation {
                rule_id: finding.rule_id,
                severity: finding.severity,
                file: finding.filepath,
                line: finding.line,
                message: finding.message,
            });
        }

        Ok(report)
    }
}
```

#### OpenTelemetry Integration
```rust
// Observability and metrics
use opentelemetry::prelude::*;

pub struct ObservabilityLayer {
    tracer: Tracer,
    meter: Meter,
    workspace_root: PathBuf,
}

impl ObservabilityLayer {
    pub fn new() -> Self {
        let tracer = opentelemetry_sdk::trace::TracerProvider::builder()
            .with_simple_exporter(opentelemetry_sdk::export::trace::SpanExporter::default())
            .install_shared_extractor();

        let meter = opentelemetry_sdk::metrics::MeterProvider::builder()
            .install_shared_extractor();

        Self {
            tracer,
            meter,
            workspace_root: PathBuf::from("."),
        }
    }

    pub fn trace_agent_execution(&self, agent_id: &str, task: &str) {
        let span = self.tracer
            .span_builder("agent.execution")
            .with_attributes(vec![
                Attribute::new("agent.id", agent_id),
                Attribute::new("task", task),
            ])
            .start(self.tracer.clone());

        // Execute task with tracing
        span.end();
    }
}
```

---

## Strategic Rust Components

### Core Rust Libraries for AEF Substrate

#### 1. `aef-exec` - Universal Execution Daemon
```rust
// bin/aef-exec.rs
use tokio::net::TcpListener;
use serde::{Deserialize, Serialize};

#[derive(Debug, Deserialize, Serialize)]
pub struct ExecutionRequest {
    pub command: CommandSpec,
    pub agent_id: String,
    pub workspace: PathBuf,
}

#[derive(Debug, Deserialize, Serialize)]
pub struct ExecutionResponse {
    pub result: ExecutionResult,
    pub metadata: ExecutionMetadata,
}

#[tokio::main]
async fn main() -> Result<(), Box<dyn Error>> {
    let listener = TcpListener::bind("0.0.0.0:8080").await?;

    loop {
        let (mut socket, _) = listener.accept().await?;

        let executor = UniversalExecutor::new(".".to_string()).await?;

        let request = receive_json::<ExecutionRequest>(&mut socket).await?;
        let response = executor.execute(request.command).await?;

        send_json(&mut socket, &response).await?;
    }
}
```

#### 2. `aef-workspace` - Workspace Management
```rust
// src/workspace.rs
use std::path::{Path, PathBuf};

pub struct AEFWorkspace {
    root: PathBuf,
    config: WorkspaceConfig,
    environment: ProjectEnvironment,
}

impl AEFWorkspace {
    pub fn new(root: &str) -> Result<Self, WorkspaceError> {
        let root_path = PathBuf::from(root);
        if !root_path.exists() {
            return Err(WorkspaceError::NotFound(root.to_string()));
        }

        let config = Self::load_config(&root_path)?;
        let environment = Self::detect_environment(&root_path)?;

        Ok(Self {
            root: root_path,
            config,
            environment,
        })
    }

    pub fn get_artifacts_root(&self) -> PathBuf {
        self.root.join(&self.config.artifact_root)
    }

    pub fn get_skills_path(&self) -> PathBuf {
        self.root.join(&self.config.active_skills_path)
    }
}
```

#### 3. `aef-verify` - Universal Verification Runner
```rust
// src/verify.rs
use std::process::Command;

pub struct VerificationRunner {
    quality_controller: QualityController,
    security_scanner: SecurityScanner,
    workspace: AEFWorkspace,
}

impl VerificationRunner {
    pub async fn run_full_verification(&self) -> Result<VerificationReport> {
        let mut report = VerificationReport::new();

        // Code quality verification
        let quality_results = self.run_quality_checks().await?;
        report.merge(quality_results);

        // Security verification
        let security_results = self.run_security_scans().await?;
        report.merge(security_results);

        // Project discovery verification
        let discovery_results = self.verify_discovery().await?;
        report.merge(discovery_results);

        Ok(report)
    }

    fn run_quality_checks(&self) -> Result<QualityReport> {
        // Execute universal quality checks via `just`
        // Uses quality.yml configuration
        Command::new("just")
            .args(["verify"])
            .current_dir(&self.workspace.root)
            .output()?;

        // Parse results and generate report
    }
}
```

---

## Implementation Strategy

### Immediate Phase (Now)

#### 1. Environment Management
- **Implement**: `mise` integration for language/runtime management
- **Deliver**: `bin/aef-env-detect` CLI tool
- **Test**: Deterministic environment detection across multiple project types

#### 2. Command Execution Abstraction
- **Implement**: `UniversalExecutor` with `just` backend
- **Deliver**: `bin/aef-exec` universal execution daemon
- **Test**: Cross-language command execution and result capture

#### 3. Core Rust Components
- **Implement**: `aef-workspace`, `aef-verify`, execution utilities
- **Test**: Workspace management and verification workflows

### Short-Term Phase (Next)

#### 4. Universal Quality Framework
- **Implement**: `QualityController` with capability-based execution
- **Deliver**: `bin/aef-quality` universal quality checker
- **Test**: Format/lint/typecheck/test across all supported languages

#### 5. Developer Tooling Integration
- **Implement**: `DeveloperToolchain` with universal tooling
- **Test**: File discovery, content search, data parsing

#### 6. Code Intelligence Foundation
- **Implement**: `CodeIntelligence` with language-agnostic analysis
- **Test**: Symbol resolution and cross-file understanding

### Long-Term Phase (Then)

#### 7. Advanced Agent Intelligence
- **Implement**: Enhanced semantic analysis and refactoring
- **Test**: Complex dependency resolution and code transformation

#### 8. Advanced Verification & Security
- **Implement**: Proactive security scanning and compliance
- **Test**: Threat detection and remediation planning

#### 9. Full Language-Agnostic Migration
- **Migrate**: Strategic components to Rust execution layer
- **Achieve**: Complete technology stack independence

---

## Technical Integration Points

### Python ↔ Rust Interaction
```rust
// Integration bridge for existing Python control plane
pub struct PythonRustBridge {
    workspace: AEFWorkspace,
}

impl PythonRustBridge {
    pub async fn execute_python_workflow(&self, task: &str) -> Result<WorkflowResult> {
        // Use existing Python orchestration for high-level tasks
        // Delegate to Rust for execution substrate operations
        // Maintain backward compatibility with current AEF
    }
}
```

### Migration Path
```yaml
# Migration roadmap
migration_phases:
  1:
    - Add mise environment management
    - Implement universal executor
    - Deploy core Rust components
    status: "In Progress"

  2:
    - Add universal quality framework
    - Deploy developer tooling
    - Implement code intelligence
    status: "Planned"

  3:
    - Advanced agent intelligence
    - Full verification & security
    - Complete technology independence
    status: "Future"
```

---

## Verification Requirements

### Test Fixtures for Substrate Components
- **Environment Detection**: `tests/fixtures/synthetic_python/`, `tests/fixtures/synthetic_rust/`
- **Command Execution**: `tests/fixtures/integration/`, `tests/fixtures/commands/`
- **Quality Framework**: `tests/fixtures/quality/`, `tests/fixtures/linting/`
- **Code Intelligence**: `tests/fixtures/analysis/`, `tests/fixtures/symbols/`

### Quality Gates
1. **Layer 1**: Environment must be detectable deterministically
2. **Layer 2**: Commands must execute consistently across languages
3. **Layer 3**: Quality checks must work for all supported technologies
4. **Layer 4**: Toolchain must provide universal capabilities
5. **Layer 5**: Code intelligence must understand all project types
6. **Layer 6**: Verification must detect security and compliance issues

---

## Success Metrics

- **Implementation Coverage**: All 6 layers fully functional
- **Language Support**: Python, Rust, TypeScript, Go, Node.js, YAML/JSON
- **Test Coverage**: 100% unit and integration tests for all layers
- **Performance**: Sub-100ms execution for common operations
- **Reliability**: 99.9% uptime for critical infrastructure components

---

## Dependencies and Requirements

### Runtime Dependencies
- **Rust**: Stable (not nightly)
- **Python**: 3.11+
- **Node.js**: 20+
- **Go**: 1.22+
- **Additional**: `mise`, `just`, `rg`, `fd`, `fzf`, `jq`, `yq`

### Build Requirements
```bash
# Environment setup
mise install python@3.11
mise install node@20
mise install rust@stable
git clone https://github.com/jdx/mise.git
mise install just

# Dependencies
cargo add serde --features serde_derive
t cargo add tokio --features full
# ... other Rust dependencies
```

---

*This context document provides the technical foundation for implementing the AEF 6-layer substrate architecture. It enables the creation of highly detailed milestone documents focused on building modular, project-agnostic infrastructure that operates independently of specific technology stacks.*
