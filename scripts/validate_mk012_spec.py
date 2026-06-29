"""Validate the mk0.12 pre-CAD engineering specification without CadQuery."""

from __future__ import annotations

import math
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cad import config as cfg  # noqa: E402


@dataclass(frozen=True)
class CheckResult:
    status: str
    title: str
    detail: str


RESULTS: list[CheckResult] = []


def report(status: str, title: str, detail: str) -> None:
    RESULTS.append(CheckResult(status, title, detail))


def close(a: float, b: float, tolerance: float = 1e-6) -> bool:
    return abs(a - b) <= tolerance


def distance_point_to_rect_gap(
    point_x: float,
    point_y: float,
    radius: float,
    bounds: tuple[float, float, float, float],
) -> float:
    x_min, x_max, y_min, y_max = bounds
    dx = max(x_min - point_x, 0.0, point_x - x_max)
    dy = max(y_min - point_y, 0.0, point_y - y_max)
    return math.hypot(dx, dy) - radius


def min_gap_from_rods_to_rect(bounds: tuple[float, float, float, float]) -> tuple[float, tuple[float, float]]:
    rod_radius = cfg.M5_ROD_CLEARANCE_DIAMETER / 2
    gaps = [
        (distance_point_to_rect_gap(x, y, rod_radius, bounds), (x, y))
        for x, y in cfg.m5_rod_centers()
    ]
    return min(gaps, key=lambda item: item[0])


def validate_revision() -> None:
    if cfg.CURRENT_REVISION == "mk0.12":
        report("PASS", "Revision", 'CURRENT_REVISION = "mk0.12".')
    else:
        report("FAIL", "Revision", f'Expected mk0.12, got "{cfg.CURRENT_REVISION}".')


def validate_stack_height() -> None:
    required_rod = (
        cfg.TOTAL_STACK_HEIGHT
        + cfg.ROD_EXTRA_THREAD_ALLOWANCE_BOTTOM
        + cfg.ROD_EXTRA_THREAD_ALLOWANCE_TOP
    )

    if close(cfg.TOTAL_STACK_HEIGHT, 238.0):
        report("PASS", "Stack height", f"TOTAL_STACK_HEIGHT = {cfg.TOTAL_STACK_HEIGHT:.1f} mm.")
    else:
        report("FAIL", "Stack height", f"Expected 238.0 mm, got {cfg.TOTAL_STACK_HEIGHT:.1f} mm.")

    if cfg.RECOMMENDED_M5_ROD_LENGTH >= required_rod:
        report(
            "PASS",
            "M5 rod length",
            f"{cfg.RECOMMENDED_M5_ROD_LENGTH:.1f} mm >= required {required_rod:.1f} mm.",
        )
    else:
        report(
            "FAIL",
            "M5 rod length",
            f"{cfg.RECOMMENDED_M5_ROD_LENGTH:.1f} mm < required {required_rod:.1f} mm.",
        )


def validate_rod_pattern() -> None:
    expected = {(-80.0, -80.0), (80.0, -80.0), (-80.0, 80.0), (80.0, 80.0)}
    actual = set(cfg.m5_rod_centers())
    symmetric = all((-x, y) in actual and (x, -y) in actual for x, y in actual)

    if actual == expected and close(cfg.M5_ROD_CLEARANCE_DIAMETER, 5.6) and symmetric:
        report(
            "PASS",
            "M5 rod pattern",
            "Rod centers are (+/-80, +/-80), clearance diameter is 5.6 mm, pattern is symmetric.",
        )
    else:
        report(
            "FAIL",
            "M5 rod pattern",
            f"Expected {sorted(expected)}, got {sorted(actual)}, clearance {cfg.M5_ROD_CLEARANCE_DIAMETER:.1f} mm.",
        )


