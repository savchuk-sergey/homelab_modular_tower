# Calculations And Checks For mk0.2

Date: 2026-06-27

## Carriage Handle Envelope

The recessed handle is cut into the carriage front plate and does not extend forward beyond `TRAY_DEPTH`.

Key parameters:

- front plate thickness: `CARRIAGE_FRONT_PLATE_THICKNESS`;
- grip width: `CARRIAGE_HANDLE_WIDTH`;
- grip height: `CARRIAGE_HANDLE_HEIGHT`;
- grip depth: `CARRIAGE_HANDLE_DEPTH`;
- top bridge: `CARRIAGE_HANDLE_TOP_BRIDGE`;
- side ribs: `CARRIAGE_HANDLE_SIDE_RIB`.

The handle is centered on the front plate. The prepared lock boss is placed inside the tray envelope.

## Side Panel Envelope

The side-panel length is derived from `OUTER_DEPTH - 2 * SIDE_PANEL_CLEARANCE`.

The panel remains a removable service cover. The primary structural loop remains:

- top frame ring;
- bottom frame ring;
- four M5 threaded rods;
- corner blocks;
- metal guide rails.

## Ventilation Keep-Out

Vent slots are skipped in the future Mini PC duct band:

- zone center: `MINIPC_DUCT_ZONE_OFFSET_Z`;
- zone height: `MINIPC_DUCT_ZONE_HEIGHT`;
- added clearance: `SIDE_PANEL_MINIPC_DUCT_CLEARANCE`.

This is a CAD keep-out only. It does not replace thermal testing.

## Prototype Checks Required

- Measure real pull force for loaded trays.
- Check front plate strain and cracks around the grip pocket.
- Check side-panel flatness after PETG printing.
- Check screw reach and driver clearance.
- Run smoke, temperature, or airflow testing before freezing the vent pattern.
