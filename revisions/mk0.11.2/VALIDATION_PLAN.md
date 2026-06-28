# mk0.11.2 Validation Plan

## Objective

Validate the stack-through-rod layer-cake prototype (`base_pedestal` +
`generic_stack_module` + `top_cap` + M5 rods) before any full tower
integration or reactivation of the deferred carriage/rail path.

---

## Step 1 — Syntax and compile check

**Command:**

```text
python -m compileall cad scripts
```

**Pass criterion:** No syntax errors.

**Status:** PASSED — `python -m compileall cad scripts` exit code 0.

---

## Step 2 — CadQuery geometry generation check

**Command:**

```python
from cad.parts.generic_stack_module import make_generic_stack_module
from cad.parts.base_pedestal import make_base_pedestal
from cad.parts.top_cap import make_top_cap
print(make_generic_stack_module().val().BoundingBox())
print(make_base_pedestal().val().BoundingBox())
print(make_top_cap().val().BoundingBox())
```

**Pass criterion:** Non-empty solids; stack module bbox approximately
190 × 190 × 70 mm (plus handle/pin allowances).

**Status:** PASSED — actual bbox: 191.7 × 194.0 × 74.0 mm (handle + alignment pins).

---

## Step 3 — Stack test assembly generation

**Command:**

```python
from cad.assembly.stack_test_assembly import build_stack_test_assembly
build_stack_test_assembly()
```

**Pass criterion:** No exceptions; contains `base_pedestal`,
`generic_stack_module`, `top_cap`, and four `m5_threaded_rod_*` references.
No carriage or rail components.

**Status:** PASSED — `stack_test_assembly_mk0112` built without exceptions.

---

## Step 4 — Selective STEP export

**Command:**

```text
python -m cad.export --revision mk0.11.2
```

**Pass criterion:** STEP/STL written for:

- `generic_stack_module`
- `base_pedestal`
- `top_cap`
- `stack_test_assembly`

Deferred mk0.11 carriage/rail parts must **not** appear in mk0.11.2 export.

**Status:** PASSED — 5 part exports + `assemblies/stack_test_assembly.step`; no deferred carriage/rail parts.

---

## Physical validation (after export)

### 1. Print `generic_stack_module`

Material: PLA prototype first, then PETG after geometry sign-off.

### 2. Check M5 rod alignment

Pass four M5 rods through corner post holes; verify alignment with
`ROD_CENTER_OFFSET` from `config.py`.

### 3. Check washer/compression pad fit

Verify M5 washer seats at top/bottom corner pads without binding.

### 4. Check top/bottom interface contact

Stack module rings mate cleanly with pedestal top and cap bottom interfaces
(alignment pins/sockets if printed).

### 5. Assemble base + module + top with rods

Build `stack_test_assembly` physically with nuts/washers at pedestal and cap.

### 6. Check stack stiffness by hand

Apply moderate lateral force at front handle; corner posts should not rack.

### 7. Check airflow opening continuity

Central opening unobstructed through module; no solid floor blocking path.

### 8. Check rear service zone clearance

Rear reserved depth ≥ 30 mm clear for future spine routing.

### 9. Check future carriage mounting zones

Side pads and M3 bosses accessible; no interference with rods, airflow, or rear zone.

### 10. Decide future side adapter / carriage path viability

Confirm reserved pad positions remain compatible with frozen U-channel rail
lateral offset without redesigning the stack module shell.

**Status:** Pending

---

## Go / No-Go for next revision

Proceed only if Steps 1–4 pass and physical checks 2, 4, 6, 7, 8, 9 pass.

If future carriage path (Step 10) fails, adjust `FUTURE_*` constants in
`config.py` only — do not implement active rails in mk0.11.2.

---

## Step 5 — Printability geometry review (added after visual inspection)

**Triggered by:** floating circular artifacts observed during visual review of
the exported `generic_stack_module` solid.

**Date:** 2026-06-28

**Findings and fixes applied:**

### Finding 1 — `_corner_rod_points` 4th point duplicated (CRITICAL)

**Files:** `generic_stack_module.py`, `base_pedestal.py`, `top_cap.py`

