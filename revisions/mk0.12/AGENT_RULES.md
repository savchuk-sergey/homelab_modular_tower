# mk0.12 - Agent Rules

Revision: mk0.12  
Architecture: MVP-2M stack-through-rod  
Status: ACTIVE AGENT INSTRUCTIONS FOR CAD SKELETON V3 WORK  

Related documents:
- README.md
- ENGINEERING_SPEC.md
- PARTS_SPEC.md
- INTERFACES.md
- VALIDATION_GATES.md
- PHYSICAL_TEST_PLAN.md
- AGENT_RULES.md
- KNOWN_ISSUES.md

## Recommended Agent Workflow

1. Read README.md.
2. Read ENGINEERING_SPEC.md.
3. Read PARTS_SPEC.md and INTERFACES.md.
4. Read VALIDATION_GATES.md before changing CAD.
5. Read AGENT_RULES.md before implementing.
6. After CAD changes, produce validation report against VALIDATION_GATES.md.
7. Do not continue to coupon parts unless all required gates pass.

## Source of Truth

- CadQuery is the CAD source of truth.
- All dimensions must live in `cad/config.py`.
- No magic numbers inside part functions.
- Each part must have a separate builder function.
- Assembly must be separate from part definitions.
- STEP/STL/PNG are derived artifacts.
- Do not treat generated exports or renders as source of truth.

## Builder Separation

- Printable builders return printable plastic only.
- Reference builders return review/assembly geometry only.
- Do not include device placeholders in printable STL.
- Do not include rods, washers, nuts, or fan placeholders in printable STL.
- Fan screw holes/bosses are printable geometry only if fan mounting is active in that part.
- TPU feet are separate TPU printable parts, not part of PETG `base_pedestal`.

## Geometry Rules

- Do not move M5 rods unless the task explicitly says so.
- Do not exceed the 190 x 190 active PETG stack footprint.
- Do not treat the fan-compatible 120 x 120 zone as a full square cutout.
- Do not treat distributed airflow as a required empty center shaft.
- Do not create decorative ribs.
- Do not create outward star ribs from M5 compression islands.
- Do not create dangling/floating ribs.
- Every rib must have valid endpoints.
- Do not block required airflow, rear service, cable, mounting, retainer, or tool access windows.
- Declare print orientation for each printable part.

## Validation Discipline

- Mark uncertain items as NOT VERIFIED instead of silently assuming.
- Preserve PASS/PARTIAL/FAIL/NOT VERIFIED status semantics.
- Produce evidence for validation gates after CAD changes.
- Do not proceed to coupon parts unless CAD skeleton v3 gates pass.
- Do not proceed to full print unless CAD validation and physical validation pass.

## Revision History Discipline

- Do not alter old revision history to pretend previous states were different.
- Use `KNOWN_ISSUES.md` for historical failures and risks.
- Keep `MVP_ENGINEERING_SPEC.md` as the consolidated legacy snapshot unless a task explicitly asks to replace it.
