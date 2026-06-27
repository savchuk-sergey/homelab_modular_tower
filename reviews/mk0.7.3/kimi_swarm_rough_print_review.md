# Kimi Agents Swarm Rough Print Review — Homelab Modular Tower mk0.7.3

**Date:** 2025-01-09  
**Revision:** mk0.7.3  
**Goal:** Evaluate whether mk0.7.3 is ready for rough draft printing and rough physical assembly as a mockup platform.  
**Scope:** Printability, assembly geometry, panel orientation, mount alignment, plastic consumption, rough assembly practicality.  
**Out of scope:** Final component dimensions, final electrical safety, final cooling performance, final stability, CFD/FEA/slicer validation, physical testing.

---

## 1. Executive Summary

mk0.7.3 is a promising rough-assembly platform with a coherent modular architecture, correct overall proportions, and all printable parts within the Bambu Lab P2S build envelope. However, **two BLOCKER-level geometry bugs** and **one HIGH-priority panel orientation bug** prevent a confident `GO FOR ROUGH MOCKUP PRINT` verdict. The model should be validated with **coupon test prints** before any broad production printing.

- **All 42 printable plastic parts fit within 256 × 256 × 256 mm** and are watertight/manifold.
- **The left side panels are oriented incorrectly** — ribs and mounting bosses face outward, away from the mount rails, making secure fastening impossible without exposed, overly long screws.
- **Split-joint tabs on rear spine and power bus parts physically overlap** — both lower and upper segments have tabs at the same location, preventing assembly.
- **Bottom filter retainer corner clips are detached** from the retainer body, making the part non-functional.
- **Total plastic consumption is ~3.7 kg mesh solid** (~4.5–5.5 kg actual filament), which is excessive for a rough mockup. A 25–30 % reduction is achievable without sacrificing assembly-critical geometry.
- **Large flat PETG parts** (grilles, filter frames, trays, wings) will warp significantly without brims and enclosure.
- **No assembly instructions, BOM, or fastener inventory** exists for the 109-part assembly.

---

## 2. Reviewed Inputs

| Path | Role |
|------|------|
| `AGENTS.md` | Project engineering rules and priorities |
| `README.md` | Project overview and revision workflow |
| `cad/config.py` | All parametric dimensions and print settings |
| `cad/assembly/tower_assembly.py` | Main assembly placement code |
| `cad/parts/frame.py` | Top/bottom structural frames |
| `cad/parts/corner_blocks.py` | Corner compression blocks |
| `cad/parts/rails.py` | Metal guide rails, rail end mounts, tray support ledges |
| `cad/parts/rods.py` | M5 threaded rods and caps |
| `cad/parts/side_panels.py` | Side panel and mount rail geometry |
| `cad/parts/feet.py` | Stability base and foot sockets |
| `cad/parts/cooling.py` | Fan grilles, cartridge, filter frame/retainer, Mini PC duct |
| `cad/parts/service_spine.py` | Rear service spine, power bus, split sections |
| `cad/parts/modules.py` | Device-specific module trays |
| `cad/parts/carriages.py` | Generic tray/carriage geometry |
| `cad/exporters/part_registry.py` | Part and export category registry |
| `revisions/mk0.7.3/REVISION.md` | Revision purpose and scope |
| `revisions/mk0.7.3/CHANGELOG.md` | Changes since previous revision |
| `revisions/mk0.7.3/DECISIONS.md` | Engineering decisions for this revision |
| `revisions/mk0.7.3/CALCULATIONS.md` | Stack calculations and printability assumptions |
| `revisions/mk0.7.3/KNOWN_ISSUES.md` | Known issues and limitations |
| `revisions/mk0.7.3/PRINTABLE_PARTS.md` | Printable parts manifest |
| `revisions/mk0.7.3/NON_PRINTABLE_PARTS.md` | Non-printable reference parts |
| `revisions/mk0.7.3/PLACEHOLDERS.md` | Placeholder geometry manifest |
| `revisions/mk0.7.3/REVIEW_GEOMETRY.md` | Review geometry manifest |
| `revisions/mk0.7.3/analysis/part_dimensions.csv` | Part bounding boxes and volumes |
| `revisions/mk0.7.3/analysis/plastic_estimate.csv` | PETG/PLA mass estimates |
| `revisions/mk0.7.3/analysis/printability_check.csv` | P2S envelope and long-thin risk |
| `revisions/mk0.7.3/analysis/stl_quality.csv` | Watertight/manifold status |
| `revisions/mk0.7.3/analysis/duplicate_geometry_check.csv` | Duplicate/near-duplicate detection |
| `renders/mk0.7.3/drawings/assembly.png` | Assembly drawing (Front, Right, Top, Isometric) |
| `renders/mk0.7.3/assembly/left.png` | Left-side assembly view |
| `renders/mk0.7.3/assembly/right.png` | Right-side assembly view |
| `renders/mk0.7.3/review/` | Review render directory (listed) |
| `renders/mk0.7.3/drawings/parts/` | Part render directory (listed) |

