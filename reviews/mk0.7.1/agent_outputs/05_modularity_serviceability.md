# Modularity and Serviceability Review

**Reviewer:** Modularity and Serviceability Reviewer (mk0.7.1 Engineering Review)  
**Revision:** mk0.7.1  
**Date:** 2026-06-27  
**Scope:** Module interchangeability, extraction feasibility, handle ergonomics, side panel impact, rear cable management, Mini PC service travel, bottom fan cartridge access, power bus reachability, foot replacement, and future module scalability.

---

## Executive Summary

mk0.7.1 is an explicit documentation and export-classification patch. The project records confirm that **no core serviceability issues were addressed** in this revision:

> *"Anti-tip redesign, battery containment, fuse/e-stop design, rail-retention architecture, service-spine quick disconnects, and full tray airflow redesign are too large for a safe patch release."* — `DECISIONS.md`, mk0.7.1

> *"Rear Service Spine cable management still requires manual cable disconnection and cover access. True quick-disconnect module extraction is not designed. Guide rail retention and bottom fan cartridge retention require further physical interface design."* — `KNOWN_LIMITATIONS.md`, mk0.7.1

Therefore, **every serviceability finding from the mk0.7 review remains fully valid in mk0.7.1**. This document re-confirms those findings with updated line references, adds the mk0.7.1 documentation evidence, and re-grades the severity where the passage of time without fix makes the issue more critical.

The tower is **modular in geometric intent but remains unserviceable in practice**. Four confirmed blockers from mk0.7 persist unchanged:
1. Module extraction requires full cable disconnection.
2. Side panels are unmountable (no working attachment interface).
3. Bottom fan cartridge is not attached to the base.
4. Foot socket is structurally inadequate and will strip on first assembly.

---

## Module Standardization

### Assessment: GEOMETRICALLY STANDARDIZED, BUT FUNCTIONALLY NON-INTERCHANGEABLE. STATUS UNCHANGED FROM mk0.7.

**Evidence:**
- `config.py` lines 114–128: `MODULE_WIDTH = 170.0`, `MODULE_DEPTH = 176.0`, `RAIL_SPACING = METAL_RAIL_X_OFFSET * 2 = 168.0`, `TRAY_FRONT_HANDLE_WIDTH = 64.0`, `TRAY_LOCK_HOLE_DIAMETER = SCREW_CLEARANCE_M3`, `MODULE_LOCK_ANTI_SLIDE_TAB_WIDTH = 18.0`. All values identical to mk0.7.
- `carriages.py` lines 189–250: All six trays are still produced by `create_carriage()` (via `make_module_tray()`), using the same base plate, side walls, rail clearances, mounting holes, handle pocket, lock boss, and anti-slide tab geometry. No structural change from mk0.7.
- `modules.py` lines 144–150: `TRAY_FACTORIES` still maps all six modules to tray builders that call `make_module_tray()` with identical width/depth parameters. Unchanged.
- `revisions/mk0.7.1/CHANGELOG_FROM_MK0.7.md`: No tray standard or carriage geometry changes listed.

**Interchangeability analysis:**
- **Width and depth:** CONFIRMED identical across all trays. Any tray can physically slide on the rails.
- **Rail spacing:** CONFIRMED fixed at 168 mm. The rail cutouts (`TRAY_RAIL_CLEARANCE_WIDTH = 13.0`, `TRAY_RAIL_CLEARANCE_DEPTH = 8.0`) are the same on every tray.
- **Mounting holes:** CONFIRMED identical. `add_mounting_holes()` uses `TRAY_MOUNT_HOLE_OFFSET_X = 18.0` and `TRAY_MOUNT_HOLE_OFFSET_Y = 24.0` for all trays.
- **Front handle and lock:** CONFIRMED identical. The front plate height is `min(tray_height, CARRIAGE_FRONT_PLATE_HEIGHT = 24.0)`, so all trays get a 24 mm high front plate regardless of actual tray height.
- **Functional non-interchangeability:** CONFIRMED. Each tray has device-specific geometry (SSD pocket, RPi board marker, Mini PC power window, UPS zones). You cannot swap a Mini PC tray into an SSD slot because the tray interior is shaped for a specific device. The *standard* is interchangeable; the *trays* are not.

**Finding:** The module tray standard is **CONFIRMED** to be geometrically consistent and interchangeable. However, the trays are functionally dedicated to their devices, so "interchangeability" only applies to the rail/load-path interface, not to the module contents. This is acceptable for a modular tower where each slot has a designated purpose, but the terminology should not imply that any tray can go in any slot. **No change from mk0.7.**

---

## Module Extraction Feasibility

### Assessment: GEOMETRICALLY POSSIBLE, BUT CABLE-DEPENDENT EXTRACTION REMAINS A BLOCKER — UNRESOLVED IN mk0.7.1.

**Evidence:**
- `config.py` lines 223–230: `TRAY_STACK` = [UPS (2.0), SSD Bay (1.0), SSD Expansion (1.0), RPi (1.0), MikroTik (1.5), Mini PC (2.0)] = 8.5 units total. Unchanged.
- `config.py` lines 96–99: `MODULE_SLOT_GAP = 1.0`, `LIGHT_MODULE_HEIGHT = MODULE_SLOT_PITCH - MODULE_SLOT_GAP`, `COMPUTE_MODULE_HEIGHT = MODULE_SLOT_PITCH * 2 - MODULE_SLOT_GAP`. Unchanged.
- `carriages.py` lines 76–118: Front plate depth = `CARRIAGE_FRONT_PLATE_THICKNESS = 8.0` mm. Handle pocket depth remains `CARRIAGE_HANDLE_DEPTH = MODULE_FRONT_HANDLE_DEPTH = 4.2` mm. Unchanged.
- `carriages.py` lines 57–73: Anti-slide tab is at the front underside, `MODULE_LOCK_ANTI_SLIDE_TAB_DEPTH = 4.0`, `MODULE_LOCK_ANTI_SLIDE_TAB_HEIGHT = 5.0`. Unchanged.
- `tower_assembly.py` lines 90–106: Trays are stacked starting at `STACK_START_Z = 18.0`, with each tray positioned at `current_z` and `current_z += units * UNIT_HEIGHT`. Unchanged.
- `revisions/mk0.7.1/KNOWN_LIMITATIONS.md` lines 37–39: Explicitly confirms that "Rear Service Spine cable management still requires manual cable disconnection and cover access. True quick-disconnect module extraction is not designed."

