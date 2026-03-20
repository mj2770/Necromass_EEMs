# Project seed notes

This file captures the highest-value project context pulled from the source folder during repository setup.

## Available dataset structure clues

- Metadata file contains 41 entries.
- Structured sample names include timepoints like `T5` and conditions such as `fresh` or `recyc`.
- Organism labels include `arthro`, `arthro1`, `pseudo`, and `pseudo1`.
- Oxygen labels include `aer` and `ana`.

## Legacy code state

- Existing PARAFAC scripts are exported from Google Colab.
- The scripts install dependencies inline and mount Google Drive.
- They expect raw files with names matching `Data_*.csv`.
- They already use starter EEM preprocessing and feature extraction ideas that were carried into this repository.

## Immediate curation needs

- Add actual raw Horiba EEM exports.
- Verify standard compounds and spectral ranges from literature.
- Decide whether the main modeling path should prioritize unified PARAFAC, K-method clustering, or both.
