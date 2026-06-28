# mk0.7.4 Rough Mockup Print Plan

## Scope

This plan gives first-pass orientation and slicing controls for mk0.7.4 rough-mockup parts. It does not claim slicer validation or physical print results.

Default material is PETG unless the category is `printable/tpu` or `printable/coupons_tpu`.

## Global Controls

| Control | Recommendation |
|---|---|
| PETG bed | Clean textured/engineering plate, tuned first layer, enclosure or draft shield if available. |
| TPU bed | TPU profile, slow first layer, dry filament. |
| Supports | Avoid unless explicitly listed. Prefer orientation changes over supports. |
| Brim | Use brim for long-thin or large flat parts. |
| Large flat parts | Print alone or in small batches after `coupon_flat_petg_tile` passes. |
| Gated interfaces | Do not print full-size gated parts until the matching coupon passes. |

## Coupon Batch

Print these before full-size gated parts.

| Part | Material | Orientation | Brim | Supports | Gate |
|---|---|---|---|---|---|
| `coupon_flat_petg_tile` | PETG | Flat on largest face | 5 mm | No | Large flat PETG behavior |
| `coupon_split_joint_tab_socket` | PETG | Flat, tab/socket opening up | 3 mm | No | Split spine and power bus parts |
| `coupon_rail_end_mount_fit` | PETG | Frame pad on bed | 3 mm | No | Rail end mounts |
| `coupon_tray_ledge_stack` | PETG | Ledge/base face on bed | 3 mm | No | Tray support ledges |
| `coupon_side_panel_mount` | PETG | Long flat panel face on bed | 5 mm | No | Side panels and mount rails |
| `coupon_bottom_filter_retainer` | PETG | Filter frame face on bed | 5 mm | No | Bottom filter frame/retainer |
| `coupon_petg_foot_socket` | PETG | Socket pad on bed | 3 mm | No | Foot sockets |
| `coupon_tpu_foot` | TPU | Foot base on bed | 3 mm | No | TPU feet |
| `coupon_fan_grille_section` | PETG | Grille flat on bed | 5 mm | No | Fan grilles |

## Base and Frame

| Part | Orientation | Brim | Supports | Notes |
|---|---|---|---|---|
| `bottom_structural_frame` | Flat, frame face on bed | 5 mm | No | Keep screw/rod holes vertical. |
| `top_structural_frame` | Flat, frame face on bed | 5 mm | No | Same as bottom frame. |
| `central_bottom_fan_frame` | Flat, fan opening vertical | 8 mm | No | Large flat part; print alone if corners lift. |
| `left_foot_extension` | Flat on broad face | 5 mm | No | Wing fastener holes vertical. |
| `right_foot_extension` | Flat on broad face | 5 mm | No | Same as left. |
| `front_stability_wing` | Flat on broad face | 5 mm | No | Long part; check bed adhesion. |
| `rear_stability_wing` | Flat on broad face | 5 mm | No | Long part; check bed adhesion. |
| `corner_block` | Tall axis vertical | 3 mm | No | Keep M5 path vertical. |
| `m5_threaded_rod_cap` | Cap opening up | 3 mm | No | Small part batch OK. |

## Rails, Ledges, and Mounts

| Part | Orientation | Brim | Supports | Gate |
|---|---|---|---|---|
| `rail_end_mount` | Frame-contact face on bed | 3 mm | No | Requires `coupon_rail_end_mount_fit`. |
| `tray_support_ledge` | Screw face up, broad face on bed | 3 mm | No | Requires `coupon_tray_ledge_stack`. |
| `side_panel_mount_rail_lower` | Long side on bed, holes horizontal | 5 mm | No | Requires `coupon_side_panel_mount`. |
| `side_panel_mount_rail_middle` | Long side on bed, holes horizontal | 5 mm | No | Requires `coupon_side_panel_mount`. |
| `side_panel_mount_rail_upper` | Long side on bed, holes horizontal | 5 mm | No | Requires `coupon_side_panel_mount`. |

## Module Trays

All trays are large functional fit-check prints. Print one tray first after rail/ledge coupons pass.

