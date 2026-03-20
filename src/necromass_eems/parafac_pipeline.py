from __future__ import annotations

from pathlib import Path

from .eem_io import find_eem_exports, read_horiba_eem_table


def run_parafac_ready_inventory(eem_dir: str | Path) -> dict:
    eem_files = find_eem_exports(eem_dir)
    shapes = []
    for eem_file in eem_files:
        eem, excitation, emission = read_horiba_eem_table(eem_file)
        shapes.append(
            {
                "file": eem_file.name,
                "eem_shape": list(eem.shape),
                "excitation_points": int(len(excitation)),
                "emission_points": int(len(emission)),
            }
        )
    return {"file_count": len(eem_files), "files": shapes}


def notes() -> str:
    return (
        "This project includes starter local code for EEM ingestion and feature analysis. "
        "A full eem-python PARAFAC execution layer can be added once raw export tables are available."
    )
