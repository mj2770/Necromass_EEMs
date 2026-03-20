from __future__ import annotations

from pathlib import Path
import json

from .eem_io import find_eem_exports, read_horiba_eem_table
from .features import build_feature_row, cluster_feature_table
from .metadata import load_metadata, summarize_metadata


def analyze_project(metadata_path: str | Path, eem_dir: str | Path, output_path: str | Path) -> dict:
    metadata_rows = load_metadata(metadata_path)
    metadata_summary = summarize_metadata(metadata_rows).to_dict()

    eem_files = find_eem_exports(eem_dir)
    feature_rows = []
    for eem_file in eem_files:
        eem, excitation, emission = read_horiba_eem_table(eem_file)
        feature_rows.append(build_feature_row(eem_file.stem, eem, excitation, emission))

    feature_table = None
    if feature_rows:
        feature_table = cluster_feature_table(feature_rows)

    output = {
        "metadata_summary": metadata_summary,
        "eem_file_count": len(eem_files),
        "feature_table": feature_table,
        "notes": [
            "PARAFAC-ready raw EEM exports must be placed in database/raw_data/eem_exports.",
            "Cluster labels are currently feature-based starter labels, not full PARAFAC cluster assignments.",
        ],
    }

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    return output
