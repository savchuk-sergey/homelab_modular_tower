# Deferred / future CAD — mk0.11 sliding carriage / rail subsystem

This folder documents and re-exports CAD that belongs to the **deferred**
sliding carriage / rail architecture.  It is preserved for future upgrade
paths but is **not active** in mk0.11.2.

## Active architecture (mk0.11.2)

`base_pedestal` + `generic_stack_module` + `top_cap`, compressed by four M5
through-rods.  See `revisions/mk0.11.2/`.

## Deferred architecture (future)

Sliding open-frame carriage on aluminum U-channel rails with POM-C shoes.
Source files remain in their original locations under `cad/parts/` and
`cad/assembly/` for backward compatibility and future rail/carriage work.

### Deferred parts

| Part | Source |
|---|---|
| `generic_module` (carriage-era shell with rail pockets) | `cad/parts/generic_module.py` |
| `generic_module_carriage` | `cad/parts/module_carriage.py` |
| `u_channel_rail_generic_module` | `cad/parts/rail_profile.py` |
| `pom_c_shoe_reference` | `cad/parts/pom_shoe.py` |

### Deferred assemblies

| Assembly | Source |
|---|---|
| `generic_module_assembly` | `cad/assembly/generic_module_assembly.py` |
| `single_module_bay_assembly` | `cad/assembly/single_module_bay_assembly.py` |

### Deferred jigs

| Jig | Source |
|---|---|
| `rail_carriage_fit_test` | `cad/jigs/rail_carriage_fit_test.py` |

## Rules

- Do not delete deferred code.
- Do not change the frozen U-channel rail standard when reactivating this path.
- Stack modules reserve future adapter zones in `generic_stack_module.py` so
  deferred carriage hardware can attach later without a full module redesign.
