# AI Power Shell

An AI-powered smart shell with command suggestions and natural language processing.

## Installation

```bash
pip install aipowershell
```

## Usage

1. Set your OpenRouter API key in your environment:
```bash
export DEEPSEEK_API="your-api-key-here"
```

2. Run the shell:
```bash
aipowershell
```

## Features

- AI-powered command suggestions
- Natural language command processing (prefix with ?)
- Error analysis and fixing
- Project structure analysis

## Examples

```bash
$ ?show current directory  # Will translate to: pwd
$ ?list all files         # Will translate to: ls -la
$ !error ModuleNotFoundError: No module named 'pandas'  # Will analyze and fix the error
```
