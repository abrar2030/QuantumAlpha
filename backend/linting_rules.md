# Code Quality Guidelines (Backend)

This document outlines the code quality guidelines for the backend services, focusing on linting, static typing, and testing.

## Linting
We recommend using `flake8` for Python code with a strict configuration. Below are some recommended rules:

- **E121, E123, E126, E131, E133:** Indentation related issues
- **E225:** Missing whitespace around operator
- **E231:** Missing whitespace after ","
- **E251:** Unexpected whitespace around keyword / parameter equals
- **E261, E262:** At least two spaces before inline comment
- **E271, E272, E273, E274:** Multiple spaces after keyword, operator or bracket
- **E302:** Expected 2 blank lines, found 1 (for top-level function/class definition)
- **E501:** Line too long (80 characters)
- **W292:** No newline at end of file
- **W391:** Blank line at end of file

## Static Typing
We enforce static typing using `mypy` to catch type errors during development. All new code should include type hints.

## Unit Testing
All critical functions and modules should have corresponding unit tests. We use `pytest` for testing. Tests should be:
- **Isolated:** Test only one component at a time.
- **Fast:** Run quickly to provide rapid feedback.
- **Repeatable:** Produce the same results every time.
- **Self-validating:** Automatically determine if the test passed or failed.

## Example (Conceptual) - `backend/data_ingestion/tests/test_data_processor.py`
```python
import pytest
from ..data_processor import process_market_data

def test_process_market_data_valid_input():
    # Example of a basic unit test for data processing
    raw_data = {"symbol": "AAPL", "price": 150.0, "volume": 1000}
    processed_data = process_market_data(raw_data)
    assert processed_data["symbol"] == "AAPL"
    assert processed_data["price"] == 150.0
    assert processed_data["volume"] == 1000
    assert "timestamp" in processed_data

def test_process_market_data_missing_field():
    with pytest.raises(ValueError, match="Missing required field"): # Example of error handling test
        process_market_data({"symbol": "GOOG"})

```