---

## 3. Final Verdict

### GO FOR COUPON TEST PRINT ONLY

The model is structurally promising and all parts are printable, but **specific geometry bugs and fit risks must be resolved with small test coupons before any full mockup printing.** The two BLOCKER findings (split-joint tab overlap and detached filter retainer clips) are localized CAD errors that can be fixed quickly. The left panel orientation bug requires a single rotation sign change. After these fixes, the model should proceed through coupon validation for rail fit, panel mount stiffness, and large-flat warping behavior.

---

## 4. Blockers for Rough Mockup

| ID | Finding | Severity | Status | Affected Parts | Evidence |
|----|---------|----------|--------|---------------|----------|
| **MA-003** | **Split-joint tabs overlap** — Both lower and upper segments of rear spine, spine cover, power bus panel, and power bus cover have alignment tabs at the same Z=0 location. When assembled, the tabs occupy the same physical volume and cannot coexist. | BLOCKER | CONFIRMED | `rear_service_spine_lower`, `rear_service_spine_upper`, `rear_service_spine_cover_lower`, `rear_service_spine_cover_upper`, `power_bus_panel_lower`, `power_bus_panel_upper`, `power_bus_cover_lower`, `power_bus_cover_upper` | `cad/parts/service_spine.py` lines 8–35; `revisions/mk0.7.3/analysis/part_dimensions.csv` (lower ends at +9, upper starts at −9) |
| **MA-004** | **Filter retainer clips are detached** — The bottom filter retainer body is 144 mm wide × 8 mm deep. Corner clips are placed at `clip_offset = 61`, so at Y = ±61. The clips are 57 mm outside the retainer body and completely detached. No geometry connects them to the body. | BLOCKER | CONFIRMED | `bottom_filter_retainer` | `cad/parts/cooling.py` lines 113–134; `config.py` (`BOTTOM_FILTER_CORNER_CLIP_SIZE=16`) |

### Why these are BLOCKERs

- **MA-003:** The split sections are explicitly designed to be bolted together at the joint. If both halves have a tab at the same location, the joint cannot be assembled. The screw holes are collinear, but the tabs physically collide. This is an impossible geometry, not a fit risk.
- **MA-004:** The retainer's only function is to hold the filter sheet against the bottom fan grille. Detached clips cannot exert any retention force. The part is non-functional as printed.

---

## 5. High Priority Findings

