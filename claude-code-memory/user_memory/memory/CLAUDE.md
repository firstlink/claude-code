# My Personal Python Preferences

## Code Style
- Use Black formatter with 88 character line length
- Use isort for import sorting
- Type hints required for all functions
- Use pathlib instead of os.path

## CLI Development with Click
- Use click.group() for command organization
- Always include help text with """docstrings"""
- Use click.option() for optional flags
- Use click.argument() for required positional args

## Decimal for Money
Always use Decimal for financial calculations, never float:
```python
from decimal import Decimal

# Correct
amount = Decimal('10.50')

# Wrong - floating point errors
amount = float(10.50)
```

## Testing
- Use pytest for all tests
- Test files: test_*.py
- Run with: pytest -v

## Common Commands
```bash
# Format code
black . && isort .

# Run tests
pytest -v

# Type check
mypy src/
```
```