# mk1.0 Preparation Checklist

## Before starting mk1.0

`mk0.9.1` deliberately leaves several items as placeholders.  Before moving
on to `mk1.0`, the following physical measurements and tests must be
completed.

## 1. Mini PC physical dimensions

* [ ] Measure the **exact** width, depth, and height of the target Mini PC.
* [ ] Measure the **weight**.
* [ ] Record the position of all ports (USB, HDMI, Ethernet, power).
* [ ] Record the position and size of any ventilation grilles or intake holes.
* [ ] Photograph the bottom (mounting holes, rubber feet, labels).
* [ ] Check whether the case is symmetrical or offset — this affects the
  carriage centering.

## 2. Rail / carriage fit test

* [ ] Buy a short length (200 mm) of the chosen aluminum U-channel
  (15 × 10 × 10 × 2 mm).
* [ ] Buy a 500 mm length of POM-C rod Ø8 mm.
* [ ] Cut one 12 mm shoe blank and press it into a printed test socket.
* [ ] Check fit:
  * too tight → increase socket diameter or sand the shoe
  * too loose → reduce socket diameter or try a Ø8.2 mm shoe
* [ ] Slide the test socket + shoe inside the real U-channel rail.
  * Check for binding, wobble, or clicking.
* [ ] Install the M3 clamp screw and verify it does not scrape the rail.

## 3. Shoe count validation

* [ ] Load the Mini PC carriage with the real device (or an equivalent mass).
* [ ] Test with 3 shoes per side (current design).
* [ ] If the carriage sags or the shoes deform, consider:
  * 4 shoes per side
  * longer shoes (15 mm instead of 12 mm)
  * switching to a linear ball-bearing rail for the Mini PC only

## 4. Cable radius and bend testing

* [ ] Measure the stiffest cable (likely HDMI or power brick cable).
* [ ] Check the minimum bend radius.
* [ ] Verify that the rear cable exit on the carriage is large enough.
* [ ] Verify that the central airflow channel is not blocked by thick cables.

## 5. Cooling validation

* [ ] Run the bottom and top fans at 100 %.
* [ ] Measure temperatures of the Raspberry Pi and Mini PC under load.
* [ ] If the Mini PC runs hot, add a local 40 mm fan mount or duct cut-outs.
* [ ] If the RPi/SSD stack overheats, add a vented side panel or heat sinks.

## 6. Power system planning

* [ ] Decide on the external AC/DC adapter (voltage, wattage).
* [ ] Measure the DC-DC converter footprint if one is planned.
* [ ] Sketch the DC bus layout (19 V, 12 V, 5 V, GND).
* [ ] Reserve module slot count for the future UPS / power distribution unit.

## 7. Router planning

* [ ] Measure the MikroTik hAP ax2 (or chosen router) bare board dimensions.
* [ ] Record Ethernet port positions and LED locations.
* [ ] Plan antenna routing if external antennas are needed.

## 8. Structural load test

* [ ] Assemble the full tower with all modules.
* [ ] Tighten the M5 rods to a moderate torque.
* [ ] Apply a gentle side load (push the tower by hand).
* [ ] Check for:
  * Sway or flex in the frame
  * Creep in the PETG interfaces
  * Loosening of the M5 nuts after 24 hours

## 9. Stability check

* [ ] Measure the full tower height with feet installed.
* [ ] Calculate the center of mass (roughly: sum of module masses × height).
* [ ] Verify that the tipping angle is > 15° in all directions.
* [ ] If not, widen the foot extension or add a stability wing.

## 10. Revision decision

Once the above checks are done, open a new git branch `cad/mk1.0` and create
`revisions/mk1.0/` with:

* `REVISION.md` — goals and scope
* `CALCULATIONS.md` — thermal, structural, and electrical calculations
* `DECISIONS.md` — why the chosen rail/shoe/power solutions were selected
* `KNOWN_ISSUES.md` — what still needs work
* `CHANGELOG.md` — delta from `mk0.9.1`
