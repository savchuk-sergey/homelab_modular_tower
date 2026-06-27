"""Export the complete tower assembly."""

from pathlib import Path

from .. import config as cfg
from ..assembly import build_assembly


def export_assembly(step_dir: Path) -> None:
    print("Exporting assembly")
    assembly = build_assembly()
    if step_dir.name.startswith("mk"):
        assembly_dir = step_dir / "assemblies"
        assembly_dir.mkdir(parents=True, exist_ok=True)
        assembly.save(str(assembly_dir / "assembly.step"))
        return

    assembly.save(str(step_dir / "assembly.step"))
    assembly_dir = Path(cfg.EXPORTS_ROOT) / "assembly"
    assembly_dir.mkdir(parents=True, exist_ok=True)
    assembly.save(str(assembly_dir / "assembly.step"))