| ID | Finding | Severity | Status | Affected Parts | Evidence |
|----|---------|----------|--------|---------------|----------|
| **ASM-001** | **Left panel ribs and mounting bosses face outward** — Left and right panels share identical geometry. Both are rotated +90° around Z. For the left panel at X=−96.5, the local +Y face (ribs, holes, bosses) maps to −X_global = outward. The mount rail is at X=−91 (inward). The bosses are on the wrong side. | HIGH | CONFIRMED | `left_side_panel_lower`, `left_side_panel_middle`, `left_side_panel_upper` | `cad/parts/side_panels.py` lines 198–220; `cad/assembly/tower_assembly.py` lines 159–212; `renders/mk0.7.3/assembly/left.png` |
| **MA-002** | **Rail end mount engagement is shallow** — The bottom mount is at Z=3.5, the rail starts at Z=5.0. The mount slot is 10.8 mm tall. The rail engages only 3.5 mm of the slot. The top mount has the same 3.5 mm overlap. This may be insufficient for a secure capture. | HIGH | CONFIRMED | `rail_end_mount` (8 instances), `metal_guide_rail` | `cad/parts/rails.py` lines 31–45; `cad/assembly/tower_assembly.py` lines 45–58; `config.py` (`METAL_RAIL_HEIGHT=287.5`, `FRAME_THICKNESS=7.0`) |
| **ASM-002** | **Right panel mounting features may overlap with mount rail** — After +90° rotation, the right panel's +Y face is at X=+85 (inward). The mounting bosses extend from X=+85 to X=+91.0 (for 4 mm rib height). The mount rail is at X=+91, from +87 to +95. The bosses overlap the rail volume. | HIGH | LIKELY | `right_side_panel_lower`, `right_side_panel_upper`, `side_panel_mount_rail` | `cad/parts/side_panels.py` lines 100–113; `cad/assembly/tower_assembly.py` lines 159–212; `part_dimensions.csv` |
| **PE-008** | **Total plastic consumption is excessive for a rough mockup** — 42 printable plastic parts total 3,732 g mesh solid volume. With slicer infill, perimeters, supports, and purge, this translates to ~4.5–5.5 kg of actual PETG filament. For a fit-check mockup, this is uneconomical and slow. | HIGH | CONFIRMED | All printable plastic parts | `revisions/mk0.7.3/analysis/plastic_estimate.csv` (sum of all rows) |
| **PRINT-004** | **Top fan grille (190 × 190 × 4 mm) will warp severely in PETG** — Large thin flat parts with low thermal mass curl aggressively at corners. The 4 mm thickness and 190 mm span make this the highest warping risk in the project. | HIGH | LIKELY | `top_fan_grille` | `revisions/mk0.7.3/analysis/printability_check.csv` (aspect_ratio=47.5); `part_dimensions.csv` |
| **PRINT-005** | **Bottom filter frame (138 × 138 × 3 mm) will warp severely in PETG** — Same category as the grille: large, thin, flat. 3 mm thickness with 138 mm span is extremely prone to corner lifting. | HIGH | LIKELY | `bottom_filter_frame` | `revisions/mk0.7.3/analysis/printability_check.csv` (aspect_ratio=46.0) |
| **PRINT-011** | **All six module trays (~172 × 178.7 × 32 mm) will warp at the 3 mm base** — The tray base is only 3 mm thick with a 172 × 178 mm footprint. PETG corner lift is nearly guaranteed without a generous brim and enclosure. | HIGH | LIKELY | `external_ssd_bay`, `mikrotik_tray`, `mini_pc_tray`, `raspberry_pi_tray`, `ssd_expansion_tray`, `ups_power_tray` | `revisions/mk0.7.3/analysis/part_dimensions.csv`; `config.py` (`TRAY_BASE_THICKNESS=3.0`) |
| **RAP-001** | **24 tray support ledges create excessive assembly complexity** — Six trays × four rails = 24 small ledges that must be placed at unique Z heights and fastened individually. This is the highest-risk step for misassembly. | HIGH | CONFIRMED | `tray_support_ledge` (24 instances) | `cad/assembly/tower_assembly.py` lines 61–69; `revisions/mk0.7.3/analysis/part_dimensions.csv` |
| **RAP-004** | **No assembly instructions or BOM exist** — With 109 part instances from 42 unique designs, a human cannot reliably infer build order from Python code alone. Rod threading, base bolting, and mount-rail insertion order are undocumented. | HIGH | CONFIRMED | All parts | `revisions/mk0.7.3/PRINTABLE_PARTS.md`; `revisions/mk0.7.3/NON_PRINTABLE_PARTS.md`; `revisions/mk0.7.3/PLACEHOLDERS.md` |
| **PRINT-007** | **Rear service spine lower/upper (132 × 40.5 × 157.75 mm) may wobble or detach** — Tall, narrow PETG prints with a small footprint are prone to gantry-induced wobble and bed detachment. | HIGH | LIKELY | `rear_service_spine_lower`, `rear_service_spine_upper` | `revisions/mk0.7.3/analysis/part_dimensions.csv` |
| **PRINT-019** | **Rear service spine cover lower/upper (46 × 6 × 156.75 mm) will wobble if printed upright** — 156 mm tall with only 6 mm base thickness. This is a very tall thin wall. Printing flat (Z=6 mm) is strongly recommended instead. | HIGH | LIKELY | `rear_service_spine_cover_lower`, `rear_service_spine_cover_upper` | `revisions/mk0.7.3/analysis/part_dimensions.csv` |
| **PE-001** | **Central bottom fan frame is overbuilt** — 190 × 190 × 16 mm, 326 g. This is 60 % thicker than the `BASE_STABILITY_THICKNESS=10.0` used elsewhere. The M5 rods carry the structural load, not the base plate. | HIGH | CONFIRMED | `central_bottom_fan_frame` | `revisions/mk0.7.3/analysis/plastic_estimate.csv` (326.43 g); `part_dimensions.csv` (257,031 mm³) |
| **PE-002** | **Base assembly is overbuilt for a mockup** — Five base sections total 932 g. The 10 mm stability wings and 16 mm central frame are production-grade overturning margins. For a fit-check mockup, 6–8 mm is adequate. | HIGH | CONFIRMED | `bottom_structural_frame`, `central_bottom_fan_frame`, `front_stability_wing`, `rear_stability_wing`, `left_foot_extension`, `right_foot_extension` | `revisions/mk0.7.3/analysis/plastic_estimate.csv` |
| **RAP-003** | **Rail end mounts and tray ledges need physical fit testing against real metal rails** — `METAL_RAIL_FRAME_CLEARANCE=1.0 mm` may be too loose or too tight depending on actual rail tolerance and print shrinkage. | HIGH | CONFIRMED | `rail_end_mount`, `tray_support_ledge`, `metal_guide_rail` | `revisions/mk0.7.3/KNOWN_ISSUES.md` line 11; `cad/parts/rails.py` |
| **RAP-002** | **Split-joint tabs require test coupons before full spine/power-bus prints** — If tab clearance or screw alignment is wrong, the two large halves will not mate. Printing 157–275 mm tall parts to discover interference is wasteful. | HIGH | CONFIRMED | All split lower/upper parts | `revisions/mk0.7.3/KNOWN_ISSUES.md` line 12; `cad/parts/service_spine.py` |

