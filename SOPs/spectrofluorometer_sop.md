# Spectrofluorometer SOP

## Instrument context

- Instrument: Horiba FluoroMax Plus spectrofluorometer
- Software: FluorEssence
- Detector range noted in source: 200 to 870 nm
- Typical EEM scan settings noted in source:
  - Excitation: 200 to 500 nm at 5 nm intervals
  - Emission: 250 to 600 nm at 5 nm intervals

## Sample preparation

1. Filter samples through 0.45 um or 0.2 um filters to reduce scattering artifacts.
2. Evaluate inner filter effect with UV-Vis absorbance across the EEM wavelength range.
3. Dilute samples when absorbance is high, especially near 240 nm.
4. Use the same cuvette type for absorbance and fluorescence measurements.

## Instrument checks

1. Turn on the instrument and confirm initialization succeeds.
2. Run the excitation monochromator calibration check.
3. Verify the xenon lamp peak is near 467 nm.
4. Run the emission calibration check using MilliQ water.
5. Verify the Raman peak is near 397 nm.

## EEM acquisition notes

1. Measure a blank before samples.
2. Run sample EEMs in 3D mode with the chosen excitation and emission ranges.
3. Apply Rayleigh masking or correction.
4. Perform blank subtraction.
5. Export both raw and corrected tables.
6. Record runtime in the instrument logbook.

## Cleaning

1. Rinse cuvettes three times with MilliQ water.
2. Soak with cuvette cleaning solution and MilliQ water for 5 minutes.
3. Rinse again three times with MilliQ water.
4. Clean the interior with lens paper.

## Standards and algorithm ideas from source notes

- Candidate standards:
  - glucosamine
  - muramic acid
  - alanine-related bacterial markers
  - protein standards
- Suggested analysis approaches:
  - PFFLR
  - PLD
  - MR-PLD
  - SOM

## Source file

Derived from [SOP_Spectrofluorometer_MJ.docx](/Users/mj2770/Documents/EEMs/necromass_EEMs/database/raw_data/original_inputs/SOP_Spectrofluorometer_MJ.docx) and mirrored in [spectrofluorometer_sop_source.txt](/Users/mj2770/Documents/EEMs/necromass_EEMs/SOPs/spectrofluorometer_sop_source.txt).
