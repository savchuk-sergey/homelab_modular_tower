# Structural Integrity Review

**Reviewer:** Structural Integrity Reviewer (mk0.7.1 Engineering Review)  
**Revision:** mk0.7.1  
**Date:** 2025-01-21  
**Scope:** Load path, frame stiffness, corner blocks, guide rails, stability base, side panels, torsion, tray stop, rear spine.

---

## Executive Summary

The mk0.7.1 revision addresses **one** structural recommendation from mk0.7: the corner blocks have been moved from mid-height to the frame corners (`z = FRAME_THICKNESS/2` and `z = TOWER_HEIGHT − FRAME_THICKNESS/2`). This places them correctly in the load path between the structural frames and the module stack. However, **all other critical structural errors from mk0.7 remain unaddressed**.

**Blockers (must fix before any build):**
1. **Side panels cannot be mounted.** The corner blocks only have panel mounting holes on their `+X` and `+Y` faces; the `−X` and `−Y` faces are solid. Even on the faces that do have holes, the hole positions (`z = center ± 6 mm`) do not align with the side panel mount points (`z = center ± 40.45 mm`). The frame has no side-panel mounting holes. The result is that the lower, middle, and upper side panels have M3 clearance holes and heat-set insert bosses, but **nothing in the structure to screw them into**.
2. **Top frame cannot be clamped.** The top structural frame has a nut seat on its bottom face (`<Z`) and a washer seat on its top face (`>Z`). Because it is the topmost frame, it needs a nut on top to pull it down against rod tension. The current geometry would leave the top frame pushed upward by an interior nut with no clamping force from above.
3. **Tray vertical support is not modeled.** The metal guide rails are simple vertical bars (10 × 3 × 287.5 mm). The trays are horizontal plates with vertical clearance slots for the rails. There are no horizontal shelves, brackets, or frame ledges to support the tray bottoms. A 1.2 kg Mini PC tray would have no vertical support except possible contact with the bottom frame (for the lowest tray) or the rear service spine (for the rear stop). The upper trays are effectively unsupported.
4. **Torsion brace mounts are unimplemented.** `config.py` enables them (`TORSION_BRACE_MOUNT_ENABLED = True`), but no geometry exists in any part file.

**Major concerns (design risk, not necessarily build-blocking):**
- Frame rail slots leave only **1.5 mm of PETG** on each side of the metal rail; tearing risk under tray load.
- Middle side panel is explicitly non-structural (3.0 mm + 2.2 mm ribs), creating a **shear discontinuity** in the middle of the tower.
- The sectional base (5 parts, M3 fasteners) has a **hinge risk** at the joints under lateral or tipping loads.
- The Mini PC tray stop is a small PETG bracket that may fail under impact from a 1.2 kg tray.
- The 3.0 mm foot socket depth with no insert provides minimal TPU engagement; the foot may rock or pull out under tipping moments.

---

## Primary Load Path (M5 Rods)

### Assessment: ADEQUATE in tension, but top frame clamping is BROKEN.

**Evidence:**
- `config.py` lines 59–63: `ROD_DIAMETER = 5.0`, `ROD_CLEARANCE = 5.6`, `ROD_CENTER_OFFSET = 12.0`, `ROD_LENGTH = TOWER_HEIGHT ≈ 321.5 mm`.
- `rods.py`: rod positions are at `x = y = 190/2 − 12 = 83 mm`, giving a 166 × 166 mm rod rectangle.
- `frame.py` lines 20–27: frames have washer seats on `>Z` and nut seats on `<Z` for both top and bottom frames.
- `tower_assembly.py` lines 16–18: corner blocks now placed at `z = FRAME_THICKNESS/2` (3.5 mm) and `z = TOWER_HEIGHT − FRAME_THICKNESS/2` (318.0 mm), i.e., at the frame corners. **CONFIRMED: this is the mk0.7.1 fix.**

**Tension capacity:**
- M5 threaded rod tensile stress area ≈ 14.2 mm².
- 4.8 grade steel yield ≈ 320 MPa → yield load per rod ≈ 4.5 kN.
- Four rods → ≈ 18 kN total yield capacity.
- Total tower mass: modules ≈ 3.83 kg + plastic structure (estimated 1–2 kg) ≈ 5–6 kg → weight ≈ 60 N.
- **Safety factor in tension: ≈ 300.** This is massive and more than sufficient.