**Root cause:** 4th tuple was `(-x, -y)` — identical to the 1st point — instead
of `(-x, y)`.  Only 3 unique corner posts, M5 holes, and compression pad pockets
existed; the rear-left corner (x=−81, y=+81) was missing entirely.

**Fix:** Changed 4th point to `(-x, y)` in all three files.  Now all 4 corner
posts, all 4 M5 clearance holes, and all 8 compression pad pockets are present.

---

### Finding 2 — `_make_future_carriage_mount_zones` floating pads (CRITICAL)

**File:** `generic_stack_module.py`

**Root cause:** The translate formula used `sign * (x_rail + sign * pad_half_width)`
where `pad_half_width = FUTURE_CARRIAGE_PAD_WIDTH / 2 = 11 mm`.  This produced
asymmetric X positions: right pad at X=+95.5 mm (outside tower boundary at ±95 mm),
left pad at X=−73.5 mm (11 mm inside rail position).  The pad Z-span of 40 mm
was also centered at Z=0, leaving both pads disconnected from the top and bottom
frame rings (rings span only Z=−35 to −31 and Z=+31 to +35).

**Fix:** Simplified translate to `(sign * x_rail, y_center, 0.0)` and changed Z-span
from `FUTURE_CARRIAGE_PAD_VERTICAL_SPAN` (40 mm) to full module `height` (70 mm).
Pads now sit symmetrically at X=±84.5 mm, overlapping with both frame rings and
producing a single connected side strip.

---

### Finding 3 — `_make_future_side_adapter_mount_points` floating M3 bosses (PRIMARY "HANGING CIRCLES")

**File:** `generic_stack_module.py`

**Root cause:** Bosses were created on the `YZ` workplane and extruded in the +X
direction for both the left and right sides.  The X-face formula
`sign * (x_rail + sign * WALL/2)` produced positions incompatible with the
(already mis-positioned) carriage pads.  Result: cylindrical bosses completely
disconnected from any solid material, appearing as floating circles in all views.

**Fix:** Removed the call from `make_generic_stack_module_shell`.  Function body
kept as a DEFERRED reference with updated docstring explaining the connectivity
issue.  Reactivate only after carriage pad geometry is redesigned for full
connectivity.

---

### Finding 4 — `_make_internal_mount_grid_placeholder` floating circular pads (SECONDARY "HANGING CIRCLES")

**File:** `generic_stack_module.py`

**Root cause:** 4×3 grid of 6 mm-diameter circular standoff pads placed at
X=[−30,−10,+10,+30], Y=[−35,−15,+5] mm — all positions inside the 125×125 mm
central airflow opening.  No floor material exists in that zone, so all 12 pads
were disconnected islands after the airflow cut.

**Fix:** Removed the call from `make_generic_stack_module_shell`.  Function body
kept as a DEFERRED reference.  Reactivate only after introducing a floor or
bridging rib, or when replacing the generic shell with a device-specific module.

---

### Finding 5 — Front alignment pins floating inside airflow channel

**Files:** `generic_stack_module.py`, `base_pedestal.py`

**Root cause:** `module_interface.apply_module_interface_features` (with `top=True`)
adds alignment pins at positions (±57, ±61) on the top face.  The front pair
(Y=−61) falls inside the 125×125 mm airflow opening where the frame ring inner
cutout removed all material.  Pins at (±57, −61) had no solid surface beneath
them — they were unreachable floating cylinders.

**Fix:** Changed to `top=False` for both `make_generic_stack_module` and
`make_base_pedestal`.  Module-to-module alignment for mk0.11.2 is fully provided
by the four M5 corner rods.  Alignment pins can be reintroduced in a future
revision once the frame ring geometry provides a bearing surface at those positions
(e.g., by redesigning the inner cutout to spare pad areas at (±57, −61)).

---

### Printability review checklist

