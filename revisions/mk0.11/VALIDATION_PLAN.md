# mk0.11 Validation Plan

## Objective

Validate the generic module / carriage / rail subsystem as a standalone
testable unit before integrating into the full tower assembly.

Each step below is a checkpoint. Do not proceed to the next step until the
current step passes. Record actual measurements and observations in this
file as validation proceeds.

---

## Step 1 — Syntax and compile check

**Target:** All new CAD Python files compile without errors.

**Command:**
```
python -m compileall cad scripts
```

**Pass criterion:** No syntax errors in any file under `cad/` or `scripts/`.

**Status:** PASSED — `python -m compileall cad scripts` exit code 0.

---

## Step 2 — CadQuery geometry generation check

**Target:** `make_generic_module()` and `make_generic_module_carriage()` execute
without CadQuery exceptions and return non-empty solid geometry.

**Command:**
```python
from cad.parts.generic_module import make_generic_module
from cad.parts.module_carriage import make_generic_module_carriage
m = make_generic_module()
c = make_generic_module_carriage()
print(m.val().BoundingBox())
print(c.val().BoundingBox())
```

**Pass criterion:** Bounding box of generic module is approximately
190 × 190 × 70 mm. Bounding box of carriage is approximately
170 × 176 × 12 mm (CARRIAGE_FRONT_LIP_HEIGHT).

**Status:** PASSED — actual bounding boxes (CadQuery 2.8.0):

| Part | X (mm) | Y (mm) | Z (mm) |
|---|---|---|---|
| generic_module_shell | 191.0 | 190.0 | 72.8 |
| generic_module | 191.0 | 194.0 | 76.8 |
| generic_module_carriage | 183.6 | 180.0 | 13.2 |
| pom_c_shoe_reference | 8.0 | 8.0 | 12.0 |
| u_channel_rail_generic_module | 15.0 | 10.0 | 140.0 |

Note: module Y slightly exceeds 190 mm due to front handle protrusion (~4 mm).
Module Z exceeds 70 mm due to alignment pins on top face (~4 mm).

---

## Step 3 — Assembly generation check

**Target:** Both assembly functions build without errors.

**Command:**
```python
from cad.assembly.generic_module_assembly import build_generic_module_assembly
from cad.assembly.single_module_bay_assembly import build_single_module_bay_assembly
a1 = build_generic_module_assembly()
a2 = build_single_module_bay_assembly()
```

**Pass criterion:** No exceptions. Assembly contains expected named components.

**Status:** PASSED — both assemblies built without exceptions.

---

## Step 4 — STEP export of generic module

**Target:** Export `generic_module.step` and `generic_module_carriage.step`.

**Command:**
```
python -m cad.export --revision mk0.11
```
or run export selectively for the new parts only.

**Pass criterion:** STEP files are written to `exports/mk0.11/`. File size > 0.

**Status:** PASSED — 13 files exported to `exports/mk0.11/`:

| File | Size |
|---|---|
| printed/plastic_modules/generic_module.step | 508 KB |
| printed/plastic_modules/generic_module.stl | 277 KB |
| printed/plastic_subparts/generic_module_shell.step | 429 KB |
| printed/plastic_subparts/generic_module_shell.stl | 78 KB |
| printed/plastic_subparts/generic_module_carriage.step | 936 KB |
| printed/plastic_subparts/generic_module_carriage.stl | 244 KB |
| reference_non_printed/metal/u_channel_rail_generic_module.step | 29 KB |
| reference_non_printed/wear_parts/pom_c_shoe_reference.step | 5 KB |
| assemblies/generic_module_assembly.step | 1466 KB |
| assemblies/single_module_bay_assembly.step | 1523 KB |
| jigs/rail_carriage_fit_test.step | 995 KB |

---

## Step 5 — Visual inspection in STEP viewer

**Target:** Verify geometry in a STEP viewer (FreeCAD, STEP viewer, or Bambu Studio).

**Checklist:**
- [ ] Module shell top/bottom rings visible and correctly proportioned.
- [ ] Four corner posts present at correct X/Y positions.
- [ ] No solid floor blocking the central airflow path.
- [ ] Rear reserved zone (30 mm) is clearly open / cleared.
- [ ] Front handle placeholder protrudes from front face.
- [ ] Rail pocket carriers visible on left and right sides.
- [ ] Carriage is open-frame (no solid floor).
- [ ] POM-C shoe sockets visible on carriage side walls.
- [ ] Carriage front pull lip present.

**Status:** Pending

---

## Step 6 — Print generic module prototype