**Compression / buckling:**
- The rods are NOT the primary compression members. The frames are clamped by nuts; the rods are in tension. The corner blocks are now between the top and bottom frames in the load path (at the frame corners), which is an improvement over mk0.7. However, the corner blocks themselves are not heavily loaded in compression because the primary compression path is frame-to-module-frame. The corner blocks mainly serve as spacers and panel mounts.
- Euler buckling for a 321.5 mm M5 rod (slenderness λ ≈ 257) is ≈ 586 N per rod. Because the rods are in tension, this is not a design driver. **CONFIRMED: rods are in tension, buckling is irrelevant.**

**Top frame clamping error:**
- The `create_frame_ring()` function in `frame.py` places the washer seat on `>Z` and the nut seat on `<Z` for both top and bottom frames.
- The bottom frame at `z = 0` has a nut underneath (`<Z`) and a washer on top (`>Z`). This is correct.
- The top frame at `z = 321.5` has a nut seat on its bottom face (`<Z`, facing the tower interior) and a washer seat on its top face (`>Z`, facing up). With no nut on top, the top frame is pushed **upward** by an interior nut. Rod tension pulls the top frame up, but there is no counter-force from above to clamp the frame against the modules or corner blocks.
- **Finding:** The top frame is structurally under-clamped. It should have a nut seat on the top face and a washer seat on the bottom face (or the frame should be inverted). This is a **CONFIRMED design error** that will prevent proper pre-tension in the rod stack.

---

## Frame Ring Stiffness

### Assessment: ADEQUATE for axial loads, but WEAKENED by rail slots.

**Evidence:**
- `config.py` lines 79–85: `FRAME_RAIL = 14.0`, `FRAME_THICKNESS = 7.0`, `FRAME_RIB_HEIGHT = 6.0`, `FRAME_RIB_WIDTH = 5.0`, `FRAME_RIB_INSET = 18.0`.
- `frame.py` lines 12–13: outer box 190 × 190 mm, inner cutout 162 × 162 mm (190 − 2×14).
- `frame.py` lines 29–33: guide rail slots are `11 × 4 mm` (10 + 1 mm clearance) cut through the 7 mm frame thickness.

**Stiffness analysis:**
- The frame is a 190 × 190 mm rectangular ring with 14 mm wide rails and 7 mm thickness. The ribs (6 mm high, 5 mm wide) add local stiffness to the top and bottom surfaces.
- Under rod tension, the frame perimeter is loaded in tension. The ring is very stiff in its plane for this load case.
- **Vertical bending:** If loaded vertically (e.g., by a module sitting on the frame), the 7 mm thick ring acts as a plate with a large central opening. The 6 mm ribs help locally but the unsupported span is 162 mm. A 6 kg total load creates negligible stress.
- **Slot weakening:** The guide rail slots are 11 mm wide in a 14 mm rail, leaving only **(14 − 11) / 2 = 1.5 mm** of material on each side of the slot. This is a severe stress concentrator. If the metal rail is loaded by a tray and transmits force to the frame, the 1.5 mm PETG ligament could tear or creep over time.
- **Finding:** Frame ring stiffness is LIKELY adequate for the current loads, but the rail slot geometry is a **CONFIRMED stress riser** that needs reinforcement.

---

## Corner Block Compression

### Assessment: ADEQUATE for compression, but MOUNTING PROVISIONS ARE BROKEN.

**Evidence:**
- `config.py` lines 86–91: `CORNER_BLOCK_SIZE = 24.0`, `CORNER_BLOCK_HEIGHT = 28.0`, `CORNER_BLOCK_PANEL_HOLE_POINTS = [(0, -6.0), (0, 6.0)]`.
- `corner_blocks.py` lines 12–24: block is 24 × 24 × 28 mm with rod clearance, washer seat, and nut seat.
- `corner_blocks.py` lines 24–25: panel holes are drilled only on `faces(">X")` and `faces(">Y")`.
- `tower_assembly.py` lines 16–18: blocks are now at `z = 3.5` and `z = 318.0`, placing them at the frame corners.

**Compression analysis:**
- Rod clamping force is the only significant compression load. With hand-tightened M5 nuts, clamping force is typically 200–500 N per rod. The corner block wall around the rod is `(24 − 5.6) / 2 = 9.2 mm`. Compressive stress in PETG at 500 N on a 9.2 mm² wall is ≈ 54 MPa. PETG compressive yield is ≈ 50–60 MPa. This is marginal but acceptable for a printed part with some anisotropy allowance. **CONFIRMED: compression is acceptable for hand-tight clamping.**
- Dynamic or over-torqued loads could exceed PETG yield.
- **Note:** In mk0.7.1, the corner blocks are now at the frame corners (between the top/bottom frames and the module stack), which improves their structural role compared to mk0.7 where they were floating at mid-height. **CONFIRMED: placement improvement is correct.**

