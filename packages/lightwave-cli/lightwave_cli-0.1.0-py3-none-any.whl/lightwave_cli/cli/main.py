"""
Main entry point for the Lightwave CLI
"""
import click
from lightwave_cli.cli.commands import init, scrum, sprint, task

@click.group()
def cli():
    """Lightwave CLI - A powerful project management tool"""
    pass

# Register command groups
cli.add_command(init.init)
cli.add_command(scrum.scrum)
cli.add_command(sprint.sprint)
cli.add_command(task.task)

if __name__ == '__main__':
    cli() 