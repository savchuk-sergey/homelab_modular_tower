"""Estimate printable STL mesh volume and material mass."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from cad import config as cfg
    from scripts.analysis.common import add_revision_arg, analysis_dir, export_category, iter_export_files, relative_to_repo, validate_current_revision, write_csv
    from scripts.analysis.stl_mesh import mesh_stats
else:
    from cad import config as cfg
    from .common import add_revision_arg, analysis_dir, export_category, iter_export_files, relative_to_repo, validate_current_revision, write_csv
    from .stl_mesh import mesh_stats


FIELDS = [
    "part_name",
    "category",
    "relative_path",
    "status",
    "mesh_volume_mm3",
    "mesh_volume_cm3",
    "petg_density_g_cm3",
    "pla_density_g_cm3",
    "estimated_petg_mass_g",
    "estimated_pla_mass_g",
    "notes",
]

PRINTED_CATEGORY_PREFIXES = (
    "printed/plastic_modules",
    "printed/plastic_subparts",
    "printed/tpu",
)


def estimate_plastic_volume(revision: str) -> Path:
    revision = validate_current_revision(revision)
    rows: list[dict[str, object]] = []
    paths: list[Path] = []
    for category_prefix in PRINTED_CATEGORY_PREFIXES:
        paths.extend(iter_export_files(revision, ".stl", category_prefix))

    for path in sorted(paths):
        row: dict[str, object] = {
            "part_name": path.stem,
            "category": export_category(path, revision),
            "relative_path": relative_to_repo(path),
            "status": "ok",
            "petg_density_g_cm3": cfg.PETG_DENSITY_G_PER_CM3,
            "pla_density_g_cm3": cfg.PLA_DENSITY_G_PER_CM3,
            "notes": "mesh solid volume only; slicer infill, perimeters, supports and purge are not included",
        }
        try:
            stats = mesh_stats(path)
            volume_cm3 = stats.volume_mm3 / 1000.0
            row.update(
                {
                    "mesh_volume_mm3": f"{stats.volume_mm3:.3f}",
                    "mesh_volume_cm3": f"{volume_cm3:.3f}",
                    "estimated_petg_mass_g": f"{volume_cm3 * cfg.PETG_DENSITY_G_PER_CM3:.3f}",
                    "estimated_pla_mass_g": f"{volume_cm3 * cfg.PLA_DENSITY_G_PER_CM3:.3f}",
                }
            )
        except Exception as exc:
            row["status"] = "error"
            row["notes"] = f"{type(exc).__name__}: {exc}"
        rows.append(row)
    return write_csv(analysis_dir(revision) / "plastic_estimate.csv", FIELDS, rows)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_revision_arg(parser)
    args = parser.parse_args()
    print(estimate_plastic_volume(args.revision))


if __name__ == "__main__":
    main()
