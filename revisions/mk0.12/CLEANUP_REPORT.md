# mk0.12 Repository Cleanup Report

## Scope

Documentation-only repository cleanup for `mk0.12 MVP-2M stack-through-rod`.

This cleanup audited root workflow documents, active `revisions/mk0.12/` documents, legacy workflow references, historical review areas, drawings, exports, and renders. It did not change CadQuery geometry, generated artifacts, coupon parts, STEP/STL files, PNG files, or render outputs.

## Summary

- Root `README.md` was outdated relative to `mk0.12` and still presented `mk0.11` as the current active workflow.
- Root `AGENTS.md` was outdated relative to the `mk0.12` specification-first workflow and still presented `mk0.1` as the current stable revision in a way that could mislead future agents.
- The required `mk0.12` active document set exists.
- `mk0.12` remains a documentation/specification state suitable for CAD skeleton v3 input, not an active CAD implementation state.
- CAD implementation status remains `NOT STARTED`.
- Coupon parts remain `BLOCKED`.
- Full print remains `BLOCKED`.

## Active source-of-truth documents

Classification: `ACTIVE_SOURCE_OF_TRUTH`

- `cad/` CadQuery source files are the CAD source of truth. They were audited as a protected area and intentionally not edited.
- Root `AGENTS.md` is the repository-level workflow source of truth for future agents.
- `revisions/mk0.12/README.md` is the active revision map and status entry point.

## Active revision documents

Classification: `ACTIVE_REVISION_DOC`

Required `mk0.12` document set check: PASS.

- `revisions/mk0.12/README.md`
- `revisions/mk0.12/ENGINEERING_SPEC.md`
- `revisions/mk0.12/PARTS_SPEC.md`
- `revisions/mk0.12/INTERFACES.md`
- `revisions/mk0.12/VALIDATION_GATES.md`
- `revisions/mk0.12/PHYSICAL_TEST_PLAN.md`
- `revisions/mk0.12/AGENT_RULES.md`
- `revisions/mk0.12/KNOWN_ISSUES.md`

## Root workflow documents

Classification: `ROOT_WORKFLOW_DOC`

- `README.md` now points to active `mk0.12`, shows the required status lines, includes the mk0.12 read order, and explicitly warns not to start CAD implementation from the root README alone.
- `AGENTS.md` now defines the revision workflow hard gate, source-of-truth precedence, required `mk0.12+` document structure, allowed status values, CAD source-of-truth policy, and legacy cleanup policy.

## Legacy/reference documents

Classification: `LEGACY_REFERENCE`

- `revisions/mk0.12/MVP_ENGINEERING_SPEC.md` is marked as consolidated legacy/reference snapshot only.
- `revisions/mk0.12/REFERENCE_APPLICATION_PLAN.md` is marked as reference/context only.
- `docs/workflow/subsystem_first_workflow.md` is marked as historical/superseded mk0.11 workflow.
- `drawings/mk0.10/README.md` remains cancelled/legacy and now points active mk0.12 work back to `revisions/mk0.12/README.md` and root `AGENTS.md`.
- Older `revisions/mk0.1/` through `revisions/mk0.11.2/` documents are historical references unless a future active revision explicitly promotes content from them.
- `cad_legacy/pre_mk012/` is legacy reference material.

## Historical review documents

Classification: `HISTORICAL_REVIEW`

- `revisions/mk0.12/CAD_SKELETON_V2_REVIEW.md` is marked as a historical CAD skeleton v2 review.
- `revisions/mk0.12/CAD_SKELETON_NOTES.md` is marked as a legacy/historical CAD skeleton note.
- `reviews/mk0.7/`
- `reviews/mk0.7.1/`
- `reviews/mk0.7.3/`
- `reviews/mk0.9.1/`
- `reviews/mk0.11.2/`

Historical review reports are evidence/reference only and must not become active requirements unless explicitly promoted into the active revision-scoped specification.

## Derived artifacts

Classification: `DERIVED_ARTIFACT`

- `exports/`
- `renders/`
- generated STEP/STL files
- generated PNG/render files
- slicer previews and screenshots if present

Derived artifacts were intentionally not changed and must not override CadQuery source or the active revision-scoped specification.

## Temporary or redundant files

Classification: `TEMPORARY_OR_REDUNDANT`

No obvious temporary trash files were deleted during this cleanup.

No `.tmp`, editor backup, empty scratch, or clearly accidental files were removed. If a file may contain engineering history, it was preserved and classified instead of deleted.

## Unknown requires review

