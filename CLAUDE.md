# Ondo Project Reference

## Common Commands
- Run development server: `./bin/dev.sh`
- Run in production: `./bin/run.sh`
- Format code: `./bin/fmt.sh`
- Lint code: `./bin/lint.sh` (add `--fix` to auto-fix)
- Type check: `./bin/types.sh`
- Run all checks: `./bin/check.sh`
- Compile CSS: `./bin/tailwind.sh` (add `-w` for watch mode)
- Run tests: `pytest -v` (single test: `pytest path/to/test.py::test_function -v`)

## Code Style Guidelines
- **Imports:** stdlib first, third-party next, local imports last, grouped with blank lines
- **Typing:** Use type hints for all functions, parameters, and return values
- **Naming:** snake_case for variables/functions, PascalCase for classes, UPPER_SNAKE_CASE for constants
- **Async:** Use async/await for IO-bound operations
- **Error handling:** Use specific exceptions, log errors, use HTTPExceptions for API errors
- **Structure:** Separate models from view logic, use FastAPI for endpoints, Jinja2 for templates
- **Formatters:** Black (formatter), Ruff (linter), MyPy (type checker)