---

## 6. Panel Orientation and Mount Alignment

### 6.1 Panel Orientation (CONFIRMED Bug)

**Observation:** In `cad/parts/side_panels.py`, `make_side_panel_tile()` uses the `side` parameter **only** for the `tag()` call, not for geometry. Left and right panels are identical.

In `cad/assembly/tower_assembly.py`, both panels are placed with the **same** `SIDE_PANEL_ASSEMBLY_ROTATION_DEG = 90.0`:
- Left panel at X=−96.5: local +Y → −X_global = **outward**. Ribs and mounting bosses face **away** from the tower.
- Right panel at X=+96.5: local +Y → −X_global = **inward**. Ribs and mounting bosses face **toward** the tower.

**Render evidence:**
- `renders/mk0.7.3/assembly/left.png` — ribs are clearly visible as raised features on the exterior.
- `renders/mk0.7.3/assembly/right.png` — exterior is smooth; ribs are hidden on the interior.

**Impact:** The left panel mounting bosses are on the outside (X≈−108), while the mount rail is on the inside (X=−91). There is a ~13 mm gap with no boss support. The screw head would be exposed on the exterior. The right panel bosses overlap the rail (confirmed by geometry), which may be intentional but needs verification.

**Fix:** Change the left panel rotation to −90.0° (or 270.0°) in `tower_assembly.py`, or create mirrored left-panel geometry in `side_panels.py`.

### 6.2 Mount Alignment Summary

| Interface | Status | Notes |
|-----------|--------|-------|
| Left panel holes ↔ mount rail | **MISALIGNED** | Holes face outward; bosses 13 mm from rail |
| Right panel holes ↔ mount rail | **ALIGNED** | Holes face inward; bosses overlap rail (needs verification) |
| Rail end mount ↔ metal rail | **SHALLOW** | Only 3.5 mm engagement; may need deeper slot or repositioned mount |
| Rail end mount M3 hole ↔ frame/rail | **NO TARGET** | Frame has no matching M3 hole; rail holes are at 70 mm spacing, not at mount Z |
| Tray support ledge ↔ tray mounting holes | **NOT DIRECT** | Ledges are at guide rail positions, not under tray mounting holes (by design) |
| Tray support ledge ↔ guide rail | **NEEDS TEST** | 1.0 mm clearance may be too tight/loose after print shrinkage |
| Corner block holes ↔ side panels | **N/A** | Corner block holes are service holes for rod access, not panel mounts |
| Foot socket ↔ foot | **ALIGNED** | Socket at Z=−20, foot at Z=−30; foot engages 6 mm into socket |
| Foot socket ↔ base sections | **PARTIAL** | Socket at (−97, −102) may overhang the front wing / left extension junction |
| Bottom fan cartridge ↔ base | **NO DIRECT MOUNT** | Cartridge holes are for the fan, not for attaching to the base |
| Split spine tabs ↔ mating tabs | **COLLISION** | Both lower and upper have tabs at same Z=0; tabs overlap |
| Bottom filter retainer clips ↔ retainer body | **DETACHED** | Clips at Y=±61 are 57 mm outside the 8 mm deep body |
| Base wing fasteners | **WITHIN BOUNDS** | Fasteners are inside section bounds (Mount Alignment Reviewer finding MA-005 was incorrect) |

---

## 7. Printability Findings

### 7.1 Build Volume — All Clear

All 42 printable plastic parts and 1 TPU part fit within the 256 × 256 × 256 mm Bambu Lab P2S axis-aligned envelope. No diagonal packing required.

### 7.2 Manifold / Watertight — All Clear

All `printable/plastic` and `printable/tpu` parts are `is_watertight=True` and `is_manifold=True` with 0 boundary edges and 0 nonmanifold edges. Only placeholders and review geometry have nonmanifold edges (expected, not production parts).

### 7.3 Warping Risks (PETG)

