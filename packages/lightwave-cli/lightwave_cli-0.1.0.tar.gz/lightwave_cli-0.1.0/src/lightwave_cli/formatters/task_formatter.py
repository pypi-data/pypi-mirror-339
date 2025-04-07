"""
Task formatting utilities for CLI output
"""
from typing import List
from lightwave.core.models.task import Task

def format_task_list(tasks: List[Task], with_subtasks: bool = False) -> str:
    """Format a list of tasks for CLI output."""
    if not tasks:
        return "No tasks found."
    
    output = []
    for task in tasks:
        # Format main task
        task_line = f"[{task.id}] {task.title} ({task.status})"
        if task.priority != "medium":
            task_line += f" [{task.priority}]"
        output.append(task_line)
        
        # Add description if present
        if task.description:
            output.append(f"  {task.description}")
        
        # Add dependencies if present
        if task.dependencies:
            deps = ", ".join(str(dep) for dep in task.dependencies)
            output.append(f"  Dependencies: {deps}")
        
        # Add subtasks if requested
        if with_subtasks and hasattr(task, 'subtasks'):
            for subtask in task.subtasks:
                output.append(f"  └─ [{subtask.id}] {subtask.title}")
        
        output.append("")  # Add blank line between tasks
    
    return "\n".join(output) 