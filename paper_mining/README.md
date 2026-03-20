# Paper Mining

This folder is for building a literature-backed reference system around EEM standards, spectral windows, and algorithms.

## Included assets

- [extract_paper_insights.py](/Users/mj2770/Documents/EEMs/necromass_EEMs/paper_mining/extract_paper_insights.py): parse text or PDF papers and extract likely standards, wavelength windows, and algorithm mentions
- [seed_topics.md](/Users/mj2770/Documents/EEMs/necromass_EEMs/paper_mining/seed_topics.md): starter topics collected from the current project notes
- [standards_reference.csv](/Users/mj2770/Documents/EEMs/necromass_EEMs/paper_mining/standards_reference.csv): living table for EEM standards and spectral references

## Example

```bash
python3 paper_mining/extract_paper_insights.py \
  --input /path/to/paper.pdf \
  --output database/processed/paper_insights.json
```

This script is heuristic by design. It gives you a structured first pass to review, not a final literature judgment.
