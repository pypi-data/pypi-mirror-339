# LightWave Core

Core library for the LightWave ecosystem, providing common utilities, models, and services.

## Installation

```bash
# Using uv (recommended)
uv install lightwave-core

## Development Setup

# open repo in the gh desktop app then open in cursor ide

# Set up a virtual environment (with uv)
uv venv

# Activate the virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install in development mode with all dev dependencies
uv pip install -e ".[all-dev]"

# Run pre-commit install to set up the git hooks
pre-commit install
```

## Usage

```python
from lightwave.core import utils

# Use the library components
```

## Structure

```txt
src/
└── lightwave/
    ├── __init__.py
    └── core/
        ├── __init__.py
        ├── models/      # Shared data models
        ├── utils/       # Utility functions
        └── services/    # Common services
```

## License

Proprietary - All rights reserved
