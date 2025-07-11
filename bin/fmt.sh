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

# Check if --check flag is provided
CHECK_MODE=false
if [[ "$1" == "--check" ]]; then
    CHECK_MODE=true
fi

# Format with Black using uvx
print_header "Running Black Formatter"
# Check which directories exist
BLACK_PATHS="src"
if [ -d "tests" ]; then
    BLACK_PATHS="$BLACK_PATHS tests"
fi

if [ "$CHECK_MODE" = true ]; then
    uvx black $BLACK_PATHS --line-length 88 --check
else
    uvx black $BLACK_PATHS --line-length 88
fi
check_result "Black"

# Final summary
print_header "Summary"
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}All checks passed successfully!${NC}"
    exit 0
else
    echo -e "${RED}${ERRORS} check(s) failed${NC}"
    exit 1
fi