from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import analyze_project
from .metadata import load_metadata, summarize_metadata
from .parafac_pipeline import run_parafac_ready_inventory


DEFAULT_METADATA = Path("database/raw_data/original_inputs/EEMs_metadata (1).csv")
DEFAULT_EEM_DIR = Path("database/raw_data/eem_exports")


def main() -> None:
    parser = argparse.ArgumentParser(description="necromass_EEMs command line interface")
    subparsers = parser.add_subparsers(dest="command", required=True)

    metadata_parser = subparsers.add_parser("metadata-summary", help="Summarize metadata file")
    metadata_parser.add_argument("--metadata", default=str(DEFAULT_METADATA))

    analyze_parser = subparsers.add_parser("analyze", help="Generate metadata and feature summary")
    analyze_parser.add_argument("--metadata", default=str(DEFAULT_METADATA))
    analyze_parser.add_argument("--eem-dir", default=str(DEFAULT_EEM_DIR))
    analyze_parser.add_argument("--output", default="database/processed/analysis_summary.json")

    inventory_parser = subparsers.add_parser("eem-inventory", help="Inspect raw EEM export tables")
    inventory_parser.add_argument("--eem-dir", default=str(DEFAULT_EEM_DIR))

    args = parser.parse_args()

    if args.command == "metadata-summary":
        df = load_metadata(args.metadata)
        print(summarize_metadata(df).to_json())
        return

    if args.command == "analyze":
        result = analyze_project(args.metadata, args.eem_dir, args.output)
        print(f"Wrote analysis summary to {args.output}")
        print(result["metadata_summary"])
        return

    if args.command == "eem-inventory":
        print(run_parafac_ready_inventory(args.eem_dir))
        return


if __name__ == "__main__":
    main()
