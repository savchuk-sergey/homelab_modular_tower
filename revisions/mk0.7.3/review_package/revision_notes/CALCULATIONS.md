# mk0.7.3 Calculations

## Assembly Stack Assumptions

- Bottom corner blocks sit above the bottom frame, not centered inside it.
- Top corner blocks sit below the top frame, not centered inside it.
- Top-frame nut seats are placed on the outer top face so the rod stack can clamp downward.
- M5 rod length must include the frame stack, nut/washer stack, and any protective cap or acorn nut clearance.

## mk0.7.3 Stack Values

- `BOTTOM_CORNER_BLOCK_Z = FRAME_THICKNESS / 2 + CORNER_BLOCK_HEIGHT / 2`.
- `TOP_CORNER_BLOCK_Z = TOWER_HEIGHT - FRAME_THICKNESS / 2 - CORNER_BLOCK_HEIGHT / 2`.
- `ROD_LENGTH = TOWER_HEIGHT + ROD_EXTRA_THREAD_ALLOWANCE`.
- `ROD_EXTRA_THREAD_ALLOWANCE = 18 mm`.
- `FOOT_SOCKET_DEPTH = 6 mm`.
- `BOTTOM_FAN_CARTRIDGE_FEATURE_OVERLAP = 4 mm`.

## Printability Assumptions

- Bambu Lab P2S printable envelope remains 256 x 256 x 256 mm.
- Tall rear-service and power-bus parts must be split instead of relying on diagonal printing.
- Segment targets should remain below 240 mm in their longest printed axis where practical.

## Generated Printability Result

The generated `printability_check.csv` for mk0.7.3 shows no axis-aligned P2S overflow in `printable/plastic`. The former tall blockers are now represented by split sections:

- `rear_service_spine_lower` / `rear_service_spine_upper`: 157.75 mm Z each.
- `rear_service_spine_cover_lower` / `rear_service_spine_cover_upper`: 156.75 mm Z each.
- `power_bus_panel_lower` / `power_bus_panel_upper`: 146.75 mm Z each.
- `power_bus_cover_lower` / `power_bus_cover_upper`: 141.75 mm Z each.

## Deferred Calculations

- Final battery thermal containment.
- Final DC current sizing and fuse values.
- Final Mini PC airflow duct pressure loss.
- Final cable bend radius by selected connector.
