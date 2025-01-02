#!/bin/bash

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Error counter
ERRORS=0

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

# Activate virtual environment
print_header "Activating Virtual Environment"
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    # Windows
    source venv/Scripts/activate
else
    # Unix/MacOS
    source venv/bin/activate
fi

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to activate virtual environment${NC}"
    exit 1
fi

# Type check with MyPy
print_header "Running MyPy Type Checker"
# ignore venv folder
mypy . --exclude venv
check_result "MyPy"

# Final summary
print_header "Summary"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}All checks passed successfully!${NC}"
    exit 0
else
    echo -e "${RED}${ERRORS} check(s) failed${NC}"
    exit 1
fi