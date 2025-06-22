# Ondo Project Reference

## Common Commands
- Install dependencies: `make install` or `./bin/install.sh`
- Run development server: `make dev` or `./bin/dev.sh`
- Run in production: `./bin/run.sh`
- Format code: `make fmt` or `./bin/fmt.sh`
- Lint code: `make lint` or `./bin/lint.sh` (add `--fix` to auto-fix)
- Type check: `make types` or `./bin/types.sh` (add `--strict` for strict mode)
- Run all checks: `make check` or `./bin/check.sh`
- Compile CSS: `make tailwind` or `./bin/tailwind.sh` (add `-w` for watch mode)

## UV Package Manager
This project uses `uv` for Python dependency management. Key commands:
- `uv sync` - Install dependencies from pyproject.toml
- `uv sync --dev` - Install including dev dependencies
- `uv run <command>` - Run command in virtual environment
- `uvx <tool>` - Run tool without installing in project

## Architecture Patterns

### Handler Patterns
- **PageResponse:** For full page or HTMX partial page responses
  ```python
  from src.server.handlers import PageResponse
  page = PageResponse("pages/template.html", layout="layouts/app.html")
  return page.render(request, {"data": data})
  ```
- **ComponentResponseHandler:** For components that can return JSON or HTML
  ```python
  from src.server.handlers import ComponentResponseHandler
  handler = ComponentResponseHandler("components/item.html")
  return await handler.respond(request, data)
  ```

### Styling & Dark Mode
- Using Franken UI components with Tailwind CSS
- Dark mode toggle available via theme switcher component
- CSS variables for theming in `styles/main.css`
- Colors use HSL format for easy theming

## Code Style Guidelines
- **Imports:** stdlib first, third-party next, local imports last, grouped with blank lines
- **Typing:** Use type hints for all functions, parameters, and return values
- **Naming:** snake_case for variables/functions, PascalCase for classes, UPPER_SNAKE_CASE for constants
- **Async:** Use async/await for IO-bound operations
- **Error handling:** Use specific exceptions, log errors, use HTTPExceptions for API errors
- **Structure:** Separate models from view logic, use FastAPI for endpoints, Jinja2 for templates
- **Formatters:** Black (formatter), Ruff (linter), MyPy (type checker)