#!/bin/bash
echo "=== AEF SKILLS HEALTH REPORT ==="
echo ""
echo "Generated: $(date)"
echo ""
echo "=== OVERVIEW ==="
total_skills=$(find skills -name "SKILL.md" | wc -l)
echo "Total SKILL.md files: $total_skills"
echo ""
echo "=== VERSION COMPLIANCE ANALYSIS ==="
echo ""
echo "Skills with -stable suffix:"
find skills -name "SKILL.md" -exec grep -l "^version:" {} \; | while read f; do
    if grep -q "-stable" "$f"; then
        basename=$(basename $(dirname "$f"))
        echo "✓ $basename"
    fi
done

echo ""
echo "Skills without -stable suffix:"
find skills -name "SKILL.md" -exec grep -l "^version:" {} \; | while read f; do
    if ! grep -q "-stable" "$f"; then
        basename=$(basename $(dirname "$f"))
        echo "✗ $basename"
    fi
done

echo ""
echo "=== SUMMARY ==="
stable_count=$(find skills -name "SKILL.md" -exec grep -l "^version:" {} \; | while read f; do
    if grep -q "-stable" "$f"; then echo "1"; else echo "0"; fi
done | awk '{sum+=$1} END {print sum}')

echo "Stable skills: $stable_count"
echo "Non-stable skills: $(($total_skills - $stable_count))"
if [ $total_skills -gt 0 ]; then
    compliance=$((stable_count * 100 / total_skills))
    echo "Compliance rate: $compliance% ($stable_count/$total_skills)"
else
    echo "Compliance: 0/0 (0%)"
fi
