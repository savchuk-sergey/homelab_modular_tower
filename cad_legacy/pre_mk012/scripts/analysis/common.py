"""Shared helpers for current-revision engineering review analysis."""

from __future__ import annotations

import argparse
import csv
import shutil
import sys
from pathlib import Path
from typing import Iterable


REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from cad import config as cfg  # noqa: E402


def current_revision() -> str:
    return cfg.CURRENT_REVISION


def validate_current_revision(revision: str) -> str:
    if revision != cfg.CURRENT_REVISION:
        raise SystemExit(
            f"Refusing to generate review outputs for {revision}; current revision is {cfg.CURRENT_REVISION}."
        )
    return revision


def add_revision_arg(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--revision", default=cfg.CURRENT_REVISION, help="Current revision to analyze.")


def exports_dir(revision: str) -> Path:
    return REPO_ROOT / cfg.EXPORTS_ROOT / revision


def revision_dir(revision: str) -> Path:
    return REPO_ROOT / "revisions" / revision


def review_package_dir(revision: str) -> Path:
    return revision_dir(revision) / cfg.REVIEW_PACKAGE_DIR_NAME


def analysis_dir(revision: str) -> Path:
    path = revision_dir(revision) / cfg.REVIEW_ANALYSIS_DIR_NAME
    path.mkdir(parents=True, exist_ok=True)
    return path


def manifests_dir(revision: str) -> Path:
    path = revision_dir(revision)
    path.mkdir(parents=True, exist_ok=True)
    return path


def require_exports(revision: str) -> Path:
    root = exports_dir(revision)
    if not root.exists():
        raise SystemExit(f"Missing exports for {revision}: {root}. Run `python -m cad.export --revision {revision}`.")
    return root


def relative_to_repo(path: Path) -> str:
    return path.resolve().relative_to(REPO_ROOT).as_posix()


def export_category(path: Path, revision: str) -> str:
    rel = path.resolve().relative_to(exports_dir(revision).resolve())
    if len(rel.parts) <= 1:
        return "."
    return "/".join(rel.parts[:-1])


def iter_export_files(revision: str, suffix: str, category_prefix: str | None = None) -> list[Path]:
    root = require_exports(revision)
    if category_prefix:
        root = root / Path(category_prefix)
    if not root.exists():
        return []
    return sorted(path for path in root.rglob(f"*{suffix}") if path.is_file())


def write_csv(path: Path, fieldnames: Iterable[str], rows: Iterable[dict[str, object]]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(fieldnames))
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return path


def copytree_replace(source: Path, destination: Path) -> None:
    if destination.exists():
        shutil.rmtree(destination)
    if source.exists():
        shutil.copytree(source, destination)


def copy_file_if_exists(source: Path, destination: Path) -> bool:
    if not source.exists():
        return False
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)
    return True
