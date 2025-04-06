# dotenv-schema

[![PyPI version](https://img.shields.io/pypi/v/dotenv-schema.svg)](https://pypi.org/project/dotenv-schema/)
[![Python Versions](https://img.shields.io/pypi/pyversions/dotenv-schema.svg)](https://pypi.org/project/dotenv-schema/)
[![License](https://img.shields.io/github/license/skyspec28/dotenv-schema.svg)](https://github.com/skyspec28/dotenv-schema/blob/main/LICENSE)
[![Test Coverage](https://img.shields.io/codecov/c/github/skyspec28/dotenv-schema.svg)](https://codecov.io/gh/skyspec28/dotenv-schema)
[![Build Status](https://img.shields.io/github/actions/workflow/status/skyspec28/dotenv-schema/python-tests.yml?branch=main)](https://github.com/skyspec28/dotenv-schema/actions)

A simple, lightweight Python tool to load, validate, and type-cast environment variables from `.env` files using a schema. This package helps you manage configuration in a type-safe way while keeping your secrets out of your codebase.

## Features

- 📝 Load variables from `.env` files into your Python environment
- ✅ Validate required environment variables
- 🔄 Automatic type casting (string, int, float, boolean)
- 🛡️ Schema validation with default values
- 🪶 Lightweight with zero dependencies

## Installation

```bash
pip install dotenv-schema
```

For development:

```bash
git clone https://github.com/skyspec28/dotenv-schema.git
cd dotenv-schema
pip install .
```

## Usage

### Basic Usage

```python
from dotenv_schema import load_env_file

# Load variables from .env file
env_vars = load_env_file()
print(env_vars)  # {'DATABASE_URL': 'postgres://...', 'DEBUG': 'true'}

# Access through os.environ
import os
print(os.environ['DATABASE_URL'])  # 'postgres://...'
```

### With Schema Validation

```python
from dotenv_schema import load_env_file, apply_schema

# Define your schema
schema = {
    'DATABASE_URL': {
        'required': True,
        'type': str
    },
    'DEBUG': {
        'type': bool,
        'default': False
    },
    'PORT': {
        'type': int,
        'default': 8000
    }
}

# Load and validate
raw_env = load_env_file()
config = apply_schema(raw_env, schema)

print(config['DEBUG'])  # True (boolean, not string)
print(config['PORT'])   # 8000 (integer, not string)
```

### Example .env file

```
# Database configuration
DATABASE_URL=postgres://user:password@localhost:5432/mydb

# Application settings
DEBUG=true
LOG_LEVEL=info

# API keys (keep these secret!)
API_KEY=your-secret-key-here
```

## API Reference

### `load_env_file(path='.env') -> dict`

Loads environment variables from a file into `os.environ` and returns them as a dictionary.

- **path**: Path to the .env file (default: '.env')
- **returns**: Dictionary of environment variables

### `apply_schema(raw_env: dict, schema: dict) -> dict`

Validates and transforms environment variables according to the provided schema.

- **raw_env**: Dictionary of raw environment variables
- **schema**: Dictionary defining the validation rules
- **returns**: Dictionary of validated and transformed environment variables

## License

MIT License - see the [LICENSE](LICENSE) file for details.

## Testing

The project uses pytest for testing. To run the tests:

```bash
# Install the package with development dependencies
pip install ".[dev]"

# Run tests
pytest

# Run tests with coverage report
pytest --cov=dotenv_schema
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

Please make sure to update tests as appropriate.