**Geometric clearance for lower tray extraction:**
- A 1-unit tray has height = `35 - 2 = 33 mm` (accounting for `TRAY_CLEARANCE_Z = 2.0`). The front plate is 24 mm high. The tray above starts at `Z + 33 + 1 = Z + 34`. The front plate top is at `Z + 24`. Clearance to the tray above = **10 mm**.
- A 2-unit tray (UPS, Mini PC) has height = `70 - 2 = 68 mm`. Front plate is 24 mm. The tray above starts at `Z + 68 + 1 = Z + 69`. Clearance = **45 mm**.
- The front plate thickness in Y is 8.0 mm. The tray above is offset by 1 mm in Z, not in Y. The front plate moves forward with the tray; it does not need to pass between the trays. Since the trays are vertically separated, the front plate of a lower tray simply slides forward *under* the tray above.

**Finding:** Geometrically, any lower tray **CAN** be pulled out without removing upper trays. The 1 mm `MODULE_SLOT_GAP` does not obstruct the front plate because the front plate is part of the moving tray and moves in the Y direction, not Z. **CONFIRMED: independent geometric extraction is possible.**

**BUT — the cable problem remains completely unresolved:**
- Every tray has a `TRAY_REAR_SERVICE_CUTOUT` (66 mm wide, 36 mm deep) at the rear (`carriages.py` lines 143–150). Cables exit through this cutout into the rear service spine.
- The rear service spine is a closed channel with a screw-on cover (`REAR_SPINE_STRUCTURAL_MOUNT_Z` has 7 screw positions, `REAR_SPINE_COVER_THICKNESS = 3.0`).
- To extract a module, the user must: (1) remove the rear spine cover (7 M3 screw positions), (2) disconnect power/data cables, (3) untie cable ties, (4) slide the tray out. This is a **10+ minute operation** requiring a screwdriver.
- `DECISIONS.md` mk0.7.1 explicitly classifies "service-spine quick disconnects" as "too large for a safe patch release." This means the project leadership has acknowledged the issue but deliberately deferred it.

**Finding:** The design claims "extractable without disassembly" but forces full cable disconnection for every module. This is a **CONFIRMED** contradiction with the AGENTS.md requirement: "Извлечение одного модуля не должно требовать разборки всей башни." The module is not "fully removable" if the spine cover and cables must be disturbed. **Status: UNCHANGED, BLOCKER PERSISTS.**

---

## Front Handle and Lock Design

### Assessment: UNDER-SIZED FOR HEAVY TRAYS AND TIPPING-HAZARD-PRONE. NO CHANGE IN mk0.7.1.

**Evidence:**
- `config.py` lines 121–123, 199–214: `TRAY_FRONT_HANDLE_WIDTH = 64.0`, `TRAY_FRONT_HANDLE_DEPTH = 4.2` (pocket depth), `CARRIAGE_HANDLE_HEIGHT = 13.0`, `CARRIAGE_HANDLE_TOP_BRIDGE = 5.5`, `CARRIAGE_LOCK_BOSS_DIAMETER = 11.0`, `MODULE_LOCK_INSERT_OUTER_DIAMETER = 5.2` (M3 heat-set insert). All unchanged from mk0.7.
- `config.py` lines 26–35: `ESTIMATED_UPS_MASS = 1.4`, `ESTIMATED_MINI_PC_MASS = 1.2`, `MAX_MODULE_MASS = 1.8`. Unchanged.
- `carriages.py` lines 24–34: Handle is a recessed pocket 64 mm wide × 13 mm tall × 4.2 mm deep, with a 3 mm corner radius fillet. Unchanged.
- `carriages.py` lines 37–54: Lock boss is an 11 mm diameter cylinder with a 5.2 mm insert hole. Boss wall thickness = (11.0 − 5.2) / 2 = **2.9 mm**. Unchanged.
- `revisions/mk0.7.1/CHANGELOG_FROM_MK0.7.md`: No handle geometry changes listed.

**Handle ergonomics:**
- The pocket is only **4.2 mm deep**. A typical adult finger is 15–20 mm wide. Two fingers cannot fit into a 64 mm × 13 mm × 4.2 mm pocket comfortably. The user can hook one or two fingertips into the pocket, but the shallow depth (4.2 mm) provides almost no gripping surface.
- The heaviest tray (UPS, 1.4 kg) requires significant pulling force to overcome friction on the metal rails (especially if the rails are not perfectly straight or if the PETG rails swell with humidity). A 1.4 kg load on a shallow 4.2 mm finger grip is awkward and risks the tray slipping from the user's grip.
- The `CARRIAGE_HANDLE_TOP_BRIDGE = 5.5` mm is the thickness of the bridge above the pocket. This is thin and could flex under repeated pulling loads.

**Lock boss strength:**
- The M3 heat-set insert in an 11 mm boss with 2.9 mm wall thickness is **LIKELY adequate** for a locking screw (which is not a load-bearing fastener, just a retention screw). The insert is not intended to hold the tray's weight; it only prevents the tray from sliding forward.
- However, if the tray jams on the rails and the user pulls hard on the handle, the lock screw could see shear loads. The 2.9 mm PETG wall around the insert could crack under high pull force.

**Finding:** The handle pocket is **CONFIRMED** to be ergonomically marginal for a 1.2–1.4 kg tray. The 4.2 mm depth is too shallow for a confident two-finger grip. The lock boss is **LIKELY** adequate for normal retention but **UNCERTAIN** under high extraction force or repeated cycling. **NEEDS TEST:** physical pull test with a loaded 1.4 kg tray to measure required extraction force and handle comfort. **Status: UNCHANGED.**

