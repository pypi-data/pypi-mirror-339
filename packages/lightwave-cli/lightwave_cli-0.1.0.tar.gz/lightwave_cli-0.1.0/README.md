# LightWave CLI

Command-line interface for LightWave ecosystem tools and utilities.

## Features

- **Documentation Sync**: Synchronize documentation from repositories
- **AI Agents**: Run AI agents using pydantic-ai for various tasks
- **UV Integration**: Wrapper for the fast UV package manager

## Installation

```bash
# Clone the repository
git clone git@github.com:kiwi-dev-la/lightwave-cli.git
cd lightwave-cli

# Install in development mode
pip install -e .
```

## Usage

### Documentation Sync

Synchronize documentation from a GitHub repository:

```bash
# Using a remote repository
lightwave docs sync --repo-url https://github.com/kiwi-dev-la/lightwave-eco-system-docs.git --branch main

# Using a locally cloned repository
lightwave docs sync --local-repo ./lightwave-eco-system-docs --branch main
```

### AI Agents

Run an AI agent with a prompt:

```bash
# Set your API key
export ANTHROPIC_API_KEY=your-api-key

# Run the docs agent
lightwave agent run docs "What are the main components of the LightWave ecosystem?"

# Run with different model
lightwave agent run docs "What's in the lightwave-cli?" --model claude-3-sonnet-20240229
```

### UV Package Manager

UV is a much faster alternative to pip for Python package management. The lightwave CLI includes wrappers for common UV commands:

```bash
# Create a virtual environment
lightwave uv venv myenv

# Install a package
lightwave uv install pydantic

# Install a package in editable mode
lightwave uv install -e /path/to/package

# Run a UV command
lightwave uv run pip list
```

## Available Agents

- **docs**: Answer questions about LightWave documentation

## Dependencies

- Python 3.11+
- typer
- rich
- gitpython
- pydantic
- pydantic-ai

## Development

To add a new agent:

1. Create a new file in `src/lightwave_cli/agents/`
2. Extend the `LightWaveAgent` class
3. Implement the `run()` method
4. Create a singleton instance named `agent`

## License

MIT
