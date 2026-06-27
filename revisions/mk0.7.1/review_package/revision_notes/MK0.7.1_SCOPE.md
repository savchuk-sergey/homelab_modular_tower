# mk0.7.1 Scope

`mk0.7.1` is a patch revision after the mk0.7 engineering review. Its purpose is to improve review readiness, export safety, and low-risk CAD correctness without pretending to solve mk0.8-scale architecture problems.

## Included In mk0.7.1

| change | why included | risk closed | expected files/details | verification |
| --- | --- | --- | --- | --- |
| Ingest mk0.7 review findings into patch docs. | Required by review workflow. | Prevents losing blocker context. | `revisions/mk0.7.1/REVIEW_FINDINGS_INPUT.md`, scope and limitation docs. | File exists and references source review artifacts. |
| Create mk0.7.1 revision/export/render structure. | Patch revision must not rewrite mk0.7. | Keeps generated artifacts separate. | `revisions/mk0.7.1/`, `exports/mk0.7.1/`, `renders/mk0.7.1/`. | Paths exist; mk0.7 files unchanged by intent. |
| Update current working CAD revision label to `mk0.7.1`. | Generated artifacts must be signed as mk0.7.1. | Avoids mixing mk0.7 and mk0.7.1 outputs. | `cad/config.py`. | `python -m cad.export --revision mk0.7.1` accepts the revision. |
| Fix export category separation and manifests. | Review flags registry duplicates/missing categories and accidental-print risk. | Reduces chance of printing placeholders/non-printables. | `cad/exporters/part_registry.py`, manifest docs. | Export tree has `printable/plastic`, `printable/tpu`, `non_printable/metal_reference`, `placeholders/devices`, `placeholders/fans`, `review`, `assemblies`. |
| Fix broken duplicate geometry analysis. | 100 percent failure in mk0.7 review package. | Restores one automated quality gate. | `scripts/analysis/detect_duplicate_geometry.py`. | `duplicate_geometry_check.csv` is generated without attribute errors. |
| Fix `bottom_fan_cartridge` handle attachment. | Low-risk confirmed nonmanifold defect. | Makes the fan cartridge export more slicer-safe. | `cad/parts/cooling.py`. | `stl_quality.csv` no longer reports this printable part as nonmanifold if exporter succeeds. |
| Add/verify fan and Raspberry Pi 3B placeholders. | Requested by task and already mostly present. | Keeps reference geometry out of printable exports. | `cad/parts/placeholders.py`, assembly and manifests. | Fan placeholder is in `placeholders/fans`; Raspberry Pi 3B placeholder is in `placeholders/devices`. |
| Add top exhaust fan placeholder to assembly. | Review flags missing active exhaust reference. | Clarifies intended top fan stack without claiming thermal validation. | `cad/assembly/tower_assembly.py`. | Assembly export includes a top fan placeholder; printable exports do not. |
| Improve airflow review clarity. | Review flags blocked tray vents and sensor placement. | Makes review geometry show vertical path and central sensor markers. | `cad/parts/review.py`, config review constants. | Review geometry exports under `review/`. |
| Document printability blockers and deferred split redesign. | Oversized spine/power parts need bigger redesign. | Prevents unsafe production-print claims. | `KNOWN_LIMITATIONS.md`, `PRINTABLE_PARTS.md`. | Limitations list all unresolved P2S blockers. |

## Excluded From mk0.7.1

- Full tower architecture redesign.
- Complete Rear Service Spine redesign.
- Full anti-tip base redesign or tray interlock.
- Battery fire-containment enclosure.
- Final DC UPS electrical design, fusing, e-stop, or validated wire sizing.
- CFD, FEA, slicer validation, or physical test claims.
- Decorative changes.
- Risky segmentation of tall spine/power bus parts unless it can be done as an isolated future branch.

## Blockers Carried Into Scope

- `CAD-001`: bottom fan cartridge nonmanifold handle.
- `EXP-001`: duplicate geometry check tool failure.
- `EXP-002`: export taxonomy ambiguity and duplicate aliases.
- `AIR-002`: top exhaust fan placeholder missing from assembly.
- `DOC-001`: review findings and scope missing for patch revision.

## Blockers Deferred To mk0.8

- `STR-001`: dynamic tipping hazard.
- `PWR-001`: fuse/e-stop/power isolation design.
- `PWR-002`: battery containment and thermal safety.
- `AIR-001`: tray airflow redesign for devices blocking vent slots.
- `AIR-003`: Mini PC duct redesign against real device vents.
- `PRN-001` and `PRN-002`: segmentation of rear spine and long power-bus parts.
- `STR-002`: full guide rail retention architecture.
- `MOD-001`: true quick-disconnect service spine workflow.
