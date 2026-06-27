# Homelab Modular Tower mk0.7.1 Revision Notes

## Purpose

`mk0.7.1` is a patch revision based on the mk0.7 engineering review. It focuses on review ingestion, export organization, placeholder separation, airflow review clarity, and restoring the analysis/package pipeline.

## Engineering Position

This revision is not a GO for full build. It does not claim CFD, FEA, slicer validation, or physical testing. Safety and architecture blockers from mk0.7 remain documented when they are too large for a patch release.

## Patch Goals

- Preserve mk0.7 history.
- Generate mk0.7.1 artifacts under separate revision paths.
- Fix low-risk confirmed CAD/export defects.
- Keep printable, non-printable, placeholder, review, and assembly geometry separated.
- Produce a review package suitable for the next engineering review pass.

## Verification Target

The expected verification path is:

```text
python -m cad.export --revision mk0.7.1
python scripts/analysis/generate_review_package.py --revision mk0.7.1
```

Generated CSV files and the review package are evidence for review only. They are not manufacturing approval.
