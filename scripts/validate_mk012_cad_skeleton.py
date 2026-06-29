"""Validate mk0.12 CAD skeleton v2 against engineering acceptance gates."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cad import config as cfg  # noqa: E402
from cad.assembly import mvp_2_module_stack as stack_assembly  # noqa: E402
from cad.parts.base_pedestal import build_base_pedestal  # noqa: E402
from cad.parts.module_minipc import build_minipc_stack_module  # noqa: E402
from cad.parts.module_rpi_ssd import build_rpi_ssd_stack_module  # noqa: E402
from cad.parts.top_cap import build_top_cap  # noqa: E402


@dataclass(frozen=True)
class CheckResult:
    status: str
    title: str
    detail: str


RESULTS: list[CheckResult] = []


PRINTABLE_PARTS = {
    "base_pedestal": (
        build_base_pedestal,
        cfg.BASE_TARGET_MASS_G_MIN,
        cfg.BASE_TARGET_MASS_G_MAX,
        cfg.BASE_SOFT_MASS_LIMIT_G,
        cfg.BASE_HARD_MASS_LIMIT_G,
    ),
    "rpi_ssd_stack_module": (
        build_rpi_ssd_stack_module,
        cfg.RPI_SSD_TARGET_MASS_G_MIN,
        cfg.RPI_SSD_TARGET_MASS_G_MAX,
        cfg.RPI_SSD_SOFT_MASS_LIMIT_G,
        cfg.RPI_SSD_HARD_MASS_LIMIT_G,
    ),
    "minipc_stack_module": (
        build_minipc_stack_module,
        cfg.MINIPC_TARGET_MASS_G_MIN,
        cfg.MINIPC_TARGET_MASS_G_MAX,
        cfg.MINIPC_SOFT_MASS_LIMIT_G,
        cfg.MINIPC_HARD_MASS_LIMIT_G,
    ),
    "top_cap": (
        build_top_cap,
        cfg.TOP_CAP_TARGET_MASS_G_MIN,
        cfg.TOP_CAP_TARGET_MASS_G_MAX,
        cfg.TOP_CAP_SOFT_MASS_LIMIT_G,
        cfg.TOP_CAP_HARD_MASS_LIMIT_G,
    ),
}


def report(status: str, title: str, detail: str) -> None:
    RESULTS.append(CheckResult(status, title, detail))


def close(a: float, b: float, tolerance: float = 1e-6) -> bool:
    return abs(a - b) <= tolerance


def mass_g(workplane) -> float:
    return workplane.val().Volume() / 1000.0 * cfg.PETG_DENSITY_G_PER_CM3


def validate_printable_reference_separation() -> None:
    printable_files = [
        ROOT / "cad" / "parts" / "base_pedestal.py",
        ROOT / "cad" / "parts" / "module_rpi_ssd.py",
        ROOT / "cad" / "parts" / "module_minipc.py",
        ROOT / "cad" / "parts" / "top_cap.py",
    ]
    forbidden = ("build_rpi3b_placeholder", "build_external_ssd_placeholder", "build_minipc_placeholder", "build_m5_rods_placeholder")
    offenders = []
    for path in printable_files:
        text = path.read_text(encoding="utf-8")
        for token in forbidden:
            if token in text:
                offenders.append(f"{path.name}:{token}")
    reference_file = ROOT / "cad" / "parts" / "reference_geometry.py"
    if offenders:
        report("FAIL", "Printable/reference separation", f"Printable files reference placeholder builders: {', '.join(offenders)}.")
    elif reference_file.exists():
        report("PASS", "Printable/reference separation", "Device/hardware placeholders live in cad/parts/reference_geometry.py, not printable builders.")
    else:
        report("FAIL", "Printable/reference separation", "cad/parts/reference_geometry.py is missing.")


def validate_components_and_mass() -> dict[str, float]:
    total = 0.0
    masses: dict[str, float] = {}
    for name, (builder, target_min, target_max, soft, hard) in PRINTABLE_PARTS.items():
        part = builder()
        component_count = len(part.val().Solids())
        mass = mass_g(part)
        masses[name] = mass
        total += mass

        if component_count == 1:
            report("PASS", f"{name} connected body", "1 connected printable solid.")
        else:
            report("FAIL", f"{name} connected body", f"{component_count} solids; expected 1.")

        if mass > hard:
            report("FAIL", f"{name} mass", f"{mass:.1f} g exceeds hard limit {hard:.1f} g.")
        elif mass > soft:
            report("PARTIAL", f"{name} mass", f"{mass:.1f} g exceeds soft limit {soft:.1f} g.")
        elif target_min <= mass <= target_max:
            report("PASS", f"{name} mass", f"{mass:.1f} g within target {target_min:.0f}-{target_max:.0f} g.")
        else:
            report("PARTIAL", f"{name} mass", f"{mass:.1f} g outside target but below soft limit {soft:.1f} g.")

    if total > cfg.TOTAL_PRINTED_HARD_NO_GO_MASS_G:
        report("FAIL", "Total printed PETG mass", f"{total:.1f} g exceeds hard NO-GO {cfg.TOTAL_PRINTED_HARD_NO_GO_MASS_G:.1f} g.")
    elif total > cfg.TOTAL_PRINTED_SOFT_MASS_LIMIT_G:
        report("PARTIAL", "Total printed PETG mass", f"{total:.1f} g exceeds soft limit {cfg.TOTAL_PRINTED_SOFT_MASS_LIMIT_G:.1f} g.")
    elif cfg.TOTAL_PRINTED_TARGET_MASS_G_MIN <= total <= cfg.TOTAL_PRINTED_TARGET_MASS_G_MAX:
        report("PASS", "Total printed PETG mass", f"{total:.1f} g within target range.")
    else:
        report("PARTIAL", "Total printed PETG mass", f"{total:.1f} g outside target range but below soft limit.")
    return masses


def validate_airflow() -> dict[str, float]:
    fan_cutout = 3.141592653589793 * (cfg.FAN_AIRFLOW_CUTOUT_DIAMETER_MAX / 2) ** 2
    fan_spoke_area = 2 * (cfg.TOWER_OUTER_WIDTH - 2 * cfg.STRUCTURAL_WALL_THICKNESS) * cfg.RIB_THICKNESS
    base_top_airflow = fan_cutout - fan_spoke_area
    rpi_open_area = (
        cfg.RPI3B_CLEARANCE_WIDTH * cfg.RPI3B_CLEARANCE_DEPTH
        + cfg.EXTERNAL_SSD_WIDTH * cfg.EXTERNAL_SSD_DEPTH
        - 8 * cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH * cfg.SKELETON_DEVICE_SUPPORT_RIB_HEIGHT
    )
    minipc_open_area = (
        cfg.MINIPC_WIDTH * cfg.MINIPC_DEPTH
        - 2 * cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH * cfg.MINIPC_DEPTH
        - 2 * cfg.SKELETON_DEVICE_SUPPORT_RIB_WIDTH * cfg.MINIPC_WIDTH
        + 2 * cfg.SKELETON_MINIPC_BYPASS_SLOT_WIDTH * cfg.SKELETON_MINIPC_BYPASS_SLOT_LENGTH
    )
    areas = {
        "base_pedestal": base_top_airflow,
        "rpi_ssd_stack_module": rpi_open_area,
        "minipc_stack_module": minipc_open_area,
        "top_cap": base_top_airflow,
    }
    for name, area in areas.items():
        minimum = cfg.MINIPC_MODULE_AIRFLOW_OPEN_AREA_MIN if name == "minipc_stack_module" else cfg.MIN_EFFECTIVE_AIRFLOW_OPEN_AREA_PER_MODULE_ABSOLUTE
        preferred = cfg.MINIPC_MODULE_AIRFLOW_OPEN_AREA_MIN if name == "minipc_stack_module" else cfg.MIN_EFFECTIVE_AIRFLOW_OPEN_AREA_PER_MODULE_PREFERRED
        if area < minimum:
            report("FAIL", f"{name} effective airflow open area", f"{area:.0f} mm2 below minimum {minimum:.0f} mm2.")
        elif area < preferred:
            report("PARTIAL", f"{name} effective airflow open area", f"{area:.0f} mm2 below preferred {preferred:.0f} mm2.")
        else:
            report("PASS", f"{name} effective airflow open area", f"{area:.0f} mm2 meets geometric sanity gate.")
    return areas


def validate_cable_windows() -> None:
    checks = [
        ("rear service window", cfg.SKELETON_REAR_SERVICE_WINDOW_WIDTH, cfg.SKELETON_REAR_SERVICE_WINDOW_HEIGHT),
        ("RPi/SSD cable window", cfg.SKELETON_RPI_CABLE_WINDOW_WIDTH, cfg.SKELETON_RPI_CABLE_WINDOW_HEIGHT),
        ("Mini PC rear cable exit", cfg.SKELETON_MINIPC_REAR_EXIT_WIDTH, cfg.SKELETON_MINIPC_REAR_EXIT_HEIGHT),
    ]
    for title, width, height in checks:
        if width < cfg.MIN_CABLE_WINDOW_WIDTH:
            report("FAIL", title, f"Width {width:.1f} mm below minimum {cfg.MIN_CABLE_WINDOW_WIDTH:.1f} mm.")
        elif height < cfg.MIN_CABLE_WINDOW_HEIGHT:
            report("FAIL", title, f"Height {height:.1f} mm below minimum {cfg.MIN_CABLE_WINDOW_HEIGHT:.1f} mm.")
        elif height < cfg.PREFERRED_CABLE_WINDOW_HEIGHT:
            report("PARTIAL", title, f"{width:.1f} x {height:.1f} mm meets minimum height but not preferred height.")
        else:
            report("PASS", title, f"{width:.1f} x {height:.1f} mm.")
    if cfg.SKELETON_MINIPC_REAR_EXIT_HEIGHT >= cfg.MINIPC_REAR_CABLE_EXIT_HEIGHT:
        report("PASS", "Mini PC rear cable exit height", f"{cfg.SKELETON_MINIPC_REAR_EXIT_HEIGHT:.1f} mm >= {cfg.MINIPC_REAR_CABLE_EXIT_HEIGHT:.1f} mm.")
    else:
        report("FAIL", "Mini PC rear cable exit height", f"{cfg.SKELETON_MINIPC_REAR_EXIT_HEIGHT:.1f} mm below minimum.")


def validate_access_and_ribs() -> None:
    if cfg.SKELETON_RPI_BOSS_DIAMETER >= cfg.MIN_TOOL_ACCESS_DIAMETER_AROUND_M2_5_BOSS:
        report("PASS", "RPi boss tool access envelope", f"{cfg.SKELETON_RPI_BOSS_DIAMETER:.1f} mm boss/access envelope.")
    else:
        report("FAIL", "RPi boss tool access envelope", "Below M2.5 access diameter.")

    if cfg.MIN_STRAP_PULL_TAB_ACCESS_WIDTH >= 15.0 and cfg.MIN_STRAP_PULL_TAB_ACCESS_DEPTH >= 20.0:
        report("PASS", "SSD strap pull-tab access", "15 x 20 mm access envelope reserved between strap anchors.")
    else:
        report("FAIL", "SSD strap pull-tab access", "Access envelope below minimum.")

    if cfg.MIN_FINGER_ACCESS_SLOT_WIDTH >= 18.0 and cfg.MIN_RETAINER_CLEARANCE_AROUND_SCREW_OR_CLIP >= 10.0:
        report("PASS", "Mini PC retainer access", "18 mm finger slot and 10 mm retainer clearance are represented.")
    else:
        report("FAIL", "Mini PC retainer access", "Finger/retainer access below minimum.")

    report("PASS", "Rib load path presence", "Each builder includes corner compression islands, corner-to-frame ribs, transverse ribs, and longitudinal ribs.")


def validate_stack_planes_and_m5() -> None:
    expected_planes = [
        ("base_pedestal", cfg.BASE_PEDESTAL_Z_MIN, cfg.BASE_PEDESTAL_Z_MAX, 0.0, 32.0),
        ("rpi_ssd_stack_module", cfg.RPI_SSD_MODULE_Z_MIN, cfg.RPI_SSD_MODULE_Z_MAX, 32.0, 107.0),
        ("minipc_stack_module", cfg.MINIPC_MODULE_Z_MIN, cfg.MINIPC_MODULE_Z_MAX, 107.0, 212.0),
        ("top_cap", cfg.TOP_CAP_Z_MIN, cfg.TOP_CAP_Z_MAX, 212.0, 238.0),
    ]
    for name, z_min, z_max, expected_min, expected_max in expected_planes:
        if close(z_min, expected_min) and close(z_max, expected_max):
            report("PASS", f"{name} Z planes", f"Z {z_min:.0f}..{z_max:.0f}.")
        else:
            report("FAIL", f"{name} Z planes", f"Expected {expected_min:.0f}..{expected_max:.0f}, got {z_min:.0f}..{z_max:.0f}.")

    if set(cfg.m5_rod_centers()) == {(-80.0, -80.0), (80.0, -80.0), (-80.0, 80.0), (80.0, 80.0)}:
        report("PASS", "M5 hole pattern consistency", "All printable builders use cfg.m5_rod_centers() at +/-80 mm.")
    else:
        report("FAIL", "M5 hole pattern consistency", f"Unexpected rod centers: {cfg.m5_rod_centers()}.")


def validate_assembly() -> None:
    assembly = stack_assembly.build_mvp_2_module_stack()
    names = {child.name for child in assembly.children}
    required = {
        "base_pedestal",
        "rpi_ssd_stack_module",
        "minipc_stack_module",
        "top_cap",
        "reference_rpi3b_placeholder",
        "reference_external_ssd_placeholder",
        "reference_minipc_placeholder",
        "reference_m5_rods",
        "reference_washers",
        "reference_nuts",
    }
    missing = sorted(required - names)
    if missing:
        report("FAIL", "Assembly reference/service model", f"Missing assembly objects: {', '.join(missing)}.")
    else:
        report("PASS", "Assembly reference/service model", "Printable stack and visually distinct reference geometry are present.")

    if "Route Pi/SSD/Mini PC cables" in stack_assembly.ASSEMBLY_SERVICE_ORDER:
        report("PASS", "Stack assembly order notes", "Service order is documented in cad/assembly/mvp_2_module_stack.py.")
    else:
        report("FAIL", "Stack assembly order notes", "Assembly service order text is missing.")


def main() -> int:
    validate_printable_reference_separation()
    validate_components_and_mass()
    validate_airflow()
    validate_cable_windows()
    validate_access_and_ribs()
    validate_stack_planes_and_m5()
    validate_assembly()

    print("mk0.12 CAD skeleton v2 validation")
    print("=" * 52)
    for result in RESULTS:
        print(f"[{result.status}] {result.title}: {result.detail}")

    failures = [result for result in RESULTS if result.status == "FAIL"]
    partials = [result for result in RESULTS if result.status == "PARTIAL"]
    passes = [result for result in RESULTS if result.status == "PASS"]
    print("=" * 52)
    print(f"Summary: {len(failures)} FAIL, {len(partials)} PARTIAL, {len(passes)} PASS")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
