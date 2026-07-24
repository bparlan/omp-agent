#!/bin/bash

# Structure Cleanup Script for Archive Docs Skill
# Version: 1.3.0
# Purpose: Enforce 3-layer registry pattern and clean up project structure

# Global variables for build artifacts
pycache_count=0
pyc_count=0
pyo_count=0

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Scan for misplaced files
scan_files() {
    print_info "Scanning for misplaced files..."

    # Scan for misplaced .md files (excluding docs/ and root special files)
    if [ -n "$(find . -maxdepth 1 -type f -name '*.md' 2>/dev/null)" ]; then
        print_warn "Found .md files in root directory:"
        find . -maxdepth 1 -type f -name '*.md' -print | sed 's|^\./||'
    fi

    # Scan for misplaced HTML/CSS files
    if [ -n "$(find . -maxdepth 2 -type f \( -name '*.html' -o -name '*.css' \) ! -path "./web/*" ! -path "./templates/*" ! -path "./docs/*" 2>/dev/null)" ]; then
        print_warn "Found HTML/CSS files outside web/ and templates/:"
        find . -maxdepth 2 -type f \( -name '*.html' -o -name '*.css' \) ! -path "./web/*" ! -path "./templates/*" ! -path "./docs/*" -print | sed 's|^\./||'
    fi

    # Scan for misplaced JSON/YAML files
    if [ -n "$(find . -maxdepth 2 -type f \( -name '*.json' -o -name '*.yaml' -o -name '*.yml' \) ! -path "./data/*" ! -path "./docs/*" 2>/dev/null)" ]; then
        print_warn "Found JSON/YAML files outside data/ and docs/:"
        find . -maxdepth 2 -type f \( -name '*.json' -o -name '*.yaml' -o -name '*.yml' \) ! -path "./data/*" ! -path "./docs/*" -print | sed 's|^\./||'
    fi

    # Scan for misplaced Python/JS files
    if [ -n "$(find . -maxdepth 2 -type f \( -name '*.py' -o -name '*.js' \) ! -path "./src/*" ! -path "./tests/*" ! -path "./docs/*" 2>/dev/null)" ]; then
        print_warn "Found Python/JS files outside src/, tests/, and docs/:"
        find . -maxdepth 2 -type f \( -name '*.py' -o -name '*.js' \) ! -path "./src/*" ! -path "./tests/*" ! -path "./docs/*" -print | sed 's|^\./||'
    fi

    # Scan for backup files (excluding templates/ and docs/)
    if [ -n "$(find . -maxdepth 1 -type f \( -name '*.backup' -o -name '*.bak' \) ! -path "./templates/*" 2>/dev/null)" ]; then
        print_warn "Found backup files in root directory:"
        find . -maxdepth 1 -type f \( -name '*.backup' -o -name '*.bak' \) -print | sed 's|^\./||'
    fi

    # Scan for build artifacts
    
    
    

    if [ "$pycache_count" -gt 0 ] || [ "$pyc_count" -gt 0 ] || [ "$pyo_count" -gt 0 ]; then
        print_warn "Found build artifacts:"
        [ "$pycache_count" -gt 0 ] && echo "  - $pycache_count __pycache__/ directories"
        [ "$pyc_count" -gt 0 ] && echo "  - $pyc_count .pyc files"
        [ "$pyo_count" -gt 0 ] && echo "  - $pyo_count .pyo files"
    fi

    # Scan for duplicates
    py_files=$(find . -maxdepth 1 -type f -name "*.py" 2>/dev/null)
    duplicate_py=$(echo "$py_files" | xargs -n1 basename | sort | uniq -d)

    if [ -n "$duplicate_py" ]; then
        print_warn "Found duplicate Python files with same basename:"
        echo "$duplicate_py" | sed 's/^/  - /'
    fi
}

# Execute cleanup
execute_cleanup() {
    print_info "Executing cleanup..."

    # Move .md files to docs/content/ (excluding docs/ and root special files)
    md_files=$(find . -maxdepth 1 -type f -name '*.md' 2>/dev/null)
    if [ -n "$md_files" ]; then
        print_info "Moving .md files to docs/content/..."
        mv $md_files docs/content/ 2>/dev/null || true
    fi

    # Move milestones to docs/milestones/ (excluding existing)
    if [ -d "milestones" ] && [ ! -d "docs/milestones" ]; then
        print_info "Moving milestones to docs/milestones/..."
        mv milestones docs/milestones/ 2>/dev/null || true
    fi

    # Create archive directory if needed
    mkdir -p docs/ingest/archived

    # Move backups to archive
    backup_files=$(find . -maxdepth 1 -type f \( -name '*.backup' -o -name '*.bak' \) 2>/dev/null)
    if [ -n "$backup_files" ]; then
        print_info "Moving backup files to docs/ingest/archived/..."
        mv $backup_files docs/ingest/archived/ 2>/dev/null || true
    fi

    # Remove build artifacts
    if [ "$pycache_count" -gt 0 ]; then
        print_info "Removing __pycache__ directories..."
        find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
    fi

    if [ "$pyc_count" -gt 0 ]; then
        print_info "Removing .pyc files..."
        find . -type f -name "*.pyc" -delete 2>/dev/null || true
    fi

    if [ "$pyo_count" -gt 0 ]; then
        print_info "Removing .pyo files..."
        find . -type f -name "*.pyo" -delete 2>/dev/null || true
    fi

    print_info "Cleanup complete!"
}

# Validate structure
validate_structure() {
    print_info "Validating structure..."

    # Re-run scans to check for compliance
    scan_files > /tmp/structure_validation.log 2>&1

    # Check if any violations found
    if [ -s /tmp/structure_validation.log ]; then
        print_warn "Some violations still present. Review structure_validation.log"
        cat /tmp/structure_validation.log
    else
        print_info "Structure is compliant! ✅"
    fi

    # Remove log file
    rm -f /tmp/structure_validation.log
}

# Show help
show_help() {
    cat << EOF
Usage: structure-cleanup.sh [OPTIONS]

Enforce 3-layer registry pattern and clean up project structure.

Options:
  -s, --scan-only      Only scan, don't execute cleanup
  -e, --execute        Execute cleanup (default)
  -v, --validate       Validate structure after cleanup
  -h, --help           Show this help message

Examples:
  # Scan for violations
  ./structure-cleanup.sh --scan-only

  # Execute cleanup
  ./structure-cleanup.sh --execute

  # Scan and execute
  ./structure-cleanup.sh

  # Scan and validate
  ./structure-cleanup.sh --scan-only --validate

EOF
}

# Parse arguments
SCAN_ONLY=false
EXECUTE=false
VALIDATE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--scan-only)
            SCAN_ONLY=true
            shift
            ;;
        -e|--execute)
            EXECUTE=true
            shift
            ;;
        -v|--validate)
            VALIDATE=true
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Default: scan if not executing
if [ "$EXECUTE" = false ]; then
    SCAN_ONLY=true
fi

# Main execution
if [ "$SCAN_ONLY" = true ]; then
    scan_files
fi

if [ "$EXECUTE" = true ]; then
    execute_cleanup
fi

if [ "$VALIDATE" = true ]; then
    validate_structure
fi
