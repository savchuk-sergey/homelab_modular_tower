"""mk0.12 MVP-2M stack-through-rod assembly skeleton."""

from __future__ import annotations

import cadquery as cq

from cad import config as cfg
from cad.parts.base_pedestal import build_base_pedestal
from cad.parts.module_minipc import build_minipc_stack_module
from cad.parts.module_rpi_ssd import build_rpi_ssd_stack_module
from cad.parts.reference_geometry import (
    build_external_ssd_placeholder,
    build_m5_rods_placeholder,
    build_minipc_placeholder,
    build_nuts_placeholder,
    build_rpi3b_placeholder,
    build_washers_placeholder,
)
from cad.parts.top_cap import build_top_cap


ASSEMBLY_SERVICE_ORDER = (
    "1. Install devices into modules before final stack compression.\n"
    "2. Route Pi/SSD/Mini PC cables to rear service windows before final compression.\n"
    "3. Stack modules on M5 rods.\n"
    "4. Verify no cable collision with rear rod keepouts.\n"
    "5. Hand-tight compression only."
)


def build_mvp_2_module_stack() -> cq.Assembly:
    """Build the mk0.12 MVP-2M stack assembly with non-printed M5 rod placeholders."""
    assembly = cq.Assembly(name=f"homelab_modular_tower_{cfg.CURRENT_REVISION}_mvp_2m")

    assembly.add(
        build_base_pedestal(),
        name="base_pedestal",
        loc=cq.Location(cq.Vector(cfg.BASE_PEDESTAL_Z_MIN, cfg.BASE_PEDESTAL_Z_MIN, cfg.BASE_PEDESTAL_Z_MIN)),
    )
    assembly.add(
        build_rpi_ssd_stack_module(),
        name="rpi_ssd_stack_module",
        loc=cq.Location(cq.Vector(cfg.BASE_PEDESTAL_Z_MIN, cfg.BASE_PEDESTAL_Z_MIN, cfg.RPI_SSD_MODULE_Z_MIN)),
    )
    assembly.add(
        build_minipc_stack_module(),
        name="minipc_stack_module",
        loc=cq.Location(cq.Vector(cfg.BASE_PEDESTAL_Z_MIN, cfg.BASE_PEDESTAL_Z_MIN, cfg.MINIPC_MODULE_Z_MIN)),
    )
    assembly.add(
        build_top_cap(),
        name="top_cap",
        loc=cq.Location(cq.Vector(cfg.BASE_PEDESTAL_Z_MIN, cfg.BASE_PEDESTAL_Z_MIN, cfg.TOP_CAP_Z_MIN)),
    )

    assembly.add(
        build_rpi3b_placeholder(),
        name="reference_rpi3b_placeholder",
        color=cq.Color(0.1, 0.45, 0.1, 0.45),
        loc=cq.Location(cq.Vector(0.0, 0.0, cfg.RPI_SSD_MODULE_Z_MIN)),
    )
    assembly.add(
        build_external_ssd_placeholder(),
        name="reference_external_ssd_placeholder",
        color=cq.Color(0.1, 0.1, 0.6, 0.45),
        loc=cq.Location(cq.Vector(0.0, 0.0, cfg.RPI_SSD_MODULE_Z_MIN)),
    )
    assembly.add(
        build_minipc_placeholder(),
        name="reference_minipc_placeholder",
        color=cq.Color(0.55, 0.15, 0.1, 0.45),
        loc=cq.Location(cq.Vector(0.0, 0.0, cfg.MINIPC_MODULE_Z_MIN)),
    )
    assembly.add(build_m5_rods_placeholder(), name="reference_m5_rods", color=cq.Color("gray"))
    assembly.add(build_washers_placeholder(), name="reference_washers", color=cq.Color(0.75, 0.75, 0.75, 1.0))
    assembly.add(build_nuts_placeholder(), name="reference_nuts", color=cq.Color(0.25, 0.25, 0.25, 1.0))

    return assembly
