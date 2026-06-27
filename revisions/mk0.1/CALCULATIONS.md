# Calculations And Checks For mk0.1

mk0.1 contains first-pass engineering assumptions and CAD layout checks. It does not contain validated mechanical, thermal, or electrical calculations.

## Envelope

Nominal tower envelope:

- width: about 190 mm
- depth: about 190 mm
- height: about 300-330 mm

The envelope is intended to fit common FDM printers with a 220 x 220 mm bed for major flat parts.

## Module Height Assumption

Base unit height:

- `UNIT_HEIGHT = 35 mm`

Module stack:

- UPS / Power Distribution: 2U
- External SSD Bay: 1U
- SSD / Expansion: 1U
- Raspberry Pi: 1U
- MikroTik hAP ax2: 1.5U placeholder
- Mini PC: 2U

## Structural Assumptions

Primary stiffness is intended to come from:

- 4x M5 threaded rods
- metal guide rails
- top frame ring
- bottom frame ring
- corner blocks

PETG parts are intended to locate, separate, and connect components. They are not intended to be the only load-bearing structure.

No load calculation has been completed for:

- M5 rod compression and preload
- metal guide rail bending
- tray load under device mass
- corner block stress
- heat-set insert pullout

## Clearance Assumptions

The model includes placeholder clearances for:

- M5 rods
- metal guide rails
- rear service spine
- module trays
- fan openings

These clearances are not physically validated.

## Cooling Assumptions

Cooling concept:

- 120 mm bottom intake
- 120 mm top exhaust
- vertical airflow
- priority Mini PC duct

No thermal simulation or temperature measurement has been completed.

## Electrical Assumptions

Power architecture:

```text
External AC/DC power supply
-> DC UPS
-> Power Bus
-> 19 V / 12 V / 5 V / GND
```

The power bus, DC UPS, fuse block, DC-DC converters, and connector zones are placeholders. No current, wire gauge, fuse, thermal, or connector retention calculations have been completed.
