# mk0.11 Engineering Decisions

## D-001: No more SVG-only planning iteration

**Decision:** SVG architecture drawings will not be iterated further for planning purposes.

**Reason:** The mk0.10 SVG iteration did not unlock any design decision that
could not be read directly from `cad/config.py`. The drawings were technically
correct but not useful for deciding carriage geometry, module wall thickness,
or airflow window sizing. Physical prototyping produces faster and more
reliable validation.

**Consequence:** `drawings/mk0.10/` is frozen as-is. No new SVG sheets will
be generated until a specific, justified need is identified.

---

## D-002: First real CAD target is the generic module

**Decision:** The first new CAD part in mk0.11 is a device-agnostic generic
module shell, not a device-specific module (UPS, router, etc.).

**Reason:** A generic module establishes the module/carriage/rail interface in
a clean, unconstrained form. Once the interface is validated, device-specific
features can be added as incremental modifications to the generic shell without
reworking the interface geometry.

**Consequence:** `cad/parts/generic_module.py` is created. No device-specific
pads, standoffs, or retainers are included in this file.

---

## D-003: Carriage is a separate file from the module shell

**Decision:** `cad/parts/module_carriage.py` is separate from
`cad/parts/generic_module.py`.

**Reason:** Consistent with project rule forbidding mixing of different parts
in one function. The carriage and the module shell are geometrically and
functionally distinct: the carriage is the sliding element with POM-C shoe
mounts; the shell is the structural outer frame.

**Consequence:** The generic module assembly (`generic_module_assembly.py`)
combines shell + carriage. Each part is exported independently.

---

## D-004: Generic module carriage wraps the existing open-frame carriage standard

**Decision:** `make_generic_module_carriage()` calls
`carriages.make_lightweight_open_frame_carriage()` with 2 shoes per side.
No new carriage geometry is introduced.

**Reason:** The mk0.9.3 open-frame carriage with POM-C shoes is the validated
carriage standard. The generic module uses the same standard without any
carriage modification, which validates the carriage interface independently
of device-specific features.

**Consequence:** `GENERIC_MODULE_SHOES_PER_SIDE = RUNNER_SHOES_PER_SIDE_RPI_SSD = 2`.
If the generic module needs 3 shoes per side in future, this constant is changed
in `config.py` only.

---

## D-005: Rail standard unchanged

**Decision:** The mk0.9.3 U-channel rail standard is frozen for mk0.11.

**Specific values frozen:**
- Rail profile: aluminum U-channel 15×10×10×2 mm
- Runner: POM-C Ø8×12 mm (purchased, non-printed)
- Clamp: M3 screw into PETG boss / heat-set insert
- Primary thread: never directly in POM-C

**Reason:** The rail standard was engineered and reviewed in mk0.9.3. Changing
it now would invalidate the existing carriage geometry. mk0.11 validates the
standard by implementing a clean first prototype, not by redesigning it.

---

## D-006: No full tower redesign until single module bay is validated

**Decision:** The tower assembly (`cad/assembly/tower_assembly.py`) will not
be modified in mk0.11.

**Reason:** Full tower integration should happen only after the generic module
bay is physically validated. Making changes to the full assembly now would
introduce untested geometry into the stable mk0.9.3 baseline.

**Consequence:** `tower_assembly.py` is unchanged. The new assemblies
(`generic_module_assembly.py`, `single_module_bay_assembly.py`) are
standalone and do not modify the tower assembly.

---

## D-007: Generic module height = RPI_SSD_MODULE_HEIGHT (70 mm)

**Decision:** `GENERIC_MODULE_HEIGHT = RPI_SSD_MODULE_HEIGHT = 70 mm`.

**Reason:** The RPi/SSD module slot is a known, validated slot height in the
tower stack. Using the same height for the generic module prototype means
the first print can be checked for fit in the existing stack without
requiring a new base/roof configuration. This is the most conservative
choice for the first prototype.

**Consequence:** If a different slot height is needed later, a new constant
is added in `config.py` and the module height is changed there. No magic
numbers in the part function.

---

## D-008: pom_shoe.py and rail_profile.py as standalone reference files

**Decision:** POM-C shoe and U-channel rail are given their own source files
(`cad/parts/pom_shoe.py`, `cad/parts/rail_profile.py`) separate from the
general `placeholders.py`.

**Reason:** `placeholders.py` already exists and contains correct geometry,
but it mixes many different placeholder types. Having dedicated files for
the key wear parts (POM-C shoe) and structural parts (U-channel rail) makes
the mk0.11 subsystem self-documenting and allows the fit test jig to import
them clearly without pulling in the full placeholder module.

**Consequence:** The placeholders.py versions remain as aliases / backward-
compatible references. No duplication of geometry — `rail_profile.py` wraps
the existing `make_aluminum_u_channel_rail_placeholder()`.