| Part | Risk | Reason | Mitigation |
|------|------|--------|------------|
| `top_fan_grille` | **HIGH** | 190 × 190 × 4 mm, aspect ratio 47.5 | Print flat, generous brim (10 mm+), enclosure, reduce cooling fan |
| `bottom_filter_frame` | **HIGH** | 138 × 138 × 3 mm, aspect ratio 46.0 | Print flat, full brim or mouse ears |
| `bottom_filter_retainer` | **HIGH** | 144 × 138 × 4 mm, aspect ratio 36.0 | Print flat, brim; clip integrity uncertain |
| All 6 trays | **HIGH** | 172–186 × 178.7 × 32 mm, 3 mm base | Brim (8–10 mm), enclosure, slow first layer |
| `front/rear_stability_wing` | **HIGH** | 250 × 47 × 10 mm, near build limit | Brim (10 mm+), enclosure, slow outer wall |
| `bottom_fan_grille` | **MEDIUM** | 190 × 190 × 7 mm | Brim (5–8 mm), print flat |
| `bottom_structural_frame` | **MEDIUM** | 190 × 190 × 13 mm, ring reduces warp vs solid | Brim (5–8 mm) |
| `central_bottom_fan_frame` | **MEDIUM** | 190 × 190 × 16 mm | Brim (5–8 mm) |
| `bottom_fan_cartridge` | **MEDIUM** | 142 × 150 × 9 mm | Brim (5–8 mm), print flat |
| `rear_service_spine_lower/upper` | **MEDIUM** | 132 × 40.5 × 157.75 mm | Wide brim (10 mm), slow outer wall, consider raft |
| `rear_service_spine_cover_lower/upper` | **MEDIUM** | 46 × 6 × 156.75 mm | **Print flat** (Z=6 mm), not upright |
| `side_panel_lower/upper` | **MEDIUM** | 176 × 13 × 100.9 mm | Print on edge (176 × 13 on bed), brim along 176 mm length |
| `side_panel_middle` | **MEDIUM** | 176 × 5.2 × 100.9 mm | Edge print on 5.2 mm base is risky; consider face-down with aggressive brim |
| `mini_pc_airflow_duct` | **MEDIUM** | 88 × 134 × 62 mm, 2 mm walls | Print upright if open-channel; use 4+ walls, avoid drafts |
| `power_bus_panel/cover` | **MEDIUM** | 34–46 × 10–15.5 × 141–146 mm | Brim (8 mm); print covers on 46 × 141 face (Z=10) |
| `side_panel_mount_rails` | **LOW** | 8 × 12 × 100.9 mm | Print flat (100.9 × 12 on bed, Z=8); holes are vertical, no supports |
| `rail_end_mount` | **LOW** | 18 × 12 × 10 mm | Orient slot vertically; no supports; batch print |
| `m5_threaded_rod_cap` | **LOW** | 12 × 12 × 8 mm | Straightforward; batch print |

### 7.4 Support Requirements

| Part | Supports Needed? | Notes |
|------|-------------------|-------|
| `side_panel_mount_rails` | No | If printed flat, holes are vertical |
| `rail_end_mount` | No | If slot is vertical |
| `mini_pc_airflow_duct` | Maybe | If internal baffles or overhangs > 45° exist; test coupon recommended |
| `bottom_fan_grille` | No | Flat print, all features are 2.5D |
| `top_fan_grille` | No | Flat print, all features are 2.5D |
| `bottom_filter_frame` | No | Flat print |
| `bottom_filter_retainer` | No | Flat print (but clips may need support if oriented poorly) |
| All frames | No | Flat print |
| All trays | No | Vertical walls and insert bosses are support-free; base is flat |
| Spine/cover split parts | No | If printed flat or on the wide face |
| `corner_block` | No | Small, compact |
| `foot_socket` | No | Small, compact |

---

## 8. Plastic Consumption Findings

### 8.1 Total Consumption

- **Mesh solid volume:** 3,732 g PETG (from `plastic_estimate.csv` sum)
- **Estimated actual filament:** 4.5–5.5 kg (including slicer infill, perimeters, supports, purge)
- **Print time estimate:** 80–120 hours (depending on settings and batching)
- **Cost estimate:** $90–140 in PETG filament

### 8.2 Top 10 Consumers

| Rank | Part | PETG Mass (g) | % of Total | Assessment |
|------|------|---------------|------------|------------|
| 1 | `central_bottom_fan_frame` | 326.43 | 8.7 % | **Overbuilt** — 16 mm thick vs 10 mm base elsewhere |
| 2 | `mini_pc_tray` | 238.07 | 6.4 % | Acceptable — heaviest load (1.2 kg) |
| 3 | `ups_power_tray` | 196.06 | 5.3 % | Acceptable — heaviest load (1.4 kg) |
| 4 | `mikrotik_tray` | 174.68 | 4.7 % | Reasonable |
| 5 | `ssd_expansion_tray` | 167.23 | 4.5 % | Reasonable |
| 6 | `raspberry_pi_tray` | 165.04 | 4.4 % | Reasonable |
| 7 | `external_ssd_bay` | 160.23 | 4.3 % | Reasonable |
| 8 | `front_stability_wing` | 148.54 | 4.0 % | **Overbuilt** — 10 mm wing for mockup stability |
| 9 | `rear_stability_wing` | 148.54 | 4.0 % | **Overbuilt** — mirror of front |
| 10 | `bottom_fan_grille` | 141.63 | 3.8 % | Heavy — 7 mm vs 4 mm top grille |

