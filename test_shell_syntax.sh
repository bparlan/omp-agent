#!/bin/bash
echo "Testing shell script syntax"
if ! bash -n test_resolver_init_001.sh; then
    echo "Syntax error in test_resolver_init_001.sh"
    exit 1
fi
if ! bash -n test_registry_init_001.sh; then
    echo "Syntax error in test_registry_init_001.sh"
    exit 1
fi
if ! bash -n test_resolution_priority_001.sh; then
    echo "Syntax error in test_resolution_priority_001.sh"
    exit 1
fi
echo "All shell scripts have valid syntax"
