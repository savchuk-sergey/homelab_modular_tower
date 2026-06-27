"""CLI entrypoint for exporting all parts and the complete STEP assembly."""

import argparse

from .exporters.export_assembly import export_assembly
from .exporters.export_parts import ensure_export_dirs, export_part, export_parts, write_manifest
from .exporters.part_registry import PARTS


def export_all(revision: str | None = None) -> None:
    step_dir, stl_dir = ensure_export_dirs(revision)
    export_parts(step_dir, stl_dir)
    export_assembly(step_dir)
    if revision:
        write_manifest(step_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Homelab Modular Tower CAD parts.")
    parser.add_argument(
        "--revision",
        default=None,
        help="Optional local revision folder under exports, for example mk0.1. Omit for exports/step and exports/stl.",
    )
    args = parser.parse_args()
    export_all(args.revision or None)


__all__ = ["PARTS", "ensure_export_dirs", "export_all", "export_part", "export_parts", "write_manifest"]
