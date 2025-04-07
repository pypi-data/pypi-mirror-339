# Getting Started with LightWave

This guide will help you get started with the LightWave ecosystem.

## Prerequisites

- Python 3.11 or higher
- Git
- UV package manager

## Installation

Install the LightWave CLI:

```bash
uv tool install lightwave-cli
```

Or install it in development mode:

```bash
git clone https://github.com/joelschaeffer/lightwave-cli.git
cd lightwave-cli
uv tool install -e .
```

## Setup Environment

Create a new virtual environment:

```bash
lightwave uv venv
source .venv/bin/activate
```

## Basic Commands

Here are some basic commands to get started:

```bash
# Show help
lightwave --help

# Run a docs agent
lightwave agent run docs "What is LightWave?"

# Install a package
lightwave uv install pydantic
``` 