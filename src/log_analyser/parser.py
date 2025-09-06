from __future__ import annotations

import re
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

from .models import AnalysisResult, DbQuery, TraceSummary

TIMESTAMP_REGEXPS = [
    # 2025-09-05 12:34:56,789
    (re.compile(r"(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}[,.]\d{3,6})"), "%Y-%m-%d %H:%M:%S,%f"),
    (re.compile(r"(?P<ts>\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}[,.]\d{3,6})"), "%Y-%m-%d %H:%M:%S.%f"),
]

# Hibernate SQL log patterns:
# DEBUG org.hibernate.SQL - select session0_.id as id1_34_...
# INFO org.hibernate.SQL_SLOW - SlowQuery: 3 milliseconds. SQL: 'com.mysql.cj.jdbc...'
DB_QUERY_REGEX = re.compile(
    r"DEBUG\s+org\.hibernate\.SQL\s+-\s+(?P<stmt>.+)$",
    re.IGNORECASE,
)

SLOW_QUERY_REGEX = re.compile(
    r"INFO\s+org\.hibernate\.SQL_SLOW\s+-\s+SlowQuery:\s+(?P<dur>[0-9.]+)\s+milliseconds\.\s+SQL:\s+'(?P<stmt>.+)'$",
    re.IGNORECASE,
)

ERROR_REGEX = re.compile(r"(ERROR|Exception|Traceback)", re.IGNORECASE)

# TraceId pattern: [traceId: 78fc5a08-b884-4a42-8478-5e166479f899]
TRACE_ID_REGEX = re.compile(r"\[traceId:\s+([\w-]+)\]", re.IGNORECASE)


def _extract_trace_id(line: str) -> str | None:
    """Extract traceId from log line."""
    match = TRACE_ID_REGEX.search(line)
    return match.group(1) if match else None


def _parse_timestamp(line: str) -> datetime | None:
    for pattern, fmt in TIMESTAMP_REGEXPS:
        m = pattern.search(line)
        if m:
            ts = m.group("ts").replace(",", ".")
            try:
                # Try both formats
                for f in {fmt, "%Y-%m-%d %H:%M:%S.%f"}:
                    try:
                        return datetime.strptime(ts, f)
                    except ValueError:
                        continue
            except Exception:
                return None
    return None


def parse_db_mode(log_file: str, trace_ids: List[str], slow_ms: float = 100.0) -> AnalysisResult:
    path = Path(log_file)
    if not path.exists():
        raise FileNotFoundError(f"Log file not found: {log_file}")

    queries: List[DbQuery] = []
    errors_by_trace: Dict[str, bool] = defaultdict(bool)
    target_traces = set(trace_ids)

    with path.open("r", encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            # Extract traceId from the line
            trace_id = _extract_trace_id(line)
            if not trace_id or trace_id not in target_traces:
                continue

            ts = _parse_timestamp(line)
            is_error = bool(ERROR_REGEX.search(line))
            if is_error:
                errors_by_trace[trace_id] = True

            # Check for regular SQL queries (DEBUG org.hibernate.SQL)
            db_match = DB_QUERY_REGEX.search(line)
            if db_match:
                stmt = db_match.group("stmt").strip()
                # For regular queries, we don't have duration info, so set to 0
                queries.append(
                    DbQuery(
                        timestamp=ts or datetime.min,
                        trace_id=trace_id,
                        statement=stmt,
                        duration_ms=0.0,
                        is_error=is_error,
                    )
                )
                continue

            # Check for slow queries (INFO org.hibernate.SQL_SLOW)
            slow_match = SLOW_QUERY_REGEX.search(line)
            if slow_match:
                duration_ms = float(slow_match.group("dur"))
                stmt = slow_match.group("stmt").strip()
                queries.append(
                    DbQuery(
                        timestamp=ts or datetime.min,
                        trace_id=trace_id,
                        statement=stmt,
                        duration_ms=duration_ms,
                        is_error=is_error,
                    )
                )

    summaries: List[TraceSummary] = []
    for tid in trace_ids:
        q = [x for x in queries if x.trace_id == tid]
        if q:
            start_time = min((x.timestamp for x in q if x.timestamp), default=None)
            end_time = max((x.timestamp for x in q if x.timestamp), default=None)
        else:
            start_time = None
            end_time = None

        total_duration = (end_time - start_time) if (start_time and end_time) else None
        total_queries = len(q)
        total_slow = sum(1 for x in q if x.duration_ms >= slow_ms)
        has_errors = bool(errors_by_trace.get(tid, False))

        # Duplicate detection by normalized statement text
        norm = [normalize_sql(x.statement) for x in q]
        counts = Counter(norm)
        duplicate_queries = sum(c for c in counts.values() if c > 1)

        summaries.append(
            TraceSummary(
                trace_id=tid,
                start_time=start_time.strftime("%Y-%m-%d %H:%M:%S") if start_time else None,
                end_time=end_time.strftime("%Y-%m-%d %H:%M:%S") if end_time else None,
                total_duration=total_duration,
                total_queries=total_queries,
                total_slow_queries=total_slow,
                has_errors=has_errors,
                duplicate_queries=duplicate_queries,
            )
        )

    return AnalysisResult(summaries=summaries, queries=queries)


_WS_MULTI = re.compile(r"\s+")
_NUMERIC = re.compile(r"\b\d+\b")


def normalize_sql(stmt: str) -> str:
    s = stmt.strip()            # 1. Remove leading/trailing whitespace
    s = _WS_MULTI.sub(" ", s)   # 2. Replace multiple spaces with a single space
    s = _NUMERIC.sub("?", s)    # 3. Replace numbers with ?
    return s.lower()            # 4. Convert to lowercase


def filter_queries_by_trace(queries: List[DbQuery], trace_ids: List[str]) -> List[DbQuery]:
    traces = set(trace_ids)
    return [q for q in queries if q.trace_id in traces]


def find_slow_queries(queries: List[DbQuery], slow_ms: float) -> List[DbQuery]:
    return [q for q in queries if q.duration_ms >= slow_ms]


def find_duplicate_queries(queries: List[DbQuery]) -> List[Tuple[str, int]]:
    counts = Counter(normalize_sql(q.statement) for q in queries)
    return [(stmt, count) for stmt, count in counts.items() if count > 1]
