# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build/Test Commands
- Install dependencies: `pip install -e ".[test]"`
- Run all tests: `pytest`
- Run single test: `pytest tests/path_to_test.py::test_function_name`
- Run linting: `flake8`
- Type checking: `pyright`

## Code Style Guidelines
- Follow PEP8 conventions with 120 character line limit
- Use snake_case for variables/functions, PascalCase for classes
- Organize imports: stdlib, third-party, local (alphabetized)
- Include docstrings for all public methods
- Use type hints for parameters and return values
- Create custom exceptions for domain-specific errors
- Avoid hard-coded paths or credentials
- Maintain test coverage for new functionality