| Part | Orientation | Brim | Supports | Notes |
|---|---|---|---|---|
| `ups_power_tray` | Tray base flat on bed | 8 mm | No | Conservative handling; heavy-module placeholder. |
| `external_ssd_bay` | Tray base flat on bed | 8 mm | No | Watch pocket edge curl. |
| `ssd_expansion_tray` | Tray base flat on bed | 8 mm | No | Same tray controls. |
| `raspberry_pi_tray` | Tray base flat on bed | 8 mm | No | Check board marker edges. |
| `mikrotik_tray` | Tray base flat on bed | 8 mm | No | Check rear Ethernet window. |
| `mini_pc_tray` | Tray base flat on bed | 8 mm | No | Print after lighter tray fit is acceptable. |
| `mini_pc_tray_stop` | Screw face horizontal, broad face on bed | 3 mm | No | Small part batch OK. |

## Rear Service Spine and Power Bus

Do not print these upright. Use wide-face orientation to reduce tall narrow risk.

| Part | Orientation | Brim | Supports | Gate |
|---|---|---|---|---|
| `rear_service_spine_lower` | Wide back face on bed | 8 mm | No | Requires `coupon_split_joint_tab_socket`. |
| `rear_service_spine_upper` | Wide back face on bed | 8 mm | No | Requires `coupon_split_joint_tab_socket`. |
| `rear_service_spine_cover_lower` | Outer cover face on bed | 5 mm | No | Requires split coupon. |
| `rear_service_spine_cover_upper` | Outer cover face on bed | 5 mm | No | Requires split coupon. |
| `power_bus_panel_lower` | Back face on bed | 5 mm | No | Requires split coupon. |
| `power_bus_panel_upper` | Back face on bed | 5 mm | No | Requires split coupon. |
| `power_bus_cover_lower` | Outer cover face on bed | 5 mm | No | Requires split coupon. |
| `power_bus_cover_upper` | Outer cover face on bed | 5 mm | No | Requires split coupon. |

## Side Panels

| Part | Orientation | Brim | Supports | Gate |
|---|---|---|---|---|
| `left_side_panel_lower` | Smooth exterior face on bed | 8 mm | No | Requires `coupon_side_panel_mount`. |
| `left_side_panel_middle` | Smooth exterior face on bed | 8 mm | No | Requires `coupon_side_panel_mount`. |
| `left_side_panel_upper` | Smooth exterior face on bed | 8 mm | No | Requires `coupon_side_panel_mount`. |
| `right_side_panel_lower` | Smooth exterior face on bed | 8 mm | No | Requires `coupon_side_panel_mount`. |
| `right_side_panel_middle` | Smooth exterior face on bed | 8 mm | No | Requires `coupon_side_panel_mount`. |
| `right_side_panel_upper` | Smooth exterior face on bed | 8 mm | No | Requires `coupon_side_panel_mount`. |

## Cooling and Filter

| Part | Orientation | Brim | Supports | Gate |
|---|---|---|---|---|
| `bottom_fan_grille` | Flat, grille face on bed | 8 mm | No | Requires `coupon_fan_grille_section`. |
| `top_fan_grille` | Flat, grille face on bed | 8 mm | No | Requires `coupon_fan_grille_section`. |
| `bottom_fan_cartridge` | Fan mounting face on bed | 5 mm | No | Brim recommended by `PRINT-017`. |
| `bottom_filter_frame` | Flat on bed | 8 mm | No | Requires `coupon_bottom_filter_retainer`. |
| `bottom_filter_retainer` | Flat on bed | 8 mm | No | Requires real filter-sheet coupon check. |
| `mini_pc_airflow_duct` | Duct side face on bed | 5 mm | Yes, only if bridge quality fails | Placeholder duct; final geometry deferred. |

## Feet

| Part | Material | Orientation | Brim | Supports | Gate |
|---|---|---|---|---|---|
| `foot_socket` | PETG | Socket pad on bed | 3 mm | No | Requires `coupon_petg_foot_socket`. |
| `foot` | TPU | Foot base on bed | 3 mm | No | Requires `coupon_tpu_foot`. |

## Batch Recommendation

1. Coupon batch.
2. Small hardware batch: `corner_block`, `m5_threaded_rod_cap`, `rail_end_mount`, `tray_support_ledge`, `mini_pc_tray_stop`.
3. Base sections and structural frames, one large plate per print if adhesion is marginal.
4. One light tray first, then remaining trays.
5. Rear spine/power-bus split parts.
6. Side-panel mount rails, then side panels.
7. Cooling/filter parts and TPU feet.

## Do Not Print Yet

Do not print the full-size gated families until their coupons pass:

- Rear spine and power bus split parts.
- Rail end mount set.
- Tray support ledge set.
- Side panel set and side-panel mount rails.
- Bottom filter frame/retainer.
- TPU feet and PETG foot sockets.
- Top/bottom fan grilles.
