"""Export individual CAD parts."""

from pathlib import Path

import cadquery as cq

from .. import config as cfg
from .part_registry import EXPORT_CATEGORIES, PARTS


def ensure_export_dirs(revision: str | None = None) -> tuple[Path, Path]:
    if revision:
        export_root = Path(cfg.EXPORTS_ROOT) / revision
        step_dir = export_root
        stl_dir = export_root
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
    if step_dir == stl_dir and step_dir.name.startswith("mk"):
        export_categorized_parts(step_dir)
        return

    for name, factory in PARTS.items():
        print(f"Exporting {name}")
        export_part(name, factory(), step_dir, stl_dir)


def export_categorized_parts(export_root: Path) -> None:
    for category, parts in EXPORT_CATEGORIES.items():
        category_dir = export_root / category
        category_dir.mkdir(parents=True, exist_ok=True)
        for name, factory in parts.items():
            print(f"Exporting {category}/{name}")
            export_part(name, factory(), category_dir, category_dir)


def write_manifest(export_root: Path) -> None:
    lines = [
        f"# {cfg.CURRENT_REVISION} export manifest",
        "",
        "Generated from CadQuery source. STEP/STL files are derived artifacts.",
        "",
    ]
    for category, parts in EXPORT_CATEGORIES.items():
        lines.append(f"## {category}")
        lines.append("")
        for name in sorted(parts):
            lines.append(f"- `{name}`")
        lines.append("")
    (export_root / "MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")
