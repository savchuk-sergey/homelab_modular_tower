# Homelab Modular Tower mk0.7.1

## Summary

`mk0.7.1` is a patch revision after the mk0.7 engineering review. It improves export separation, placeholder clarity, airflow review evidence, and the automated analysis/review package pipeline.

## Status

Conditional review package only. This revision is not approved for a full physical build.

## Main Changes

- mk0.7 review findings were consolidated into patch scope documentation.
- Generated artifacts now target `exports/mk0.7.1/` and `revisions/mk0.7.1/`.
- Printable plastic, TPU, metal references, device placeholders, fan placeholders, review geometry, and assemblies are separated.
- `bottom_fan_cartridge` was adjusted to export as a connected printable body.
- Top fan placeholder and central airflow review markers were added/clarified.
- Duplicate geometry analysis was repaired.
- mk0.7.1 review package ZIP was generated.

## Evidence Boundary

No CFD, FEA, slicer validation, electrical validation, or physical testing was performed.
