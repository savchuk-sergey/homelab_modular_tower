# mk0.7.4 Rough Mockup Assembly Sequence

## Gate Before Large Prints

Print and inspect the coupon set before printing full-size gated parts:

- Split spine and power-bus parts: `coupon_split_joint_tab_socket`
- Rail end mounts: `coupon_rail_end_mount_fit`
- Tray support ledges: `coupon_tray_ledge_stack`
- Side panels: `coupon_side_panel_mount`
- Bottom filter system: `coupon_bottom_filter_retainer`
- Feet: `coupon_petg_foot_socket` and `coupon_tpu_foot`
- Large flat parts and grilles: `coupon_flat_petg_tile` and `coupon_fan_grille_section`

## Base and Vertical Structure

1. Print the sectional base parts: central bottom fan frame, left/right foot extensions, front/rear stability wings.
2. Dry-fit the base sections on a flat surface.
3. Install M3 wing fasteners while the base is still flat and accessible from above.
4. Install the bottom structural frame on the base center section.
5. Insert the four M5 rods through the frame and base clearances.
6. Add M5 washers and nuts below the lower frame, but leave them loose enough for squaring.
7. Add lower corner blocks.
8. Install the top structural frame and upper corner blocks.
9. Square the tower envelope, then tighten M5 nuts gradually in a diagonal sequence.

Base fastener access rule: all base wing screws and lower M5 nuts must be reachable before tray ledges, guide rails, or side panels are installed.

## Metal Guide Rails and Rail End Mounts

1. Place the four metal guide rails at the CAD guide positions:

| Rail | X | Y |
|---|---:|---:|
| Front left | `-84.0` | `-58.0` |
| Front right | `84.0` | `-58.0` |
| Rear left | `-84.0` | `58.0` |
| Rear right | `84.0` | `58.0` |

2. Install bottom rail end mounts first.
3. Slide/seat each metal rail into the lower capture.
4. Install top rail end mounts.
5. Add vertical M3 screws through the rail end mounts into the frame targets.
6. Add side M3 rail screws only after the rail coupon confirms the slot and screw path are usable.

## Tray Support Ledges

mk0.7.4 keeps individual tray support ledges and controls misassembly risk with an indexed installation table. This is Option C from the iteration plan.

Install four ledges per tray level, one at each guide rail position:

| Tray level | Tray | Bottom Z | Ledge Z target |
|---:|---|---:|---:|
| 0 | `ups_power_tray` | `18.0` | `16.0` |
| 1 | `external_ssd_bay` | `88.0` | `86.0` |
| 2 | `ssd_expansion_tray` | `123.0` | `121.0` |
| 3 | `raspberry_pi_tray` | `158.0` | `156.0` |
| 4 | `mikrotik_tray` | `193.0` | `191.0` |
| 5 | `mini_pc_tray` | `245.5` | `243.5` |

Mark each rail with the tray level number before fastening ledges. Do not install all 24 ledges from memory; use the table and check left/right/front/rear symmetry at every level.

## Tray Stack

1. Insert trays from bottom to top:

| Order | Tray | Units | Bottom Z | Top Z | Center Z |
|---:|---|---:|---:|---:|---:|
| 1 | `ups_power_tray` | `2.0` | `18.0` | `86.0` | `52.0` |
| 2 | `external_ssd_bay` | `1.0` | `88.0` | `121.0` | `104.5` |
| 3 | `ssd_expansion_tray` | `1.0` | `123.0` | `156.0` | `139.5` |
| 4 | `raspberry_pi_tray` | `1.0` | `158.0` | `191.0` | `174.5` |
| 5 | `mikrotik_tray` | `1.5` | `193.0` | `243.5` | `218.2` |
| 6 | `mini_pc_tray` | `2.0` | `245.5` | `313.5` | `279.5` |

2. Check that each tray can be removed without loosening the neighboring tray.
3. Install the front lock screw only after tray sliding resistance is acceptable.
4. Keep Mini PC and UPS trays unloaded until ledge and rail coupons pass.

## Rear Service Spine and Power Bus

1. Install the rear service spine body after tray sliding is validated.
2. Route only placeholder low-voltage paths during rough mockup. Do not install mains AC inside the tower.
3. Install the power bus panel placeholder.
4. Install the rear spine cover and power bus cover last, so cable/service access stays open during fit checks.

## Side Panels

1. Install side-panel mount rails before side panels.
2. Verify left/right orientation:

| Side | Rotation | Expected result |
|---|---:|---|
| Left | `-90 deg` | Ribs and bosses face inward. |
| Right | `90 deg` | Ribs and bosses face inward. |

3. Install lower and upper structural side panels before middle panels.
4. Tighten panel screws lightly until all panels are seated.
5. Remove and reinstall one panel from each side to confirm service access is not trapped.

## Cooling, Filter, and Feet

1. Install TPU feet into PETG sockets only after the foot coupons pass.
2. Install the bottom fan cartridge.
3. Install the bottom filter frame and retainer after the filter-retainer coupon passes with the actual filter sheet.
4. Install bottom intake fan and top exhaust fan.
5. Install top fan grille last.

## Stop Conditions

Stop assembly and update `KNOWN_ISSUES.md` if any of these occur:

- A coupon fails and the full-size part depends on that interface.
- A tray cannot be removed without loosening another module.
- A rail end mount cracks during screw installation.
- A side-panel boss collides with the mount rail.
- Base fasteners become inaccessible after an installed step.
