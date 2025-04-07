"""
Task-related CLI commands
"""
import click
from lightwave.core.services.task_service import TaskService
from lightwave_cli.formatters.task_formatter import format_task_list

@click.group()
def task():
    """Manage tasks"""
    pass

@task.command()
@click.option("--status", "-s", help="Filter by status")
@click.option("--with-subtasks", is_flag=True, help="Show subtasks")
@click.option("--file", "-f", default="tasks/tasks.json", help="Tasks file path")
def list(status, with_subtasks, file):
    """List all tasks with IDs, titles, and status."""
    service = TaskService(file_path=file)
    tasks = service.list_tasks(status_filter=status)
    
    # Format and display tasks
    click.echo(format_task_list(tasks, with_subtasks=with_subtasks))

@task.command()
@click.argument('task_id', type=int)
@click.option("--num-subtasks", "-n", type=int, default=3, help="Number of subtasks to generate")
@click.option("--research", is_flag=True, help="Include research in task expansion")
@click.option("--prompt", "-p", help="Additional context for task expansion")
def expand(task_id, num_subtasks, research, prompt):
    """Expand a task into subtasks."""
    service = TaskService()
    try:
        expanded_task = service.expand_task(
            task_id=task_id,
            num_subtasks=num_subtasks,
            with_research=research,
            context_prompt=prompt
        )
        click.echo(format_task_list([expanded_task]))
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort() 