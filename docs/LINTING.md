# QuantumAlpha Linting Guide

This document provides instructions for using the comprehensive linting system set up for the QuantumAlpha project.

## Overview

The linting system covers three main components of the project:

1. **Python Backend** - Uses flake8, pylint, black, and isort
2. **Web Frontend** - Uses ESLint and Prettier
3. **Mobile Frontend** - Uses ESLint and Prettier with React Native specific rules

## Prerequisites

The linting script will automatically install required dependencies, but you should have the following installed:

- Python 3.x
- Node.js and npm
- Bash shell

## Using the Lint Script

The main script `lint.sh` is located in the project root directory. It provides a unified interface for running all linters.

### Basic Usage

To run all linters on all parts of the project:

```bash
./lint.sh
```

### Command Line Options

The script supports the following options:

| Option          | Description                         |
| --------------- | ----------------------------------- |
| `-h, --help`    | Show help message                   |
| `-b, --backend` | Run only backend linting            |
| `-w, --web`     | Run only web frontend linting       |
| `-m, --mobile`  | Run only mobile frontend linting    |
| `-f, --fix`     | Attempt to fix issues automatically |
| `-v, --verbose` | Show detailed output                |
| `-r, --report`  | Generate HTML reports               |

### Examples

Run only backend linters:

```bash
./lint.sh --backend
```

Run web and mobile linters with auto-fix:

```bash
./lint.sh -w -m -f
```

Generate HTML reports for all components:

```bash
./lint.sh --report
```

Run with verbose output:

```bash
./lint.sh --verbose
```

## Configuration Files

The linting configuration files are stored in the following locations:

### Python Backend

- `.flake8` - Flake8 configuration
- `.pylintrc` - Pylint configuration
- `pyproject.toml` - Black and isort configuration

### Web Frontend

- `.eslintrc.js` - ESLint configuration
- `.prettierrc` - Prettier configuration
- `tsconfig.json` - TypeScript configuration

### Mobile Frontend

- `.eslintrc.js` - ESLint configuration with React Native specific rules
- `.prettierrc` - Prettier configuration
- `tsconfig.json` - TypeScript configuration for React Native

## Reports

When using the `--report` option, HTML reports will be generated in the `lint_reports` directory with subdirectories for each component:

- `lint_reports/python/` - Python backend reports
- `lint_reports/web/` - Web frontend reports
- `lint_reports/mobile/` - Mobile frontend reports

## Integration with CI/CD

You can integrate this linting script into your CI/CD pipeline by adding the following command to your workflow:

```bash
./lint.sh || exit 1
```

This will fail the build if any linting issues are found.

## Customizing Linting Rules

To customize the linting rules:

1. Modify the configuration files in the respective `lint_configs` directories
2. Run the lint script to apply the new rules

## Troubleshooting

If you encounter any issues with the linting script:

1. Run with the `--verbose` flag to see detailed output
2. Ensure all dependencies are correctly installed
3. Check that the configuration files are properly formatted

For more specific issues, refer to the documentation of the individual linting tools:

- [flake8](https://flake8.pycqa.org/)
- [pylint](https://pylint.pycqa.org/)
- [black](https://black.readthedocs.io/)
- [isort](https://pycqa.github.io/isort/)
- [ESLint](https://eslint.org/)
- [Prettier](https://prettier.io/)
