# Homelab Modular Tower CAD Revision mk0.3

Date: 2026-06-27

Status: engineering platform revision / pre-measurement revision

## Purpose

mk0.3 converts the mk0.2 layout-oriented model into a stricter mechanical platform for the future measured revision mk0.4.

The revision is intentionally not a final production enclosure. It does not freeze real mounting points for the Mini PC, Raspberry Pi, MikroTik hAP ax2, UPS/DC UPS assembly, SSD devices, cable exits, or Mini PC duct openings. Those features still require physical teardown, measurement, and prototype checks.

## Difference from mk0.2

mk0.2 focused on service handles and removable side panels. mk0.3 focuses on the shared mechanical standard:

- standardized blade module geometry;
- M3 front screw retention prepared for heat-set inserts;
- clearer top and bottom structural frames;
- replaceable top and bottom fan grilles;
- larger rear service spine for cable and power-bus planning;
- visible device placeholder volumes in the assembly;
- explicit Mini PC airflow duct placeholder;
- corrected M5 rod placement so the model height is not inflated by rod positioning.

## What changed

The module tray standard now has explicit `MODULE_*` parameters in `cad/config.py`. Existing tray parameters remain as aliases where older code still uses them.

Each module tray keeps the same envelope, rear cable escape concept, side rail clearance, front handle zone, front lock boss, and anti-slide feature. The preferred retention strategy for mk0.3 is one M3 screw per module from the front side.

Top and bottom frames are now named and treated as structural frames. Fan grilles are separate replaceable parts rather than being treated as the structural frame.

The rear service spine is wider and deeper than in mk0.2. It includes cable windows at module heights, tie slots, cover-rail geometry, and a basic power/signal zone divider. It still does not define the final DC UPS or PCB/busbar layout.

The assembly includes temporary placeholder volumes for Mini PC, Raspberry Pi, MikroTik hAP ax2, UPS/DC UPS block, External SSD, SSD/Expansion, and power bus zone.

## Height target

The configured tower body height is 321.5 mm, which is inside the 300-330 mm target range. The generated assembly review bounding box is 335.0 mm high, including structural frame thickness, ribs, and removable fan grilles. This reaches the allowed mk0.3 engineering maximum without artificially compressing placeholder modules.

No module was artificially compressed to unrealistic dimensions. The height target is reached by keeping the mk0.2 stack compact and correcting the rod placement.

## Not finalized before real measurements

The following are intentionally not final in mk0.3:

- Mini PC mounting holes, duct openings, port windows, and heatsink interface;
- Raspberry Pi mounting holes, connector exits, and fan clearance;
- MikroTik hAP ax2 board or enclosure mounting pattern;
- UPS/DC UPS battery, fuse, BMS, converter, and connector retention;
- exact Ethernet, USB, DC, and fan-wire connector geometry;
- final power-bus implementation;
- final cable bend radius checks;
- final airflow validation.

## Known limitations

- Device placeholders are approximate and must not be used as production dimensions.
- The rear service spine is a mechanical reservation, not a complete electrical design.
- The Mini PC duct is a placeholder and must be rebuilt after teardown measurements.
- Fan grille open area is improved geometrically but not validated with airflow testing.
- M3 front retention requires physical access checks with real module handles and cables installed.
- Heat-set insert bosses are prepared, but insert brand, melt depth, and print orientation still need prototype validation.
- Side panels remain service covers and are not counted as the main load path.

## Assembly assumptions

Expected assembly sequence:

1. Install the bottom structural frame.
2. Install the four M5 threaded rods.
3. Add reinforced corner blocks.
4. Install metal guide rails.
5. Install the rear service spine.
6. Insert module trays from the front.
7. Install bottom and top fan grilles.
8. Install the top structural frame.
9. Install side service panels/covers.

Modules are intended to slide out toward the front. Removing one module should not require disassembling the full tower. Cables should exit each module toward the rear service spine.

## Engineering trade-offs

mk0.3 prefers screw retention over printed snap locks because PETG snap features are risky for repeated service cycles. The cost is slower tool-assisted extraction.

The rear spine is enlarged, which consumes more rear internal envelope, but it makes cable routing, strain relief, and future cover design more realistic.

The fan grilles are separated from the structural frames. This adds part count, but makes fan/filter service and grille iteration easier.

The model uses visible placeholders in assembly renders. This makes review clearer, but these solids are not final printable device mounts.

## Next tasks for mk0.4

- Measure the disassembled Mini PC board, heatsink, ports, airflow openings, and cable exits.
- Measure the Raspberry Pi, MikroTik hAP ax2, UPS/DC UPS components, SSDs, and power connectors.
- Replace placeholder volumes with measured keep-out zones and mounting patterns.
- Validate front M3 lock access with real trays and cable bundles.
- Prototype one module tray in PETG and measure rail friction and insert strength.
- Prototype the rear spine cable windows and tie-slot access.
- Rebuild the Mini PC duct around real intake/exhaust geometry.
- Validate fan grille airflow and filter service.
- Decide final power-bus mounting hardware and connector family.
