#!/bin/bash
# Health check for code-search skill in Oh My Pi

echo "=== Code-Search Skill Health Check ==="
echo ""

echo "1. Skill Structure:"
for f in SKILL.md code_indexer.py code-search.sh; do
    if [ -f "$f" ]; then
        echo "   ✓ $f exists"
    else
        echo "   ✗ $f missing"
    fi
done

echo ""
echo "2. Python Dependencies:"
python3 -c "import tree_sitter; import tree_sitter_language_pack; print('   ✓ tree-sitter available')" 2>/dev/null || echo "   ✗ tree-sitter not available"
python3 -c "import tree_sitter; from tree_sitter import Parser, Language; print('   ✓ Parser, Language available')" 2>/dev/null || echo "   ✗ Parser/Language not available"

echo ""
echo "3. Optional Dependencies (semantic search):"
python3 -c "import ollama; print('   ✓ ollama available')" 2>/dev/null || echo "   ⚠ ollama not installed (optional)"
python3 -c "import sqlite_vec; print('   ✓ sqlite-vec available')" 2>/dev/null || echo "   ⚠ sqlite-vec not installed (optional)"

echo ""
echo "4. Dry Run Test (skeleton generation):"
python3 -c "import code_indexer; print('   ✓ code_indexer imports successfully')" 2>/dev/null || echo "   ✗ code_indexer import failed"

echo ""
echo "5. Semantic Search Test (optional):"
python3 -c "
import code_indexer
import ollama, sqlite_vec
print('   ✓ semantic search dependencies available')
" 2>/dev/null || echo "   ⚠ semantic search dependencies unavailable"

echo ""
echo "=== Skill ready ==="