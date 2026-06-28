"""Generate the current revision external engineering review package."""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
    from cad.export import export_all
    from scripts.analysis.check_print_volume import check_print_volume
    from scripts.analysis.check_stl_quality import check_stl_quality
    from scripts.analysis.common import (
        REPO_ROOT,
        add_revision_arg,
        copy_file_if_exists,
        copytree_replace,
        exports_dir,
        relative_to_repo,
        require_exports,
        review_package_dir,
        revision_dir,
        validate_current_revision,
    )
    from scripts.analysis.detect_duplicate_geometry import detect_duplicate_geometry
    from scripts.analysis.estimate_plastic_volume import estimate_plastic_volume
    from scripts.analysis.generate_parts_manifest import generate_parts_manifest
    from scripts.analysis.measure_parts import measure_parts
else:
    from cad.export import export_all
    from .check_print_volume import check_print_volume
    from .check_stl_quality import check_stl_quality
    from .common import (
        REPO_ROOT,
        add_revision_arg,
        copy_file_if_exists,
        copytree_replace,
        exports_dir,
        relative_to_repo,
        require_exports,
        review_package_dir,
        revision_dir,
        validate_current_revision,
    )
    from .detect_duplicate_geometry import detect_duplicate_geometry
    from .estimate_plastic_volume import estimate_plastic_volume
    from .generate_parts_manifest import generate_parts_manifest
    from .measure_parts import measure_parts


REVISION_NOTE_FILES = (
    "REVISION.md",
    "REVISION_NOTES.md",
    "CALCULATIONS.md",
    "DECISIONS.md",
    "KNOWN_ISSUES.md",
    "KNOWN_LIMITATIONS.md",
    "CHANGELOG.md",
    "CHANGELOG_FROM_MK0.7.md",
    "COUPON_TEST_PLAN.md",
    "FASTENER_BOM.md",
    "ASSEMBLY_SEQUENCE.md",
    "PRINT_PLAN.md",
    "FINAL_READINESS_REVIEW.md",
    "MANIFEST.md",
    "REVIEW_FINDINGS_INPUT.md",
    "MK0.7.1_SCOPE.md",
    "MK0.7.1_SELF_CHECK.md",
    "PRINTABLE_PARTS.md",
    "NON_PRINTABLE_PARTS.md",
    "PLACEHOLDERS.md",
    "REVIEW_GEOMETRY.md",
)


def generate_review_package(revision: str, refresh_exports: bool = False) -> Path:
    revision = validate_current_revision(revision)
    if refresh_exports or not exports_dir(revision).exists():
        export_all(revision)
    require_exports(revision)

    package = review_package_dir(revision)
    package.mkdir(parents=True, exist_ok=True)

    _copy_optional_tree(exports_dir(revision), package / "exports")
    _copy_optional_tree(REPO_ROOT / "renders" / revision, package / "renders")
    _copy_optional_tree(REPO_ROOT / "drawings" / revision, package / "drawings")
    _copy_revision_notes(revision, package)

    csv_outputs = [
        measure_parts(revision),
        check_print_volume(revision),
        estimate_plastic_volume(revision),
        check_stl_quality(revision),
        detect_duplicate_geometry(revision),
    ]
    manifest_outputs = generate_parts_manifest(revision)
    _copy_analysis_outputs(csv_outputs, package)
    _copy_manifest_outputs(manifest_outputs, package)
    checklist = _write_requirements_checklist(revision, package, csv_outputs, manifest_outputs)
    overview = _write_assembly_overview(revision, package)
    review_inputs = _write_review_inputs(revision, csv_outputs, manifest_outputs, checklist, overview)
    copy_file_if_exists(review_inputs, package / "revision_notes" / "REVIEW_INPUTS.md")
    _write_package_zip(revision, package)
    return package


def _copy_optional_tree(source: Path, destination: Path) -> None:
    if source.exists() and not destination.exists():
        copytree_replace(source, destination)
        return
    if source.exists():
        _copy_missing_files(source, destination)
        return
    destination.mkdir(parents=True, exist_ok=True)
    (destination / "README.md").write_text(
        "No artifacts were found for this category in the current revision workspace.\n",
        encoding="utf-8",
    )


