# mk0.7.3 Revision

## Purpose

mk0.7.3 is a rough assembly platform revision. Its purpose is to make the tower mechanically coherent enough for targeted fit-test prints and a rough mockup assembly.

This revision is not a finished product release. Final component dimensions, final connector geometry, UPS/battery containment, thermal validation, and production cable routing are deferred to mk1.0.

## Scope

- Fix physically impossible structural placement introduced in mk0.7.1.
- Make the M5 rod, frame, and corner-block stack assemble in a plausible order.
- Add real rough mounting interfaces for side panels, guide rails, tray support, and feet.
- Improve bottom fan cartridge service features enough for fit testing.
- Split oversized rear-service and power-bus parts into printable sections.
- Keep power, UPS, connector, and device geometry as explicit placeholder envelopes.

## Non-Goals

- Final power bus design.
- Final UPS or battery package.
- Final Mini PC duct.
- Final connector selection.
- Full thermal validation.
- Full production BOM.
- Full prototype readiness.

## Target Outcome

The expected verdict after mk0.7.3 is at most `GO FOR PARTIAL TEST PRINT` for critical subassemblies:

- frame corner plus corner block,
- side panel mount,
- rail support and tray edge,
- foot socket and base section,
- fan cartridge handle and filter retention,
- split rear-spine joint.

## Verification Summary

The mk0.7.3 pipeline was generated with:

```text
conda run -n cadquery python scripts/run_revision_pipeline.py --revision mk0.7.3
```

The pipeline completed successfully. Analysis outputs are stored under `revisions/mk0.7.3/analysis/`, and the review package is stored under `revisions/mk0.7.3/review_package/`.
