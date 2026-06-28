# mk0.9.1 Assembly Guide

## Step-by-step

### 1. Feet
* Insert the four TPU feet into the base module foot-mount sockets.
* Secure from the top with an M5 washer and M5 nut (or M3 screw if using the
  printed counterbore design).
* Check that the tower stands stable and that the bottom intake gap is
  ~12 mm.

### 2. Bottom fan
* Place the 120 mm intake fan on the base module fan mount.
* Align the fan holes with the 105 mm spacing mount holes.
* Fasten with four M3 × 4 mm screws (or M3 × 6 mm with washers).
* Cable should point toward the rear service zone.

### 3. Dust filter
* Slide the dust filter sheet into the filter slot under the base module.
* Ensure it sits flush and does not bulge into the fan blades.

### 4. Aluminum U-channel rails
* Cut two lengths of 15 × 10 × 10 × 2 mm U-channel to **145 mm** (for the
  RPi/SSD module) and two lengths to **155 mm** (for the Mini PC module).
* Deburr the cut ends with a file.
* Slide each rail into the side wall pocket of the corresponding module shell.
* Secure the rail ends with the printed **rail end clips** and M3 screws.
* Do **not** use glue.

### 5. POM-C shoes
* Cut the Ø8 mm POM-C rod into 12 mm blanks (4 for RPi/SSD, 6 for Mini PC,
  plus spares).
* Press each shoe into the carriage socket by hand.  It should be snug but
  not require tools.
* Insert the M3 clamp screw into the PETG boss and tighten until it lightly
  touches the shoe.  **Do not** thread the screw into the POM-C.
* Check that the shoe protrudes ~6 mm toward the rail.

### 6. RPi/SSD carriage
* Mount the Raspberry Pi 3B on the four standoffs with M2.5 screws.
* Slide the external SSD between the two retainer rails.
* Insert the carriage into the RPi/SSD module shell from the front.
* The POM-C shoes should slide smoothly inside the U-channel rails.
* Engage the front M3 lock screw to prevent accidental pull-out.

### 7. Mini PC placeholder carriage
* Place the Mini PC placeholder (or the real device if available) on the four
  support pads.
* Insert the carriage into the Mini PC module shell.
* Check smooth travel and lock with the front M3 screw.

### 8. Roof module
* Place the 120 mm exhaust fan on the roof fan mount.
* Fasten with M3 screws.
* Insert the top guard mesh into the filter slot.

### 9. Stack the tower
* Lower the RPi/SSD module onto the base module.
* Lower the Mini PC module onto the RPi/SSD module.
* Lower the roof module onto the Mini PC module.
* Ensure alignment pins engage between each pair.

### 10. M5 rods
* Insert the four M5 threaded rods through the corner posts.
* Add a washer and nut at the bottom of each rod.
* Add a washer and nut at the top and tighten evenly.
* **Do not** over-torque — the goal is to remove stack slack, not to bend the
  frames.

### 11. Functional checks
* Verify that both carriages slide in and out without binding.
* Verify that the bottom fan spins freely and does not hit the dust filter.
* Verify that the top fan spins freely.
* Check that no cables obstruct the central airflow channel.
* Confirm the tower is stable and does not rock on the TPU feet.

## Maintenance

* **Shoe replacement:** loosen the M3 clamp screw, pull the old shoe out with
  pliers, press the new one in, re-tighten the clamp screw.
* **Filter cleaning:** slide the dust filter out from the front, rinse with
  water, dry completely, re-insert.
* **Foot replacement:** the TPU feet are press-fit and held by a single
  fastener from the top.
