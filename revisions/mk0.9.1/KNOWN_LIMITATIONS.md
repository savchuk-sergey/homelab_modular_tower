# mk0.9.1 Known Limitations

## Experimental rail / carriage system

* The aluminum U-channel rail and POM-C shoe combination is **untested** in
  physical hardware.
* Real rail dimensions may vary by ±0.2 mm depending on supplier.
* If the purchased rail has a thicker or thinner wall, the shoe clearance
  will change.  Always verify with a caliper before cutting stock.

## Shoe fit

* The Ø8 mm POM-C shoe with 8.3 mm PETG socket is designed for a hand-press
  fit.  If your printer over-extrudes, the socket may be too tight.
* If the shoe is too loose, it will rattle and wear prematurely.
* A drop of Loctite on the **clamp screw** (not on the shoe) can help, but
  do not glue the shoe itself.

## Clamp screw interference

* The M3 clamp screw must not project into the U-channel rail clearance.
* Verify in CAD or with a test print that the screw head / tip does not
  scrape the rail when the carriage moves.

## Mini PC dimensions

* The Mini PC placeholder is based on estimated dimensions (130 × 130 × 55 mm).
* The carriage pads and retainers will almost certainly need adjustment once
  the real device is measured.
* Do not treat the Mini PC module as final.

## Airflow

* Airflow is geometrically open but has not been validated by CFD or physical
  smoke testing.
* The Mini PC placeholder may block more air than the final device.
* If the real Mini PC has side vents, the airflow guide may need cut-outs.

## Power / router / rear service spine

* Not implemented in `mk0.9.1`.
* Reserved zones are present but no geometry is finalised.
* Cable management is ad-hoc until the rear service spine is designed.

## Weight estimates

* The target weights are based on solid-volume approximation
  (density × CAD volume).
* Actual slicer estimates may differ by ±15 % due to infill, supports, and
  bridging settings.
* If the slicer reports > 1100 g PETG, the design is too heavy and must be
  further lightened.

## TPU feet

* The TPU foot design assumes a Shore 95A hardness.
* Softer TPU may compress too much and reduce the intake gap below 10 mm.
* Harder TPU (or printed PETG feet) will transmit more vibration.

## Print tolerances

* The shoe socket (8.3 mm) and shoe (8.0 mm) have a 0.3 mm clearance.
* This is tight for FDM printing.  A tolerance test coupon is strongly
  recommended before printing full carriages.
