# mk0.9.1 Design Notes

## Why massive plastic is a bad idea

In `mk0.9` the base and some modules tried to gain stiffness through thick
PETG walls and solid floors.  PETG has:

* Low elastic modulus (~2 GPa)
* High creep under sustained load
* Poor surface hardness for sliding wear

A 10 mm thick PETG slab weighs ~250 g but contributes less stiffness than a
single M5 threaded rod (~5 g of steel).  The correct approach is to let the
metal rods and aluminum rails carry the loads, and use PETG only for
positioning, cable management, and service features.

## Why M5 rods must give global stiffness

The four M5 rods act as a vertical tension/compression cage.  When the nuts
are tightened:

* The base and roof frames are pressed together.
* Corner posts are in compression.
* Rods are in tension.
* The whole stack behaves like a rigid column.

This is why the base and roof can be light frames — the rods do the
structural work.

## Why base / roof should be frames

Frames have high stiffness-to-weight ratio when loaded in the plane of the
rings.  By making the base and roof thin rings with corner posts, we:

* reduce print time and material
* keep the airflow path open
* allow easy visual inspection of the interior
* avoid thick sections that warp during printing

## Why carriages must be open-frame

A solid tray floor blocks vertical airflow.  In a tower with a bottom intake
and top exhaust, every module must be as transparent to air as possible.

Open-frame carriages with local pads:

* preserve the central chimney effect
* reduce weight by 40–60 % compared to a solid tray
* still provide mounting points for devices

## Why POM-C was chosen as the sliding element

| Material | Wear resistance | Friction vs. aluminum | Cost |
|----------|---------------|----------------------|------|
| PETG | poor | high | low |
| POM-C (Delrin) | excellent | low | moderate |
| Oil-impregnated bronze | good | very low | high |

POM-C is the sweet spot for a prototype:
* cheap enough to experiment with
* easy to machine or buy as rod stock
* low friction against anodized aluminum
* does not require lubrication for short strokes

## Why the shoes must be replaceable

Wear is inevitable.  If the sliding surface is printed into the carriage,
the whole carriage must be re-printed when wear occurs.  Replaceable shoes:

* cost ~1 g of POM-C each
* can be swapped in minutes
* allow testing different diameters (Ø8 vs Ø10) without re-printing the
tray

## Why self-tapping screws directly into POM-C are forbidden

* POM-C has low thread shear strength.
* Repeated insertion destroys the hole.
* A clamp screw that presses against the shoe (without cutting threads into
it) is repeatable and serviceable.

## Why Ø8 mm was chosen for the current rail standard

* Rail inner channel ≈ 11 mm (15 outer − 2 × 2 wall).
* Ø10 mm would leave ~0.5 mm clearance per side — risky for print
  tolerances and thermal expansion.
* Ø8 mm gives ~1.5 mm clearance per side — safe for a first prototype.
* If Ø8 proves too loose under load, we can try Ø8.5 or Ø9.5 without
changing the carriage geometry (only the shoe diameter).

## Why Ø10 mm is not used in the current configuration

* Would require either a wider rail profile or accepting a very tight fit.
* Tight fit increases risk of binding due to PETG print tolerance (~0.2 mm)
and humidity swelling.
* Kept as a future option if the rail profile is changed to 20 × 10 × 10 × 2
  or similar.
