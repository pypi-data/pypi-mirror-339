# Lightwave Core Library

Core library for the Lightwave task and project management system. This library provides the fundamental functionality, models, and services used by the Lightwave CLI and other tools.

## Features

- Task management with subtasks and dependencies
- Sprint planning and tracking
- Scrum project organization
- Team member management
- File-based data storage with JSON
- Comprehensive error handling
- Type-safe models using Pydantic

## Installation

```bash
pip install lightwave-core
```

## Usage

### Basic Task Management

```python
from lightwave.core import TaskService, Task

# Initialize the service
service = TaskService()

# Create a new task
task = service.create_task({
    "title": "Implement user authentication",
    "description": "Add OAuth2 authentication to the API",
    "priority": "high"
})

# Add subtasks
task = service.expand_task(
    task_id=task.id,
    num_subtasks=3,
    context_prompt="Break down the OAuth implementation"
)

# List all tasks
tasks = service.list_tasks()

# Get a specific task
task = service.get_task(1)

# Update a task
updated_task = service.update_task(1, {
    "status": "in_progress",
    "details": "Using Auth0 for OAuth provider"
})
```

### Sprint Management

```python
from lightwave.core import Sprint
from datetime import datetime, timedelta

sprint = Sprint(
    id="sprint-1",
    name="Authentication Sprint",
    scrum_id="main-project",
    start_date=datetime.utcnow(),
    end_date=datetime.utcnow() + timedelta(days=14),
    goal="Complete user authentication system"
)
```

### Scrum Project Setup

```python
from lightwave.core import Scrum, TeamMember

team_member = TeamMember(
    id="user-1",
    name="John Doe",
    email="john@example.com",
    role="developer"
)

scrum = Scrum(
    id="main-project",
    name="Authentication System",
    department_id="engineering",
    description="Implement secure user authentication"
)

scrum.add_team_member(team_member)
```

## Development

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/kiwi-dev-la/lightwave-core.git
   cd lightwave-core
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install development dependencies:
   ```bash
   pip install -e ".[dev,test]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

### Running Tests

```bash
pytest
```

### Code Quality

- Format code:
  ```bash
  ruff format .
  ```

- Run linter:
  ```bash
  ruff check .
  ```

- Run type checker:
  ```bash
  mypy src
  ```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and ensure code quality checks pass
5. Submit a pull request

## License

Proprietary - All rights reserved

## Related Projects

- [lightwave-cli](https://github.com/kiwi-dev-la/lightwave-cli) - Command-line interface for Lightwave
- [lightwave-web](https://github.com/kiwi-dev-la/lightwave-web) - Web interface for Lightwave (coming soon)