**Critical mounting flaw:**
- `corner_blocks.py` lines 24–25 only drill holes on the `+X` and `+Y` faces. For a block at `x = −83`, the `>X` face is at `x = −71` (pointing **inward** toward the tower center). The outer face (`<X`) at `x = −95` has **no holes**.
- The side panels are placed at `x ≈ ±96.5` (outer face of the tower). The left panel’s inner surface is at `x ≈ −95`. It needs to screw into the corner block’s outer face (`<X` at `x = −95`), but that face is solid.
- **Result:** The left side panel cannot be mounted to the left corner blocks. The rear side (if any) cannot be mounted to the rear blocks. Only the right and front faces have holes. This is a **CONFIRMED design error** that makes side panel attachment impossible on two of the four tower faces.
- Even on the faces that do have holes, the hole positions are at `z = center ± 6 mm` (28 mm block height, holes centered at ±6). The side panel mount points are at `z = panel_center ± 40.45 mm` (100.9 mm tall panel, 10 mm frame inset). The holes do not align vertically. This is a **CONFIRMED misalignment**.

---

## Guide Rail Load Path

### Assessment: METAL RAILS ARE ADEQUATE, BUT FRAME MOUNTING IS UNDEFINED.

**Evidence:**
- `config.py` lines 104–111: `METAL_RAIL_WIDTH = 10.0`, `METAL_RAIL_THICKNESS = 3.0`, `METAL_RAIL_HEIGHT = 287.5`, `METAL_RAIL_M3_SPACING = 70.0`.
- `rails.py` lines 18–27: rail is a simple 10 × 3 × 287.5 mm bar with M3 clearance holes on the 10 mm face.
- `frame.py` lines 29–33: frame has 11 × 4 mm slots for the rails, cut through the full 7 mm frame thickness.

**Rail strength:**
- Metal rail cross-section: 10 × 3 mm = 30 mm².
- In bending (tray load distributed along the rail), a 3 mm thick steel/aluminum rail is very stiff. Each rail carries at most a fraction of the heaviest tray (1.2 kg Mini PC divided by 4 rails ≈ 3 N per rail). The rail is orders of magnitude stronger than needed.

**Mounting problem:**
- The frame has a slot for the rail, but **no screw holes or insert bosses** to fasten the rail to the frame. The rail is shown as a vertical bar placed at `z = TOWER_HEIGHT / 2` in the assembly, but there is no modeled bracket, screw, or clamp holding it to the frame.
- The frame slot leaves only **1.5 mm** of PETG on each side. If the rail is inserted and loaded, the thin PETG ligaments will tear.
- **Finding:** The guide rail load path is **UNCERTAIN** because the mounting mechanism is not modeled. The frame slot geometry is **CONFIRMED** inadequate as a load-bearing joint without reinforcement or fasteners.

---

## Stability Base Analysis

### Assessment: FOOTPRINT IS ADEQUATE, BUT SECTIONAL JOINTS ARE A HINGE RISK.

**Evidence:**
- `config.py` lines 21–25: `BASE_WIDTH = 250.0`, `BASE_DEPTH = 260.0`, `FOOT_EXTENSION_X = 30.0`, `FOOT_EXTENSION_Y = 35.0`.
- `config.py` lines 344–345: `BASE_STABILITY_FOOT_OFFSET_X = 97.0`, `BASE_STABILITY_FOOT_OFFSET_Y = 102.0`.
- `config.py` lines 604–606: `STABILITY_COM_X = 0.0`, `STABILITY_COM_Y = 8.0`, `STABILITY_COM_Z = 167.18`.
- `config.py` lines 515, 608: `MINI_PC_TRAY_SERVICE_TRAVEL = 78.0`, `STABILITY_SERVICE_TRAY_Y = −78.0`.
- `config.py` line 348: `FOOT_SOCKET_DEPTH = 3.0`.
- `feet.py` lines 90–130: base is built from 5 separate sections (central, left extension, right extension, front wing, rear wing) joined by M3 fasteners at 70 mm spacing.

