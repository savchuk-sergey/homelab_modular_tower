# mk0.12 - Revision Map

Revision: mk0.12  
Architecture: MVP-2M stack-through-rod  
Status: Revision-scoped document set active for CAD skeleton v3 input  

Related documents:
- README.md
- ENGINEERING_SPEC.md
- PARTS_SPEC.md
- INTERFACES.md
- VALIDATION_GATES.md
- PHYSICAL_TEST_PLAN.md
- AGENT_RULES.md
- KNOWN_ISSUES.md

## Status

```text
SPECIFICATION: PASS FOR CAD SKELETON V3 INPUT
CAD IMPLEMENTATION: NOT STARTED
COUPON PARTS: BLOCKED
FULL PRINT: BLOCKED
NEXT STEP: mk0.12 CAD skeleton cleanup v3
```

## Architecture

mk0.12 is an MVP-2M stack-through-rod architecture for a compact Homelab Modular Tower. The active stack is:

1. `base_pedestal`
2. `rpi_ssd_stack_module`
3. `minipc_stack_module`
4. `top_cap`

The tower uses a frozen 190 x 190 mm footprint, four M5 rods at X/Y +/-80, and a 238 mm stack height. It is not a hot-swappable blade chassis. Primary device installation and cable routing must happen before final stack compression.

Coupon parts and full print are blocked until the CAD skeleton v3 validation gates pass. Physical coupons follow CAD validation; full print follows coupon and physical validation.

## Read Order

1. ENGINEERING_SPEC.md
2. PARTS_SPEC.md
3. INTERFACES.md
4. VALIDATION_GATES.md
5. AGENT_RULES.md
6. PHYSICAL_TEST_PLAN.md
7. KNOWN_ISSUES.md

## Legacy Snapshot

`MVP_ENGINEERING_SPEC.md` remains as the consolidated legacy snapshot. These revision-scoped documents split that content by purpose without changing engineering decisions. If a requirement appears ambiguous, preserve the stricter interpretation and verify against `MVP_ENGINEERING_SPEC.md`.

The revision-scoped documents are the active source of truth for new mk0.12 CAD work.
`MVP_ENGINEERING_SPEC.md` is fallback/context only.
If the legacy snapshot conflicts with the revision-scoped documents, the revision-scoped documents win.
If ambiguity remains, preserve the stricter interpretation and validate against `VALIDATION_GATES.md`.