| Check | Result |
|---|---|
| Connected body — `generic_stack_module_shell` | PASS — 1 solid |
| Connected body — `generic_stack_module` | PASS — 1 solid |
| Connected body — `base_pedestal` | PASS — 1 solid |
| Connected body — `top_cap` | PASS — 1 solid |
| Floating island check | PASS — no floating islands after fixes |
| M5 hole check (4 unique corners) | PASS — 4 clearance holes at all corners |
| Compression pad pocket check | PASS — 8 pockets (top+bottom × 4 corners) |
| Airflow opening clear | PASS — central 125×125 mm channel open |
| Rear service zone clear | PASS — rear 30 mm reserved zone intact |
| Future carriage mounting zones integrated | PASS — full-height side strips connected to rings |
| No hanging carriage bosses | PASS — deferred, removed from printable part |
| No floating mount grid | PASS — deferred, removed from printable part |
| Export complete | PASS — 5 STEP parts + assembly exported |
| Render sanity | PASS — 7 views generated, no visible floating artifacts |

**Slicer preview required before print.**  Open `generic_stack_module.step` in
Bambu Studio or PrusaSlicer, verify:
- Single island in object list
- No unsupported circles or blobs inside airflow channel
- Supports only if needed for the front handle overhang (minor, on outer face)

**Expected print orientation:** bottom interface face (Z−) on the build plate,
Z+ up.  No mandatory supports for the frame rings or corner posts.  The front
handle lip protrudes 2 mm beyond the front face — may need a small brim or
first-layer adhesion check.

---

## Requirement verification checklist

Conducted: 2026-06-29.  Audited all 10 structural requirements against current
CAD state in `cad/parts/` (flat structure — no `cad/current/mk0.11.2/` path).

### Summary table

| Requirement | Status | Evidence | Risk | Next action |
|---|---|---|---|---|
| Stack-through-rod architecture | **PASS** | Non-sliding stackable layer; no rail pockets, POM-C sockets, or sliding geometry. Four M5 rods are explicit load path. | None. | None. |
| M5 through holes | **PASS** | 4× `ROD_CLEARANCE` (5.6 mm) holes through full bbox height at (±81, ±81) mm via `apply_module_interface_features`. All 4 unique corners verified in Step 5 fix. | Hardware clearance not yet physically tested. | Test with real M5 rod on first print. |
| Top/bottom interface | **PASS** | Top and bottom frame rings on all three stack parts (base/module/cap) use identical `_make_frame_ring` formula. Perimeter contact surface valid. Pin engagement disabled (top=False); M5 rod columns provide alignment. | Module-to-cap pin socket present but no mating pin — gap is intentional for mk0.11.2. | Physically verify ring-to-ring mating contact. |
| Compression pads around M5 rods | **PARTIAL** | Washer seat pockets at each corner post. `STACK_MODULE_COMPRESSION_PAD_DIAMETER` (12 mm) is 0.4 mm larger than `CORNER_POST_SIZE` (11.6 mm) — seat rim fractionally overlaps into ring material. | Minor: 0.4 mm overhang into ring is negligible for PETG compression load. Not a structural FAIL. | Physical test with M5 washer and modest torque. |
| Airflow opening | **PASS** | Central 125×125 mm vertical channel (`AIRFLOW_CHANNEL_WIDTH` × `AIRFLOW_CHANNEL_DEPTH`), full module height. No solid floor. Aligned with base intake and top exhaust clearance zones. | CFD/physical airflow not tested. | Verify visually with physical print. |
| Rear service zone | **PASS** | `REAR_RESERVED_DEPTH` = 30 mm zone explicitly preserved as open corridor. Ring rear cutout provides unobstructed channel at all stack levels. | No tie-slot or cable clip geometry yet. | Accept as open zone for mk0.11.2. |
| Future cable management reserve | **PARTIAL** | 30 mm rear open zone is the only cable management reserve. No tie-slot placeholders, no cable pass-through holes, no strain relief bosses in CAD. | Future routing relies on open zone without structured anchor points. | Add rear cable tie slots and/or anchor bosses in mk0.12 or device-specific module. |
| Future carriage mounting zones | **PARTIAL** | Full-height side pads at X = ±84.5 mm (`FUTURE_CARRIAGE_PAD_X_OFFSET`) integrated into top and bottom frame rings. Bottom adapter pads present at lower interface ring. M3 insert bosses deferred (floating island issue — Step 5, Finding 3). | Future adapter has solid material to fasten into but no pilot holes or heat-set boss geometry yet. | Redesign boss connectivity in mk0.12; reactivate `_make_future_side_adapter_mount_points` after fixing. |
| Device mounting placeholder | **FAIL** | Internal mount grid (`_make_internal_mount_grid_placeholder`) exists as a deferred function but is NOT called in the printable shell. All 12 pads would float in the airflow zone (Step 5, Finding 4). | Generic shell provides no internal device attachment. | Accepted deferral for mk0.11.2 structural shell. Reactivate after adding bridging rib/floor or in device-specific module. |
| Front handle / label placeholder | **PASS** | 64×4×12 mm pull lip at bottom-front (Y = −97 mm, Z spans −35 to −23 mm from module center). Clearly identifies front face. Protrudes 2 mm beyond tower front face — does not interfere with stack compression. | Minor first-layer adhesion concern (lip outside main footprint). | Check in slicer; add brim if needed. |
| Printability | **PASS** | Single connected solid confirmed post Step 5 fixes. 4 unique corner holes. 8 compression pad pockets (top + bottom × 4). Airflow channel open. No floating islands. | Slicer island/support check not yet performed in actual slicer. | Open `generic_stack_module.step` in Bambu Studio / PrusaSlicer before printing. |
| Config / no magic numbers | **PASS** | All geometry values reference named constants from `cad/config.py`. `rails` import decoupling fix applied (this audit): `FUTURE_CARRIAGE_PAD_X_OFFSET` added to `config.py`; `rails.u_channel_rail_x_offset()` calls replaced in `generic_stack_module.py`. | None remaining. | None. |
| Base / top compatibility | **PASS** | All three parts use identical `_corner_rod_points` formula: `TOWER_WIDTH/2 − ROD_CENTER_OFFSET`. Frame ring geometry identical across base/module/cap. Compression pad constants shared. | None. | Physical fit test with all three parts on rods. |
| Stack assembly clarity | **PASS** | `stack_test_assembly` shows base + 1 module + cap + 4 reference M5 rods. No carriage, rail, or POM-C components. Layer-cake structure unambiguous. Step 3 PASSED. | None. | None. |