def validate_boundary_clearances() -> None:
    rod_radius = cfg.M5_ROD_CLEARANCE_DIAMETER / 2
    x_gap = cfg.OUTER_HALF_WIDTH - cfg.M5_ROD_CENTER_OFFSET_X - rod_radius
    y_gap = cfg.OUTER_HALF_DEPTH - cfg.M5_ROD_CENTER_OFFSET_Y - rod_radius

    if x_gap >= 10.0 and y_gap >= 10.0:
        report(
            "PASS",
            "Rod vs outer boundary",
            f"X/Y gaps are {x_gap:.1f}/{y_gap:.1f} mm; expected 95 - 80 - 2.8 = 12.2 mm.",
        )
    else:
        report("FAIL", "Rod vs outer boundary", f"X/Y gaps are {x_gap:.1f}/{y_gap:.1f} mm.")

    washer_radius = cfg.M5_WASHER_SEAT_DIAMETER / 2
    washer_x_gap = cfg.OUTER_HALF_WIDTH - cfg.M5_ROD_CENTER_OFFSET_X - washer_radius
    washer_y_gap = cfg.OUTER_HALF_DEPTH - cfg.M5_ROD_CENTER_OFFSET_Y - washer_radius
    report(
        "PARTIAL",
        "Washer seat vs outer boundary",
        f"X/Y gaps are {washer_x_gap:.1f}/{washer_y_gap:.1f} mm; 8.5 mm is coupon-validation territory.",
    )

    fan_half = cfg.FAN_ALIGNED_AIRFLOW_ZONE_WIDTH / 2
    rod_fan_gap = cfg.M5_ROD_CENTER_OFFSET_X - fan_half - rod_radius
    if rod_fan_gap >= 10.0:
        report(
            "PASS",
            "Rod vs fan-aligned zone",
            f"Gap is {rod_fan_gap:.1f} mm; expected 80 - 60 - 2.8 = 17.2 mm.",
        )
    else:
        report("FAIL", "Rod vs fan-aligned zone", f"Gap is only {rod_fan_gap:.1f} mm.")


def validate_fan_assumptions() -> None:
    if cfg.FAN_AIRFLOW_CUTOUT_DIAMETER_MAX <= 110.0 and cfg.FAN_ENVELOPE_SIZE == 120.0:
        report(
            "PARTIAL",
            "Fan screw bosses vs cutout",
            "Fan envelope is not a full square cutout; +/-52.5 mm screw centers need boss material and CAD/slicer review.",
        )
    else:
        report(
            "FAIL",
            "Fan screw bosses vs cutout",
            "Full 120 x 120 square void would fail fan mounting-hole implementation.",
        )


def validate_rear_service_zone() -> None:
    rear_rod_y = cfg.M5_ROD_CENTER_OFFSET_Y
    if cfg.REAR_SERVICE_ZONE_Y_MIN <= rear_rod_y <= cfg.REAR_SERVICE_ZONE_Y_MAX:
        report(
            "PARTIAL",
            "Rear service zone vs rear rods",
            "Rear rods at Y=+80 are intentionally inside the +65..+95 rear service zone; CAD routing review required.",
        )
    else:
        report("FAIL", "Rear service zone vs rear rods", f"Rear rod Y={rear_rod_y:.1f} is outside service zone.")

    keepout_inner_edge = cfg.REAR_ROD_KEEPOUT_CENTER_X_ABS - cfg.REAR_ROD_KEEPOUT_RADIUS
    if cfg.PRIMARY_REAR_CABLE_CORRIDOR_X_MAX < keepout_inner_edge:
        report(
            "PASS",
            "Primary rear cable corridor geometry",
            f"Corridor max X {cfg.PRIMARY_REAR_CABLE_CORRIDOR_X_MAX:.1f} mm < keepout inner edge {keepout_inner_edge:.1f} mm.",
        )
        report(
            "PARTIAL",
            "Primary rear cable bundle thickness",
            "Real cable bundle thickness, connector strain relief, and tie routing still need physical/CAD review.",
        )
    else:
        report("FAIL", "Primary rear cable corridor", "Cable corridor overlaps rear rod keepout.")


