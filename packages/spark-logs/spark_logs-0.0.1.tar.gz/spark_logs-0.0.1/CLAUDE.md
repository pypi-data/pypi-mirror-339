# Spark Logs Project Guidelines

## Commands
- **Install**: `pip install -e .`
- **Add dependency**: `uv add [DEPENDENCY]`
- **Run**: `spark-logs --project [PROJECT_ID] --cluster [CLUSTER_NAME] --app-id [APP_ID]`
- **Interactive Mode**: `spark-logs` (follows prompts)
- **Lint Check**: `python -m ruff check .`
- **Type Check**: `python -m basedpyright`
- **Format Code**: `python -m ruff format .`

## Code Style
- Follow Google Python Style Guide (as indicated by pydocstyle convention)
- Type hints required for function parameters and return values
- Max line length: 88 characters
- Imports order: standard library, third party, local application
- Use logger instead of print statements
- Snake_case for variables and function names
- CamelCase for class names
- Use try/except blocks for error handling with specific exceptions
- Use f-strings for string formatting
- Docstrings required (Google style) for public API functions
- Group related imports, with a blank line between groups

## Project Structure
- CLI code in `cli/`
- Core functionality in `src/spark_logs/`
- Logs saved to `logs/` directory (configurable)
