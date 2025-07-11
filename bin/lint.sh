#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Error counter
ERRORS=0

FIX=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --fix) FIX=true ;;
        *) echo "Unknown parameter: $1"; exit 1 ;;
    esac
    shift
done

# Function to print section headers
print_header() {
    echo -e "\n${YELLOW}=== $1 ===${NC}"
}

# Function to check command result
check_result() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ $1 passed${NC}"
    else
        echo -e "${RED}✗ $1 failed${NC}"
        ERRORS=$((ERRORS + 1))
    fi
}

# Ensure we're in the project root (adjust this path as needed)
cd "$(dirname "$0")/.." || exit 1

# Lint with Ruff using uvx
print_header "Running Ruff Linter"
# Check which directories exist
RUFF_PATHS="src"
if [ -d "tests" ]; then
    RUFF_PATHS="$RUFF_PATHS tests"
fi

if [ "$FIX" = true ]; then
    uvx ruff check $RUFF_PATHS --fix
else
    uvx ruff check $RUFF_PATHS
fi
check_result "Ruff"

# Final summary
print_header "Summary"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}All checks passed successfully!${NC}"
    exit 0
else
    echo -e "${RED}${ERRORS} check(s) failed${NC}"
    exit 1
fi