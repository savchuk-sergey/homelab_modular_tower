# mk0.7.4 Coupon Test Plan

## Purpose

These coupons gate large mk0.7.4 rough-mockup prints. They validate fit, screw access, and basic print behavior for interfaces that the CAD cannot prove physically.

No full-size rear spine, tray stack, side-panel set, fan grille set, or filter assembly should be printed until the relevant coupon is printed, inspected, and recorded here.

## Coupon Exports

| Coupon | Export category | Interface under test | Material | Required before |
|---|---|---|---|---|
| `coupon_split_joint_tab_socket` | `printable/coupons_petg` | Rear spine / power-bus split tab, socket, M3 path | PETG | Full spine and power-bus split prints |
| `coupon_rail_end_mount_fit` | `printable/coupons_petg` | Rail end mount capture, vertical frame screw target | PETG plus real metal rail for fit check | Full rail end mount set |
| `coupon_tray_ledge_stack` | `printable/coupons_petg` | Tray ledge, tray edge, rail keepout relationship | PETG | Full tray stack support ledges |
| `coupon_side_panel_mount` | `printable/coupons_petg` | Side-panel boss to mount-rail screw path and clearance | PETG | Full side-panel set |
| `coupon_bottom_filter_retainer` | `printable/coupons_petg` | Filter frame/retainer corner grip and stiffness | PETG plus real filter sheet | Bottom filter assembly |
| `coupon_petg_foot_socket` | `printable/coupons_petg` | PETG socket boss for TPU foot | PETG | Base foot socket set |
| `coupon_tpu_foot` | `printable/coupons_tpu` | TPU foot fit, screw clearance, counterbore | TPU | Base feet |
| `coupon_flat_petg_tile` | `printable/coupons_petg` | Baseline PETG shrink/warp tile | PETG | Large flat parts |
| `coupon_fan_grille_section` | `printable/coupons_petg` | Fan grille bar adhesion, screw hole quality, edge curl | PETG | Top/bottom fan grilles |

## Suggested Print Order

1. `coupon_flat_petg_tile`
2. `coupon_split_joint_tab_socket`
3. `coupon_rail_end_mount_fit`
4. `coupon_tray_ledge_stack`
5. `coupon_side_panel_mount`
6. `coupon_bottom_filter_retainer`
7. `coupon_petg_foot_socket` and `coupon_tpu_foot`
8. `coupon_fan_grille_section`

## Acceptance Checks

| Coupon | Pass condition | Failure response |
|---|---|---|
| `coupon_flat_petg_tile` | Tile stays flat enough that corners do not lift into the first functional layer height. | Tune PETG profile, brim, bed prep, or enclosure before large plates. |
| `coupon_split_joint_tab_socket` | Tab enters socket without cracking; M3 screw path remains usable after insertion. | Adjust `SPLIT_JOINT_SOCKET_CLEARANCE`, tab width, or tab depth. |
| `coupon_rail_end_mount_fit` | Real rail enters capture slot; vertical screw path aligns with frame pad; no wall splits. | Adjust `METAL_RAIL_FRAME_CLEARANCE`, capture depth, or screw offset. |
| `coupon_tray_ledge_stack` | Representative tray edge rests cleanly on ledge and does not collide with rail keepout. | Adjust ledge height/depth or tray rail clearance. |
| `coupon_side_panel_mount` | Screw passes from panel boss into rail path; boss clears rail volume with visible margin. | Add local relief, change rail inset, or change boss/rib height. |
| `coupon_bottom_filter_retainer` | Filter sheet can be inserted/retained without breaking retainer corner. | Change retainer rail width, height, or corner pad geometry. |
| `coupon_petg_foot_socket` / `coupon_tpu_foot` | TPU foot seats in socket and screw/counterbore remain accessible. | Adjust socket clearance, TPU diameter, or counterbore. |
| `coupon_fan_grille_section` | Bars stay attached, no severe curl, screw holes remain round enough for fan screws. | Add brim, change orientation, or revise bar width/thickness. |

## Result Table

| Coupon | Result | Required Change | Status |
|---|---|---|---|
| `coupon_flat_petg_tile` | Not printed | TBD | `NOT TESTED` |
| `coupon_split_joint_tab_socket` | Not printed | TBD | `NOT TESTED` |
| `coupon_rail_end_mount_fit` | Not printed | TBD | `NOT TESTED` |
| `coupon_tray_ledge_stack` | Not printed | TBD | `NOT TESTED` |
| `coupon_side_panel_mount` | Not printed | TBD | `NOT TESTED` |
| `coupon_bottom_filter_retainer` | Not printed | TBD | `NOT TESTED` |
| `coupon_petg_foot_socket` | Not printed | TBD | `NOT TESTED` |
| `coupon_tpu_foot` | Not printed | TBD | `NOT TESTED` |
| `coupon_fan_grille_section` | Not printed | TBD | `NOT TESTED` |

## Gate Status

Chunk 3 state: `PASS WITH COUPON REQUIRED` once these coupon STLs export successfully and remain manifold. Physical results are still required before the related full-size prints.
