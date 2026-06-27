# mk0.7.1 Known Limitations

## Not Build-Ready

mk0.7.1 remains a review-oriented patch. The full tower is not approved for physical build, electrical operation, or unattended use.

## No Simulation Or Physical Validation

- No CFD was performed.
- No FEA was performed.
- No physical prototype was printed or assembled as part of this revision.
- No slicer-specific orientation, support, infill, brim, raft, or print-time validation was performed.
- No electrical safety validation was performed.

## Deferred Safety Blockers

- Dynamic tipping risk with the Mini PC tray extended remains unresolved.
- Lithium battery containment, thermal cutoff, BMS integration, and venting remain unresolved.
- DC bus fusing, emergency stop, and isolation remain unresolved.
- Power bus electrical current capacity and insulation are not validated.

## Deferred Airflow Blockers

- Device placeholders still block tray-base vent slots. A future tray/standoff/side-vent redesign is required.
- Mini PC duct geometry remains a placeholder and is not matched to measured Mini PC vents.
- Filter material, pressure drop, and service position remain unresolved.
- Top exhaust fan placeholder clarifies assembly intent but does not validate cooling.

## Deferred Printability Blockers

- `rear_service_spine` still requires a future split redesign for Bambu Lab P2S printing.
- `power_bus_panel`, `power_bus_cover`, and `rear_service_spine_cover` still need split-joint or orientation planning.
- Large flat PETG parts remain warping risks and need slicer validation.

## Deferred Serviceability Blockers

- Rear Service Spine cable management still requires manual cable disconnection and cover access.
- True quick-disconnect module extraction is not designed.
- Guide rail retention and bottom fan cartridge retention require further physical interface design.

## Placeholder Limits

- MikroTik hAP ax2 and Mini PC dimensions are not verified against actual hardware.
- Raspberry Pi 3B placeholder is an engineering clearance reference, not a decorative or fully detailed board model.
- Fan placeholders represent standard 120 x 120 x 25 mm keepout geometry and do not model wire routing.