def validate_device_envelopes() -> None:
    rpi_bounds = cfg.rect_bounds(
        cfg.RPI3B_CENTER_X,
        cfg.RPI3B_CENTER_Y,
        cfg.RPI3B_CLEARANCE_WIDTH,
        cfg.RPI3B_CLEARANCE_DEPTH,
    )
    rpi_gap, rpi_rod = min_gap_from_rods_to_rect(rpi_bounds)
    if rpi_gap > 0.0:
        report(
            "PASS",
            "Raspberry Pi envelope vs rods",
            f"Nearest rod {rpi_rod} leaves {rpi_gap:.1f} mm to the clearance rectangle.",
        )
    else:
        report("FAIL", "Raspberry Pi envelope vs rods", f"Rod/clearance overlap is {-rpi_gap:.1f} mm.")

    ssd_bounds = cfg.rect_bounds(
        cfg.EXTERNAL_SSD_PREFERRED_CENTER_X,
        cfg.EXTERNAL_SSD_PREFERRED_CENTER_Y,
        cfg.EXTERNAL_SSD_WIDTH,
        cfg.EXTERNAL_SSD_DEPTH,
    )
    _, ssd_x_max, _, _ = ssd_bounds
    ssd_lateral_gap = cfg.M5_ROD_CENTER_OFFSET_X - ssd_x_max - cfg.M5_ROD_CLEARANCE_DIAMETER / 2
    if ssd_lateral_gap > 0.0:
        report(
            "PARTIAL",
            "SSD preferred envelope vs rods",
            f"Right rod X-edge gap is {ssd_lateral_gap:.1f} mm; strap/rib geometry is not defined yet.",
        )
    else:
        report("FAIL", "SSD preferred envelope vs rods", f"Rod/SSD lateral overlap is {-ssd_lateral_gap:.1f} mm.")

    minipc_bounds = cfg.rect_bounds(
        cfg.MINIPC_CENTER_X,
        cfg.MINIPC_CENTER_Y,
        cfg.MINIPC_CLEARANCE_WIDTH,
        cfg.MINIPC_CLEARANCE_DEPTH,
    )
    minipc_gap, minipc_rod = min_gap_from_rods_to_rect(minipc_bounds)
    if minipc_gap > 0.0:
        report(
            "PASS",
            "Mini PC envelope vs rods",
            f"Nearest rod {minipc_rod} leaves {minipc_gap:.1f} mm; CAD retainers still need local review.",
        )
    else:
        report("FAIL", "Mini PC envelope vs rods", f"Rod/Mini PC clearance overlap is {-minipc_gap:.1f} mm.")

    minipc_rear_edge = cfg.MINIPC_CENTER_Y + cfg.MINIPC_DEPTH / 2
    rear_clearance = cfg.REAR_SERVICE_ZONE_Y_MIN - minipc_rear_edge
    if rear_clearance >= cfg.MINIPC_REAR_CABLE_CLEARANCE:
        report(
            "PASS",
            "Mini PC rear cable clearance",
            f"Rear edge Y={minipc_rear_edge:.1f}; service zone starts at {cfg.REAR_SERVICE_ZONE_Y_MIN:.1f}; clearance {rear_clearance:.1f} mm.",
        )
    else:
        report("FAIL", "Mini PC rear cable clearance", f"Only {rear_clearance:.1f} mm available.")


def validate_feet() -> None:
    inner_edge = cfg.TPU_FOOT_CENTER_OFFSET_PREFERRED - cfg.TPU_FOOT_SIZE_X / 2
    fan_half = cfg.FAN_ALIGNED_AIRFLOW_ZONE_WIDTH / 2
    clearance = inner_edge - fan_half

    if clearance >= cfg.TPU_FOOT_INTAKE_CLEARANCE_PREFERRED:
        report(
            "PASS",
            "Foot pad vs fan/intake zone",
            f"Preferred foot inner edge is {inner_edge:.1f} mm; fan zone half is {fan_half:.1f}; clearance {clearance:.1f} mm.",
        )
    elif clearance >= cfg.TPU_FOOT_INTAKE_CLEARANCE_MIN:
        report(
            "PARTIAL",
            "Foot pad vs fan/intake zone",
            f"Clearance {clearance:.1f} mm meets minimum but not preferred value.",
        )
    else:
        report("FAIL", "Foot pad vs fan/intake zone", f"Clearance {clearance:.1f} mm is below minimum.")


def main() -> int:
    validate_revision()
    validate_stack_height()
    validate_rod_pattern()
    validate_boundary_clearances()
    validate_fan_assumptions()
    validate_rear_service_zone()
    validate_device_envelopes()
    validate_feet()

    print("mk0.12 MVP-2M stack-through-rod validation")
    print("=" * 52)
    for result in RESULTS:
        print(f"[{result.status}] {result.title}: {result.detail}")

    failures = [result for result in RESULTS if result.status == "FAIL"]
    partials = [result for result in RESULTS if result.status == "PARTIAL"]

    print("=" * 52)
    print(f"Summary: {len(failures)} FAIL, {len(partials)} PARTIAL, {len(RESULTS) - len(failures) - len(partials)} PASS")

    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