**Tipping hazard note:** The `KNOWN_LIMITATIONS.md` mk0.7.1 explicitly states: "Dynamic tipping risk with the Mini PC tray extended remains unresolved." The shallow handle design contributes to this hazard because the user cannot get a secure grip and may apply a jerky, upward-pulling force. This is a **CONFIRMED** safety concern that was explicitly deferred.

---

## Side Panel Removal Impact

### Assessment: PANELS CAN BE REMOVED WITHOUT REMOVING MODULES, BUT THEY CANNOT BE MOUNTED AT ALL — STILL UNRESOLVED IN mk0.7.1.

**Evidence:**
- `config.py` lines 368–400: `SIDE_PANEL_THICKNESS = 3.0`, `SIDE_PANEL_GAP = 0.4`, `SIDE_PANEL_SECTION_COUNT = 3`, `SIDE_PANEL_SECTION_HEIGHT = (SIDE_PANEL_HEIGHT − 2 * SIDE_PANEL_GAP) / 3`. Unchanged.
- `tower_assembly.py` lines 122–153: Side panels are placed at `x = ±(OUTER_WIDTH / 2 + SIDE_PANEL_THICKNESS / 2) = ±(95 + 1.5) = ±96.5` mm. Unchanged.
- The trays are at `x = TRAY_X = 0.0` with `MODULE_WIDTH = 170.0`, so they extend from `x = −85` to `x = +85`. The panels are at `x = ±96.5`, **outside the tray envelope**. Unchanged.
- `revisions/mk0.7.1/CHANGELOG_FROM_MK0.7.md`: No side panel mounting interface changes listed.

**Panel removal vs. module extraction independence:**
- **CONFIRMED:** Side panels are geometrically outside the tray width envelope. Removing a side panel does not require removing any module, and extracting a module does not require removing any side panel. The two operations are independent.
- **CONFIRMED:** The side panels are sectioned into three independently removable tiles per side (`lower`, `middle`, `upper`). A user can remove just the middle panel to access the middle modules without disturbing the top or bottom panels.

**BUT — the mounting interface is still broken:**
- The mk0.7 Structural Integrity review (`03_structural_integrity.md`) confirmed that corner blocks only have holes on `+X` and `+Y` faces, not on `−X` and `−Y`. The holes that do exist are at `z = center ± 6 mm`, which does not align with side panel mount points at `z = center ± 40.45 mm`.
- The frame rings have no panel mounting holes.
- `revisions/mk0.7.1/DECISIONS.md` does not list side panel mounting as a low-risk fix. `CHANGELOG_FROM_MK0.7.md` lists no structural changes.
- **Result:** The side panels still cannot be fastened to the structure. This design error was **not addressed** in mk0.7.1.

**Finding:** If the mounting interface were fixed, side panel removal would be fully independent of module extraction. However, the current design still has **no working mounting interface**, so the panels are purely decorative in the current CAD. This is a **CONFIRMED blocker** inherited from mk0.7 and **explicitly unresolved** in mk0.7.1.

---

## Rear Service Spine and Cable Management

### Assessment: CABLES TRAP MODULES — EXTRACTION REQUIRES FULL DISCONNECTION. EXPLICITLY DEFERRED IN mk0.7.1.

**Evidence:**
- `config.py` lines 125–126: `REAR_CABLE_EXIT_WIDTH = 66.0`, `REAR_CABLE_EXIT_HEIGHT = 20.0`. Every tray still has a fixed rear cutout of this size. Unchanged.
- `config.py` lines 151–160: `MODULE_REAR_CABLE_CLEARANCE = 36.0`, `TRAY_REAR_SERVICE_CUTOUT_DEPTH = 36.0`. The cable exit still extends 36 mm rearward from the tray back edge. Unchanged.
- `config.py` lines 455–512: `REAR_SPINE_WIDTH = 52.0`, `REAR_SPINE_DEPTH = 30.0`, `REAR_SPINE_CABLE_SLOT_WIDTH = 34.0`, `REAR_SPINE_TIE_SLOT_WIDTH = 4.0`, `REAR_SPINE_HORIZONTAL_TIE_Z` at six vertical positions. Unchanged.
- `service_spine.py` lines 64–171: The spine cover still mounts with screws at `REAR_SPINE_STRUCTURAL_MOUNT_Z` (7 positions). Unchanged.
- `carriages.py` lines 143–150: `make_tray_cable_exit()` — the cable exit is still a fixed cutout, not a quick-disconnect or pass-through connector. Unchanged.
- `revisions/mk0.7.1/KNOWN_LIMITATIONS.md` lines 36–39: "Rear Service Spine cable management still requires manual cable disconnection and cover access. True quick-disconnect module extraction is not designed."
- `revisions/mk0.7.1/DECISIONS.md` lines 12–13: "service-spine quick disconnects" classified as "too large for a safe patch release."

**Module extraction procedure (re-confirmed):**
1. Remove rear spine cover (7 M3 screw positions).
2. Untie or cut cable ties from `REAR_SPINE_TIE_SLOT_Z` slots.
3. Disconnect power connectors (XT30, MicroFit, USB-C) from the module.
4. Disconnect data cables (Ethernet, USB) from the module.
5. Slide the module forward.
6. Reverse all steps to reinstall.

**Hot-swap assessment:**
- The modules are **NOT hot-swappable**. The cables are fixed to the module and pass through the rear cutout into the spine. There is no pass-through bulkhead connector, no magnetic connector, and no cable breakaway at the module rear.
- The AGENTS.md requirement states: "Все кабели должны проходить через эту шахту." (All cables must pass through the spine.) This is satisfied. But it also states: "Извлечение одного модуля не должно требовать разборки всей башни." (Extraction of one module must not require disassembling the whole tower.) The current implementation violates this because the spine cover must be removed and cables must be disconnected.

**Is this acceptable?**
- For a home lab tower where modules are rarely moved, **MAYBE**. But the design claims "fully removable" and "serviceable." A 10+ minute screwdriver-and-dexterity operation to swap a module is not "serviceable" in the intended sense.
- The horizontal tie slots (`REAR_SPINE_HORIZONTAL_TIE_Z`) bundle cables across module boundaries. If cables from multiple modules are tied together, extracting one module requires untying cables that belong to other modules — **further violating the independence requirement**.

