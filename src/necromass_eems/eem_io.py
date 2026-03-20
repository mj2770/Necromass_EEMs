from __future__ import annotations

from pathlib import Path
import csv


def read_horiba_eem_table(file_path: str | Path) -> tuple[list[list[float]], list[float], list[float]]:
    file_path = Path(file_path)
    with file_path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))

    excitation = [float(value) for value in rows[0][1:] if value.strip()]
    emission: list[float] = []
    values_by_emission: list[list[float]] = []

    for row in rows[2:]:
        if not row or not row[0].strip():
            continue
        emission.append(float(row[0]))
        values_by_emission.append([float(value or 0.0) for value in row[1:1 + len(excitation)]])

    values_by_excitation = [list(column) for column in zip(*values_by_emission)]
    return values_by_excitation, excitation, emission


def find_eem_exports(eem_dir: str | Path) -> list[Path]:
    eem_dir = Path(eem_dir)
    if not eem_dir.exists():
        return []
    return sorted(eem_dir.glob("Data_*.csv"))