### 8.3 Reduction Opportunities (Safe for Rough Mockup)

| Change | Estimated Savings | Engineering Justification |
|--------|-----------------|---------------------------|
| Reduce `central_bottom_fan_frame` to 8–10 mm | ~100–130 g | M5 rods carry load; base only distributes fan/filter load |
| Reduce stability wings to 6 mm | ~60 g each | Mockup only needs to stand upright, not survive dynamic loads |
| Reduce foot extensions to 6 mm | ~40 g each | Same justification |
| Reduce tray base/wall to 2 mm (5 lighter trays) | ~200–250 g total | 2 mm PETG + ribs is stiff enough for static fit-check |
| Reduce shear panel ribs to 2 mm | ~100–150 g | M5 rods provide primary stiffness; panels are covers |
| Reduce `rear_service_spine_depth` to 20 mm | ~70–90 g | 20 mm still houses power bus for mockup |
| Reduce `bottom_fan_grille` to 4 mm | ~40 g | Match `FAN_GRILLE_THICKNESS=4.0` config parameter |
| **Total potential reduction** | **~700–1,000 g** | ~20–27 % of total mesh solid |

### 8.4 Duplicate Geometry

Exact duplicates (mirrored pairs, expected and unavoidable):
- `front_stability_wing` = `rear_stability_wing`
- `left_foot_extension` = `right_foot_extension`
- `left_side_panel_lower` = `right_side_panel_lower`
- `left_side_panel_middle` = `right_side_panel_middle`
- `left_side_panel_upper` = `right_side_panel_upper`
- `side_panel_mount_rail_lower` = `middle` = `upper` (3 identical rails)

Near duplicates (could be unified in CAD):
- `bottom_structural_frame` ≈ `top_structural_frame` (minor differences: top has nut seats, bottom has washer seats)
- `power_bus_cover_lower` ≈ `power_bus_cover_upper`
- `rear_service_spine_cover_lower` ≈ `rear_service_spine_cover_upper`

These duplicates are **not waste** — they represent symmetric design standardization. However, printing only one side of a mirrored pair for a mockup (e.g., print only left panels and left extensions) could halve the part count for early fit-checking.

---

## 9. Rough Assembly Practicality

### 9.1 Part Count

- 42 unique printable plastic designs
- 109 total instances in assembly
- 2 non-printable metal references (M5 rod, guide rail)
- 8 device placeholders + 1 fan placeholder (not printed)
- 11 review geometry parts (not printed)

**Verdict:** 42 unique parts is high for a rough mockup. The cognitive load of tracking, slicing, and orienting so many unique STLs increases misidentification risk. Consider printing only critical subassemblies first (frame + one tray + one panel).

### 9.2 Fastener Inventory Gaps

| Fastener | Configured? | Inventoried? | Count (Estimated) |
|----------|-------------|--------------|-------------------|
| M5 threaded rod | Yes (4×) | Yes (non-printable) | 4 rods |
| M5 nut | Yes (geometry reserved) | **NO** | 8+ nuts |
| M5 washer | Yes (geometry reserved) | **NO** | 8+ washers |
| M5 rod cap (printable) | Yes | Yes | 4 caps |
| M3 screw | Yes (clearance holes) | **NO** | 50+ screws (panels, rails, ledges, mounts, spine) |
| M3 heat-set insert | Yes (boss geometry) | **NO** | 20+ inserts |

**Impact:** A human cannot purchase or prepare hardware without an inventory. The assembly cannot begin until a BOM is produced.

### 9.3 Assembly Complexity Issues

| Issue | Severity | Notes |
|-------|----------|-------|
| 24 tray support ledges at unique Z heights | HIGH | No jig or alignment helper exists |
| 5 base sections with hidden wing fasteners | MEDIUM | Fasteners are inside the assembly; some may be inaccessible after base is built |
| Split-joint M3 screws at 4 interfaces | MEDIUM | Tabs overlap; screws cannot be installed even if holes align |
| Side panel mount rails are "rough mockup interfaces" | MEDIUM | No documented shear transfer; insert bosses may strip if over-tightened |
| No written assembly sequence | HIGH | Build order must be inferred from Python code |
| TPU foot → PETG socket press fit | LOW | Untested; 0.6 mm clearance may be too loose/tight |
| M5 rod cap is non-structural placeholder | LOW | Must not be used as a real fastener |