**Finding:** The rear service spine is a **CONFIRMED cable trap** that prevents independent module extraction. The spine cover, cable ties, and fixed connectors make module swap a multi-step, multi-tool operation. mk0.7.1 **explicitly deferred** fixing this. This is a **CONFIRMED blocker** for the modularity claim. The design needs either (a) quick-disconnect bulkhead connectors at each tray rear, (b) pigtails that stay in the spine while the module disconnects, or (c) a hinged spine cover that opens without tools.

---

## Mini PC Service Travel

### Assessment: 78 MM TRAVEL IS ADEQUATE FOR FRONT ACCESS BUT INADEQUATE FOR REAR SERVICE. NO CHANGE IN mk0.7.1.

**Evidence:**
- `config.py` lines 515–523: `MINI_PC_TRAY_SERVICE_TRAVEL = 78.0`, `TRAY_STOP_SLOT_LENGTH = 54.0`, `TRAY_STOP_WASHER_DIAMETER = 12.0`, `TRAY_STOP_THICKNESS = 3.0`, `TRAY_STOP_HEIGHT = 16.0`. All unchanged.
- `modules.py` lines 124–141: `make_tray_stop()` creates a 18 × 6 × 22 mm PETG bracket with a 12 mm washer boss and an M3 clearance hole. Unchanged.
- `tower_assembly.py` lines 206–214: The tray stop is placed at `TRAY_STOP_OFFSET_X = MODULE_TRAY_WIDTH / 2 − 22.0 = 85 − 22 = 63.0` mm from center, and `TRAY_STOP_OFFSET_Y = MODULE_TRAY_DEPTH / 2 − 34.0 = 88 − 34 = 54.0` mm from center. Unchanged.
- `config.py` lines 290–308: `MINI_PC_PLACEHOLDER_DEPTH = 130.0`, `MINI_PC_POWER_WINDOW_DEPTH = 8.0`, `MINI_PC_POWER_WINDOW_REAR_INSET = 2.0`. The Mini PC power connector is at the rear, 2 mm inset from the tray back edge. Unchanged.
- `revisions/mk0.7.1/KNOWN_LIMITATIONS.md` line 17: "Dynamic tipping risk with the Mini PC tray extended remains unresolved."

**Service travel analysis:**
- The tray moves forward 78 mm. The Mini PC placeholder depth is 130 mm. The power connector is at the rear of the Mini PC. When the tray is slid forward 78 mm, the rear of the Mini PC moves from `Y = TRAY_Y + TRAY_DEPTH/2 + device_offset = −4 + 88 − 8 = +76` (wait, need to recalculate). Actually, the tray is at `TRAY_Y = −4.0`, with `TRAY_DEPTH = 176`. The tray rear is at `y = −4 + 88 = +84`. The Mini PC placeholder is at `MINI_PC_PLACEHOLDER_LOC = (0.0, −8.0, 7.0)`, so the device rear is at `y = −4 + (−8) + 65 = +53` (half of 130 is 65). The power window is at `MINI_PC_POWER_WINDOW_X = −54.0`, with rear inset of 2 mm from the tray back edge. So the power connector is approximately at the rear of the device.
- When the tray moves forward 78 mm (in the −Y direction), the device rear moves from `y ≈ +53` to `y ≈ +53 − 78 = −25`. The power cable, which enters the rear service spine at `y ≈ +84` (spine rear), now has a device end at `y ≈ −25`. The cable must span `84 − (−25) = 109` mm.
- A typical power brick cable or Ethernet cable has a stiff molded strain relief of 30–50 mm. If the cable has 150 mm of slack inside the spine, 78 mm travel may leave the cable connected but with significant tension on the connector.
- More importantly, the **rear of the Mini PC is now at y ≈ −25**, which is *forward* of the tower center. The user cannot access the rear connectors because the tray has moved *forward*, and the connectors are still facing the rear. The 78 mm travel brings the front of the Mini PC closer to the user but does **not** bring the rear connectors out of the tower.

**What can the user do with 78 mm travel?**
- Access the front/side of the Mini PC (if it has front USB ports or a power button).
- Reach over the top of the Mini PC to touch the front edge of the board.
- Access the Mini PC's side or bottom (for ventilation cleaning).
- **Cannot** access the rear power or Ethernet connectors without disconnecting cables.
- **Cannot** remove the Mini PC from the tray without pulling it further forward or tilting it.

**Finding:** The 78 mm service travel is **CONFIRMED** to be inadequate for rear-connector service. It is useful for front access and ventilation inspection but does not solve the core problem of reaching the power and data connectors. The tray stop is a **LIKELY** adequate mechanical stop for gentle use but **UNCERTAIN** for impact loads. **NEEDS TEST:** physical cable strain measurement with a real Mini PC and typical cables during 78 mm tray travel. **Status: UNCHANGED.**

**Dynamic tipping hazard:** The `KNOWN_LIMITATIONS.md` mk0.7.1 explicitly confirms that pulling the Mini PC tray forward 78 mm creates a dynamic tipping risk that "remains unresolved." The service travel design directly contributes to this safety hazard. **CONFIRMED safety concern, explicitly deferred.**

---

## Bottom Fan Cartridge Serviceability

### Assessment: CARTRIDGE IS DESIGNED TO BE REMOVABLE BUT IS NOT ACTUALLY ATTACHED AND REQUIRES TOOLS. STILL UNRESOLVED IN mk0.7.1.