**Stability envelope:**
- Feet are at (±97, ±102) mm from center. The base footprint is 250 × 260 mm.
- COM is at (0, 8, 167). The COM projection is 8 mm toward the rear from the geometric center.
- Distance to front tipping line (line between front feet at y = −102): 102 + 8 = **110 mm**.
- Distance to side tipping line (line between left feet at x = −97): **97 mm**.
- With the Mini PC tray extended 78 mm forward, the COM shifts by approximately:
  - `Δy = (1.2 kg × 78 mm) / 6 kg ≈ 15.6 mm` forward.
  - New COM_y = 8 + 15.6 = 23.6 mm (rearward offset becomes smaller).
  - Distance to front tipping line = 102 − 23.6 = **78.4 mm**.
- The `STABILITY_MARGIN = 18.0` is a hardcoded value. Even with the tray extended, the margin to the front tipping line is 78.4 mm, which is comfortable. **CONFIRMED: static stability is adequate.**

**Sectional base risk:**
- The base is 5 separate PETG parts joined by M3 screws at `BASE_WING_FASTENER_SPACING = 70.0` and `BASE_WING_FASTENER_OFFSET = 18.0`.
- The wings are thin plates (10 mm thick) with M3 clearance holes. Under lateral tipping or shear, the joints can act as **hinges** because the M3 screws provide clamping but little bending stiffness across the joint.
- The `BASE_WING_OVERLAP = 12.0` mm is small. The joint is essentially a lap joint 12 mm wide.
- A 6 kg tower with COM at 167 mm height subjected to a lateral push of 10 N (≈ 1 kg side load) creates a tipping moment of 10 × 167 = 1670 N·mm. The base joints must transfer this shear. With only 2 M3 screws per joint, the joint stiffness is low.
- **Finding:** Static stability is **CONFIRMED** adequate. Joint stiffness of the sectional base is **LIKELY** insufficient to prevent flexing or hinging under lateral loads. The base should be tested as a solid plate or redesigned with tongue-and-groove or interlocking features.

**Foot socket depth:**
- `FOOT_SOCKET_DEPTH = 3.0` mm (`feet.py` line 18). The TPU foot sits in a 3 mm deep socket with no threaded insert or press-fit feature; it is retained by a single M5 screw (`FOOT_SCREW_DIAMETER = 5.3`).
- 3 mm is very shallow for a load-bearing socket. Under tipping or vibration, the TPU foot may rock in the socket, or the socket lip may deform. **LIKELY** adequate for static loads but **UNCERTAIN** for dynamic or tipped loads. **NEEDS TEST:** pull-out and rocking test of the TPU foot.

---

## Side Panel Shear Transfer

### Assessment: MIDDLE PANEL IS NON-STRUCTURAL, AND MOUNTING IS IMPOSSIBLE.

**Evidence:**
- `config.py` lines 368–401: `SIDE_PANEL_THICKNESS = 3.0`, `SIDE_SHEAR_PANEL_THICKNESS = 3.0`, `SIDE_SHEAR_PANEL_STRUCTURAL_SECTIONS = (0, 2)`.
- `side_panels.py` lines 26–33: `_is_structural_section(index)` returns `True` for indices 0 and 2 (lower and upper), `False` for index 1 (middle).
- `side_panels.py` lines 30–33: `_panel_thickness(1)` returns `SIDE_PANEL_THICKNESS = 3.0` mm; `_panel_thickness(0)` and `_panel_thickness(2)` return `SIDE_SHEAR_PANEL_THICKNESS = 3.0` mm.
- `side_panels.py` lines 36–39: `_rib_height(1)` returns `SIDE_PANEL_RIB_HEIGHT = 2.2` mm; `_rib_height(0)` and `_rib_height(2)` return `SIDE_SHEAR_PANEL_RIB_HEIGHT = 4.0` mm.
- `part_dimensions.csv` (referenced in mk0.7): middle panel Y thickness = 5.2 mm; lower/upper panel Y thickness = 13.0 mm (including overlap ribs).

**Structural discontinuity:**
- The lower and upper panels are designated as “structural” with 3.0 mm base + 4.0 mm ribs + 6.0 mm overlap ribs = 13.0 mm total thickness.
- The middle panel is designated as “non-structural” with 3.0 mm base + 2.2 mm ribs = 5.2 mm total thickness.
- **This creates a deliberate structural discontinuity in the exact center of the tower.** The tower’s shear stiffness is provided by the panels, but the middle panel is explicitly half as stiff. If the tower is loaded laterally (e.g., pushed from the side), the middle section will deform disproportionately.
- **Finding:** The non-structural middle panel is a **CONFIRMED** design weakness. The intent may have been to allow a removable service panel, but the structural cost is high.

