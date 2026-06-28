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


def write_print_manifest(export_root: Path) -> None:
    lines = [
        f"# {cfg.CURRENT_REVISION} Print Manifest",
        "",
        "This manifest separates printable prototype parts from reference-only geometry.",
        "CadQuery source remains the source of truth; STEP/STL files are derived artifacts.",
        "",
        "## Print these for module-level prototype",
        "",
        "- `base_module`",
        "- `rpi_ssd_module`",
        "- `mini_pc_placeholder_module`",
        "- `roof_module`",
        "- `foot` / TPU feet",
        "- `rail_end_clip` if rail end retention is tested as a separate printed part",
        "",
        "## Do not print separately if printing module assemblies",
        "",
        "- `rpi_ssd_carriage` if it is already included in `rpi_ssd_module`",
        "- `mini_pc_placeholder_carriage` if it is already included in `mini_pc_placeholder_module`",
        "- `bottom_grill` if it is already included in `base_module`",
        "- `top_filter_slot` if it is already included in `roof_module`",
        "- `foot_mounts` if they are already included in `base_module`",
        "",
        "## Reference only / do not print",
        "",
        "- `aluminum_u_channel_rail_placeholder`",
        "- `pom_c_shoe_placeholder`",
        "- `m5_threaded_rod`",
        "- fan placeholders",
        "- device placeholders",
        "- filter placeholders",
        "- `tpu_foot_placeholder` unless it is intentionally selected instead of `foot`",
        "",
        "## Legacy / do not use for mk0.9.3",
        "",
        "- old trays",
        "- old flat rail mounts",
        "- old rail ledges",
        "- `rail_end_mount`",
        "- `tray_support_ledge`",
        "- `rpi_ssd_tray`",
        "- `mini_pc_placeholder_tray`",
        "",
    ]
    (export_root / "PRINT_MANIFEST.md").write_text("\n".join(lines), encoding="utf-8")
