# mk0.9.1 Printing Guide

## Material summary

| Material | Role | Target weight |
|----------|------|---------------|
| PETG | All structural frames, carriages, brackets | ≤ 900 g |
| TPU | Feet only (vibration isolation) | ≤ 50 g |
| POM-C rod | **Do not print** — buy Ø8 mm rod stock | — |
| Aluminum U-channel | **Do not print** — buy 15 × 10 × 10 × 2 mm profile | — |

## Print orientation

### Base module

* **Orientation:** flat on the build plate (Z = module height).
* **Supports:** none for the frame; small supports may be needed for the
  foot-mount overhangs if your printer bridges poorly.
* **Infill:** 20–25 % gyroid or honeycomb.
* **Walls:** 3 perimeters (≈ 1.2 mm).
* **Top/bottom layers:** 3–4.
* **Why:** large flat surfaces print best when oriented horizontally;
  bridging across the fan opening should be manageable with PETG.

### RPi/SSD carriage

* **Orientation:** flat on the build plate (carriage floor down).
* **Supports:** none.  The open frame is self-supporting.
* **Infill:** 15–20 % for the peripheral frame; 30 % for the shoe bosses.
* **Walls:** 3 perimeters.
* **Critical:** print the shoe socket holes vertically so the M3 clamp screw
  boss is strong.

### Mini PC placeholder carriage

* Same orientation and settings as the RPi/SSD carriage.
* Shoe bosses are more numerous — ensure adequate cooling.

### Roof module

* **Orientation:** flat on the build plate.
* **Supports:** none.
* **Infill:** 20 %.
* The fan shroud is thin — use 3 perimeters minimum.

### TPU feet

* **Orientation:** standing on the cylindrical face (print height = foot
  height).
* **Infill:** 15 %.
* **Walls:** 2 perimeters.
* **Speed:** slow (30–40 mm/s) for TPU.

## Important reminders

1. **PETG is NOT the sliding surface.**  The POM-C shoes are.  Do not attempt
   to print the shoes from PETG or PLA.
2. **Aluminum rails are NOT printed.**  They are commercial extrusions cut to
   length.
3. **Do not use supports inside the airflow window.**  The open-frame design
   is intended to be support-free.
4. **Check first-layer squish** on the thin frame rings — warping will cause
   misalignment with the module above.
5. **Calibrate extrusion multiplier** before printing the carriages.  The shoe
   socket diameter (8.3 mm) is tight; over-extrusion will make it impossible
   to press the POM-C shoe in.

## Suggested print order

1. TPU feet (small, low risk, lets you tune TPU settings).
2. Rail end clips (small, quick validation of M3 clearances).
3. RPi/SSD carriage (validate shoe socket fit with a POM-C off-cut).
4. Mini PC placeholder carriage (same fit check).
5. Base module (largest print; do this once you are confident in settings).
6. Roof module (second largest).
7. M5 rod caps (batch of 4, quick).
