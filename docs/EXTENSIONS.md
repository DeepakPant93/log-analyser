# VS Code Extensions for Log Analyser

This document outlines the essential VS Code extensions required to develop and work effectively with the log-analyser CLI application. These extensions provide enhanced development experience, code quality, and productivity features specifically tailored for this Python-based log analysis tool.

## Required Extensions

### 1. Even Better TOML
**Extension ID:** `tamasfe.even-better-toml`

**Description:**
Provides syntax highlighting, validation, and formatting for TOML files. Essential for editing the `pyproject.toml` configuration file.

**Why it's needed:**
- Project uses `pyproject.toml` for dependencies and build settings
- Validates TOML syntax and catches configuration errors
- Auto-formatting and IntelliSense for TOML properties

---

### 2. Makefile Tools
**Extension ID:** `ms-vscode.makefile-tools`

**Description:**
Provides IntelliSense, debugging, and task execution for Makefiles. Essential for running development commands.

**Why it's needed:**
- Project uses Makefile for development workflow (`setup`, `bake`, `run`, `lint`, `test`, `clean`)
- IntelliSense for Make targets and variables
- Easy execution of make commands from VS Code

---

### 3. Markdown All in One
**Extension ID:** `yzhang.markdown-all-in-one`

**Description:**
Enhanced Markdown editing with live preview, table formatting, and documentation features.

**Why it's needed:**
- Project has extensive Markdown documentation (`README.md`, `docs/COMMANDS.md`)
- Live preview for documentation files
- Table formatting for command documentation

---

### 4. Python
**Extension ID:** `ms-python.python`

**Description:**
Official Python extension providing IntelliSense, debugging, testing, and environment management.

**Why it's needed:**
- Core extension for Python development
- IntelliSense and debugging capabilities
- Virtual environment management
- Code navigation and refactoring tools
- **Requires:** Python 3.12+ (as specified in `pyproject.toml`)

---

### 5. Python Debugger
**Extension ID:** `ms-python.debugpy`

**Description:**
Advanced debugging capabilities for Python applications with breakpoints and step-through debugging.

**Why it's needed:**
- Debug the CLI application with breakpoints
- Step-through debugging capabilities
- Variable inspection and watch expressions
- **Pre-configured:** Debug setup included in `.vscode/settings.json`

---

### 6. Ruff
**Extension ID:** `astral-sh.ruff`

**Description:**
Extremely fast Python linter and code formatter with comprehensive rule set and VS Code integration.

**Why it's needed:**
- Project configured to use Ruff for linting and formatting
- Fast, comprehensive code analysis (10-100x faster than alternatives)
- Automatic code formatting and import sorting
- Real-time error detection and fixing
- **Configured:** Set as default formatter with format-on-save enabled

---

## Installation Instructions

1. Open VS Code Extensions view (Ctrl+Shift+X / Cmd+Shift+X)
2. Search for each extension by name or ID
3. Click "Install" for each extension

**Alternative:** Use Command Palette (Ctrl+Shift+P) → "Extensions: Install Extensions"

## Development Workflow

With these extensions installed:
- **Code Development**: Python extension for IntelliSense and debugging
- **Code Quality**: Ruff for real-time linting and formatting
- **Documentation**: Markdown All in One for editing docs
- **Build Management**: Makefile Tools for development commands
- **Configuration**: Even Better TOML for project settings

## Troubleshooting

**Common Issues:**
- **Ruff not working**: Check Python interpreter is set correctly
- **Makefile Tools**: Ensure Makefile is in workspace root
- **Python debugging**: Verify virtual environment and interpreter path
- **TOML errors**: Check syntax in `pyproject.toml`

---

*This guide ensures optimal development experience for the log-analyser CLI application.*
