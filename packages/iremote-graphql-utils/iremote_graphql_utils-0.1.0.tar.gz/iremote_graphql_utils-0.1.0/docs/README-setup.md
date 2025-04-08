# graphql-utils (project setup)

Project setup for the `graphql-utils` package.

## Prerequisites

- Python 3.8 or higher
- UV Environment

## Setup

```bash
uv init --package graphql-utils
```

## Naming Conventions

- Package name: `graphql-utils`
- Module name: `graphql_utils`
- Class names: `GraphQLUtils`, `GraphQLClient`, etc.
- Function names: `fetch_data`, `parse_response`, etc.
- Variable names: `response_data`, `query_string`, etc.
- Constants: `API_URL`, `DEFAULT_TIMEOUT`, etc.
- Test files: `test_graphql_utils.py`, `test_graphql_client.py`, etc.
- Example files: `example_usage.py`, `example_query.py`, etc.
- Documentation files: `README.md`, `CONTRIBUTING.md`, etc.

## Directories

- `src/graphql_utils`: The main package directory.
- `tests`: Contains unit tests for the package.
- `docs`: Documentation files.
- `examples`: Example usage of the package.
- `scripts`: Utility scripts for development and testing.

## Gen AI prompt

```markdown
Imagine you are helping a Python developer who is building a utility package for GraphQL, focusing on functionalities like schema splitting, validation, and formatting. The developer has decided to name their Git repository `graphql-utils` and is using the `uv` package manager.

Provide the recommended standard Python package directory structure for this project. Ensure the structure includes:

- A top-level directory named `graphql-utils`.
- A `src` subdirectory to house the main package code.
- Within `src`, a subdirectory named `graphql_utils` (matching the intended import name).
- Example Python files within the `graphql_utils` package for schema splitting, validation, and formatting.
- A `tests` subdirectory for unit tests.
- Corresponding example test files within the `tests` directory for the schema utility modules.
- The necessary configuration file for `uv` (and pip), which is `pyproject.toml`.
- A `README.md` file for project documentation.
- A `LICENSE` file for licensing information.

Only provide the directory structure, listing the directories and files with their relative paths. Do not include any content within the files.
```
