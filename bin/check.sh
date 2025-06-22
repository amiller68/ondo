#!/bin/bash

# Source utilities
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
source "$SCRIPT_DIR/utils.sh"

# Ensure we're in the project root
cd "$PROJECT_ROOT" || exit 1

# Check which directories exist
CHECK_PATHS="src"
if [ -d "tests" ]; then
    CHECK_PATHS="$CHECK_PATHS tests"
fi

# Format with Black using uvx
print_header "Running Black Formatter"
uvx black $CHECK_PATHS --line-length 88 --check
check_result "Black"

# Lint with Ruff using uvx
print_header "Running Ruff Linter"
uvx ruff check $CHECK_PATHS
check_result "Ruff"

# Type check with MyPy using uvx
print_header "Running MyPy Type Checker"
uvx mypy src
check_result "MyPy"

# Final summary
print_summary "All checks passed successfully!"