"""Run export, analysis, manifest and review-package generation for the current revision."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cad import config as cfg
from scripts.analysis.generate_review_package import generate_review_package


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default=cfg.CURRENT_REVISION)
    args = parser.parse_args()
    if args.revision != cfg.CURRENT_REVISION:
        raise SystemExit(f"Refusing to run pipeline for {args.revision}; current revision is {cfg.CURRENT_REVISION}.")
    print(generate_review_package(args.revision, refresh_exports=True))


if __name__ == "__main__":
    main()