def _copy_missing_files(source: Path, destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for path in source.rglob("*"):
        if not path.is_file():
            continue
        target = destination / path.relative_to(source)
        if target.exists():
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def _copy_revision_notes(revision: str, package: Path) -> None:
    notes_dir = package / "revision_notes"
    notes_dir.mkdir(parents=True, exist_ok=True)
    source_dir = revision_dir(revision)
    for filename in REVISION_NOTE_FILES:
        copy_file_if_exists(source_dir / filename, notes_dir / filename)


def _copy_analysis_outputs(outputs: list[Path], package: Path) -> None:
    analysis = package / "analysis"
    analysis.mkdir(parents=True, exist_ok=True)
    for path in outputs:
        copy_file_if_exists(path, analysis / path.name)


def _copy_manifest_outputs(outputs: list[Path], package: Path) -> None:
    manifests = package / "manifests"
    manifests.mkdir(parents=True, exist_ok=True)
    for path in outputs:
        copy_file_if_exists(path, manifests / path.name)


def _write_requirements_checklist(revision: str, package: Path, csv_outputs: list[Path], manifests: list[Path]) -> Path:
    exports_root = package / "exports"
    lines = [
        f"# {revision} Review Package Requirements Checklist",
        "",
        "This checklist records whether evidence files exist. It does not approve the engineering design.",
        "",
        f"- Exports copied: `{(package / 'exports').exists()}`",
        f"- Assembly STEP present: `{(exports_root / 'assemblies' / 'assembly.step').exists()}`",
        f"- Analysis CSV count: `{len(csv_outputs)}`",
        f"- Manifest document count: `{len(manifests)}`",
        f"- Renders included: `{(package / 'renders').exists()}`",
        f"- Drawings included: `{(package / 'drawings').exists()}`",
        "",
        "## CSV files",
        "",
    ]
    for path in csv_outputs:
        lines.append(f"- `{relative_to_repo(path)}`")
    lines.extend(["", "## Manifest files", ""])
    for path in manifests:
        lines.append(f"- `{relative_to_repo(path)}`")
    output = package / "REVIEW_REQUIREMENTS_CHECKLIST.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def _write_assembly_overview(revision: str, package: Path) -> Path:
    root = package / "exports"
    counts = {
        "printable STL": len(list((root / "printable").rglob("*.stl"))) if (root / "printable").exists() else 0,
        "non-printable STL": len(list((root / "non_printable").rglob("*.stl"))) if (root / "non_printable").exists() else 0,
        "placeholder STL": len(list((root / "placeholders").rglob("*.stl"))) if (root / "placeholders").exists() else 0,
        "review STL": len(list((root / "review").rglob("*.stl"))) if (root / "review").exists() else 0,
        "assembly STEP": len(list((root / "assemblies").rglob("*.step"))) if (root / "assemblies").exists() else 0,
    }
    lines = [
        f"# {revision} Assembly Overview",
        "",
        "This file summarizes available generated artifacts for external review. It does not validate fit, strength, airflow, print orientation, or assembly procedure.",
        "",
    ]
    for label, count in counts.items():
        lines.append(f"- {label}: `{count}`")
    lines.extend(
        [
            "",
            "Primary assembly artifact:",
            "",
            f"- `{relative_to_repo(root / 'assemblies' / 'assembly.step')}`",
        ]
    )
    output = package / "ASSEMBLY_OVERVIEW.md"
    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def _write_review_inputs(
    revision: str,
    csv_outputs: list[Path],
    manifests: list[Path],
    checklist: Path,
    overview: Path,
) -> Path:
    output = revision_dir(revision) / "REVIEW_INPUTS.md"
    lines = [
        f"# {revision} Review Inputs",
        "",
        "This review package prepares evidence for external engineering review by AI agents. It does not make unsupported engineering approval claims.",
        "",
        "## Included Artifacts",
        "",
        f"- Export copy: `revisions/{revision}/review_package/exports/`",
        f"- Analysis CSV files: `revisions/{revision}/review_package/analysis/`",
        f"- Manifest documents: `revisions/{revision}/review_package/manifests/`",
        f"- Revision notes copy: `revisions/{revision}/review_package/revision_notes/`",
        f"- Assembly overview: `{relative_to_repo(overview)}`",
        f"- Requirements checklist: `{relative_to_repo(checklist)}`",
        "",
        "## CSV Meaning",
        "",
        "- `part_dimensions.csv`: bounding boxes for STL and STEP exports where the file could be parsed.",
        "- `printability_check.csv`: axis-aligned printable STL dimensions compared with configured Bambu Lab P2S volume and long-thin geometry flags.",
        "- `plastic_estimate.csv`: mesh solid volume and PETG/PLA mass estimates from printable STL files.",
        "- `stl_quality.csv`: STL triangle count plus watertight/manifold indicators from edge counting.",
        "- `duplicate_geometry_check.csv`: geometry hash and near-duplicate grouping based on STL geometry, bounding box and volume.",
        "",
        "## What Was Measured",
        "",
        "- Generated STL bounding boxes.",
        "- Generated STEP bounding boxes where CadQuery could import the STEP file.",
        "- Printable STL mesh volume.",
        "- STL edge-based watertight/manifold indicators.",
        "- Duplicate and near-duplicate STL signatures.",
        "",
        "## What Was Not Measured",
        "",
        "- Mechanical strength, stiffness, fatigue or fastener pull-out.",
        "- Thermal performance, airflow pressure drop or CFD.",
        "- Slicer-specific print time, supports, infill, purge, seam placement or print orientation.",
        "- Real-world assembly tolerance stack-up.",
        "- Electrical safety or power-distribution validation.",
        "",
        "## Known Limitations",
        "",
        "- Mesh volume is not slicer material usage.",
        "- Axis-aligned print-volume checks do not search for rotated fit.",
        "- Long-thin geometry detection is a heuristic for review prioritization.",
        "- STL watertight/manifold checks are based on exported mesh edges and may not identify every CAD modeling issue.",
        "- Placeholder and review geometry are included for context but are not printable production parts.",
        "",
        "## Generated Files",
        "",
    ]
    for path in [*csv_outputs, *manifests, checklist, overview]:
        lines.append(f"- `{relative_to_repo(path)}`")
    output.write_text("\n".join(lines), encoding="utf-8")
    return output


def _write_package_zip(revision: str, package: Path) -> Path:
    zip_path = package / f"{revision}_review_package.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(package.rglob("*")):
            if path == zip_path or not path.is_file():
                continue
            archive.write(path, path.relative_to(package))
    return zip_path


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    add_revision_arg(parser)
    parser.add_argument("--refresh-exports", action="store_true", help="Recreate current revision exports before packaging.")
    args = parser.parse_args()
    print(generate_review_package(args.revision, refresh_exports=args.refresh_exports))


if __name__ == "__main__":
    main()
