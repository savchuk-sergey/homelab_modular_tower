# mk0.9.2 BOM Notes

## Printable PETG

Pipeline mesh estimates from `analysis/plastic_estimate.csv`:

| Part | Estimated PETG mass |
| --- | ---: |
| base_module | 255.310 g |
| rpi_ssd_module | 258.641 g |
| rpi_ssd_carriage | 38.957 g |
| mini_pc_placeholder_module | 276.321 g |
| mini_pc_placeholder_carriage | 47.201 g |
| roof_module | 273.122 g |
| bottom_grill | 52.085 g |
| dust_filter_slot | 9.933 g |
| top_filter_slot | 14.641 g |
| foot_mounts | 6.421 g |
| rail_end_clip | 0.729 g |
| m5_threaded_rod_cap | 0.898 g |

These are mesh solid-volume estimates only.

## Printable TPU

| Part | Estimated mass |
| --- | ---: |
| foot | 5.137 g |
| tpu_foot_placeholder | 5.137 g |

## Non-printed references

- Four M5 threaded rods remain the primary vertical structural reference.
- Aluminum U-channel rail placeholder: 15 x 10 x 10 x 2 mm profile.
- POM-C shoe placeholder: 8 mm diameter, 12 mm length.

## Open BOM items

- Real fastener count for rail pocket/end-stop installation needs manual
  assembly review.
- Slicer-specific material use must be checked before print planning.
