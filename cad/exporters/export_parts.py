"""Export individual CAD parts."""

from pathlib import Path

import cadquery as cq

from .. import config as cfg
from .part_registry import PARTS


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


def export_parts(step_dir: Path, stl_dir: Path) -> None:
    for name, factory in PARTS.items():
        print(f"Exporting {name}")
        export_part(name, factory(), step_dir, stl_dir)
