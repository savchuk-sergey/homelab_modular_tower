# Power Concept

Homelab Modular Tower v1 is designed around a low-voltage internal DC architecture.

Important safety rule: do not place exposed 220 V / mains AC circuitry inside this printed enclosure.

The intended architecture is:

- External certified AC/DC power brick outside the tower.
- DC input enters the UPS / Power Distribution tray.
- DC UPS module manages backup power.
- Internal rear service spine distributes low-voltage DC.
- Separate protected rails for 19 V, 12 V, 5 V, and GND.

## Internal Rails

The `power_bus_panel` CAD part is a placeholder for future real components:

- terminal blocks
- fuses
- DC-DC converters
- module quick-disconnects
- M3 mounting holes

Each rail should have its own fuse or resettable protection sized for the actual load. Wire gauge, connector current rating, thermal behavior, and battery protection must be checked before real use.

## Module Connectors

Planned placeholder connector zones:

- XT30 for 19 V Mini PC power
- JST-VH or Molex MicroFit for 12 V MikroTik power
- USB-C or dedicated 5 V connector for Raspberry Pi
- USB-C cable routing for External SSD Bay

The power bus panel includes simple CAD windows for these connector classes. They are not final connector cutouts and do not define current rating, retention, or strain relief.

These are mechanical placeholder zones only. Exact connector models, panel cutouts, wire bend radius, strain relief, and retention features must be designed after measurements.

## Battery And UPS Warning

LiFePO4 packs, BMS boards, DC UPS boards, fuse blocks, and DC-DC converters require electrical validation. Check charging profile, fuse sizing, short-circuit protection, wire temperature, airflow, and enclosure temperature before powering real hardware.
