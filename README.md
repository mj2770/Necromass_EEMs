# necromass_EEMs

Local project scaffold for necromass-related Excitation Emission Matrix (EEM) workflows. This repository consolidates:

- SOPs and methodology notes from the original Word documents
- Python code for EEM metadata handling, feature extraction, and PARAFAC-oriented analysis
- A database-style folder preserving the currently available source files as raw inputs
- A `paper_mining` toolkit for extracting standards, spectral windows, and algorithm notes from EEM literature

## Current source inventory

This project was initialized from the files found in `/Users/mj2770/Documents/EEMs` on March 19, 2026:

- `EEMS analysis and methdology.docx`
- `SOP_Spectrofluorometer_MJ.docx`
- `EEMs_metadata (1).csv`
- `EEMs_metadata.xlsx`
- `k_parafac.py`
- `k_parafac_revised (1).py`
- `K-parafac.ipynb`
- `EEMs_files_metadata.ipynb`

Important note: the folder does not currently include the full exported raw EEM scan tables referenced by the legacy Colab scripts, such as `Data_*.csv`. The analysis package is ready for those files once they are added under [database/raw_data](/Users/mj2770/Documents/EEMs/necromass_EEMs/database/raw_data).

## Project layout

- [SOPs](/Users/mj2770/Documents/EEMs/necromass_EEMs/SOPs): cleaned SOP and methodology notes plus text conversions from the original `.docx` files
- [src/necromass_eems](/Users/mj2770/Documents/EEMs/necromass_EEMs/src/necromass_eems): reusable Python package for metadata parsing and EEM analysis
- [database](/Users/mj2770/Documents/EEMs/necromass_EEMs/database): raw and processed data storage
- [paper_mining](/Users/mj2770/Documents/EEMs/necromass_EEMs/paper_mining): scripts and seed references for mining papers about EEM standards, spectral regions, and algorithms
- [notebooks](/Users/mj2770/Documents/EEMs/necromass_EEMs/notebooks): preserved notebooks from the source folder
- [refs](/Users/mj2770/Documents/EEMs/necromass_EEMs/refs): curated reference notes and starter tables

## Quick start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=src python3 -m necromass_eems.cli metadata-summary
```

If you later add exported EEM scan tables:

```bash
PYTHONPATH=src python3 -m necromass_eems.cli analyze \
  --metadata database/raw_data/original_inputs/EEMs_metadata\ \(1\).csv \
  --eem-dir database/raw_data/eem_exports \
  --output database/processed/analysis_summary.json
```

## GitHub publishing

The repository has been scaffolded locally as `necromass_EEMs`. Creating the remote GitHub repository still requires GitHub access from this machine. If you want, the next step can be:

1. initialize git locally
2. create the GitHub repo named `necromass_EEMs`
3. push the first commit

## Immediate next data task

To make the PARAFAC workflow fully runnable, place the raw exported EEM sample tables into:

- [database/raw_data/eem_exports](/Users/mj2770/Documents/EEMs/necromass_EEMs/database/raw_data/eem_exports)

The code already expects Horiba-style exported EEM tables and will parse them once those files are present.
