# mk0.9.2 - Rail/carriage implementation fix

## Summary

`mk0.9.2` is a corrective CAD revision based on
`reviews/mk0.9.1/kimi_implementation_review.md`.

The revision keeps the mk0.9.1 module scope:

- base module;
- Raspberry Pi 3B + external SSD module;
- Mini PC placeholder module;
- roof module.

It does not implement final power distribution, router, UPS, full Rear Service
Spine, or final Mini PC tray/duct geometry.

## Confirmed changes

- `CURRENT_REVISION` is now `mk0.9.2`.
- The POM-C shoe clamp no longer uses the failing chamfer operation.
- The clamp now includes an explicit PETG heat-set insert boss volume.
- New rail/carriage dimensions were moved into `cad/config.py`.
- Active RPi/SSD and Mini PC placeholder module shells include printable
  U-channel rail pocket carriers and rail end stops.
- Aluminum U-channel rails and POM-C shoes remain exported as non-printed or
  placeholder artifacts, not printable plastic parts.
- The empty stray `revisionsmk0.9.1/` directory was removed.

## Verification

Passed on 2026-06-28:

- `python -m compileall cad scripts`
- targeted CadQuery build of both carriage factories
- targeted CadQuery build of `build_assembly()`
- `conda run -n cadquery python scripts/export_revision.py --revision mk0.9.2`
- `conda run -n cadquery python scripts/run_revision_pipeline.py --revision mk0.9.2`
- `conda run -n cadquery python scripts/render_views.py --out renders\mk0.9.2 --mode views --target all --revision mk0.9.2 --size 1200 --tolerance 2.0`

Generated evidence:

- `exports/mk0.9.2/`
- `renders/mk0.9.2/`
- `revisions/mk0.9.2/analysis/`
- `revisions/mk0.9.2/review_package/`

## Engineering status

`mk0.9.2` is a buildable and exportable corrective iteration. It is suitable
for external engineering review and partial fit/print planning, but it is not
a final print approval.
