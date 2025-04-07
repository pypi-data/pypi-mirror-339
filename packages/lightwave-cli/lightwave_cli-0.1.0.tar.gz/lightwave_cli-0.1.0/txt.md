# Lightwave Core and CLI Architecture

You should structure your code with a clear separation of concerns between the core library and the CLI application:

## 1. Core Library (lightwave-core)

This is your current project. It should:

- Provide all the fundamental functionality, APIs, models, and business logic
- Be usable programmatically by any application, not just the CLI
- Have minimal dependencies
- Not contain CLI-specific code

**Structure within the core:**

```txt
src/
└── lightwave/
    ├── __init__.py
    └── core/
        ├── __init__.py            # Package version and exports
        ├── models/                # Data models and schemas
        │   └── ...
        ├── services/              # Core business services
        │   └── ...
        ├── utils/                 # Utility functions
        │   └── ...
        └── exceptions.py          # Custom exceptions
```

### 2. CLI Application (lightwave-cli)

This should be a separate package that:

- Depends on lightwave-core
- Handles CLI-specific concerns (argument parsing, formatting output, etc.)
- Provides a user-friendly command-line interface
- Implements all commands described in your rules docs

**Recommended structure for the CLI package:**

```txt
src/
└── lightwave_cli/
    ├── __init__.py            # Package version and exports
    ├── cli/                   
    │   ├── __init__.py
    │   ├── main.py            # Entry point
    │   └── commands/          # Command implementations
    │       ├── __init__.py
    │       ├── init.py        # 'lightwave init' implementation
    │       ├── scrum.py       # Scrum-related commands
    │       ├── sprint.py      # Sprint-related commands
    │       └── task.py        # Task-related commands
    ├── formatters/            # Output formatting
    │   └── ...
    └── config/                # CLI configuration management
        └── ...
```

## Specific Recommendations

### 1. Core Library Responsibilities

- **Data models**: Define all entities (Task, Sprint, Scrum, etc.) using Pydantic models
- **Service layer**: Implement business logic for managing tasks, sprints, etc.
- **Utilities**: Provide helpers for common operations
- **Repository layer**: Handle data persistence (file operations, database, etc.)

Example of a core module:

```python
# src/lightwave/core/models/task.py
from pydantic import BaseModel, Field
from typing import List, Optional

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: str = "pending"
    dependencies: List[int] = Field(default_factory=list)
    priority: str = "medium"
    details: Optional[str] = None
    test_strategy: Optional[str] = None
    
    def is_blocked(self, completed_tasks: List[int]) -> bool:
        """Check if task is blocked by dependencies."""
        return any(dep not in completed_tasks for dep in self.dependencies)
```

### 2. CLI Application Responsibilities

- **Command parsing**: Use a library like Click or argparse
- **Output formatting**: Handle pretty printing, tables, colors
- **User interaction**: Prompts, confirmations, progress bars
- **CLI-specific config**: Handle CLI config files, environment variables

Example of a CLI command implementation:

```python
# src/lightwave_cli/cli/commands/task.py
import click
from lightwave.core.services.task_service import TaskService
from lightwave_cli.formatters.task_formatter import format_task_list

@click.command()
@click.option("--status", "-s", help="Filter by status")
@click.option("--with-subtasks", is_flag=True, help="Show subtasks")
@click.option("--file", "-f", default="tasks/tasks.json", help="Tasks file path")
def list_tasks(status, with_subtasks, file):
    """List all tasks with IDs, titles, and status."""
    service = TaskService(file_path=file)
    tasks = service.list_tasks(status_filter=status)
    
    # Format and display tasks (CLI-specific concern)
    click.echo(format_task_list(tasks, with_subtasks=with_subtasks))
```

### 3. Communication Between Core and CLI

- CLI should import and use core functionality
- Core should never import from CLI
- Use well-defined interfaces in core that CLI can consume
- Pass configuration from CLI to core rather than having core read CLI-specific config

## Implementation Guidelines

1. **Keep the Core Clean**:
   - No CLI-specific code in core
   - No direct printing to stdout/stderr
   - Return data, don't format it for display
   - Throw exceptions, don't handle them with user messages

2. **Structure CLI Commands**:
   - Group related commands (like in your dev_workflow docs)
   - Use command groups (e.g., `lightwave scrum`, `lightwave sprint`)
   - Provide consistent help text
   - Implement shell completion

3. **Configuration Management**:
   - Core should define what configuration it needs
   - CLI should handle reading config files, env vars, CLI args
   - CLI passes configuration to core

4. **Testing**:
   - Core should have high test coverage
   - CLI should focus on integration tests
   - Mock core services in CLI tests

## Example Interaction

Here's an example of how the CLI would interact with core:

```python
# CLI code (in lightwave-cli package)
def expand_task(task_id, num_subtasks, research, prompt):
    # Initialize the service from core
    task_service = TaskService()
    
    try:
        # Call core functionality
        expanded_task = task_service.expand_task(
            task_id=task_id,
            num_subtasks=num_subtasks,
            with_research=research,
            context_prompt=prompt
        )
        
        # Format and display results (CLI concern)
        print_expanded_task(expanded_task)
        
    except TaskNotFoundException as e:
        # Handle error with user-friendly message (CLI concern)
        click.echo(f"Error: Task {task_id} not found.", err=True)
        sys.exit(1)
```

By following this architecture, you'll have a maintainable codebase with a clear separation of concerns, making it easier to evolve both components independently.