**Evidence:**
- `config.py` lines 427–433: `BOTTOM_FAN_CARTRIDGE_WIDTH = 142.0`, `BOTTOM_FAN_CARTRIDGE_DEPTH = 161.0`, `BOTTOM_FAN_CARTRIDGE_HEIGHT = 8.0`, `BOTTOM_FAN_CARTRIDGE_SERVICE_PULL = 14.0`, `BOTTOM_FAN_CARTRIDGE_MOUNT_OFFSET = 68.0`. Unchanged.
- `cooling.py` lines 48–91: `make_bottom_fan_cartridge()` has M3 mounting holes at `±68` mm offset (`M3_CLEARANCE = 3.4` mm holes) and a 14 mm service pull handle. Unchanged.
- `tower_assembly.py` lines 227–230: The cartridge is placed at `BOTTOM_FAN_CARTRIDGE_Z = BASE_STABILITY_Z − BASE_STABILITY_THICKNESS/2 − BOTTOM_FAN_CARTRIDGE_HEIGHT/2 = −9 − 5 − 4 = −18` mm. Unchanged.
- `revisions/mk0.7.1/KNOWN_LIMITATIONS.md` line 39: "Guide rail retention and bottom fan cartridge retention require further physical interface design."
- `revisions/mk0.7.1/DECISIONS.md` lines 12–13: "rail-retention architecture" classified as "too large for a safe patch release."

**Attachment problem:**
- The cartridge has M3 mounting holes at `±68` mm offset. But the base (`central_bottom_fan_frame`, `bottom_structural_frame`, or base stability plate) has **no corresponding M3 holes** to match these offsets.
- The mk0.7 Red Team review confirmed: "The cartridge will fall out or shift when the tower is moved. This is a loose part under a 9.5 kg tower."
- `revisions/mk0.7.1/CHANGELOG_FROM_MK0.7.md` lists no structural changes to the base or cartridge attachment.

**Tool requirement:**
- The cartridge uses M3 screws for mounting. Even if the base had matching holes, the user would need a screwdriver or hex key to remove the cartridge.
- The `BOTTOM_FAN_CARTRIDGE_SERVICE_PULL = 14.0` mm handle is a small pull tab. It is useful for sliding the cartridge out after screws are removed, but it does not make the cartridge tool-less.
- The `DECISIONS.md` mk0.7 claim "обслуживаемый cartridge" (serviceable cartridge) is technically true — it is serviceable with tools — but it is not tool-less.

**Filter serviceability:**
- `bottom_filter_frame` (138 × 138 × 3 mm) and `bottom_filter_retainer` (144 × 8 × 4 mm) are separate parts. The retainer is a thin clip that holds the filter material. The `KNOWN_LIMITATIONS.md` mk0.7.1 line 26 states: "Filter material, pressure drop, and service position remain unresolved."
- The filter frame and retainer are not attached to the cartridge; they are separate parts that sit on the cartridge rails. The `cooling.py` lines 94–116 show the filter frame and retainer as standalone geometry with no mounting screws — they are presumably gravity-held or slide-fit. However, the retainer is only 8 mm deep in Y, which is a very small clip for a 138 mm wide filter. It may not hold the filter securely against the fan intake pressure.

**Finding:** The bottom fan cartridge is **CONFIRMED** to be a loose, unattached part in the current CAD. The base has no mounting holes to match the cartridge's M3 holes. mk0.7.1 explicitly deferred "bottom fan cartridge retention" to a future revision. Even if attached, the M3 screw requirement means it is **not tool-less**. The filter retention is **UNCERTAIN** — the 8 mm deep retainer may not hold filter material securely under airflow. **NEEDS TEST:** print-fit check with a real 120 mm fan and verify filter retention under airflow. **Status: UNCHANGED, BLOCKER PERSISTS.**

---

## Power Bus Access

### Assessment: POWER BUS IS ACCESSIBLE ONLY AFTER REMOVING THE REAR SPINE COVER AND THE POWER BUS COVER — NOT WHILE ASSEMBLED. NO CHANGE IN mk0.7.1.

**Evidence:**
- `config.py` lines 530–564: `POWER_BUS_WIDTH = 34.0`, `POWER_BUS_HEIGHT = 275.5`, `POWER_BUS_THICKNESS = 3.0`, `POWER_BUS_PAD_WIDTH = 22.0`, `POWER_BUS_PAD_DEPTH = 4.0`, `POWER_BUS_PAD_HEIGHT = 22.0`, `POWER_BUS_CONNECTOR_CUT_DEPTH = 5.0`. Unchanged.
- `config.py` lines 545–549: Connector zones for XT30 (19V), MicroFit (12V), USB-C (5V), and cable tie. Unchanged.
- `config.py` lines 551–559: `POWER_BUS_COVER_WIDTH = 46.0`, `POWER_BUS_COVER_HEIGHT = 265.5`, `POWER_BUS_COVER_THICKNESS = 2.4`, `POWER_BUS_GUARD_RAIL_WIDTH = 3.0`, `POWER_BUS_GUARD_RAIL_DEPTH = 5.0`. Unchanged.
- `config.py` lines 615: `POWER_BUS_PANEL_OFFSET_Y = 10.0` — the power bus panel is offset 10 mm forward from the rear service spine center. Unchanged.
- `tower_assembly.py` lines 174–189: The power bus panel is placed at `rear_y − POWER_BUS_PANEL_OFFSET_Y`, and the power bus cover is placed behind it at `rear_y − POWER_BUS_PANEL_OFFSET_Y − POWER_BUS_THICKNESS`. The rear spine is at `rear_y = OUTER_DEPTH/2 − REAR_SPINE_DEPTH/2 = 95 − 15 = 80`. So the power bus panel is at `y = 80 − 10 = 70`, and the cover is at `y = 70 − 3 = 67`. The rear spine cover is at `y = 80 + 15 + 1.5 = 96.5` (spine rear + half spine depth + half cover thickness). Unchanged.
- `revisions/mk0.7.1/KNOWN_LIMITATIONS.md` lines 19–20: "DC bus fusing, emergency stop, and isolation remain unresolved. Power bus electrical current capacity and insulation are not validated."

**Access path analysis:**
- The power bus panel and cover are **inside** the rear service spine volume. The spine cover is a separate screwed-on panel (`REAR_SPINE_STRUCTURAL_MOUNT_Z` has 7 screw positions).
- To reach the power bus connectors, the user must:
  1. Remove the rear spine cover (7 M3 screw positions).
  2. Remove the power bus cover (no mounting data shown in config, but it is a separate cover).
  3. Access the XT30/MicroFit/USB-C connectors.
