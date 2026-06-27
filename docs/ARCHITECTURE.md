# Architecture

Homelab Modular Tower v1 is a compact modular mini-blade tower. It is sized around a roughly 190 x 190 mm footprint so major printed parts fit on a common 220 x 220 mm FDM printer bed.

The tower is built around four M5 vertical threaded rods at the corners. Printed top and bottom frame rings clamp the stack, while corner blocks provide rod alignment, washer/nut seats, and side-panel fastening points. This keeps the printed parts mostly in compression and lets metal hardware carry the long vertical load path.

The trays also reference four internal metal guide rails. In v1 these are placeholder 10 x 3 mm vertical rails with M3 holes. They make the intended tray support path visible in CAD and avoid relying only on thin PETG side guides.

## Module Stack

Modules are arranged bottom to top:

1. UPS / Power Distribution, 2U
2. External SSD Bay, 1U
3. SSD / Expansion, 1U
4. Raspberry Pi, 1U
5. MikroTik hAP ax2, 1.5U placeholder
6. Mini PC, 2U

One unit is 35 mm. Each module is a removable tray with a base, side guides, front handle, ventilation, M3 service holes, and a rear connector zone.

## Why UPS Is At The Bottom

The UPS/power tray can be heavier than the logic modules because it may contain a battery pack, fuse block, BMS, DC UPS board, and DC-DC converters. Keeping it at the bottom lowers the center of gravity and keeps higher-maintenance electronics above the heavier mass.

## Why Mini PC Is At The Top

The Mini PC is the highest heat-density module in this concept. Placing it near the top and rear exhaust shortens the hot-air path. A separate removable duct gives the Mini PC a priority cooling path without blocking tray removal.

## Module Service

Each tray is intended to slide forward. Rear connector zones are placeholders for quick-disconnect DC and data routing. The design assumes the user can remove one module without disassembling the whole tower after loosening only module-specific fasteners and disconnecting the rear service connectors.

Tray models include clearance cutouts around the M5 rod zones, rear service spine, and metal guide rails. The rail geometry still needs physical validation before printing a load-bearing version.

## Airflow

The intended airflow path is bottom/front intake to top/rear exhaust. The bottom fan panel includes rails for a 120 mm dust filter. Side panels include perforation for passive intake and pressure relief. The Mini PC duct directs part of the vertical airflow toward the Mini PC cooler zone.

## Rear Service Spine

The rear service spine is a removable vertical cable channel. It reserves space for:

- Ethernet and USB routing
- fan wiring
- low-voltage power lines
- quick-disconnect module connectors
- a separate power bus placeholder panel

The spine and power bus are deliberately modeled as simple placeholders in v1. Real connector and PCB footprints must be measured before v2.
