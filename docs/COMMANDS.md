# Log Analyser CLI Commands

This document provides a comprehensive guide to all available commands in the Log Analyser CLI application.

## Getting Help

To get help for any command, use the `--help` flag:

```bash
log-analyser --help                    # General help
log-analyser analyse --help           # Help for specific command
log-analyser list-queries --help      # Help for list-queries command
```

## Command Overview

| #   | Command                  | Description                                                      |
| --- | ------------------------ | ---------------------------------------------------------------- |
| 1   | `analyse`                | Analyze logs and generate summary statistics for given trace IDs |
| 2   | `list-queries`           | List all queries for the given trace ID(s)                       |
| 3   | `list-slow-queries`      | List all slow queries for the given trace ID(s)                  |
| 4   | `list-duplicate-queries` | List all duplicate queries for the given trace ID(s)             |

## Command Details

### 1. `analyse` Command

**Purpose**: Analyze logs and generate summary statistics for given trace IDs.

**Usage**:
```bash
log-analyser analyse <log_file> <trace_ids> [OPTIONS]
```

**Arguments** (Mandatory):
- `log_file`: Path to the log file to analyze
- `trace_ids`: One or more trace IDs (comma-separated)

**Options** (Optional):
- `--mode`: Analysis mode (default: "DB", currently only DB mode is supported)
- `--slow-ms`: Threshold for slow queries in milliseconds (default: 500.0)
- `--format`: Output format - table, json, or yaml (default: table)
- `--output-file`: Save output to file (optional)

**Example**:
```bash
log-analyser analyse logs/db.log "trace-123,trace-456" --slow-ms 200 --format json --output-file analysis.json
```

**Output**: Summary statistics including trace ID, timing information, query counts, error status, and duplicate query count.

---

### 2. `list-queries` Command

**Purpose**: List all queries for the given trace ID(s).

**Usage**:
```bash
log-analyser list-queries <log_file> <trace_ids> [OPTIONS]
```

**Arguments** (Mandatory):
- `log_file`: Path to the log file to analyze
- `trace_ids`: One or more trace IDs (comma-separated)

**Options** (Optional):
- `--format`: Output format - table, json, or yaml (default: table)
- `--output-file`: Save output to file (optional)

**Example**:
```bash
log-analyser list-queries logs/db.log "trace-123" --format table --output-file queries.txt
```

**Output**: Detailed list of all queries with timestamp, trace ID, duration, statement, and error status.

**Note**: If duration or rows shows as -1, it means that statistical information (time/rows) is not available for that particular query in the log format.

---

### 3. `list-slow-queries` Command

**Purpose**: List all slow queries for the given trace ID(s).

**Usage**:
```bash
log-analyser list-slow-queries <log_file> <trace_ids> [OPTIONS]
```

**Arguments** (Mandatory):
- `log_file`: Path to the log file to analyze
- `trace_ids`: One or more trace IDs (comma-separated)

**Options** (Optional):
- `--slow-ms`: Threshold for slow queries in milliseconds (default: 100.0)
- `--format`: Output format - table, json, or yaml (default: table)
- `--output-file`: Save output to file (optional)

**Example**:
```bash
log-analyser list-slow-queries logs/db.log "trace-123,trace-456" --slow-ms 500 --format json
```

**Output**: List of queries that exceed the specified duration threshold with timestamp, trace ID, duration, and statement.

---

### 4. `list-duplicate-queries` Command

**Purpose**: List all duplicate queries for the given trace ID(s).

**Usage**:
```bash
log-analyser list-duplicate-queries <log_file> <trace_ids> [OPTIONS]
```

**Arguments** (Mandatory):
- `log_file`: Path to the log file to analyze
- `trace_ids`: One or more trace IDs (comma-separated)

**Options** (Optional):
- `--format`: Output format - table, json, or yaml (default: table)
- `--output-file`: Save output to file (optional)

**Example**:
```bash
log-analyser list-duplicate-queries logs/db.log "trace-123" --format yaml --output-file duplicates.yaml
```

**Output**: List of normalized statements and their occurrence counts, sorted by frequency (highest first).

## Output Formats

The application supports three output formats:

- **table** (default): Human-readable table format using GitHub-style tables
- **json**: JSON format with proper indentation
- **yaml**: YAML format with Unicode support

## Installation and Usage

1. **Install the package**:
   ```bash
   pip install -e .
   ```

2. **Run commands**:
   ```bash
   log-analyser <command> [arguments] [options]
   ```

3. **Get help**:
   ```bash
   log-analyser --help
   log-analyser <command> --help
   ```

## Notes

- All commands require a log file path and trace ID(s) as mandatory arguments
- Trace IDs can be provided as a comma-separated list for multiple traces
- The `--output-file` option allows saving results to a file instead of displaying on console
- Currently, only DB mode is supported for analysis
- All datetime values are displayed in ISO format
- Duration values are shown in appropriate units (seconds for total duration, milliseconds for individual queries)
