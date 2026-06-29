# mk0.12 - Physical Test Plan

Revision: mk0.12  
Architecture: MVP-2M stack-through-rod  
Status: BLOCKED UNTIL CAD SKELETON V3 VALIDATION PASSES  

Related documents:
- README.md
- ENGINEERING_SPEC.md
- PARTS_SPEC.md
- INTERFACES.md
- VALIDATION_GATES.md
- PHYSICAL_TEST_PLAN.md
- AGENT_RULES.md
- KNOWN_ISSUES.md

## Policy

```text
CAD skeleton v3 validation gates first.
Coupon parts after CAD skeleton v3 passes.
Full print only after coupon and physical checks pass.

COUPON PARTS: BLOCKED until CAD skeleton v3 passes validation.
FULL PRINT: BLOCKED until CAD skeleton v3 and physical validation pass.
```

## Test Sequence

| Step | Test | Required Evidence | Status |
| ---: | --- | --- | --- |
| 0 | CAD skeleton v3 validation gates | All required gates in `VALIDATION_GATES.md` pass or are explicitly waived | REQUIRED BEFORE COUPONS |
| 1 | Print M5 corner coupon | Corner pad, 5.6 mm hole, 13 mm washer seat, 1.2 mm seat depth | BLOCKED |
| 2 | Test M5 rod clearance | M5 rod passes without force after PETG cooling | BLOCKED |
| 3 | Test washer seat fit | 12 mm washer fits 13 mm seat without rocking or excessive slop | BLOCKED |
| 4 | Test PETG shrink/tolerance | Measured hole and seat diameters recorded | BLOCKED |
| 5 | Print rear cable window coupon | 30 mm rear reserve and segmented corner clearance represented | BLOCKED |
| 6 | Test cable bend with actual cables | Mini PC power, Ethernet, HDMI/DisplayPort if used, USB, and SSD cable bend within rear service zone without rod collision | BLOCKED |
| 7 | Print reduced-height stack module | M5 holes align through at least two stacked layers | BLOCKED |
| 8 | Test stack compression with rods/washers/nuts | Hand-tight only; no crushing, cracking, or major layer separation at pads | BLOCKED |
| 9 | Place real Raspberry Pi and SSD mock/envelope | Board/SSD envelopes fit; cable path remains open | BLOCKED |
| 10 | Place real Mini PC mock/envelope | 130 x 130 x 55 device and cable exits fit | BLOCKED |
| 11 | Slicer preview for full modules | No unsupported long bridges, impossible overhangs, hidden airflow blockage, or support traps | BLOCKED |
| 12 | Fan cutout/screw boss review | Fan screw boss material remains around 105 x 105 screw centers if fan mounting is active | BLOCKED |
| 13 | Foot pad/intake clearance check | TPU foot geometry leaves 3 to 5 mm clearance from fan-compatible intake boundary | BLOCKED |
| 14 | Full MVP print | Allowed only after CAD gates, coupons, physical checks, and slicer preview pass or are explicitly waived | BLOCKED UNTIL VALIDATED |

## Physical Risk Notes

- 30 mm rear service depth assumes flexible or angled cables where needed.
- Straight stiff HDMI, thick DC barrel plugs, and rigid USB adapters are not guaranteed.
- M5 stack compression must be hand-tight only.
- PETG washer seats, compression pads, and rib/load paths require coupon validation before full print.
- Mini PC thermal behavior still requires physical thermal observation after geometry passes CAD gates.
