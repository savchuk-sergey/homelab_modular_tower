# Homelab Modular Tower CAD Revision mk0.4

mk0.4 does not increase the base tower body height relative to mk0.3. The configured body height remains 321.5 mm without feet. The four removable feet add 25.0 mm of bottom intake clearance, so the assembled envelope with feet is expected to be about 346.5 mm before render/export tessellation margins.

mk0.4 не является финальной печатной версией.
mk0.4 является инженерной ревизией для улучшения печатопригодности, airflow и подготовки к slot-based архитектуре.

## Revision Goal

The goal of mk0.4 is to correct the main mk0.3 engineering weaknesses without turning the project into a taller two-mini-PC variant. This revision keeps the current module stack concept, improves bottom airflow, reduces large PETG panel risk, and introduces the first slot-based parameters for future modular growth.

## Changes From mk0.3

- Added a separate removable `foot` part intended for TPU printing.
- Added four feet to the assembly at the M5 rod corner positions.
- Added a 25.0 mm bottom air gap for the 120 mm intake fan.
- Replaced full-height left/right side panels in the assembly with three removable panel sections per side.
- Added slot-based configuration parameters: `MODULE_SLOT_COUNT`, `MODULE_SLOT_PITCH`, `LIGHT_MODULE_HEIGHT`, `COMPUTE_MODULE_HEIGHT`, `FRAME_SEGMENT_HEIGHT`, and `FRAME_SEGMENT_COUNT`.
- Added a separate `rear_service_spine_cover` part.
- Added service-spine section and cable-tie parameters for future segmented spine work.
- Updated the export registry with mk0.4 parts and compatibility aliases for frame and fan panel naming.

## mk0.3 Problems Addressed

- The bottom intake is no longer placed directly on the desk surface; the feet create a real intake plenum below the lower fan grille.
- Side panels are no longer large single PETG sheets in the active assembly. Each side is split into lower, middle, and upper sections.
- Side panels remain removable service/skin parts and are not required for the structural load path.
- The project now has explicit height-slot parameters for future module placement work.
- Rear service spine development is prepared through cover and cable-tie-slot parameters.

## Remaining mk0.4 Limits

- The structural skeleton is still a mk0.3-style full-height rod, rail, corner-block, top-frame, and bottom-frame assembly.
- `bottom_frame + repeated_middle_frame_segments + top_frame` is documented and parameterized, but middle frame segment parts are not yet implemented.
- Module tray placement still uses the existing `TRAY_STACK` unit layout rather than a full slot allocator.
- Side panel middle-section screw targets assume the future segment/mount standard; mk0.5 should add explicit middle segment mounting bosses or rails.
- The rear service spine is still one vertical printed part plus cover, not a fully segmented spine.
- Device placeholders remain approximate until real hardware measurements are taken.

## Why Body Height Was Not Increased

mk0.4 is focused on airflow, printability, serviceability, and future architecture. Increasing the tower now for a second mini PC would mix two separate engineering steps: stabilizing the current platform and designing a larger module stack. Keeping the base body height near mk0.3 makes changes easier to compare and avoids forcing users to reprint a taller skeleton before the segment strategy is proven.

## Future Expansion Strategy

Future revisions should migrate the load-bearing skeleton toward:

```text
bottom_frame + repeated_middle_frame_segments + top_frame
```

The intended expansion strategy is:

- Keep `bottom_frame` and `top_frame` reusable.
- Add printed `middle_frame_segment` parts when more module slots are required.
- Use longer M5 threaded rods for taller builds.
- Use additional metal guide rail length or rail sections for the expanded module stack.
- Add more side panel tiles instead of reprinting full side skins.
- Add more rear service spine sections instead of reprinting one taller spine.
- Keep cable routing inside the Rear Service Spine.
- Treat trays, covers, ducts, holders, and panel tiles as replaceable service parts.

This strategy should allow future modules to be added by changing slot/segment counts and printing only the new intermediate parts rather than replacing the whole tower skeleton.

## mk0.5 TODO

- Implement actual `middle_frame_segment` geometry with M5 rod pass-throughs, rail interfaces, and side-panel mounting points.
- Convert module placement from `TRAY_STACK` units to a stricter slot allocator.
- Split the rear service spine into repeated vertical sections with a matching segmented cover.
- Add explicit side-panel section mounting bosses on frame segments or dedicated panel rails.
- Validate fan intake clearance and pressure losses with physical measurements.
- Measure all real devices and replace placeholder envelopes.
- Add collision or clearance tests around panel sections, feet, fan grilles, and tray extraction paths.
