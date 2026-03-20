# EEM Analysis Methodology Notes

## Main themes captured from source notes

- Preprocessing choices strongly affect EEM interpretation.
- Inner filter effect correction should be documented and, when possible, absorbance-based.
- Rayleigh and Raman masking parameters should stay tied to actual instrument settings.
- Unified PARAFAC and cluster-specific PARAFAC both matter for this dataset.
- Low concentration and overlapping fluorophores are expected challenges.

## Working analysis workflow

1. Read Horiba-style exported EEM tables into a sample-by-excitation-by-emission array.
2. Apply scatter handling and wavelength trimming.
3. Extract simple features such as peak intensities and regional integrations.
4. Fit a unified PARAFAC model.
5. Optionally fit cluster-specific models using a K-method style workflow.
6. Compare Fmax, reconstruction error, and cluster stability.

## Open technical questions preserved from notes

- Was inner filter effect corrected using absorbance-based methods for all samples?
- Where are the missing standards and timepoint files?
- Which spectral regions are most defensible for bacterial, protein-like, and humic-like features in this dataset?
- Should quenching be incorporated as an explicit factor in the clustering workflow?

## Seed spectral windows mentioned in notes

- Peak target around Ex 350 / Em 450
- Regional integration example around Ex 250 to 300 / Em 380 to 450
- Bacteria-like region from paper notes around Ex 250 to 350 / Em 310 to 370

## Source file

Derived from [EEMS analysis and methdology.docx](/Users/mj2770/Documents/EEMs/necromass_EEMs/database/raw_data/original_inputs/EEMS%20analysis%20and%20methdology.docx) and mirrored in [analysis_methodology_source.txt](/Users/mj2770/Documents/EEMs/necromass_EEMs/SOPs/analysis_methodology_source.txt).
