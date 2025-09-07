from __future__ import annotations

from typing import Optional

import typer

from log_analyser.models import OutputFormat
from log_analyser.output import dump, maybe_write
from log_analyser.parser import (
    AnalysisResult,
    find_duplicate_queries,
    find_slow_queries,
    parse_db_mode,
)

app = typer.Typer(help="Analyze logs by trace IDs. Default mode: DB")

HELP_OUTPUT_FORMAT = f"Output format: {', '.join([member.value for member in OutputFormat])}"
HELP_OUTPUT_FILE = "Save output to file"
HELP_LOG_FILE = "Path to log file"
HELP_TRACE_IDS = "One or more trace IDs"


@app.command("analyse", help="Analyse logs and generate summary statistics")
def analyze(
    log_file: str = typer.Argument(..., help=HELP_LOG_FILE),
    trace_ids: str = typer.Argument(..., help=HELP_TRACE_IDS),
    mode: str = typer.Option("DB", "--mode", case_sensitive=False, help="Analysis mode (DB)"),
    slow_ms: float = typer.Option(500.0, "--slow-ms", help="Threshold for slow queries in ms"),
    format: str = typer.Option(OutputFormat.TABLE.value, "--format", help=HELP_OUTPUT_FORMAT),
    output_file: Optional[str] = typer.Option(None, "--output-file", help=HELP_OUTPUT_FILE),
):
    mode = mode.upper()
    if mode != "DB":
        raise typer.BadParameter("Only DB mode is currently supported")

    result: AnalysisResult = parse_db_mode(log_file, trace_ids.split(","), slow_ms=slow_ms)
    output_format: OutputFormat = OutputFormat(format.lower())
    payload = [
        {
            "trace_id": s.trace_id,
            "start_time": s.start_time,
            "end_time": s.end_time,
            "total_duration_sec": s.total_duration.total_seconds() if s.total_duration else None,
            "total_queries": s.total_queries,
            "total_slow_queries": s.total_slow_queries,
            "has_errors": s.has_errors,
            "duplicate_queries": s.duplicate_queries,
        }
        for s in result.summaries
    ]
    content = dump(payload, output_format)
    maybe_write(output_file, content)
    typer.echo(content)


@app.command("list-queries", help="List all queries for the given trace id")
def list_queries(
    log_file: str = typer.Argument(..., help=HELP_LOG_FILE),
    trace_ids: str = typer.Argument(..., help=HELP_TRACE_IDS),
    format: str = typer.Option(OutputFormat.TABLE.value, "--format", help=HELP_OUTPUT_FORMAT),
    output_file: Optional[str] = typer.Option(None, "--output-file", help=HELP_OUTPUT_FILE),
):
    result = parse_db_mode(log_file, trace_ids.split(","))
    output_format: OutputFormat = OutputFormat(format.lower())
    payload = [
        {
            "timestamp": q.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "trace_id": q.trace_id,
            "duration_ms": q.duration_ms,
            "rows": q.rows,
            "statement": q.statement,
            "is_error": q.is_error,
        }
        for q in result.queries
    ]
    content = dump(payload, output_format)
    maybe_write(output_file, content)
    typer.echo(content)


@app.command("list-slow-queries", help="List all slow queries for the given trace id")
def list_slow_queries(
    log_file: str = typer.Argument(..., help=HELP_LOG_FILE),
    trace_ids: str = typer.Argument(..., help=HELP_TRACE_IDS),
    slow_ms: float = typer.Option(500.0, "--slow-ms", help="Threshold for slow queries in ms"),
    format: str = typer.Option(OutputFormat.TABLE.value, "--format", help=HELP_OUTPUT_FORMAT),
    output_file: Optional[str] = typer.Option(None, "--output-file", help=HELP_OUTPUT_FILE),
):
    result = parse_db_mode(log_file, trace_ids.split(","))
    slow = find_slow_queries(result.queries, slow_ms=slow_ms)
    output_format: OutputFormat = OutputFormat(format.lower())
    payload = [
        {
            "timestamp": q.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "trace_id": q.trace_id,
            "duration_ms": q.duration_ms,
            "statement": q.statement,
        }
        for q in slow
    ]
    content = dump(payload, output_format)
    maybe_write(output_file, content)
    typer.echo(content)


@app.command("list-duplicate-queries", help="List all duplicate queries for the given trace id")
def list_duplicate_queries(
    log_file: str = typer.Argument(..., help=HELP_LOG_FILE),
    trace_ids: str = typer.Argument(..., help=HELP_TRACE_IDS),
    format: str = typer.Option(OutputFormat.TABLE.value, "--format", help=HELP_OUTPUT_FORMAT),
    output_file: Optional[str] = typer.Option(None, "--output-file", help=HELP_OUTPUT_FILE),
):
    result = parse_db_mode(log_file, trace_ids.split(","))
    dups = find_duplicate_queries(result.queries)
    output_format: OutputFormat = OutputFormat(format.lower())
    payload = [
        {"statement": stmt, "count": count}
        for stmt, count in sorted(dups, key=lambda x: (-x[1], x[0]))
    ]
    content = dump(payload, output_format)
    maybe_write(output_file, content)
    typer.echo(content)


if __name__ == "__main__":
    app()
    