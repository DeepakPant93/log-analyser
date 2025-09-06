# log-analyser

A Typer-based CLI application that analyzes logs based on trace IDs (DB mode). This tool is specifically designed to analyze logs following a structured pattern with trace IDs, span IDs, and contextual information.

## Supported Log Pattern

This log-analyser tool is especially designed to analyze logs with the following pattern:

```
%d ${CONTEXT_NAME} [%thread] [traceId: %X{traceId:-NO_TRACE}] [spanId: %X{spanId:-NO_SPAN}] [companyId: %X{companyId:-NO_COMPANY}] [userId: %X{userId:-NO_USER}] %-5level %logger{36} - %msg%n
```

The tool extracts and analyzes trace IDs, span IDs, and other contextual information from logs following this structured format.

## Quick Start

### Using Make Commands (Recommended)

```bash
# Set up the environment and install dependencies
make setup

# Activate the virtual environment
make activate

# Build the package
make bake

# Run the CLI with arguments
make run ARGS="analyze logs/db.log trace123 --format table"

# Quick check if CLI is working
make check

# Run linting
make lint

# Run tests
make test

# Clean build artifacts
make clean
```

### Manual Installation

```bash
# Create virtual environment
uv venv -p 3.12
uv pip install -e .
```

## Available Commands

| Command                  | Description                                                      |
| ------------------------ | ---------------------------------------------------------------- |
| `analyze`                | Analyze logs and generate summary statistics for given trace IDs |
| `list-queries`           | List all queries for the given trace ID(s)                       |
| `list-slow-queries`      | List all slow queries for the given trace ID(s)                  |
| `list-duplicate-queries` | List all duplicate queries for the given trace ID(s)             |

### Quick Examples

```bash
# Analyze logs for specific trace IDs
log-analyser analyze logs/db.log trace123 --mode DB --format table

# List all queries for multiple trace IDs
log-analyser list-queries logs/db.log trace123 trace456 --format json --output-file result.json

# Find slow queries (default threshold: 100ms)
log-analyser list-slow-queries logs/db.log trace123 --slow-ms 200 --format table

# Find duplicate queries
log-analyser list-duplicate-queries logs/db.log trace123 trace456 --format yaml
```

## Detailed Documentation

For comprehensive command documentation, options, and advanced usage examples, see:

- **[COMMANDS.md](docs/COMMANDS.md)** - Complete command reference with detailed options and examples
- **[Makefile](Makefile)** - Available make commands for development and deployment

## Key Features

- **Trace-based Analysis**: Analyze logs by trace IDs to understand request flows
- **Query Performance**: Identify slow queries with customizable thresholds
- **Duplicate Detection**: Find repeated queries that might indicate inefficiencies
- **Multiple Output Formats**: Support for table, JSON, and YAML output formats
- **File Export**: Save results to files for further processing
- **Structured Log Support**: Optimized for logs with trace ID, span ID, and contextual information

## Configuration

- **Default Mode**: DB (database log analysis)
- **Slow Query Threshold**: 100ms (customizable with `--slow-ms`)
- **Output Formats**: table (default), json, yaml
- **File Output**: Use `--output-file` to save results to a file

## Development

See the [Makefile](Makefile) for available development commands:

- `make setup` - Set up development environment
- `make lint` - Run code linting
- `make test` - Run tests
- `make clean` - Clean build artifacts

