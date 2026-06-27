# mk0.7.1 Self Check

| check | result | evidence |
| --- | --- | --- |
| mk0.7 history was not rewritten | PASS | Patch files are under `revisions/mk0.7.1`, `exports/mk0.7.1`, and current CAD source. |
| Generated artifacts are signed as mk0.7.1 | PASS | `cad/config.py` has `CURRENT_REVISION = "mk0.7.1"`. |
| Export categories are separated | PASS | `exports/mk0.7.1/` contains `printable`, `non_printable`, `placeholders`, `review`, and `assemblies`. |
| Printable plastic parts are separate from TPU | PASS | `foot` is exported under `printable/tpu`. |
| Fan placeholder is not printable | PASS | `fan_120x120x25_placeholder` is exported under `placeholders/fans`. |
| Raspberry Pi 3B placeholder is not printable | PASS | `raspberry_pi_3b_placeholder` is exported under `placeholders/devices`. |
| Review geometry is not printable | PASS | Review artifacts are exported under `review`. |
| `bottom_fan_cartridge` STL quality blocker is fixed | PASS | `stl_quality.csv` reports it as watertight/manifold. |
| Duplicate geometry check pipeline is restored | PASS | `duplicate_geometry_check.csv` was generated without the mk0.7 AttributeError. |
| Analysis CSV files exist | PASS | `part_dimensions.csv`, `printability_check.csv`, `plastic_estimate.csv`, `stl_quality.csv`, `duplicate_geometry_check.csv`. |
| Review package ZIP exists | PASS | `revisions/mk0.7.1/review_package/mk0.7.1_review_package.zip`. |
| Known limitations are documented | PASS | `KNOWN_LIMITATIONS.md` documents unresolved safety, airflow, printability, and serviceability risks. |
| No unsupported CFD/FEA/physical-test claims | PASS | Revision docs explicitly state none were performed. |

## Remaining NO-GO Items

- Full tower build remains NO-GO until safety, power, airflow, printability, and serviceability blockers are resolved.
- Physical fit and print tests are still required.
- Electrical safety validation is still required.
