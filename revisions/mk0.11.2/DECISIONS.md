# mk0.11.2 Engineering Decisions

## D-009: Stack-through-rod architecture for first prototype

**Decision:** mk0.11.2 uses stack-through-rod architecture.  Modules are
stackable layers compressed by four M5 threaded rods between `base_pedestal`
and `top_cap`.  Sliding carriage/rail system is deferred.  Each stack module
reserves future carriage/adapter mounting zones.

**Reason:** This keeps the first prototype simple, stiff, printable, and
testable while preserving an upgrade path toward slide-out serviceability.

**Trade-off:** Middle module removal requires loosening/disassembling the
stack in mk0.11.2.  Independent module extraction is deferred.

**Consequence:**

- Active CAD: `generic_stack_module`, `base_pedestal`, `top_cap`,
  `stack_test_assembly`.
- Deferred CAD: `generic_module` (rail-pocket era), carriage, rails, bay
  assemblies — see `cad/deferred/README.md`.

---

## D-010: generic_stack_module replaces generic_module as active target

**Decision:** New part file `cad/parts/generic_stack_module.py` is the active
module shell.  `cad/parts/generic_module.py` is preserved unchanged as the
deferred carriage-era shell with rail pockets.

**Reason:** Renaming in place would rewrite mk0.11 history and break deferred
rail validation geometry.  A separate file makes the architecture correction
explicit without retroactive edits.

---

## D-011: Future carriage zones are placeholders only

**Decision:** Stack modules include reinforced side pads, M3 insert bosses,
and bottom adapter pad placeholders at future rail lateral positions.  No
POM-C shoe sockets, no U-channel pockets, no sliding assembly geometry.

**Reason:** Preserves a future side-adapter upgrade path without implementing
or validating the deferred rail subsystem in mk0.11.2.

**Constraints:** Future zones must not interfere with M5 rods, central airflow,
or rear service zone.

---

## D-012: No full tower redesign in mk0.11.2

**Decision:** `tower_assembly.py` remains unchanged.  Validation is limited
to `stack_test_assembly`.

**Reason:** Same rationale as D-006 in mk0.11 — validate the subsystem before
integrating into the full tower stack.

---

## Inherited deferred decisions (unchanged)

The following mk0.11 decisions remain valid for the **deferred** rail path:

- D-004: Generic carriage wraps open-frame standard
- D-005: U-channel rail standard frozen
- D-008: Dedicated pom_shoe / rail_profile reference files

They do not apply to the active mk0.11.2 stack prototype.
