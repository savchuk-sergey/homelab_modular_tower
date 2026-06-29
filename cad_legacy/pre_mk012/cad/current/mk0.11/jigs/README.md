# cad/current/mk0.11/jigs — Active mk0.11 Test Jig Files

This directory is the intended home for **new** mk0.11 fit test and validation
jigs beyond the initial rail/carriage fit test.

## What belongs here

- Additional print-fit jigs (e.g., a shoe retention force test jig).
- Module/carriage interface dimensional verification jigs.
- Any jig created for mk0.11 validation that is not the initial rail/carriage fit test.

## What does NOT belong here

- `cad/jigs/rail_carriage_fit_test.py` — that already exists at the flat level
  and is the primary mk0.11 fit test jig.

## Current active mk0.11 jig (in cad/jigs/)

| File | Role |
|---|---|
| `cad/jigs/rail_carriage_fit_test.py` | Rail / carriage / POM-C shoe fit test jig |

Corresponding export: `exports/mk0.11/jigs/rail_carriage_fit_test.step`

## Planned next jigs (not yet created)

| Jig | Purpose | Prerequisite |
|---|---|---|
| `rail_shoe_test_jig.py` | POM-C shoe retention force and fit test | After rail_carriage_fit_test passes |
| `module_bay_interface_jig.py` | Module-to-frame interface dimensional check | After single module bay passes |

Create these jigs only when the prerequisite validation steps pass.
See `revisions/mk0.11/VALIDATION_PLAN.md` for the full step-by-step plan.

## AGENTS.md rules that apply here

- All dimensions must be in `cad/config.py` — no magic numbers.
- Jigs must not modify the parts they test — they are measurement references only.
- Export each jig to `exports/mk0.11/jigs/`.
