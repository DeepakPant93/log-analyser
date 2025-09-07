from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import List, Optional


class OutputFormat(Enum):
    """Output format options for the log analyzer."""
    TABLE = "table"
    JSON = "json"
    YAML = "yaml"


@dataclass
class DbQuery:
    timestamp: datetime
    trace_id: str
    statement: str
    duration_ms: float
    rows: int = -1
    is_error: bool = False


@dataclass
class TraceSummary:
    trace_id: str
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    total_duration: Optional[timedelta]
    total_queries: int
    total_slow_queries: int
    has_errors: bool
    duplicate_queries: int


@dataclass
class AnalysisResult:
    summaries: List[TraceSummary]
    queries: List[DbQuery]