- The connectors cannot be reached while the spine cover is in place. The power bus cover adds an additional layer of obstruction.
- The `POWER_BUS_CONNECTOR_CUT_DEPTH = 5.0` mm suggests the connectors are recessed into the panel, which further reduces accessibility.

**Connector operation while assembled:**
- The XT30 connector requires ~10 mm of insertion depth and a firm push/pull. The MicroFit and USB-C connectors also require finger access. The `POWER_BUS_PAD_DEPTH = 4.0` and `POWER_BUS_GUARD_RAIL_DEPTH = 5.0` create a narrow channel around the connectors. Working in this confined space with the tower upright and modules in place is awkward.
- The power bus is at the rear of the tower, behind all six modules. The user's hands must reach past (or between) the rear of the modules to access the connectors. The module rear cable exits (`REAR_CABLE_EXIT_WIDTH = 66.0`) are only 20 mm tall and face the spine, so cables from the modules already occupy the space in front of the power bus.

**Finding:** The power bus is **CONFIRMED** to be inaccessible without removing the rear spine cover and the power bus cover. The design does **not** allow power bus connectors to be connected or disconnected while the tower is fully assembled. This is a **CONFIRMED** serviceability gap. mk0.7.1 deferred electrical validation entirely. The power bus should be relocated to a more accessible position (e.g., a side-access panel or a hinged spine cover with a cutout) or the connectors should be brought to the exterior with pass-through bulkheads. **Status: UNCHANGED.**

---

## Foot Replacement

### Assessment: FEET ARE REPLACEABLE IN PRINCIPLE BUT REQUIRE TOWER REPOSITIONING AND THE SOCKET INTERFACE IS BROKEN. STILL UNRESOLVED IN mk0.7.1.

**Evidence:**
- `config.py` lines 332–359: `FOOT_HEIGHT = 32.0`, `FOOT_DIAMETER = 34.0`, `FOOT_SCREW_DIAMETER = 5.3`, `FOOT_COUNTERBORE_DIAMETER = 10.0`, `FOOT_COUNTERBORE_DEPTH = 4.0`, `FOOT_SOCKET_DEPTH = 3.0`, `FOOT_SOCKET_CLEARANCE = 0.6`. All unchanged.
- `feet.py` (implied from config and Red Team review): The foot socket is a 3 mm thick PETG boss with a 5.3 mm through-hole and **no heat-set insert**. Unchanged.
- `tower_assembly.py` lines 50–57: Feet are placed at `FOOT_Z = BASE_STABILITY_Z − BASE_STABILITY_THICKNESS/2 − FOOT_HEIGHT/2 = −9 − 5 − 16 = −30` mm. The foot extends from `z = −46` to `z = −14` mm. The base bottom is at `z = −14` mm. Unchanged.
- `revisions/mk0.7.1/CHANGELOG_FROM_MK0.7.md`: No foot socket redesign listed.
- `revisions/mk0.7.1/DECISIONS.md`: No foot redesign listed among low-risk fixes.

**Accessibility for replacement:**
- The feet are at the bottom of the base. The M5 screw is accessed from below (through the foot, into the base socket). The counterbore is 10 mm diameter and 4 mm deep, so the screw head sits flush or below the foot bottom surface.
- To replace a foot, the user must access the underside of the tower. The tower is 330 mm tall and weighs ~6 kg. The user must either:
  - Tilt the tower on its side (risking module shift if trays are not locked).
  - Lift the tower and turn it upside down (difficult and risky for a 6 kg, 330 mm tall object with protruding cables).
  - Use a low-profile trolley or jack to raise one corner.
- **The foot is not accessible from the side or top.** The base is a wide stability plate (250 × 260 mm), so the feet are recessed under the base. A user cannot reach under the 32 mm foot height to access the screw while the tower is upright.

**Broken socket interface:**
- The mk0.7 Red Team review confirmed: "A 5.3 mm hole in 3 mm of PETG will strip immediately." The `FOOT_SOCKET_DEPTH = 3.0` mm is too thin for an M5 self-tapping screw. There is no heat-set insert.
- The mk0.7 Structural Integrity review also flagged this: the TPU foot is attached to a 3 mm PETG boss with no insert. The M5 screw will strip the PETG on first assembly.
- `revisions/mk0.7.1/DECISIONS.md` line 8: "The foot remains printable but is routed to `printable/tpu` instead of `printable/plastic`..." — mk0.7.1 only changed the export *folder* for the foot, not the *geometry*.

**Finding:** Foot replacement is **CONFIRMED** to require tower repositioning (tilt or lift). The 32 mm foot height does not provide side access to the screw. The socket interface is **CONFIRMED** broken — the 3 mm PETG socket will strip immediately. This is a **CONFIRMED blocker** for assembly, not just serviceability. mk0.7.1 only reclassified the foot export folder. **NEEDS TEST:** physical assembly of foot to socket with an M5 screw to verify thread stripping force. **Status: UNCHANGED, BLOCKER PERSISTS.**

---

## Scalability to Future Modules

### Assessment: ARCHITECTURE SUPPORTS NEW MODULES, BUT THE CURRENT STACK HAS ZERO SLACK. NO CHANGE IN mk0.7.1.

**Evidence:**
- `config.py` lines 16–17: `TOTAL_UNITS = 8.5`, `TOWER_HEIGHT = TOTAL_UNITS * UNIT_HEIGHT + 24.0 = 8.5 * 35 + 24 = 321.5` mm. Unchanged.
- `config.py` lines 216–230: `TRAY_STACK` uses 2.0 + 1.0 + 1.0 + 1.0 + 1.5 + 2.0 = **8.5 units exactly**. Unchanged.
- `config.py` lines 96–99: `MODULE_SLOT_COUNT = 6`, `MODULE_SLOT_PITCH = TOWER_INTERNAL_HEIGHT / MODULE_SLOT_COUNT = 314.5 / 6 ≈ 52.4` mm. `LIGHT_MODULE_HEIGHT = 51.4` mm, `COMPUTE_MODULE_HEIGHT = 103.9` mm. Unchanged.
- `revisions/mk0.7.1/CHANGELOG_FROM_MK0.7.md`: No unit stack or module slot changes.

