# mk0.7.4 Iteration Plan

## Purpose

mk0.7.4 is a draft print-readiness revision based on the mk0.7.3 Kimi Agents Swarm review.

The goal is not to turn the tower into a final product. The goal is to move from:

```text
mk0.7.3 verdict: GO FOR COUPON TEST PRINT ONLY
```

to:

```text
mk0.7.4 target verdict: GO FOR ROUGH MOCKUP PRINT
```

This requires resolving all confirmed geometry blockers, closing the highest-risk assembly gaps, reducing waste for the rough mockup, and producing enough documentation for a human to print and assemble the draft without reverse-engineering the Python assembly.

## Source Review

Primary review artifacts:

- `reviews/mk0.7.3/kimi_swarm_rough_print_review.md`
- `reviews/mk0.7.3/kimi_swarm_findings.csv`
- `reviews/mk0.7.3/kimi_swarm_unknowns.md`
- `reviews/mk0.7.3/kimi_swarm_action_plan.md`

## Scope

mk0.7.4 should fix or explicitly close:

- confirmed BLOCKER findings: `MA-003`, `MA-004`;
- confirmed or likely HIGH mechanical assembly findings: `ASM-001`, `ASM-002`, `MA-002`, rail-end-mount screw target;
- rough-print blockers caused by missing BOM and missing assembly order: `RAP-004`, `RAP-007`, `RAP-008`;
- first-print waste risks: `PE-001`, `PE-002`, `PE-003`, `PE-004`, `PE-005`, `PE-008`, `PE-009`;
- print-orientation risks that can be handled with documentation and coupons: `PRINT-004`, `PRINT-005`, `PRINT-007`, `PRINT-011`, `PRINT-019`;
- fit risks that must be validated before full mockup print: `RAP-002`, `RAP-003`, `RAP-005`, `RAP-009`, `RAP-011`.

## Non-Goals

These stay out of mk0.7.4 unless a change is required to preserve rough mockup assembly:

- final Mini PC duct geometry against real device ports;
- final MikroTik, Raspberry Pi, UPS, SSD, battery, and connector measurements;
- final power bus electrical design;
- fuse values, wire gauge, DC current sizing, and electrical safety review;
- CFD, thermal measurement, smoke testing, or production cooling validation;
- final side-panel shear-transfer architecture;
- final production BOM.

## Iteration Gates

Each chunk must end with one of these states:

- `PASS`: changes are implemented and verified enough to continue.
- `PASS WITH COUPON REQUIRED`: CAD is coherent, but physical validation is still needed before full print.
- `BLOCKED`: do not proceed until the issue is resolved.

Do not batch unrelated geometry fixes into the same commit. The safest rhythm is one mechanical interface per patch, then export or targeted inspection.

## Chunk 0 - Revision Setup

### Goal

Create a clean mk0.7.4 working revision without rewriting mk0.7.3 history.

### Work

- Create a branch for the revision, for example `cad/mk0.7.4`.
- Update `cad/config.py` `CURRENT_REVISION` from `mk0.7.3` to `mk0.7.4`.
- Create `revisions/mk0.7.4/` documentation files:
  - `REVISION.md`
  - `CALCULATIONS.md`
  - `DECISIONS.md`
  - `KNOWN_ISSUES.md`
  - `CHANGELOG.md`
  - `ITERATION_PLAN.md`
  - later: `ASSEMBLY_SEQUENCE.md`, `FASTENER_BOM.md`, `PRINT_PLAN.md`, `COUPON_TEST_PLAN.md`

### Exit Criteria

- `mk0.7.4` docs exist.
- No CAD geometry changes yet.
- Pipeline still refuses wrong revision and accepts the current configured revision.

## Chunk 1 - Impossible Geometry Blockers

### Findings

- `MA-003`: split-joint tabs overlap.
- `MA-004`: bottom filter retainer clips are detached.

### Work

