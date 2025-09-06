from __future__ import annotations

import json
from dataclasses import asdict, is_dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any, List, Sequence

import yaml
from tabulate import tabulate

from log_analyser.models import OutputFormat


def _serialize(obj: Any) -> Any:
    if is_dataclass(obj):
        return {k: _serialize(v) for k, v in asdict(obj).items()}
    if isinstance(obj, datetime):
        return obj.isoformat()
    if isinstance(obj, timedelta):
        return obj.total_seconds()
    if isinstance(obj, (list, tuple)):
        return [_serialize(x) for x in obj]
    return obj


def dump(data: Any, fmt: OutputFormat = OutputFormat.TABLE, headers: Sequence[str] | None = None) -> str:
    fmt = fmt.value.lower()
    if fmt == OutputFormat.JSON.value:
        return json.dumps(_serialize(data), indent=2, ensure_ascii=False)
    if fmt == OutputFormat.YAML.value:
        return yaml.safe_dump(_serialize(data), sort_keys=False, allow_unicode=True)

    # table default
    rows: List[List[Any]]
    if isinstance(data, list):
        if not data:
            return "(no results)"
        first = data[0]
        if isinstance(first, dict):
            headers = headers or list(first.keys())
            rows = [[_serialize(item.get(h)) for h in headers] for item in data]
        else:
            # assume list of dataclasses or simple objects
            if hasattr(first, "__dataclass_fields__"):
                headers = headers or list(first.__dataclass_fields__.keys())
                rows = [[_serialize(getattr(item, h)) for h in headers] for item in data]
            else:
                rows = [[_serialize(item)] for item in data]
                headers = headers or ["value"]
    else:
        # single object
        d = _serialize(data)
        if isinstance(d, dict):
            headers = ["field", "value"]
            rows = [[k, v] for k, v in d.items()]
        else:
            headers = ["value"]
            rows = [[d]]

    return tabulate(rows, headers=headers, tablefmt="github")


def maybe_write(output: str | None, content: str) -> None:
    if output:
        Path(output).write_text(content, encoding="utf-8")