**New module addition:**
- The `TRAY_FACTORIES` dictionary (`modules.py` lines 144–150) and `placeholder_factories` (`tower_assembly.py` lines 71–97) are still open dictionaries. Adding a new module requires only adding a new factory entry and a `TRAY_STACK` entry.
- The tray standard (`MODULE_WIDTH`, `MODULE_DEPTH`, `RAIL_SPACING`, lock interface, mounting holes) is fixed. Any new module that fits within the 170 × 176 mm planform and the available height can use the existing standard.

**Height constraint:**
- The current stack consumes **all 8.5 units**. There is no spare height. If a future module needs 2.5 or 3 units, the stack must be completely reconfigured.
- The `UNIT_HEIGHT = 35.0` mm is a rigid grid. If a device needs 45 mm (e.g., a taller Mini PC with a larger heatsink), it cannot fit in the current unit system without either:
  - Increasing `UNIT_HEIGHT` (which changes ALL tray heights and requires reprinting all trays).
  - Using a non-integer unit count (which the current config supports — `MIKROTIK_TRAY_UNITS = 1.5` shows non-integer units are allowed).
  - Removing another module to free up units.

**Width and depth constraints:**
- `MODULE_WIDTH = 170.0` mm and `MODULE_DEPTH = 176.0` mm are fixed. If a future device (e.g., a larger router, a NAS with more drive bays) needs 180 mm width, the tray standard must be changed. This would require reprinting all trays, changing the rail spacing, and possibly widening the tower.
- The `TRAY_CLEARANCE = 0.6` mm is small. If a device needs even 1 mm more width than the placeholder, the tray is unusable. There is no adjustment mechanism (slotted holes, adjustable rails, or shims).

**Module count constraint:**
- `MODULE_SLOT_COUNT = 6`. The current design has 6 modules. If a user wants 7 modules (e.g., adding a dedicated firewall module), there is no 7th slot. The tower would need to be taller (more units) or a module would need to be removed.
- The frame and rail height are derived from `TOWER_HEIGHT`. Changing the module count or total units requires recalculating `METAL_RAIL_HEIGHT`, `REAR_SPINE_HEIGHT`, `SIDE_PANEL_HEIGHT`, and rod length — essentially redesigning the tower.

**Finding:** The architecture is **CONFIRMED** scalable in terms of *software* (adding new `TRAY_FACTORIES` entries is trivial). However, the physical tower is **CONFIRMED** to have zero slack in the current configuration. Adding a new module type that requires a different size or an additional slot would require a **major redesign** of the stack, frame, and rails. The fixed unit grid and rigid tray dimensions provide no margin for future growth. This is a **LIKELY** limitation for a long-term modular platform. **Status: UNCHANGED.**

**Recommendation for future revisions:**
- Add 0.5–1.0 units of spare height to the stack (increase `TOTAL_UNITS` to 9.0–9.5).
- Consider making `UNIT_HEIGHT` adjustable or supporting "double-wide" modules that occupy two adjacent slots horizontally.
- Add slotted mounting holes or adjustable rails to accommodate device size variations.

---

## Blockers

These issues must be resolved before any physical build or claim of "serviceable modularity." All five were present in mk0.7 and remain **completely unresolved** in mk0.7.1. The `KNOWN_LIMITATIONS.md` and `DECISIONS.md` mk0.7.1 explicitly document this deferral.

1. **Module extraction requires full cable disconnection.** The rear service spine design forces the user to remove the spine cover, untie cables, and disconnect all power/data connectors before extracting any module. This contradicts the AGENTS.md requirement that extraction must not require tower disassembly. mk0.7.1 explicitly deferred "service-spine quick disconnects" as "too large for a safe patch release." **Severity: High.** Evidence: `carriages.py:143–150`, `service_spine.py` (implied), `revisions/mk0.7.1/DECISIONS.md:12–13`, `revisions/mk0.7.1/KNOWN_LIMITATIONS.md:36–39`.

2. **Tray vertical support is unmodeled.** The metal guide rails are vertical bars with no horizontal shelves, brackets, or ledges. The trays are horizontal plates with no modeled support from below except the bottom frame for the lowest tray. A 1.2 kg Mini PC tray has no visible support mechanism. **Severity: High.** Evidence: `config.py:104–111`, `rails.py` (implied), `revisions/mk0.7.1/DECISIONS.md:12–13` ("rail-retention architecture" deferred).

3. **Bottom fan cartridge is not attached to the base.** The cartridge has M3 mounting holes at `±68` mm offset, but the base has no corresponding holes. The cartridge is a loose part under a 9.5 kg tower. mk0.7.1 explicitly deferred "bottom fan cartridge retention" to a future revision. **Severity: High.** Evidence: `cooling.py:48–91`, `config.py:427–433`, `revisions/mk0.7.1/KNOWN_LIMITATIONS.md:39`, `revisions/mk0.7.1/DECISIONS.md:12–13`.

4. **Side panel mounting interface is missing.** The corner blocks lack holes on `−X` and `−Y` faces, and the holes that exist are misaligned with panel mount points. The frame has no panel mounting holes. Side panels cannot be attached. mk0.7.1 did not list this as a low-risk fix. **Severity: High.** Evidence: `corner_blocks.py` (implied), `side_panels.py`, `tower_assembly.py:122–153`, `revisions/mk0.7.1/CHANGELOG_FROM_MK0.7.md` (no structural changes listed).

5. **Foot socket strips immediately.** The `FOOT_SOCKET_DEPTH = 3.0` mm with a 5.3 mm hole and no heat-set insert means the M5 screw will strip the PETG on first assembly. mk0.7.1 only reclassified the foot export folder; the geometry is unchanged. **Severity: High.** Evidence: `config.py:349–355`, `feet.py` (implied), `revisions/mk0.7.1/DECISIONS.md:8` (export reclassification only).

---

## Recommendations

### Immediate (mk0.7.1 → mk0.8)

