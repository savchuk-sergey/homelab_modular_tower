# mk0.11.2 — Stack-Through-Rod Architecture

## Scope

mk0.11.2 corrects the ambiguous carriage/module direction from mk0.11 and
mk0.11.1.  The first physical prototype is a **layer-cake stack** compressed
by four M5 through-rods — not a sliding carriage prototype.

### Active architecture

```text
base_pedestal
  + generic_stack_module(s)
  + top_cap
  -> compressed by 4x M5 through-rods
```

Stack modules are printable PETG layers with:

- top/bottom interface rings and alignment features;
- M5 pass-through holes at corner posts;
- local washer compression pad zones;
- central vertical airflow opening;
- rear service reserved zone;
- internal device mounting placeholder grid;
- front handle / label zone placeholder;
- **future** carriage / side-adapter mounting zones (pads + M3 bosses only).

Primary validation assembly: `stack_test_assembly`.

### Deferred architecture

Sliding open-frame carriage on aluminum U-channel rails with POM-C shoes.
Source code is preserved under `cad/deferred/` and original part paths.
Not exported or validated as part of mk0.11.2.

---

## CAD targets (mk0.11.2)

| Target | Source |
|---|---|
| `generic_stack_module` | `cad/parts/generic_stack_module.py` |
| `base_pedestal` | `cad/parts/base_pedestal.py` |
| `top_cap` | `cad/parts/top_cap.py` |
| `stack_test_assembly` | `cad/assembly/stack_test_assembly.py` |

Export:

```text
python -m cad.export --revision mk0.11.2
```

---

## Out of scope

- Full tower CAD integration
- Active carriage, rails, or POM-C shoe sockets in stack modules
- UPS / router / Mini PC module finalization
- Rear Service Spine revision
- Changes to the frozen U-channel rail standard
- Solid floors blocking vertical airflow

---

## Relationship to prior mk0.11.x work

| Revision | Status |
|---|---|
| mk0.11 | Subsystem-first workflow; carriage/rail generic module — **superseded for active prototype** |
| mk0.11.1 | Branch work toward carriage validation — **not active in mk0.11.2** |
| mk0.11.2 | **Active**: stack-through-rod prototype with future adapter reserve |

Historical mk0.11 files (`generic_module.py`, `module_carriage.py`, bay
assemblies, fit jig) are **not deleted**.  They are marked deferred in
`cad/deferred/README.md`.

---

## Frozen decisions inherited

Same as mk0.11 / mk0.9.3 where not explicitly changed:

- CadQuery source in `cad/` is the source of truth
- M5 rods are the primary vertical load path
- PETG is connector/positioner, not sole load bearer
- Rear service zone: 30 mm reserved
- Vertical airflow: bottom intake / top exhaust concept
- All dimensions in `cad/config.py`

---

## Status

Working revision.  CAD compile and selective export are the first validation
gates.  Physical print validation follows `VALIDATION_PLAN.md`.