**Mounting impossibility:**
- As detailed in the Corner Block section, the side panels have 4 mount holes per tile (at corners, inset 10 mm), but the corner blocks only have 2 holes per face at `z = center ± 6 mm`. The positions do not align.
- The frame rings have no panel mounting holes.
- The base has no panel mounting holes.
- **Result:** The side panels cannot be fastened to the structure. They are designed with M3 holes, bosses, and heat-set inserts, but there is nothing to screw them into. This is a **CONFIRMED** design error.

---

## Torsion Resistance

### Assessment: INADEQUATE. No diagonal bracing, weak middle panel, and torsion brace mounts are unimplemented.

**Evidence:**
- `config.py` lines 524–528: `TORSION_BRACE_MOUNT_ENABLED = True`, `TORSION_BRACE_HOLE_DIAMETER = M4_CLEARANCE`, `TORSION_BRACE_MOUNT_THICKNESS = 4.0`, etc.
- `side_panels.py` lines 72–91: diagonal ribs are present but thin (`rib_width = 2.4 mm` for non-structural, 3.0 mm for structural).
- The frame is a rectangular ring with no cross-bracing.
- The rear service spine is the only longitudinal member that could resist racking.

**Torsion analysis:**
- The tower is a rectangular box (190 × 190 mm) held by 4 rods at the corners. Without side panels, the frame is free to rack (twist) because the rod arrangement has no diagonal stiffness.
- The side panels provide shear stiffness if properly fastened. With the middle panel being non-structural and all panels unmountable, the effective shear stiffness is negligible.
- The rear service spine (52 × 30 × 297.5 mm) is mounted at the rear and provides some resistance to racking, but it is a plastic box with 3 mm walls, not a rigid frame.
- `TORSION_BRACE_MOUNT_ENABLED = True` in config, but **no geometry implements it** in any of the parts files (`frame.py`, `side_panels.py`, `corner_blocks.py`, `modules.py`).
- **Finding:** Torsion resistance is **LIKELY** inadequate. The tower will rack under uneven loading or lateral forces. The unimplemented torsion braces should be built or the frame should be stiffened another way. **NEEDS TEST:** physical twist test with a dial gauge.

---

## Mini PC Tray Stop Adequacy

### Assessment: MARGINAL. Small PETG bracket under impact load from a 1.2 kg tray.

**Evidence:**
- `config.py` lines 515–523: `MINI_PC_TRAY_SERVICE_TRAVEL = 78.0`, `TRAY_STOP_WASHER_DIAMETER = 12.0`, `TRAY_STOP_THICKNESS = 3.0`, `TRAY_STOP_HEIGHT = 16.0` (`MODULE_SIDE_WALL_HEIGHT + 4 = 12 + 4`).
- `modules.py` lines 124–141: stop is a 18 × 6 × 22 mm bracket with a 12 mm diameter washer boss and an M3 clearance hole.
- `part_dimensions.csv` (referenced in mk0.7): `mini_pc_tray_stop` = 18 × 6 × 22 mm.

**Load analysis:**
- The stop must arrest a 1.2 kg tray that has been pulled out 78 mm and released or bumped.
- Impact energy at low speed (e.g., 0.3 m/s) is `E = ½mv² = 0.5 × 1.2 × 0.09 = 0.054 J`. This is small, but the stop is only 6 mm wide and 3 mm thick in the load direction.
- The stop is mounted by a single M3 screw. The PETG bracket could crack at the screw hole or the washer boss could shear off.
- The 12 mm washer spreads the load over a small area. The effective shear area of the boss is small.
- **Finding:** The tray stop is **LIKELY** adequate for gentle handling but **UNCERTAIN** for accidental drops or bumps. A metal stop or a larger PETG bracket with two screws would be safer. **NEEDS TEST:** drop-test the tray against the stop.

---

## Rear Service Spine Structural Role

### Assessment: PROVIDES SOME BRACING, BUT PRIMARILY A CABLE CHANNEL.