Classification: `UNKNOWN_REQUIRES_REVIEW`

- `exports/mk0.9_debug/` exists under generated artifacts. It was not changed or deleted because it may be useful historical debug evidence.
- Older revision documentation varies by structure before `mk0.12`. This is acceptable as history, but future active work should not copy those structures without an explicit revision decision.

## Files changed

- `AGENTS.md`
- `README.md`
- `docs/workflow/subsystem_first_workflow.md`
- `drawings/mk0.10/README.md`
- `revisions/mk0.12/REFERENCE_APPLICATION_PLAN.md`
- `revisions/mk0.12/CLEANUP_REPORT.md`

## Files intentionally not changed

- `cad/**/*.py`
- `cad/`
- `exports/`
- `renders/`
- `revisions/mk0.12/README.md`
- `revisions/mk0.12/ENGINEERING_SPEC.md`
- `revisions/mk0.12/PARTS_SPEC.md`
- `revisions/mk0.12/INTERFACES.md`
- `revisions/mk0.12/VALIDATION_GATES.md`
- `revisions/mk0.12/PHYSICAL_TEST_PLAN.md`
- `revisions/mk0.12/AGENT_RULES.md`
- `revisions/mk0.12/KNOWN_ISSUES.md`
- `revisions/mk0.12/CAD_SKELETON_NOTES.md`
- `revisions/mk0.12/CAD_SKELETON_V2_REVIEW.md`
- `revisions/mk0.12/MVP_ENGINEERING_SPEC.md`
- historical `revisions/` content outside `mk0.12`
- historical `reviews/` content

## Conflicts found

- Root `README.md` presented `mk0.11` as the current revision even though active engineering focus is `mk0.12`.
- Root `AGENTS.md` presented `mk0.1` as the current stable revision without distinguishing historical baseline from active revision focus.
- Root `AGENTS.md` treated the pre-`mk0.12` revision document structure as generally mandatory.
- Root `AGENTS.md` contained a hard independent-removal rule that conflicted with the accepted `mk0.12` stack-through-rod MVP limitation.
- `docs/workflow/subsystem_first_workflow.md` described the mk0.11 workflow in active language that could be misread as current for mk0.12.
- `revisions/mk0.12/REFERENCE_APPLICATION_PLAN.md` lacked a direct warning that it is reference/context only.

## Conflicts resolved

- Root `README.md` now identifies `mk0.12 MVP-2M stack-through-rod` as the active engineering focus.
- Root `README.md` now marks `mk0.11` subsystem-first workflow as historical/superseded for active work.
- Root `README.md` now links directly to `revisions/mk0.12/README.md` and lists the full mk0.12 read order.
- Root `AGENTS.md` now distinguishes historical baseline, active revision focus, and revision-scoped source of truth.
- Root `AGENTS.md` now defines the specification-first hard gate and blocks CAD when the active specification is missing, incomplete, contradictory, or structurally invalid.
- Root `AGENTS.md` now defines coupon and full-print gates.
- Root `AGENTS.md` now defines the required `mk0.12+` document structure.
- Root `AGENTS.md` now explicitly allows the documented `mk0.12` stack-through-rod serviceability limitation.
- `docs/workflow/subsystem_first_workflow.md` is marked historical/superseded for mk0.12.
- `revisions/mk0.12/REFERENCE_APPLICATION_PLAN.md` is marked reference/context only.

## Remaining manual review items

- Decide whether `exports/mk0.9_debug/` should be archived, ignored, or deleted in a separate generated-artifact cleanup task.
- Decide whether older workflow documents outside `mk0.12` should receive additional legacy headers in a broader history-normalization pass.
- Accept or revise the root `AGENTS.md` hard-gate wording before starting `mk0.12 CAD skeleton cleanup v3`.
- Confirm that `PASS FOR CAD SKELETON V3 INPUT` is the intended `SPECIFICATION` status phrase for mk0.12 going forward.

## CAD status

CAD IMPLEMENTATION: NOT STARTED

No CadQuery geometry was changed.

## Coupon status

COUPON PARTS: BLOCKED

Coupon parts were not created, generated, unlocked, or reclassified.

## Full print status

FULL PRINT: BLOCKED

Full print remains blocked until coupon and physical validation pass.

## Final recommendation

Do not start CAD implementation until the mk0.12 specification structure and source-of-truth policy are accepted.

After acceptance, the next engineering step remains `mk0.12 CAD skeleton cleanup v3`, followed by CAD validation gates before any coupon parts or full print.