1. In `cad/parts/service_spine.py`, redesign `_split_section()` so lower/upper split parts do not both carry occupying tabs at the same joint volume.
   - Preferred direction: lower segment has the positive alignment tab; upper segment has a matching recess or socket.
   - Apply consistently to rear spine, spine cover, power bus panel, and power bus cover split exports.
   - Keep all tab, slot, screw, and clearance dimensions parameterized in `cad/config.py`.

2. In `cad/parts/cooling.py`, redesign `bottom_filter_retainer`.
   - The clips must be physically connected to the retainer body.
   - Prefer a simple printable retainer geometry over a fragile snap-fit.
   - If clip flexibility is still unproven, document it as coupon-required, not print-ready.

### Verification

- Export affected parts.
- Confirm affected STL files remain watertight/manifold.
- Visually inspect split lower/upper parts and the retainer.
- Add mk0.7.4 `DECISIONS.md` entries for the chosen joint and filter retention approach.

### Exit Criteria

- `MA-003` is closed in CAD.
- `MA-004` is closed in CAD.
- Full mockup is still blocked until coupons pass, but impossible geometry is gone.

## Chunk 2 - Side Panel and Rail Mount Interfaces

### Findings

- `ASM-001`: left panel ribs and bosses face outward.
- `ASM-002`: right panel bosses/ribs may overlap the mount rail.
- `MA-002`: rail end mount engagement is too shallow.
- Rail end mount M3 hole has no clear mating target.
- `RAP-005`: side-panel mount rail boss strength is untested.

### Work

1. Fix left side panel orientation in `cad/assembly/tower_assembly.py`.
   - Minimal fix: left panels rotate `-90.0` while right panels keep `+90.0`.
   - Better future-proof fix: make left/right panel orientation explicit instead of relying on one global `SIDE_PANEL_ASSEMBLY_ROTATION_DEG`.

2. Check and fix right panel boss-to-rail collision.
   - If the boss/rib volume occupies the side-panel mount rail volume, add local relief/cutouts or reduce rib/boss height near rail contact.
   - Do not remove the mount standard unless a replacement standard is documented.

3. Increase rail end mount engagement.
   - Target at least 8-10 mm of rail capture for mockup.
   - Prefer parameterized mount/slot geometry in `cad/parts/rails.py`.

4. Add a real screw target for rail end mounts.
   - Either add matching frame holes or redesign the rail end mount fastening strategy.
   - The solution must be visible in CAD and reflected in the assembly sequence.

### Verification

- Render or inspect left/right side views.
- Confirm both panel exteriors are smooth and bosses face inward.
- Confirm rail end mount has useful rail capture depth.
- Confirm screw path has a mating target and is accessible.

### Exit Criteria

- Left side panel can be fastened from the intended side.
- Right side panel no longer has unresolved CAD collision against the mount rail.
- Rail end mounts are mechanically plausible before coupon testing.

## Chunk 3 - Fit Coupons Before Large Prints

### Findings

- `RAP-002`: split joints require coupon testing.
- `RAP-003`: real metal rail tolerance is unknown.
- `RAP-005`: side panel mount rail and insert boss strength are unknown.
- `RAP-009`: bottom filter retention needs physical validation.
- `RAP-011`: grille/filter orientation needs test tiles.
- Unknowns `UNK-003`, `UNK-004`, `UNK-005`, `UNK-006`, `UNK-008`.

### Work

Create a coupon test plan and, where practical, small exported coupon geometry:

- split-joint tab/socket with M3 screw path;
- rail end mount plus real metal guide rail interface;
- tray support ledge plus rail plus representative tray edge;
- side panel mount rail plus representative panel section with insert boss;
- bottom filter retainer plus filter frame plus real filter sheet;
- TPU foot plus PETG socket;
- large flat PETG tile, 50 x 50 x 3 mm;
- representative top fan grille section.

### Verification

Each coupon gets a simple result table:

```text
Coupon | Result | Required Change | Status
```

### Exit Criteria

- No full-size spine, tray stack, side panel set, or grilles are printed before the relevant coupons pass.
- Coupon failures become new mk0.7.4 findings and feed back into Chunk 1 or Chunk 2.

## Chunk 4 - Mockup Mass Reduction