### Future readiness assessment

**Future carriage / side adapter readiness:**
Physical material exists at X = ±84.5 mm (full-height side pads, width 2.4 mm).
Adapter can be bolted in after print by drilling pilot holes through the pad.
Heat-set insert boss geometry is deferred — reactivating it after pad redesign
is the recommended path.  No module redesign needed if `FUTURE_CARRIAGE_PAD_X_OFFSET`
remains frozen.  Constraint: M5 corner posts at X = ±81 mm must not interfere with
adapter fasteners — 3.5 mm clearance between post edge and pad center.

**Future cable management readiness:**
Rear 30 mm open corridor provides vertical cable routing space.
No structured tie points exist in mk0.11.2.  Adding rear cable tie slot features
to the frame ring rear wall is the next recommended step.  Bend radius is not
constrained by any geometry in the rear zone.

**Future airflow readiness:**
Central 125×125 mm opening preserved at all stack levels.  Base includes bottom
intake clearance zone; top cap includes exhaust clearance zone.
Bottom 120 mm fan and top 120 mm fan can be added without module redesign —
the 125 mm opening is larger than the fan air-opening diameter (112 mm).
Stack module creates no dead-air layer.

**Future multi-module scaling readiness:**
All three parts use the same ring/post formula from `config.py`.
A second `generic_stack_module` stacks identically.  M5 hole, airflow, rear zone,
and side pad positions repeat for every module.  Risk of module-unique geometry
is low; the only device-specific features (mount grid, device pads) are in
deferred functions that are not called in the shell.

---

### Remaining physical risks (not yet tested)

- M5 rod real clearance (5.6 mm) not tested against actual rod diameter
- M5 washer seat depth (1.8 mm) compression not tested
- PETG shrink / dimensional tolerance not tested
- Slicer island/support analysis not yet verified in actual slicer
- Airflow path continuity not physically tested
- Future carriage zone positions not validated against actual U-channel rail