---

## 10. Required Test Coupons

Before any full mockup print, the following test coupons should be printed and validated:

| # | Coupon | What to Test | Why |
|---|--------|--------------|-----|
| 1 | **Split-joint tab** — Print a small block with the tab geometry, M3 hole, and mating slot from `service_spine.py` | Screw clearance, tab overlap, alignment | BLOCKER: tabs overlap in current CAD |
| 2 | **Rail end mount + metal guide rail** — Print one `rail_end_mount` and test against the actual metal rail | Slot fit, screw hole alignment, engagement depth | HIGH: only 3.5 mm engagement; may need repositioning |
| 3 | **Tray support ledge + metal rail + tray bottom** — Print one ledge and test slide fit | Rail clearance, tray support, ledge stability | HIGH: 1.0 mm clearance may be wrong after shrinkage |
| 4 | **Side panel mount rail + panel section** — Print one mount rail and one panel section (e.g., `left_side_panel_middle`) | Screw fit, boss strength, panel stiffness | HIGH: left panel orientation is wrong; right panel may overlap |
| 5 | **Bottom filter retainer + filter frame + filter sheet** — Print retainer and frame, insert filter | Clip retention, vibration resistance | BLOCKER: clips are detached |
| 6 | **TPU foot + PETG socket** — Print one foot and one socket | Insertion force, screw retention, fit | LOW: 0.6 mm clearance untested |
| 7 | **Large thin flat test tile** — Print a 50 × 50 × 3 mm square in PETG | Warping behavior, brim effectiveness | HIGH: all trays and grilles depend on this |
| 8 | **Top fan grille (or 50 × 50 section)** — Print a representative section of the 4 mm grille | Support-free flatness, bar adhesion, corner lift | HIGH: 190 mm span is high-risk |

---

## 11. Action Plan for Codex

### Immediate (Before Any Coupon Print)

1. **Fix left panel orientation** — `cad/assembly/tower_assembly.py`: change left panel rotation from `90.0` to `-90.0` (or `270.0`). Alternatively, mirror left-panel geometry in `cad/parts/side_panels.py`. This is a one-line fix with high impact.
2. **Fix split-joint tab overlap** — `cad/parts/service_spine.py`: redesign `_split_section()` so only **one** segment (e.g., lower) has the tab and the other (upper) has a matching slot. Remove the tab from the upper segment.
3. **Fix filter retainer clips** — `cad/parts/cooling.py`: either attach the corner clips to the retainer body with proper geometry (e.g., extend the body to the clip locations, or add connecting ribs), or redesign the retention mechanism.
4. **Verify right panel boss-to-rail overlap** — In `cad/parts/side_panels.py`, check if `_make_side_panel_mounts()` produces bosses that extend into the mount rail volume. If so, either recess the rail mounting surface or reduce boss diameter.
5. **Increase rail end mount engagement** — Either move the bottom mount from Z=3.5 to Z=5.0+ (so the rail starts inside the slot), or increase the slot depth from 10.8 mm to 15+ mm.
6. **Add base fastener models** — Model the M3 bolts that join the 5 base sections in `cad/parts/feet.py` or assembly, and verify access from top/bottom.
7. **Add M3 hole to frame for rail end mount** — `cad/parts/frame.py`: add an M3 clearance hole at each rail position on the frame face, aligned with the rail end mount's >Y face hole.

### Short-Term (Before Full Mockup Print)

8. **Generate fastener BOM** — Count every M3 clearance hole, M3 insert boss, M5 nut seat, and M5 washer seat in the assembly. Produce a text manifest with quantities.
9. **Write rough assembly sequence** — Produce a numbered step-by-step guide: Base → Rods → Corner Blocks → Rails → Ledges → Tray Stack → Spine → Panels → Fans → Feet.
10. **Create mockup-thickness parameter set** — In `cad/config.py`, add optional `MOCKUP_*` parameters: `MOCKUP_BASE_THICKNESS=6.0`, `MOCKUP_TRAY_BASE=2.0`, `MOCKUP_TRAY_WALL=2.0`, `MOCKUP_SHEAR_RIB=2.0`. This allows quick config-driven mass reduction for rough prints without altering production geometry.
11. **Reduce central_bottom_fan_frame to 8–10 mm** — Match the base stability thickness or introduce a mockup parameter.
12. **Reduce bottom_fan_grille to 4 mm** — Match `FAN_GRILLE_THICKNESS=4.0` in `config.py`.
13. **Reduce rear_service_spine_depth to 20 mm** — For mockup only; verify power bus still fits.