### Findings

- `PE-008`: total printable plastic is excessive.
- `PE-001`: central bottom fan frame is overbuilt.
- `PE-002`: base assembly is overbuilt for rough mockup.
- `PE-003`: trays are heavy for static fit-check.
- `PE-004`: side panel ribs are heavy for a mockup.
- `PE-005`: rear service spine depth may be excessive for rough routing.
- `PE-009`: bottom fan grille thickness is inconsistent with `FAN_GRILLE_THICKNESS`.

### Work

Add a controlled mockup parameter set instead of random local thinning:

- `MOCKUP_BASE_THICKNESS`
- `MOCKUP_CENTRAL_FRAME_THICKNESS`
- `MOCKUP_TRAY_BASE_THICKNESS`
- `MOCKUP_TRAY_SIDE_WALL`
- `MOCKUP_SIDE_SHEAR_RIB_HEIGHT`
- `MOCKUP_REAR_SPINE_DEPTH`
- `MOCKUP_BOTTOM_GRILLE_THICKNESS` or direct use of existing `FAN_GRILLE_THICKNESS`

Preferred policy:

- keep `mini_pc_tray` and `ups_power_tray` more conservative than light trays;
- reduce only mockup geometry, not the future production intent;
- document every reduction in `CALCULATIONS.md` with the tradeoff.

### Verification

- Regenerate plastic estimate.
- Compare mk0.7.4 mass against mk0.7.3.
- Target reduction: 700-1000 g mesh-equivalent if achievable without weakening the rough assembly path.

### Exit Criteria

- Plastic mass is reduced enough to make the draft print economically sane.
- No reduced part becomes thinner than the intended printable wall/rib standard.

## Chunk 5 - Assembly Practicality and BOM

### Findings

- `RAP-001`: 24 tray support ledges create high assembly risk.
- `RAP-004`: no assembly instructions or BOM.
- `RAP-006`: base fastener access is under-modeled.
- `RAP-007`: M5 nuts/washers missing from manifest.
- `RAP-008`: M3 screws/inserts missing from manifest.
- `RAP-012`: too many unique print and assembly steps for an unmanaged mockup.

### Work

1. Produce `revisions/mk0.7.4/FASTENER_BOM.md`.
   - M5 rods, nuts, washers, optional nylock/acorn nuts.
   - M3 screws by length class if known; otherwise mark length as `TBD after stack check`.
   - M3 heat-set inserts.
   - Any required real metal guide rails.

2. Produce `revisions/mk0.7.4/ASSEMBLY_SEQUENCE.md`.
   - Base sections.
   - M5 rods and corner blocks.
   - Metal guide rails.
   - Rail end mounts.
   - Tray support ledges.
   - Tray stack.
   - Rear service spine and power bus placeholders.
   - Side panel mount rails and panels.
   - Fans, filter frame, retainer, feet.

3. Decide how to reduce ledge misassembly risk.
   - Option A: add a printed spacing jig/index gauge.
   - Option B: replace individual ledges with longer indexed support rails.
   - Option C: keep individual ledges but add a dimensioned installation table and assembly marks.

4. Model or document base fastener access.
   - Bolts inserted from top/bottom must be clear before the tower is built up.

### Verification

- A human can identify all hardware before printing.
- Assembly order does not require removing already-installed major modules.
- Ledge installation has either a jig or a clear indexed measurement procedure.

### Exit Criteria

- `RAP-004`, `RAP-007`, `RAP-008` are closed by documentation.
- `RAP-001` is either reduced by CAD or controlled by jig/instructions.

## Chunk 6 - Print Plan and Orientation Controls

### Findings

- `PRINT-004`: top fan grille warp risk.
- `PRINT-005`: bottom filter frame warp risk.
- `PRINT-007`: rear service spine tall narrow print risk.
- `PRINT-011`: trays warp at thin base.
- `PRINT-017`: bottom fan cartridge brim recommended.
- `PRINT-019`: rear spine covers should not be printed upright.
- `PRINT-018`: power bus covers/panels need careful orientation.