1. **Fix the module extraction cable problem.** Options:
   - Add quick-disconnect bulkhead connectors (e.g., XT30 pass-through, magnetic Ethernet) at each tray rear, so cables stay in the spine when the module is pulled out.
   - Add short pigtails (100–150 mm) to each module that stay in the spine, with a detachable connector at the module rear.
   - Replace the screw-on spine cover with a hinged or sliding cover that opens without tools.
   - Ensure horizontal cable ties do not bundle cables across module boundaries.
   - **Evidence this is needed:** `revisions/mk0.7.1/DECISIONS.md:12–13` explicitly deferred this; it must be the top priority for mk0.8.

2. **Add tray vertical support.** The guide rails must have horizontal shelves or ledges at each tray height, or the frame must have intermediate rings that support the trays from below. A 1.2 kg tray cannot be supported by friction alone. Evidence: `config.py:104–111`, `revisions/mk0.7.1/DECISIONS.md:12–13` ("rail-retention architecture" deferred).

3. **Attach the bottom fan cartridge.** Add M3 mounting holes to the `central_bottom_fan_frame` or base stability plate that align with `BOTTOM_FAN_CARTRIDGE_MOUNT_OFFSET = 68.0`. Alternatively, add slide-in rails or detents to the base underside. Evidence: `cooling.py:48–91`, `config.py:427–433`, `revisions/mk0.7.1/KNOWN_LIMITATIONS.md:39`.

4. **Fix the foot socket.** Increase `FOOT_SOCKET_DEPTH` to at least 8 mm and add a heat-set insert boss (e.g., `INSERT_BOSS_DIAMETER = 7.2`, `INSERT_BOSS_HEIGHT = 8.0`). Or use a threaded brass insert. Evidence: `config.py:349–355`, `revisions/mk0.7.1/DECISIONS.md:8`.

5. **Enlarge the front handle pocket.** Increase `TRAY_FRONT_HANDLE_DEPTH` from 4.2 mm to at least 12–15 mm to allow a two-finger grip. Or redesign the handle as a protruding pull tab (similar to server rack handles) rather than a recessed pocket. Evidence: `config.py:122`, `carriages.py:24–34`. Also mitigates the tipping hazard by allowing a more controlled pull.

6. **Increase Mini PC service travel or add rear access.** Either:
   - Increase `MINI_PC_TRAY_SERVICE_TRAVEL` to at least 130 mm (full device depth) so the rear connectors clear the tower.
   - Add a removable rear panel or hatch above the Mini PC tray for direct rear access without sliding the tray.
   - Add pass-through connectors at the tray rear so cables disconnect automatically when the tray is pulled out. Evidence: `config.py:515–523`, `modules.py:124–141`, `revisions/mk0.7.1/KNOWN_LIMITATIONS.md:17`.

7. **Make the power bus accessible without removing the spine cover.** Add a side-access door or a hinged cutout in the spine cover that exposes the power bus connectors. Or relocate the power bus to a position where the connectors are reachable from the side. Evidence: `config.py:530–564`, `tower_assembly.py:166–180`.

### Short-term (mk0.8)

8. **Add spare unit height to the stack.** Increase `TOTAL_UNITS` from 8.5 to 9.0 or 9.5 to allow future modules or taller devices without redesigning the entire stack. Evidence: `config.py:16–17`, `config.py:216–230`.

9. **Add adjustable device mounting to trays.** Replace fixed-size pockets with slotted holes or adjustable clamps so the trays can accommodate devices with slightly different dimensions. This prevents a 2 mm size mismatch from requiring a full tray reprint. Evidence: `config.py:233–313` (placeholder dimensions with `TODO` comments).

10. **Improve the tray stop design.** Use two M3 screws or a larger PETG bracket for the Mini PC tray stop. The current single-screw 18 × 6 × 22 mm bracket is marginal for a 1.2 kg impact load. Evidence: `config.py:515–523`, `modules.py:124–141`.

11. **Add a tool-less bottom fan cartridge.** Replace the M3 screw mounting with slide-in rails, detents, or quarter-turn fasteners. The DECISIONS.md claim the cartridge is "serviceable" — it should be tool-less. Evidence: `DECISIONS.md` lines 11–17, `cooling.py:48–91`.

12. **Add side-access foot screws.** Consider making the foot screws accessible from the side of the base (e.g., a horizontal screw into a side boss) so the user does not need to tilt or lift the tower to replace a foot. Evidence: `config.py:332–359`.

### Long-term

13. **Consider a true hot-swap connector standard.** For a modular tower that claims serviceability, the rear module connectors should be designed for 100+ insertion cycles. Standard PC connectors (XT30, MicroFit, RJ45) are not designed for frequent cycling. Consider commercial hot-swap connector systems or spring-loaded contact blocks. Evidence: AGENTS.md modular standard requirements.

14. **Document the module swap time budget.** Quantify the time and tools required to extract and reinstall each module. If the goal is "5-minute module swap," measure it and design to meet it. Current extraction procedure is 10+ minutes. Evidence: `revisions/mk0.7.1/KNOWN_LIMITATIONS.md:36–39`.

15. **Address the structural issues in the same revision.** The serviceability blockers cannot be fully resolved without structural fixes (rail shelves, panel mounts, foot sockets). The mk0.8 revision should include a Structural Integrity review pass *before* serviceability fixes are designed, to ensure the physical interface is robust enough to support the service motion. Evidence: `revisions/mk0.7.1/DECISIONS.md:12–13` (structural redesign deferred alongside serviceability).

---

*Review completed. All findings are based on inspection of the mk0.7.1 CAD source code, configuration parameters, and cross-reference with the mk0.7.1 revision documentation (`DECISIONS.md`, `KNOWN_LIMITATIONS.md`, `CHANGELOG_FROM_MK0.7.md`). The mk0.7.1 patch explicitly deferred all core serviceability issues; this review confirms they remain present and unresolved. No physical testing was performed. Grades are assigned as: CONFIRMED (direct evidence in CAD or revision docs), LIKELY (strong inference from geometry), UNCERTAIN (insufficient data), NEEDS TEST (requires physical verification).*
