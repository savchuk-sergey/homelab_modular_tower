# mk0.7.1 Changelog

## Added

- `revisions/mk0.7.1/REVIEW_FINDINGS_INPUT.md`
- `revisions/mk0.7.1/MK0.7.1_SCOPE.md`
- `revisions/mk0.7.1/analysis/*.csv`
- `revisions/mk0.7.1/review_package/mk0.7.1_review_package.zip`
- Pipeline wrapper scripts:
  - `scripts/export_revision.py`
  - `scripts/analyze_revision.py`
  - `scripts/package_review.py`
  - `scripts/run_revision_pipeline.py`

## Changed

- Current CAD revision label is `mk0.7.1`.
- Export categories separate plastic printable parts, TPU printable parts, metal references, placeholders, review geometry, and assembly output.
- Fan placeholder includes a non-printable airflow direction marker.
- Assembly includes both bottom and top fan placeholders.
- Airflow review markers use named constants and central temperature marker positions.

## Fixed

- `bottom_fan_cartridge` exports as a connected watertight/manifold printable STL.
- Duplicate geometry check uses the configured cubic-mm tolerance name.
- Power bus cover holes align with the power bus panel screw offset.
- Fan grille Z placement no longer uses the mk0.7 overlapping offsets.

## Deferred

- Full airflow redesign around blocked tray vents.
- Spine and power-bus split-joint redesign for P2S.
- Anti-tip, battery safety, fusing/e-stop, and real electrical validation.
- Rail fastening and true quick-disconnect service-spine architecture.
