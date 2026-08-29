#!/bin/bash
echo "=== AEF SKILLS HEALTH CHECK REPORT ==="
echo ""
echo "Generated: $(date)"
echo ""
echo "=== OVERVIEW ==="
# Count total SKILL.md files
total_skills=$(find skills -name "SKILL.md" | grep -v "skills/README.md" | wc -l)
echo "Total SKILL.md files: $total_skills"
echo ""
echo "=== VERSION SUFFIX COMPLIANCE ANALYSIS ==="
echo ""

stable_skills=0
not_stable_skills=0
malformed_files=0
large_files=0
empty_versions=0

echo "Skills with -stable suffix:"
find skills -name "SKILL.md" | while read skill_file; do
    # Skip README.md subdirectory issue
    if [[ "$skill_file" == *"skills/README.md"* ]]; then
        continue
    fi

    skill_name=$(basename $(dirname "$skill_file"))

    # Read version field
    version_line=$(grep "^version:" "$skill_file" | head -1)

    if [[ -z "$version_line" ]]; then
        echo "❌ $skill_name: NO VERSION FIELD"
        malformed_files=$((malformed_files + 1))
        not_stable_skills=$((not_stable_skills + 1))
        continue
    fi

    version=${version_line#version: }

    # Check for -stable suffix
    if [[ "$version" == *-stable ]]; then
        echo "✅ $skill_name: $version"
        stable_skills=$((stable_skills + 1))
    else
        echo "❌ $skill_name: $version"
        not_stable_skills=$((not_stable_skills + 1))
    fi

    # Check file size (>10KB)
    size_kb=$(du -k "$skill_file" | cut -f1)
    if [[ $size_kb -gt 10 ]]; then
        large_files=$((large_files + 1))
    fi
done

echo ""
echo "=== DETAILED ANALYSIS ==="
echo ""

# Create summary file
SUMMARY_FILE="skills_health_summary.txt"
{
    echo "=== AEF SKILLS HEALTH CHECK SUMMARY ==="
    echo ""
    echo "Generated: $(date)"
    echo ""
    echo "=== STATISTICS ==="
    echo "Total SKILL.md files: $total_skills"
    echo "Stable skills (-stable suffix): $stable_skills"
    echo "Not stable skills: $not_stable_skills"
    echo "Malformed files (missing version): $malformed_files"
    echo "Large files (>10KB): $large_files"
    echo ""
    echo "=== COMPLIANCE ==="
    if [[ $total_skills -gt 0 ]]; then
        compliance=$((stable_skills * 100 / total_skills))
        echo "Compliance rate: $compliance% ($stable_skills/$total_skills)"
    else
        echo "Compliance: 0/0 (0%)"
    fi
    echo ""
    echo "=== HEALTH ISSUES IDENTIFIED ==="
    echo ""
    echo "1. Version suffix compliance:"
    echo "   Skills missing -stable suffix: $not_stable_skills/$total_skills ($((not_stable_skills*100/total_skills))%)"
    echo ""
    echo "2. File structure validation:"
    echo "   Skills with malformed frontmatter: $malformed_files/$total_skills ($((malformed_files*100/total_skills))%)"
    echo ""
    echo "3. File size concerns:"
    echo "   Skills with large files (>10KB): $large_files/$total_skills ($((large_files*100/total_skills))%)"
    echo ""
    echo "=== PRIORITY ASSESSMENT ==="
    echo "CRITICAL (requires immediate action):"
    echo "   Skills missing -stable suffix: $not_stable_skills"
    echo "   Skills with malformed frontmatter: $malformed_files"
    echo ""
    echo "HIGH (should be addressed):"
    echo "   Skills with large files: $large_files"
    echo ""
    echo "MEDIUM (monitor):"
    echo "   Skills with version compliance: $((total_skills - not_stable_skills - malformed_files))/$total_skills"
    echo ""
    echo "=== SPECIFIC SKILLS REQUIRING ATTENTION ==="
    echo ""
    echo "Skills missing -stable suffix:"
    find skills -name "SKILL.md" | while read skill_file; do
        if [[ "$skill_file" == *"skills/README.md"* ]]; then
            continue
        fi
        version_line=$(grep "^version:" "$skill_file" | head -1)
        if [[ -z "$version_line" ]] || ! echo "$version_line" | grep -q "-stable"; then
            skill_name=$(basename $(dirname "$skill_file"))
            echo "   - $skill_name: $(echo "$version_line" | sed 's/^version: //')"
        fi
    done
    echo ""
    echo "=== RECOMMENDATIONS ==="
    echo ""
    echo "IMMEDIATE ACTIONS REQUIRED:"
    echo "1. Add -stable suffix to all skills without it:"
    find skills -name "SKILL.md" | while read skill_file; do
        if [[ "$skill_file" == *"skills/README.md"* ]]; then
            continue
        fi
        version_line=$(grep "^version:" "$skill_file" | head -1)
        if [[ -z "$version_line" ]] || ! echo "$version_line" | grep -q "-stable"; then
            skill_name=$(basename $(dirname "$skill_file"))
            version=$(echo "$version_line" | sed 's/^version: //')
            echo "   - Update $skill_name from version: $version to version: $version-stable"
        fi
    done
    echo ""
    echo "2. Ensure all skills have proper YAML frontmatter:"
    find skills -name "SKILL.md" | while read skill_file; do
        if [[ "$skill_file" == *"skills/README.md"* ]]; then
            continue
        fi
        frontmatter_count=$(grep -c "^---$" "$skill_file")
        if [[ $frontmatter_count -lt 2 ]]; then
            skill_name=$(basename $(dirname "$skill_file"))
            echo "   - Fix $skill_name frontmatter (needs proper --- delimiters)"
        fi
    done
    echo ""
    echo "3. Validate file integrity:"
    find skills -name "SKILL.md" | while read skill_file; do
        if [[ "$skill_file" == *"skills/README.md"* ]]; then
            continue
        fi
        # Check for NUL bytes
        if grep -q $'\x00' "$skill_file"; then
            skill_name=$(basename $(dirname "$skill_file"))
            echo "   - Remove NUL bytes from $skill_name SKILL.md"
        fi
    done
    echo ""
} > "$SUMMARY_FILE"

echo "Summary saved to $SUMMARY_FILE"

echo "=== HEALTH CHECK COMPLETE ==="
echo ""
echo "Key findings:"
echo "- Total skills analyzed: $total_skills"
echo "- Stable skills: $stable_skills"
echo "- Immediate action required: $not_stable_skills skills need -stable suffix"
echo "- Frontmatter issues: $malformed_files skills need validation"
echo ""
echo "For detailed analysis, see $SUMMARY_FILE"
