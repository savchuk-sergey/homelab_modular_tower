# mk0.12 CAD Skeleton Notes

> NOTE:
> This is a legacy/historical CAD skeleton note.
> It is not the active CAD skeleton v3 status.
> The active source for mk0.12 CAD skeleton v3 input is the revision-scoped document set:
> `README.md`, `ENGINEERING_SPEC.md`, `PARTS_SPEC.md`, `INTERFACES.md`,
> `VALIDATION_GATES.md`, `PHYSICAL_TEST_PLAN.md`, `AGENT_RULES.md`, and `KNOWN_ISSUES.md`.
> Coupon parts remain BLOCKED until CAD skeleton v3 passes `VALIDATION_GATES.md`.

## Implemented

A legacy CAD skeleton snapshot for `mk0.12 MVP-2M stack-through-rod` was implemented in an earlier iteration.
This note is historical and must not be treated as active CAD skeleton v3 status.

Active stack order:

```text
base_pedestal:        Z 0..32
rpi_ssd_stack_module: Z 32..107
minipc_stack_module:  Z 107..212
top_cap:              Z 212..238
```

Historical CAD files from the legacy skeleton snapshot:

- `cad/parts/stack_interface.py`
- `cad/parts/base_pedestal.py`
- `cad/parts/module_rpi_ssd.py`
- `cad/parts/module_minipc.py`
- `cad/parts/top_cap.py`
- `cad/assembly/mvp_2_module_stack.py`

The assembly includes four non-printed M5 rod placeholders at `(+/-80, +/-80)`.

## Skeleton / Placeholder Scope

This is not final production CAD.  The model currently validates the stack footprint, M5 through-rod pattern, washer seats, compression-pad zones, fan-compatible base/top openings, rear service reserved zone, device envelopes, and basic Z alignment.

Device placeholders:

- Raspberry Pi 3B clearance envelope and board marker.
- External SSD preferred envelope at the active mk0.12 position.
- Mini PC physical placeholder and clearance outline.

Airflow is represented as distributed relief / bypass geometry.  The model intentionally does not create a mandatory empty `120 x 120` vertical shaft.

Fan-compatible openings use circular cutouts sized from `FAN_AIRFLOW_CUTOUT_DIAMETER_MAX`, preserving screw-boss material around the `105 x 105` fan pattern.

## Validation

Passed:

```text
python scripts/validate_mk012_spec.py
Summary: 0 FAIL, 5 PARTIAL, 11 PASS
```

CadQuery smoke-test passed in the project CadQuery environment:

```text
conda run -n cadquery python -c "from cad.assembly.mvp_2_module_stack import build_mvp_2_module_stack; build_mvp_2_module_stack(); print('OK')"
OK
```

## Remaining PARTIAL Items

The following risks remain intentionally open:

- PETG washer seat compression.
- Actual cable bend radius and real cable bundle thickness.
- Mini PC thermal behavior.
- Nut/tool access until physical/CAD access mock validation.
- Fan cutout / screw boss review until slicer review.
- SSD strap/rib final geometry.

## Intentionally Not Implemented

The skeleton does not implement:

- final ducts;
- decorative side panels;
- active rails;
- sliding carriage;
- POM-C shoe sockets;
- UPS module;
- MikroTik module;
- final cable-management spine;
- STEP/STL/PNG final exports.

## Print Status

Full print is not allowed for this revision state.

Superseded status: this legacy skeleton note is not sufficient for coupon parts or full print.
Current active status is defined by `README.md` and `VALIDATION_GATES.md`.
CAD skeleton v3 must still pass the revision-scoped validation gates before coupon parts.