### Validation (Before Declaring GO FOR ROUGH MOCKUP PRINT)

14. **Print all 8 coupons** from Section 10 and validate fit, strength, and warping.
15. **Re-run the revision pipeline** (`python scripts/run_revision_pipeline.py --revision mk0.7.3`) after CAD fixes to regenerate analysis CSVs, manifests, and renders.
16. **Re-run this review** on the fixed revision to confirm BLOCKERs are resolved and no new geometry bugs were introduced.

---

## 12. Unknowns / Deferred to mk1.0

The following items are **explicitly out of scope** for this mk0.7.3 rough-mockup review and are deferred to mk1.0 per `REVISION.md`, `KNOWN_ISSUES.md`, and user instructions:

| Item | Why Deferred |
|------|--------------|
| Real Mini PC dimensions and port locations | Placeholder envelope only; mk1.0 will measure actual device |
| Real MikroTik hAP ax2 board dimensions | Placeholder envelope only |
| Real UPS/battery dimensions and containment | Placeholder envelope only |
| Real SSD/SSD expansion dimensions | Placeholder envelopes only |
| Power connector selection (XT30, JST-VH, MicroFit, USB-C) | Placeholder connector cutouts only |
| Final fuse block, switch, DC input geometry | Placeholder envelopes only |
| Final Mini PC airflow duct validation | Placeholder duct; needs real device intake/exhaust measurements |
| Final cable routing and wire harness engineering | Rough service envelope only |
| Thermal validation (CFD, smoke test, physical measurement) | Explicitly deferred to mk1.0 |
| Full production BOM and electrical safety review | mk0.7.3 is a rough mockup, not a production release |
| Final stability/tipping analysis with real masses | Rough stability envelope exists; final analysis deferred |
| Torsion brace hardware selection and testing | TORSION_BRACE_MOUNT_ENABLED=True but no hardware specified |
| Metal guide rail material and stiffness validation | Non-printable reference only; mk1.0 will select real rail |

---

## 13. Appendix: CSV and Render Evidence

### 13.1 Printability Check (`revisions/mk0.7.3/analysis/printability_check.csv`)

- All 43 printable entries (`printable/plastic` + `printable/tpu`) have `fits_axis_aligned=True`.
- Three parts flagged `long_thin_risk=True`:
  - `bottom_filter_frame`: aspect ratio 46.0 (138 × 138 × 3 mm)
  - `bottom_filter_retainer`: aspect ratio 36.0 (144 × 138 × 4 mm)
  - `top_fan_grille`: aspect ratio 47.5 (190 × 190 × 4 mm)
- Max part dimension: `ups_power_tray` at 186.5 mm (still well under 256 mm).

### 13.2 STL Quality (`revisions/mk0.7.3/analysis/stl_quality.csv`)

- All `printable/plastic` and `printable/tpu` parts: `is_watertight=True`, `is_manifold=True`, `boundary_edges=0`, `nonmanifold_edges=0`.
- Nonmanifold entries are all placeholders or review geometry (not production parts).

### 13.3 Plastic Estimate (`revisions/mk0.7.3/analysis/plastic_estimate.csv`)

- 42 printable plastic parts, 1 TPU part.
- Total mesh solid PETG mass: 3,732.3 g.
- Largest single part: `central_bottom_fan_frame` at 326.43 g.
- Heaviest subsystem: six module trays at 1,101.3 g (29.5 % of total).
- Second heaviest subsystem: base assembly at 932.4 g (25.0 % of total).
- Third heaviest subsystem: side panels + mount rails at 659.9 g (17.7 % of total).

### 13.4 Duplicate Geometry (`revisions/mk0.7.3/analysis/duplicate_geometry_check.csv`)

- Exact duplicate groups: `exact_001` (front/rear wing), `exact_002` (left/right extension), `exact_003`–`exact_005` (side panels), `exact_006` (3 mount rails).
- Near duplicate groups: `near_001` (bottom/top frame), `near_007` (power bus covers), `near_008` (spine covers).

### 13.5 Assembly Renders

- `renders/mk0.7.3/drawings/assembly.png`: Front, Right, Top, Isometric views of full assembly. Overall dimensions 250 × 260 × 418 mm. 109 parts.
- `renders/mk0.7.3/assembly/left.png`: Left-side view. Ribs visible as raised X-pattern on exterior of left panel. Mount rails visible as small vertical bars between panel and tower.
- `renders/mk0.7.3/assembly/right.png`: Right-side view. Smooth exterior surface; ribs are hidden on interior.
- `renders/mk0.7.3/assembly/isometric.png`: Front-right isometric. Both visible side panels show different surface finishes (left = ribbed exterior, right = smooth exterior), confirming orientation asymmetry.

---

*End of review.*
