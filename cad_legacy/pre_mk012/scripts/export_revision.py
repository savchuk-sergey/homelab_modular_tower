"""Export the current CAD revision into exports/<revision>."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from cad import config as cfg
from cad.export import export_all


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--revision", default=cfg.CURRENT_REVISION)
    args = parser.parse_args()
    if args.revision != cfg.CURRENT_REVISION:
        raise SystemExit(f"Refusing to export {args.revision}; current revision is {cfg.CURRENT_REVISION}.")
    export_all(args.revision)


if __name__ == "__main__":
    main()
