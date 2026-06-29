"""Run analysis CSV generation for the current CAD revision."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cad import config as cfg
from scripts.analysis.check_print_volume import check_print_volume
from scripts.analysis.check_stl_quality import check_stl_quality
from scripts.analysis.detect_duplicate_geometry import detect_duplicate_geometry
from scripts.analysis.estimate_plastic_volume import estimate_plastic_volume
from scripts.analysis.measure_parts import measure_parts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default=cfg.CURRENT_REVISION)
    args = parser.parse_args()
    if args.revision != cfg.CURRENT_REVISION:
        raise SystemExit(f"Refusing to analyze {args.revision}; current revision is {cfg.CURRENT_REVISION}.")
    for path in (
        measure_parts(args.revision),
        check_print_volume(args.revision),
        estimate_plastic_volume(args.revision),
        check_stl_quality(args.revision),
        detect_duplicate_geometry(args.revision),
    ):
        print(path)


if __name__ == "__main__":
    main()
