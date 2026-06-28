# mk0.7.4 Rough Mockup Fastener BOM

## Scope

This is a rough-mockup hardware list for assembly planning. It identifies hardware classes and minimum counts, but screw lengths remain `TBD after stack check` where the final stack depends on real rail, washer, insert, or printed-part tolerance.

## Primary Structure

| Item | Size | Count | Notes |
|---|---:|---:|---|
| Threaded rods | M5 x `339.5 mm` | 4 | Main vertical load path; cut length from `ROD_LENGTH`. |
| Hex nuts | M5 | 8 minimum | One top and one bottom per rod. Use 16 if locking both sides of both structural frames. |
| Flat washers | M5 | 8 minimum | One under each nut; use larger count if leveling or shimming is needed. |
| Nylock or acorn nuts | M5 | 4 optional | Top-side finish/locking after mockup fit is verified. |
| Printed rod caps | M5 cap print | 4 | Cosmetic/protective, not structural. |

## Metal Rails

| Item | Size | Count | Notes |
|---|---:|---:|---|
| Metal guide rails | `10 x 3 x 287.5 mm` nominal | 4 | Real rail tolerance is coupon-gated by `coupon_rail_end_mount_fit`. |
| Rail end mount screws into frame | M3, length TBD | 8 | One vertical screw per rail end mount. |
| Rail-to-mount side screws | M3, length TBD | 8 | Optional for rough mockup if the rail end capture is already tight; validate with coupon first. |
| Heat-set inserts or tapped frame targets | M3 | 8 | Required if frame holes are converted from clearance-only to insert/tapped targets. |

## Tray Stack

| Item | Size | Count | Notes |
|---|---:|---:|---|
| Tray support ledge screws | M3, length TBD | 24 | Six tray levels x four guide rail positions. |
| Tray support ledge inserts or rail nuts | M3 | 24 | Depends on final choice: inserts in printed ledges, tapped metal rails, or small rail nuts. |
| Module front lock screws | M3, length TBD | 6 | One per removable tray front lock. |
| Module front lock heat-set inserts | M3 `5.2 x 5.0 mm` nominal | 6 | Uses `HEAT_SET_INSERT_M3_DIAMETER` and `HEAT_SET_INSERT_M3_DEPTH`. |

## Side Panels

| Item | Size | Count | Notes |
|---|---:|---:|---|
| Side-panel mount rail screws | M3, length TBD | 24 | Six panel tiles x four panel mount points. |
| Structural side-panel heat-set inserts | M3 `5.2 x 5.0 mm` nominal | 16 | Lower and upper structural tiles only: two sides x two sections x four bosses. |
| Side-panel middle-section nuts/inserts | M3, TBD | 8 | Middle tiles are not treated as shear panels in mk0.7.4. |

## Rear Service Spine and Power Bus

| Item | Size | Count | Notes |
|---|---:|---:|---|
| Rear service spine frame screws | M3, length TBD | 7 | Uses `REAR_SPINE_STRUCTURAL_MOUNT_Z`. |
| Rear service spine cover screws | M3, length TBD | 7 | Cover is removable for cable service. |
| Power bus panel screws | M3, length TBD | 8 | Two screws per voltage/ground rail placeholder. |
| Power bus cover screws | M3, length TBD | 8 | Match power bus panel service points. |

## Cooling and Base

| Item | Size | Count | Notes |
|---|---:|---:|---|
| 120 mm fan screws | M4 or fan screw, TBD | 8 | Four bottom intake, four top exhaust. Match actual fan hardware. |
| Bottom fan cartridge screws | M3, length TBD | 4 | Uses cartridge mount holes. |
| Bottom filter retainer screws or clips | TBD | TBD | Coupon decides whether screw retention is needed. |
| Foot screws | M5 or coarse screw, TBD | 4 | Validate PETG socket plus TPU foot with `coupon_petg_foot_socket` and `coupon_tpu_foot`. |
| Sectional base wing screws | M3, length TBD | 16 | Four wing sections x four wing fasteners. |

## Consumables and Tools

| Item | Count | Notes |
|---|---:|---|
| M3 heat-set inserts | 60 minimum | Covers known insert-like positions with margin for failed installs and optional targets. |
| M3 screw assortment | 1 set | Include short lengths around 6-16 mm; exact lengths are stack-check gated. |
| M5 washers/nuts spare | 1 small set | Useful for leveling and temporary mockup locking. |
| Threadlocker | optional | Use only after fit is confirmed. |

## Open BOM Checks

| Check | Status |
|---|---|
| Confirm exact metal rail stock and hole pattern | `TBD after rail coupon` |
| Confirm M3 screw lengths through rail end mounts | `TBD after stack check` |
| Confirm side-panel screw length and insert depth | `TBD after side-panel coupon` |
| Confirm foot screw type | `TBD after TPU/PETG coupon` |
| Confirm fan screw type from actual 120 mm fans | `TBD after fan selection` |
