# mk0.9.3 Review Inputs

This review package prepares evidence for external engineering review by AI agents. It does not make unsupported engineering approval claims.

## Included Artifacts

- Export copy: `revisions/mk0.9.3/review_package/exports/`
- Analysis CSV files: `revisions/mk0.9.3/review_package/analysis/`
- Manifest documents: `revisions/mk0.9.3/review_package/manifests/`
- Revision notes copy: `revisions/mk0.9.3/review_package/revision_notes/`
- Assembly overview: `revisions/mk0.9.3/review_package/ASSEMBLY_OVERVIEW.md`
- Requirements checklist: `revisions/mk0.9.3/review_package/REVIEW_REQUIREMENTS_CHECKLIST.md`

## CSV Meaning

- `part_dimensions.csv`: bounding boxes for STL and STEP exports where the file could be parsed.
- `printability_check.csv`: axis-aligned printable STL dimensions compared with configured Bambu Lab P2S volume and long-thin geometry flags.
- `plastic_estimate.csv`: mesh solid volume and PETG/PLA mass estimates from printable STL files.
- `stl_quality.csv`: STL triangle count plus watertight/manifold indicators from edge counting.
- `duplicate_geometry_check.csv`: geometry hash and near-duplicate grouping based on STL geometry, bounding box and volume.

## What Was Measured

- Generated STL bounding boxes.
- Generated STEP bounding boxes where CadQuery could import the STEP file.
- Printable STL mesh volume.
- STL edge-based watertight/manifold indicators.
- Duplicate and near-duplicate STL signatures.

## What Was Not Measured

- Mechanical strength, stiffness, fatigue or fastener pull-out.
- Thermal performance, airflow pressure drop or CFD.
- Slicer-specific print time, supports, infill, purge, seam placement or print orientation.
- Real-world assembly tolerance stack-up.
- Electrical safety or power-distribution validation.

## Known Limitations

- Mesh volume is not slicer material usage.
- Axis-aligned print-volume checks do not search for rotated fit.
- Long-thin geometry detection is a heuristic for review prioritization.
- STL watertight/manifold checks are based on exported mesh edges and may not identify every CAD modeling issue.
- Placeholder and review geometry are included for context but are not printable production parts.

## Generated Files

- `revisions/mk0.9.3/analysis/part_dimensions.csv`
- `revisions/mk0.9.3/analysis/printability_check.csv`
- `revisions/mk0.9.3/analysis/plastic_estimate.csv`
- `revisions/mk0.9.3/analysis/stl_quality.csv`
- `revisions/mk0.9.3/analysis/duplicate_geometry_check.csv`
- `revisions/mk0.9.3/PRINTABLE_PARTS.md`
- `revisions/mk0.9.3/NON_PRINTABLE_PARTS.md`
- `revisions/mk0.9.3/PLACEHOLDERS.md`
- `revisions/mk0.9.3/REVIEW_GEOMETRY.md`
- `revisions/mk0.9.3/review_package/REVIEW_REQUIREMENTS_CHECKLIST.md`
- `revisions/mk0.9.3/review_package/ASSEMBLY_OVERVIEW.md`