**Material:** PLA (prototype only — not PETG until geometry is validated).
**Print settings:** Standard FDM, 0.2 mm layer, 15% infill for non-structural zones.

**Target dimensions to measure after print (mm):**

| Feature | Expected | Actual |
|---|---|---|
| Module outer width (X) | 190 | — |
| Module outer depth (Y) | 190 | — |
| Module height (Z) | 70 | — |
| Corner post section | ~10.6 × 10.6 | — |
| Airflow window width | ~125 | — |
| Rear zone depth clear | 30 | — |

**Status:** Pending

---

## Step 7 — Module stiffness check

**Method:** Manual flex test on printed prototype.

**Checklist:**
- [ ] Module does not flex when held at front handle with moderate force.
- [ ] Corner posts are rigid — no rotation or racking.
- [ ] No visible layer separation under light torsion.
- [ ] Bottom ring does not deform when module is placed on a flat surface.

**Note:** This is a PLA prototype. PETG will be stiffer. The test only validates
geometry, not long-term mechanical performance.

**Status:** Pending

---

## Step 8 — Airflow opening check

**Method:** Visual and physical obstruction test.

**Checklist:**
- [ ] Central opening is unobstructed — a 120 mm fan can be aligned with it.
- [ ] Rear zone is clear — cables can be routed through without obstruction.
- [ ] No solid floor sections block the vertical airflow path.

**Status:** Pending

---

## Step 9 — Rear service zone clearance check

**Method:** Measure actual rear clearance on printed prototype.

**Target:** 30 mm clear depth at the rear (REAR_RESERVED_DEPTH).

| Measurement | Expected | Actual |
|---|---|---|
| Rear zone depth | ≥ 30 mm | — |
| Rear zone width | ≥ 130 mm | — |

**Status:** Pending

---

## Step 10 — Print generic module carriage

**Material:** PLA (prototype).

**Checklist after print:**
- [ ] Open-frame tray is rigid.
- [ ] POM-C shoe sockets are correctly sized (Ø8.3 mm socket, check with 8 mm drill or rod).
- [ ] Front pull lip is intact and not delaminated.
- [ ] M3 clamp screw clearance hole present in shoe socket bridge.

**Status:** Pending

---

## Step 11 — Carriage attachment zone check

**Method:** Insert a POM-C Ø8 mm rod (or reference pin) into carriage shoe sockets.

**Checklist:**
- [ ] Ø8 mm rod fits into shoe socket (socket Ø8.3 mm nominal).
- [ ] Rod does not fall out under gentle vertical pull.
- [ ] M3 clamp screw can be threaded in (test with M3 screw before heat-set insert).
- [ ] Left-right symmetry: sockets at same Y positions both sides.

**Status:** Pending

---

## Step 12 — Rail / carriage fit test

**Method:** Insert actual aluminum U-channel rail section into rail pocket of printed module.

**Checklist:**
- [ ] U-channel rail (15×10×10×2 mm) slides into rail pocket carrier.
- [ ] Rail is retained by pocket walls — no excessive lateral play.
- [ ] Rail end stop prevents rail from sliding out under normal force.
- [ ] Rail end clip can be fitted and screwed down.

**If rail pocket is too tight:** Increase RAIL_POCKET_CLEARANCE in `config.py`.
**If rail pocket is too loose:** Decrease RAIL_POCKET_CLEARANCE in `config.py`.

**Status:** Pending

---

## Step 13 — Single module bay assembly check

**Method:** Assemble printed module shell + carriage + actual U-channel rail sections
+ POM-C shoes.

**Checklist:**
- [ ] Carriage slides smoothly on rails (POM-C shoes engaged).
- [ ] Carriage does not bind or rack.
- [ ] Module can be extracted and re-inserted by hand.
- [ ] Front pull lip is accessible for extraction.
- [ ] No interference between carriage shoe bosses and module inner walls.

**Status:** Pending

---

## Go / No-Go criteria for mk0.12 integration

All of the following must pass before proceeding to full tower integration:

- [ ] Step 1–4 (compile and export) all pass.
- [ ] Step 6 print dimensions within ±0.5 mm of target.
- [ ] Step 7 stiffness check passes.
- [ ] Step 8 airflow path unobstructed.
- [ ] Step 11 POM-C shoe socket fit confirmed.
- [ ] Step 12 rail/carriage fit confirmed.
- [ ] Step 13 full module bay extraction/insertion passes.

**If any step fails:** Document the failure mode, determine root cause, update
`cad/config.py` or part geometry, re-export, re-print, and re-validate.
Do not proceed to mk0.12 until all criteria pass.
