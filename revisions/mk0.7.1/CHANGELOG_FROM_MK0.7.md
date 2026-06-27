# mk0.7.1 Changelog From mk0.7

## Added

- Patch revision documentation under `revisions/mk0.7.1/`.
- Structured review finding ingestion in `REVIEW_FINDINGS_INPUT.md`.
- Patch scope definition in `MK0.7.1_SCOPE.md`.
- Separate export and render target folders for mk0.7.1.
- Manifests for printable, non-printable, placeholder, and review geometry.
- Self-check document for final patch verification.

## Changed

- Current working revision is intended to move from `mk0.7` to `mk0.7.1`.
- Export structure is intended to keep printable plastic, TPU, metal references, device placeholders, fan placeholders, review geometry, and assemblies separate.
- Analysis pipeline is intended to regenerate mk0.7.1 CSVs instead of reusing mk0.7 review outputs.

## Fixed

- Confirmed low-risk fixes are tracked in `MK0.7.1_SCOPE.md` and implemented in CAD/export/pipeline commits after this documentation layer.

## Not Changed

- Historical mk0.7 documentation remains unchanged.
- Major safety, electrical, anti-tip, full airflow, and print-splitting redesigns are deferred to mk0.8.