**Evidence:**
- `config.py` lines 456–512: `REAR_SPINE_WIDTH = 52.0`, `REAR_SPINE_DEPTH = 30.0`, `REAR_SPINE_HEIGHT = 297.5`, `REAR_SPINE_STRUCTURAL_WALL = 3.4`, `REAR_SPINE_RIB_THICKNESS = 3.0`, `REAR_SPINE_RIB_HEIGHT = 5.0`.
- `REAR_SPINE_STRUCTURAL_MOUNT_Z` has 7 mounting points at ±126, ±84, ±42, 0 mm.
- `part_dimensions.csv` (referenced in mk0.7): `rear_service_spine` envelope = 80 × 40 × 297.5 mm (including mounting tabs).

**Structural contribution:**
- The spine is a 3.4 mm wall plastic box with 3 mm ribs and 7 mounting tabs along its height. It mounts to the rear of the tower.
- It acts as a backplane that resists parallelogram deformation (racking) of the tower. The 7 mounting points give it a reasonable shear transfer path to the frame or modules.
- However, it is still a plastic box. Its stiffness is much lower than a metal backplane. The 3.4 mm walls will flex under torsion.
- It also serves as the cable management channel and the backstop for the trays (the tray rear stops hit it).
- **Finding:** The rear service spine contributes **LIKELY** modest torsion and shear resistance, but it is **not a primary structural member**. It should be treated as a service accessory with secondary structural benefit. If the design depends on it for stiffness, the dependence is too high.

---

## Blockers

These issues must be resolved before any physical build or further revision:

1. **Side panel mounting is impossible.** Corner blocks lack holes on `−X` and `−Y` faces, and the holes that do exist are misaligned with the panel mount points. The frame has no panel holes. The side panels cannot be attached.
2. **Top frame clamping is incorrect.** The top frame has a nut seat on the bottom face and a washer seat on the top face. A topmost frame needs a nut on top to pull it down against rod tension. The current geometry cannot be properly clamped.
3. **Tray vertical support is missing.** The metal guide rails are vertical bars with no horizontal shelves or brackets. The trays are horizontal plates with no modeled support from below (except the bottom frame for the lowest tray). A 1.2 kg Mini PC tray has no visible support mechanism.
4. **Torsion brace mounts are unimplemented.** `config.py` enables them, but no geometry exists.

---

## Recommendations

### Immediate (mk0.7.1 → mk0.8)
1. **Fix corner block panel holes:**
   - Add holes on all four side faces (`<X`, `>X`, `<Y`, `>Y`).
   - Align the hole positions with the side panel mount points (or vice versa).
   - Add corresponding threaded inserts or nut traps in the corner blocks for M3 screws.
2. **Fix top frame clamping:**
   - Either add a nut seat on the top face of the top frame, or model the top frame as an inverted copy of the bottom frame so the nut seat is on the outer face.
3. **Add tray support mechanism:**
   - Model horizontal shelves or ledges on the metal guide rails at each tray height.
   - Alternatively, add intermediate frame rings at each module height to support the trays from below.
   - The current vertical-bar rails cannot support horizontal trays.
4. **Implement torsion braces or cross-bracing:**
   - If `TORSION_BRACE_MOUNT_ENABLED = True`, model the mount bosses and the brace geometry (e.g., a diagonal rod or strap between opposite corners).
   - Alternatively, make the middle side panel structural and ensure all panels are properly fastened.
5. **Reinforce frame rail slots:**
   - Add material around the guide rail slots. A 1.5 mm ligament is too thin.
   - Consider metal threaded inserts or washers at the slot edges to prevent tearing.
6. **Deepen the foot socket or add an insert:**
   - 3.0 mm is too shallow for a load-bearing TPU socket. Increase to at least 6 mm or add a dovetail/press-fit feature.

### Short-term (mk0.8)
7. **Strengthen the sectional base:**
   - Replace the 5-part base with a single plate, or add tongue-and-groove interlocks and more fasteners at the joints.
   - Consider a metal bottom plate for stiffness.
8. **Improve the tray stop:**
   - Use two M3 screws or a larger bracket.
   - Consider a metal stop or a PETG stop with a steel insert.
9. **Add FEA or physical test plan:**
   - A simple torsion test (apply a known side load and measure deflection) would validate the side panel and spine stiffness.
   - A drop test of the Mini PC tray would validate the stop.
   - A foot pull-out test would validate the socket depth.

### Long-term
10. **Reduce reliance on plastic for structural stiffness:**
    - The `AGENTS.md` philosophy states “plastic parts are connectors/positioners, NOT primary load-bearing elements.” The current design violates this by making the side panels, rear spine, and base critical to stiffness. Add metal plates or brackets where possible.

---

*Review completed. All findings are based on hand calculations and inspection of the CAD source code. No FEA was performed.*
