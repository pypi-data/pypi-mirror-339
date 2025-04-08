# add2anki Development Guidelines

## Project Management
- This project uses `uv` for Python package management
- The project uses `just` for task automation

## Build & Test Commands
- Install dependencies: `just setup`
- Run all tests: `just test`
- Run single test: `just test tests/test_file.py::test_function`
- Format code: `just format`
- Format code and fix module import order and unused imports: `just fix`
- Lint code: `just lint`
- Type check: `just typecheck`
- Run all checks: `just check`
- Run application: `just run [args]`

## Code Style Guidelines
- **Python version**: 3.11+
- **Line length**: 120 characters
- **Formatting**: Use `ruff` for formatting with `just format`
- **Type checking**: Strict mode with complete annotations
- **Imports**: Sorted using Ruff's "I" rule (stdlib → third-party → local)
- **Quotes**: Double quotes for strings
- **Naming**: PascalCase for classes, snake_case for functions/variables
- **Exceptions**: Custom hierarchy with base class `add2ankiError`
- **Documentation**: Google-style docstrings with Args, Returns, Raises
- **Testing**: Use pytest with specific test naming pattern
- Prefer a functional style. Prefer comprehensions or map and filter over reduce.

## Type Hints
- Use type hints.
- In type hints, use `X | Y` instead of union. Use `dict[K, V]` instead of `Dict`.

## Developer Documentation
- Maintain developer documentation in `./docs`.
