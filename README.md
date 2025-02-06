# Codebatcher (cbatch)

A CLI tool that formats your codebase into a structured markdown file, making it easier to provide context to AI tools like ChatGPT or Claude.

## Features

- 📝 Converts your entire codebase into a single, well-structured markdown file
- 🎯 Intelligent file filtering with `.cbatchignore` support
- ⚙️ Configurable project metadata through `cbatch.ini`
- 📊 Token estimation for AI context windows
- 🚀 Simple and intuitive CLI interface

## Installation

Install codebatcher using pip:

```bash
pip install codebatcher
```

## Quick Start

1. Navigate to your project directory:
```bash
cd your-project
```

2. Initialize cbatch configuration:
```bash
cbatch init
```

3. Generate the structured codebase file:
```bash
cbatch update
```

## Commands

- `cbatch init` - Initialize configuration and create default ignore patterns
- `cbatch update [path] [output-file]` - Update/create the structured codebase file
- `cbatch tokens` - Display estimated token count for the generated file

## Configuration

### cbatch.ini

During initialization (`cbatch init`), you can configure:
- Codebase Type (e.g., FastAPI backend, React frontend)
- Deployment Location
- General Description
- Execution Command

Example `cbatch.ini`:
```ini
[General]
codebase_type = FastAPI backend
deployment_location = AWS
general_description = REST API for user management
execution_command = uvicorn main:app --reload

[Summary]
input_token_estimate = 12345
```

### .cbatchignore

Similar to `.gitignore`, specify patterns for files and directories to exclude. Default patterns include:

- Common version control files (`.git/`, `.gitignore`)
- Build artifacts (`*.pyc`, `build/`, `dist/`)
- Environment files (`.env`, `venv/`)
- Dependencies (`node_modules/`)
- System files (`.DS_Store`)
- Temporary files (`*.swp`, `temp/`, `tmp/`)
- Log files (`*.log`)

Add custom patterns by editing `.cbatchignore`:
```
# Custom ignore patterns
secrets/
*.config.js
private/*
```

## Output Format

The generated markdown file (`codebatch.md` by default) includes:

1. Instructions section
2. General project information
3. Structured listing of all codebase files with their contents

Example structure:
```markdown
# Instructions #

This file represents the entire codebase...

## General Info ##

**Codebase Type**: FastAPI backend
**Deployment Location**: AWS
...

## Files ##

### `src/main.py` ###
```python
# File contents here
```
```

## Use Cases

- Providing context to AI tools about your entire codebase
- Generating documentation overviews
- Sharing code context with team members
- Creating structured backups of your source code

## Token Estimation

The tool provides a simple word-count based token estimation to help you stay within AI context windows. Check the current estimate using:

```bash
cbatch tokens
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[MIT License](LICENSE)

## Author

Zach (zh93@nau.edu)