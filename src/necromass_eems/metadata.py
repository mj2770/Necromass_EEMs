from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import csv
import json
import re


SAMPLE_PATTERN = re.compile(
    r"^Data_BlankSub_Graph_S1_(?P<timepoint>[^_]+)_(?P<treatment>[^_]+)_(?P<organism>[^_]+)(?:_(?P<oxygen>[^_]+))?$",
    re.IGNORECASE,
)


@dataclass
class MetadataSummary:
    sample_count: int
    controls_count: int
    timepoints: list[str]
    treatments: list[str]
    organisms: list[str]
    oxygen_conditions: list[str]

    def to_dict(self) -> dict:
        return {
            "sample_count": self.sample_count,
            "controls_count": self.controls_count,
            "timepoints": self.timepoints,
            "treatments": self.treatments,
            "organisms": self.organisms,
            "oxygen_conditions": self.oxygen_conditions,
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)


def _normalize_token(value: str | None) -> str | None:
    if value is None:
        return None
    cleaned = value.strip().lower()
    return cleaned or None


def parse_sample_name(name: str) -> dict:
    match = SAMPLE_PATTERN.match(name.strip())
    if not match:
        return {
            "sample_name": name,
            "is_structured_sample": False,
            "timepoint": None,
            "treatment": None,
            "organism": None,
            "oxygen": None,
            "is_control": True,
        }

    values = {key: _normalize_token(value) for key, value in match.groupdict().items()}
    return {
        "sample_name": name,
        "is_structured_sample": True,
        "timepoint": values["timepoint"],
        "treatment": values["treatment"],
        "organism": values["organism"],
        "oxygen": values["oxygen"],
        "is_control": False,
    }


def load_metadata(metadata_path: str | Path) -> list[dict]:
    metadata_path = Path(metadata_path)
    rows: list[dict] = []
    with metadata_path.open(newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            rows.append({**row, **parse_sample_name(row["name"])})
    return rows


def summarize_metadata(rows: list[dict]) -> MetadataSummary:
    sample_rows = [row for row in rows if row["is_structured_sample"]]
    controls_count = len(rows) - len(sample_rows)

    def unique_clean(key: str) -> list[str]:
        values = {row[key] for row in sample_rows if row.get(key)}
        return sorted(values, key=str.lower)

    return MetadataSummary(
        sample_count=len(sample_rows),
        controls_count=controls_count,
        timepoints=unique_clean("timepoint"),
        treatments=unique_clean("treatment"),
        organisms=unique_clean("organism"),
        oxygen_conditions=unique_clean("oxygen"),
    )