### Work

Produce `revisions/mk0.7.4/PRINT_PLAN.md` with per-part orientation:

- print flat, edge, or wide-face orientation;
- brim width;
- supports yes/no;
- material: PETG/TPU;
- first-layer caution for large flat parts;
- batch grouping recommendation;
- do-not-print-yet markers for parts gated by coupons.

### Verification

- Every printable part has a recommended orientation.
- Large flat parts have brim/enclosure guidance.
- Tall narrow parts are either reoriented or explicitly marked as risky.

### Exit Criteria

- No part relies on guesswork at slicing time.

## Chunk 7 - Full mk0.7.4 Pipeline and Review Package

### Work

Run the revision pipeline for mk0.7.4:

```text
conda run -n cadquery python scripts/run_revision_pipeline.py --revision mk0.7.4
```

Verify outputs:

- exports refresh successfully;
- all printable STLs are watertight/manifold;
- all parts fit the target build volume;
- plastic estimate reflects mockup reduction;
- review package includes updated docs and manifests.

### Exit Criteria

- No pipeline failure.
- No new blocker from export, manifold, or build-volume checks.

## Chunk 8 - Final Readiness Review

### Work

Re-run external engineering review on the mk0.7.4 package.

The review prompt should require:

- evidence status: `CONFIRMED`, `LIKELY`, `UNCERTAIN`, `NEEDS TEST`;
- no invented CFD, FEA, slicer, or physical test results;
- final verdict: `GO FOR FULL PRINT`, `GO FOR PARTIAL TEST PRINT`, or `NO-GO UNTIL BLOCKERS ARE FIXED`.

### Exit Criteria

mk0.7.4 can be called draft print-ready only if:

- all blocker geometry is fixed;
- side panel and rail interfaces are mechanically plausible;
- coupon-required interfaces either passed or are excluded from full print;
- BOM and assembly sequence exist;
- print orientation plan exists;
- pipeline passes;
- external review gives at least `GO FOR PARTIAL TEST PRINT`, ideally `GO FOR ROUGH MOCKUP PRINT`.

## Recommended Commit Slices

1. `mk0.7.4 docs scaffold and iteration plan`
2. `fix split joints and filter retainer blockers`
3. `fix side panel orientation and rail mount interfaces`
4. `add coupon test plan and coupon exports`
5. `add mockup mass reduction parameters`
6. `add fastener BOM and assembly sequence`
7. `add print plan and orientation guidance`
8. `refresh mk0.7.4 exports and review package`

## Finding-to-Chunk Map

| Finding | Chunk |
|---|---|
| `MA-003` | Chunk 1 |
| `MA-004` | Chunk 1 |
| `ASM-001` | Chunk 2 |
| `ASM-002` | Chunk 2 |
| `MA-002` | Chunk 2 |
| Rail end mount screw target | Chunk 2 |
| `RAP-002` | Chunk 3 |
| `RAP-003` | Chunk 3 |
| `RAP-005` | Chunk 3 |
| `RAP-009` | Chunk 3 |
| `RAP-011` | Chunk 3 |
| `PE-001` | Chunk 4 |
| `PE-002` | Chunk 4 |
| `PE-003` | Chunk 4 |
| `PE-004` | Chunk 4 |
| `PE-005` | Chunk 4 |
| `PE-008` | Chunk 4 |
| `PE-009` | Chunk 4 |
| `RAP-001` | Chunk 5 |
| `RAP-004` | Chunk 5 |
| `RAP-006` | Chunk 5 |
| `RAP-007` | Chunk 5 |
| `RAP-008` | Chunk 5 |
| `RAP-012` | Chunk 5 |
| `PRINT-004` | Chunk 6 |
| `PRINT-005` | Chunk 6 |
| `PRINT-007` | Chunk 6 |
| `PRINT-011` | Chunk 6 |
| `PRINT-017` | Chunk 6 |
| `PRINT-018` | Chunk 6 |
| `PRINT-019` | Chunk 6 |
| `ASM-005` | Chunk 7 / Chunk 8 |

