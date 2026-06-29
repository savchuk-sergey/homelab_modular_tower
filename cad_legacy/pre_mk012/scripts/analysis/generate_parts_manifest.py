"""Generate human-readable part manifests from revision exports."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from scripts.analysis.common import add_revision_arg, iter_export_files, manifests_dir, relative_to_repo, validate_current_revision
else:
    from .common import add_revision_arg, iter_export_files, manifests_dir, relative_to_repo, validate_current_revision


MANIFEST_TARGETS = {
    "PRINTABLE_PARTS.md": ("Printable Parts", "printable"),
    "NON_PRINTABLE_PARTS.md": ("Non-Printable Reference Parts", "non_printable"),
    "PLACEHOLDERS.md": ("Device and Fan Placeholders", "placeholders"),
    "REVIEW_GEOMETRY.md": ("Review Geometry", "review"),
}


def generate_parts_manifest(revision: str) -> list[Path]:
    revision = validate_current_revision(revision)
    outputs: list[Path] = []
    for filename, (title, category) in MANIFEST_TARGETS.items():
        paths = sorted({path.with_suffix("") for path in [*iter_export_files(revision, ".stl", category), *iter_export_files(revision, ".step", category)]})
        lines = [
            f"# {title}",
            "",
            f"Revision: `{revision}`",
            "",
            "This manifest lists generated export artifacts. CadQuery source remains the source of truth.",
            "",
        ]
        if not paths:
            lines.append("No artifacts found for this category.")
        for stem_path in paths:
            name = stem_path.name
            step_path = stem_path.with_suffix(".step")
            stl_path = stem_path.with_suffix(".stl")
            lines.append(f"## {name}")
            lines.append("")
            lines.append(f"- Category: `{category}`")
            lines.append(f"- STEP: `{relative_to_repo(step_path)}`" if step_path.exists() else "- STEP: not found")
            lines.append(f"- STL: `{relative_to_repo(stl_path)}`" if stl_path.exists() else "- STL: not found")
            lines.append("")
        output = manifests_dir(revision) / filename
        output.write_text("\n".join(lines), encoding="utf-8")
        outputs.append(output)
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_revision_arg(parser)
    args = parser.parse_args()
    for path in generate_parts_manifest(args.revision):
        print(path)


if __name__ == "__main__":
    main()
