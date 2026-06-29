# mk0.12 - Known Issues

Revision: mk0.12  
Architecture: MVP-2M stack-through-rod  
Status: HISTORICAL FAILURES AND RISKS FOR CAD SKELETON V3  

Related documents:
- README.md
- ENGINEERING_SPEC.md
- PARTS_SPEC.md
- INTERFACES.md
- VALIDATION_GATES.md
- PHYSICAL_TEST_PLAN.md
- AGENT_RULES.md
- KNOWN_ISSUES.md

## Historical CAD Skeleton v2 Failures

`v2` references in this document are historical previous failures only. They are not active future implementation names.

- Previous CAD skeleton v2 expanded printable parts to approximately 205 x 205 mm.
- `minipc_stack_module` exceeded the footprint in Y.
- Outward ribs/tabs appeared from M5 rod guide/compression islands.
- Some ribs looked hanging, floating, or unfinished.
- Rib structure looked automatically generated and not load-path-aware.
- There was no guarantee that every rib had two valid endpoints.
- `rpi_ssd_stack_module` was not watertight.
- Coupon parts were blocked.
- Kilogram-scale or near-solid skeleton behavior was a design failure.

## Risks Not To Repeat

- Fan zone interpreted as a full 120 x 120 square cutout.
- Distributed airflow interpreted as a required empty center shaft.
- Rear service represented only as annotation.
- Airflow represented only as annotation.
- Reference geometry included in printable STL.
- TPU feet merged into PETG `base_pedestal` STL.
- Active PETG features protruding outside the frozen footprint.
- M5 compression island ribs generated radially in all directions.
- Rib endpoints connected only to reference geometry.
- Cable, airflow, rear service, mounting, retainer, or tool access blocked by ribs.

## Current Blocking Status

```text
COUPON PARTS: BLOCKED until CAD skeleton v3 passes validation.
FULL PRINT: BLOCKED until CAD skeleton v3 and physical validation pass.
NEXT STEP: mk0.12 CAD skeleton cleanup v3
```
