# Paper Mining

This folder is for building a literature-backed reference system around EEM standards, spectral windows, and algorithms.

## Included assets

- [extract_paper_insights.py](/Users/mj2770/Documents/EEMs/necromass_EEMs/paper_mining/extract_paper_insights.py): parse local files, DOI lists, or URLs and extract likely standards, wavelength windows, algorithm mentions, and citation hints
- [seed_topics.md](/Users/mj2770/Documents/EEMs/necromass_EEMs/paper_mining/seed_topics.md): starter topics collected from the current project notes
- [standards_reference.csv](/Users/mj2770/Documents/EEMs/necromass_EEMs/paper_mining/standards_reference.csv): living table for EEM standards and spectral references

## Example

Run on a local paper or note file:

```bash
python3 paper_mining/extract_paper_insights.py \
  --input /path/to/paper.pdf \
  --output database/processed/paper_insights.json \
  --table-output database/processed/paper_insights.csv
```

Run on a DOI or URL list file with one entry per line:

```bash
python3 paper_mining/extract_paper_insights.py \
  --input-list paper_mining/doi_or_url_list.txt \
  --output database/processed/literature_summary.json \
  --table-output database/processed/literature_summary.csv
```

Supported `--input` values:

- local `.txt`, `.md`, `.pdf`, and other readable files
- a `.txt`, `.md`, or `.csv` list file passed with `--input-list`, containing one local path, DOI, or URL per line
- direct DOI values like `10.1016/j.watres.2024.123456`
- direct URLs like `https://doi.org/...` or a paper landing page

Outputs:

- JSON with one summary per source plus unique combined algorithms, standards, and citation hints
- CSV table with one row per source-window match, ready to inspect in Excel

This script is heuristic by design. It gives you a structured first pass to review, not a final literature judgment.
