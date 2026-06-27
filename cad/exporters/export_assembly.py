"""Export the complete tower assembly."""

from pathlib import Path

from ..assembly import build_assembly


def export_assembly(step_dir: Path) -> None:
    print("Exporting assembly")
    build_assembly().save(str(step_dir / "assembly.step"))
