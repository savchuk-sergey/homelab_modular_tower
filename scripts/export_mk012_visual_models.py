"""Export mk0.12 CAD skeleton review models."""

from __future__ import annotations

from pathlib import Path
import sys

import cadquery as cq

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cad import config as cfg
from cad.assembly.mvp_2_module_stack import build_mvp_2_module_stack
from cad.parts.base_pedestal import build_base_pedestal
from cad.parts.module_minipc import build_minipc_stack_module
from cad.parts.module_rpi_ssd import build_rpi_ssd_stack_module
from cad.parts.top_cap import build_top_cap


def main() -> None:
    root = Path("exports") / cfg.CURRENT_REVISION / "review"
    step_dir = root / "step"
    stl_dir = root / "stl"
    step_dir.mkdir(parents=True, exist_ok=True)
    stl_dir.mkdir(parents=True, exist_ok=True)

    parts = {
        "base_pedestal": build_base_pedestal(),
        "rpi_ssd_stack_module": build_rpi_ssd_stack_module(),
        "minipc_stack_module": build_minipc_stack_module(),
        "top_cap": build_top_cap(),
    }

    for name, shape in parts.items():
        cq.exporters.export(shape, str(step_dir / f"{name}.step"))
        cq.exporters.export(shape, str(stl_dir / f"{name}.stl"), tolerance=0.2, angularTolerance=0.2)

    assembly = build_mvp_2_module_stack()
    assembly.save(str(step_dir / "mvp_2_module_stack.step"))

    manifest = root / "EXPORT_MANIFEST.md"
    manifest.write_text(
        "# mk0.12 Review Exports\n\n"
        "Generated from the active CadQuery mk0.12 skeleton. These files are derived artifacts for CAD skeleton validation and visual review only.\n\n"
        "## STEP\n\n"
        + "".join(f"- `step/{path.name}`\n" for path in sorted(step_dir.glob("*.step")))
        + "\n## STL\n\n"
        + "".join(f"- `stl/{path.name}`\n" for path in sorted(stl_dir.glob("*.stl")))
        + "\nSTL files are review/validation exports only. No final print release is implied by these exports.\n",
        encoding="utf-8",
    )

    print(f"Exported {len(list(step_dir.glob('*.step')))} STEP files")
    print(f"Exported {len(list(stl_dir.glob('*.stl')))} STL files")
    print(root)


if __name__ == "__main__":
    main()
