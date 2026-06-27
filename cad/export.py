"""Export all parts and the complete STEP assembly."""

import argparse
from pathlib import Path

import cadquery as cq

from . import airflow, assembly, config as cfg, frame, panels, power_bus, trays


PARTS = {
    "frame_top": frame.create_frame_top,
    "frame_bottom": frame.create_frame_bottom,
    "corner_block": frame.create_corner_block,
    "m5_threaded_rod": frame.create_m5_threaded_rod,
    "metal_guide_rail": frame.create_metal_guide_rail,
    "ups_power_tray": trays.create_ups_power_tray,
    "external_ssd_bay": trays.create_external_ssd_bay,
    "ssd_expansion_tray": trays.create_ssd_expansion_tray,
    "raspberry_pi_tray": trays.create_raspberry_pi_tray,
    "mikrotik_tray": trays.create_mikrotik_tray,
    "mini_pc_tray": trays.create_mini_pc_tray,
    "power_bus_panel": power_bus.create_power_bus_panel,
    "rear_service_spine": power_bus.create_rear_service_spine,
    "left_side_panel": panels.create_left_side_panel,
    "right_side_panel": panels.create_right_side_panel,
    "bottom_fan_panel": panels.create_bottom_fan_panel,
    "top_fan_panel": panels.create_top_fan_panel,
    "mini_pc_airflow_duct": airflow.create_mini_pc_airflow_duct,
}


def ensure_export_dirs(revision: str | None = None) -> tuple[Path, Path]:
    if revision:
        export_root = Path(cfg.EXPORTS_ROOT) / revision
        step_dir = export_root / "step"
        stl_dir = export_root / "stl"
    else:
        step_dir = Path(cfg.STEP_DIR)
        stl_dir = Path(cfg.STL_DIR)
    step_dir.mkdir(parents=True, exist_ok=True)
    stl_dir.mkdir(parents=True, exist_ok=True)
    return step_dir, stl_dir


def export_part(name: str, part: cq.Workplane, step_dir: Path, stl_dir: Path) -> None:
    cq.exporters.export(part, str(step_dir / f"{name}.step"))
    cq.exporters.export(
        part,
        str(stl_dir / f"{name}.stl"),
        tolerance=cfg.STL_TOLERANCE,
        angularTolerance=cfg.STL_ANGULAR_TOLERANCE,
    )


def export_all(revision: str | None = cfg.CURRENT_REVISION) -> None:
    step_dir, stl_dir = ensure_export_dirs(revision)
    for name, factory in PARTS.items():
        print(f"Exporting {name}")
        export_part(name, factory(), step_dir, stl_dir)

    print("Exporting assembly")
    assembly.build_assembly().save(str(step_dir / "assembly.step"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export Homelab Modular Tower CAD parts.")
    parser.add_argument(
        "--revision",
        default=cfg.CURRENT_REVISION,
        help="Revision folder under exports, for example mk0.1. Use empty string for legacy exports/step and exports/stl.",
    )
    args = parser.parse_args()
    export_all(args.revision or None)
