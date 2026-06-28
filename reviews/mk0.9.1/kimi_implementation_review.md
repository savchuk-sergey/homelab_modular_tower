# mk0.9.1 Kimi Implementation Review

## 1. Executive Summary

Краткий вывод: ревизия `mk0.9.1` сейчас **непригодна как рабочая CAD-ревизия**, потому что `build_assembly()`, экспорт и рендеры падают на геометрии `pom_c_shoe_clamp`.

Соответствие требованиям частичное:

- PASS: ревизионная документация `revisions/mk0.9.1/` создана; ключевые параметры rail/runner/feet/weight targets добавлены в `cad/config.py`; заявленная архитектура из 4 модулей отражена в assembly.
- PARTIAL: base/roof облегчены и имеют fan/filter/grille logic, но точный вес не проверен; rail/carriage subsystem задуман правильно, но не собирается и не имеет полноценных rail pockets в module shells.
- FAIL: assembly/export/render pipeline не проходит; `exports/mk0.9.1` и `renders/mk0.9.1` отсутствовали до проверки, экспорт создал только частичные ignored artifacts и остановился на `rpi_ssd_module`.

Главные риски:

- blocker в CadQuery geometry делает ревизию непроверяемой;
- rail/carriage subsystem пока не доказан геометрически;
- документация сильнее реализации: она обещает сменные башмаки, rail retention и легкие каретки, но часть этих решений нельзя проверить из-за падения сборки;
- параметры добавлены, но новые детали всё ещё содержат magic numbers.

Можно переходить к исправлениям, но только целевым этапом: сначала починить сборку кареток, затем повторить export/render/analysis и только после этого оценивать weight/airflow/printability.

## 2. Reviewed Scope

Проверено:

- CAD config: `cad/config.py`
- Assembly: `cad/assembly/tower_assembly.py`
- Part registry/export categories: `cad/exporters/part_registry.py`
- mk0.9.1 parts: `cad/parts/base_module.py`, `cad/parts/roof_module.py`, `cad/parts/rpi_ssd_module.py`, `cad/parts/mini_pc_placeholder_module.py`, `cad/parts/carriages.py`, `cad/parts/placeholders.py`, `cad/parts/rails.py`, `cad/parts/module_interface.py`, `cad/parts/feet.py`, `cad/parts/rods.py`, `cad/parts/airflow.py`
- Revision docs: `revisions/mk0.9.1/README.md`, `CHANGELOG.md`, `DESIGN_NOTES.md`, `BOM.md`, `PRINTING.md`, `ASSEMBLY.md`, `KNOWN_LIMITATIONS.md`, `MK1_PREPARATION.md`
- Exports/renders folders
- Commands:
  - `python -m compileall cad scripts`
  - `conda run -n cadquery python -c "from cad.assembly import build_assembly; ..."`
  - `conda run -n cadquery python scripts\export_revision.py --revision mk0.9.1`
  - `conda run -n cadquery python scripts\render_views.py --out renders\mk0.9.1 --mode views --target all --revision mk0.9.1 --size 1200 --tolerance 2.0`
  - targeted factory checks for base, roof, RPi/SSD carriage, Mini PC carriage

## 3. Requirement Compliance Matrix

| Requirement | Status | Evidence | Notes |
|---|---|---|---|
| Four-module architecture: base, RPi/SSD, Mini PC placeholder, roof | PARTIAL | `cad/assembly/tower_assembly.py:97-108` | Four modules are added, but assembly fails before completion. |
| No final power/router/DC UPS/full rear spine/final Mini PC duct | PARTIAL | `revisions/mk0.9.1/README.md:23-46`; legacy `cad/parts/service_spine.py`, `cad/parts/modules.py` still exist | Current assembly does not add these modules, but legacy factories/config remain and need clear exclusion in manifests. |
| Rail profile 15x10x10x2 | PASS | `cad/config.py:774-778`; `cad/parts/placeholders.py:198-212` | Correct wall thickness 2.0 and inner width 11.0 are configured. |
| Runner shoes POM-C Ø8 | PASS | `cad/config.py:788-806`; `cad/parts/placeholders.py:186-195` | Correct runner material/diameter/length are configured. |
| Rail placeholders are non-printed | PASS | `cad/exporters/part_registry.py:101-105` | Rail placeholder is in `non_printable/metal_reference`, not printable plastic. |
| POM-C shoes are non-printed placeholders | PASS | `cad/exporters/part_registry.py:107-110` | Shoe placeholder is under placeholders/devices, not printable plastic. |
| Printed STL excludes aluminum rails and POM-C shoes | PARTIAL | `cad/exporters/part_registry.py:83-112` | Registry categories are correct, but full export fails before all artifacts can be verified. |
| PETG not final sliding surface | PARTIAL | `cad/parts/carriages.py:266-325`; `cad/assembly/tower_assembly.py:44-91` | PETG sockets and POM-C placeholders exist, but carriage fails to build and fit cannot be checked. |
| M3 clamp screw into PETG, not POM-C | PARTIAL | `cad/config.py:804-806`; `cad/parts/carriages.py:282-293` | Intent is present; implementation uses a clamp bridge, but it fails on chamfer and lacks explicit heat-set insert geometry. |
| Replaceable shoes, no glue-only retention | PARTIAL | `revisions/mk0.9.1/ASSEMBLY.md:31-36`; `cad/parts/carriages.py:266-293` | Concept documented; geometry currently not buildable. |
| RPi/SSD carriage: 2 shoes per side, open frame, airflow window | FAIL | `cad/config.py:801`; failure in `cad/parts/carriages.py:404` | Code requests 2 shoes per side, but factory fails. |
| Mini PC carriage: 3 shoes per side, placeholder pads, airflow window | FAIL | `cad/config.py:802`; failure in `cad/parts/carriages.py:457` | Code requests 3 shoes per side, but factory fails. |
| Feet restored, 10-15 mm clearance, preferred 12 mm | PASS | `cad/config.py:822-826`; `cad/parts/base_module.py:76-87`; `cad/assembly/tower_assembly.py:129-139` | `FOOT_ENABLED`, `FOOT_HEIGHT`, `BOTTOM_AIR_INTAKE_CLEARANCE` exist; foot mounts and assembly feet exist. |
| Base module lightweight frame, fan, 105 mm holes, grill, filter, foot mounts | PARTIAL | `cad/parts/base_module.py:39-119`; targeted factory check OK bbox `(190,190,68)` | Base builds, but actual weight and airflow area are not verified. |
| Roof module lightweight frame, exhaust fan, 105 mm holes, grill/filter/shroud | PARTIAL | `cad/parts/roof_module.py:9-68`; targeted factory check OK bbox `(190,190,69)` | Roof builds, but weight/exhaust obstruction need export/render/slicer verification. |
| M5 vertical rods x4 through modules | PARTIAL | `cad/assembly/tower_assembly.py:29-41`; `cad/parts/module_interface.py:69-87` | Rod placeholders and clearance holes exist, but full assembly fails. |
| Alignment pins/bosses/sockets and local fixation | PASS | `cad/parts/module_interface.py:45-104`; front lock hole in `cad/parts/carriages.py:374-379` | Interface features exist; lock geometry is not fully validated due carriage failure. |
| Central vertical airflow path | PARTIAL | `cad/parts/airflow.py`; `cad/parts/base_module.py:47-73`; `cad/parts/roof_module.py:25-57`; `cad/parts/carriages.py:338-345` | Design intent is present, but no render/section validation because assembly fails. |
| Weight targets documented/configured | PARTIAL | `cad/config.py:72-74`, `cad/config.py:828-834`; `revisions/mk0.9.1/BOM.md:3-15` | Slicer/volume validation not completed for mk0.9.1. |
| Expected source file structure | PARTIAL | `cad/parts/*` | No `cad/assembly.py`, `grills.py`, `filters.py`, `fasteners.py`; logic exists in `cad/assembly/`, base/roof/rods. Structure is acceptable but less separated than requested. |
| Revision docs present | PASS | `revisions/mk0.9.1/` contains all requested files | Docs exist and cover corrective intent, placeholders, mk1 prep, BOM, printing, assembly. |
| Exports/renders present | FAIL | `exports/mk0.9.1` and `renders/mk0.9.1` were absent before checks; export failed after partial base artifacts | No complete mk0.9.1 export/render set. |
| Build/import/export/render commands | FAIL | Command logs below | Compile passes; assembly/export/render fail on carriage clamp chamfer. |

## 4. Critical Findings

ID: MK091-P0-001  
Priority: P0  
Area: CadQuery build / rail-carriage subsystem  
File(s): `cad/parts/carriages.py`  
Description: `make_pom_c_shoe_clamp()` fails during `.edges("|Z").chamfer(cfg.FILLET_RADIUS)`. Both `make_rpi_ssd_carriage()` and `make_mini_pc_placeholder_carriage()` fail through this path.  
Why it matters: The full assembly cannot be built, export cannot finish, and renders cannot be generated. This blocks all downstream engineering verification.  
Evidence: `conda run -n cadquery python -c "from cad.assembly import build_assembly; build_assembly()"` fails with `OCP.StdFail.StdFail_NotDone: BRep_API: command not done` at `cad/parts/carriages.py:293`. Targeted factory checks show `base_module` and `roof_module` OK, both carriage factories FAIL.  
Suggested fix: Refactor the clamp geometry into a simpler, robust printable solid. Avoid chamfering the unioned bridge/lip composite, or chamfer only known-safe edges before union. Move clamp dimensions into `config.py`.

ID: MK091-P0-002  
Priority: P0  
Area: Export pipeline  
File(s): `scripts/export_revision.py`, `cad/exporters/part_registry.py`, `cad/parts/rpi_ssd_module.py`, `cad/parts/carriages.py`  
Description: `conda run -n cadquery python scripts\export_revision.py --revision mk0.9.1` fails while exporting `printable/plastic/rpi_ssd_module`.  
Why it matters: mk0.9.1 cannot produce a complete STEP/STL artifact set, so printed/non-printed separation cannot be verified from actual outputs.  
Evidence: Export log: `Exporting printable/plastic/base_module`, `bottom_grill`, `foot_mounts`, then failure on `rpi_ssd_module` at the same clamp chamfer. Only partial ignored artifacts are present under `exports/mk0.9.1/printable/plastic/`.  
Suggested fix: Fix MK091-P0-001 first, then rerun full export and ensure all categories complete.

ID: MK091-P0-003  
Priority: P0  
Area: Render / visual engineering review  
File(s): `scripts/render_views.py`, `cad/assembly/tower_assembly.py`, `cad/parts/carriages.py`  
Description: `render_views.py` fails because it calls `build_assembly()`, which fails on the carriage clamp.  
Why it matters: No front/rear/left/right/top/bottom/isometric render set exists for mk0.9.1, so airflow, feet, module order, rail placement, and carriage geometry cannot be visually audited.  
Evidence: `conda run -n cadquery python scripts\render_views.py --out renders\mk0.9.1 --mode views --target all --revision mk0.9.1 --size 1200 --tolerance 2.0` fails at `collect_render_items()` -> `build_assembly()` -> `make_pom_c_shoe_clamp()`.  
Suggested fix: Fix the carriage clamp, then regenerate views and drawing sheets.

ID: MK091-P1-001  
Priority: P1  
Area: Rail/module integration  
File(s): `cad/parts/rails.py`, `cad/parts/rpi_ssd_module.py`, `cad/parts/mini_pc_placeholder_module.py`, `cad/assembly/tower_assembly.py`  
Description: U-channel rail placeholders are added to assembly as separate non-printed objects, but module shells do not appear to cut rail pockets or include rail end retention clips. `make_rail_pocket_cutter()` and `make_rail_end_clip()` exist but are not applied to module shells.  
Why it matters: The rail standard is only represented visually. There is no verified printable interface that physically receives and retains the aluminum U-channel.  
Evidence: `cad/parts/rails.py:103-124` defines pocket/clip helpers; `cad/parts/rpi_ssd_module.py:62-87` and `cad/parts/mini_pc_placeholder_module.py:62-87` build shells and carriages without using them. Assembly adds rails at `cad/assembly/tower_assembly.py:66-76`.  
Suggested fix: Add parametric side rail pockets and rail-end retention features to the RPi/SSD and Mini PC module shells, or explicitly document that mk0.9.1 only validates carriage runner geometry and not rail mounting.

ID: MK091-P1-002  
Priority: P1  
Area: Export completeness / review artifacts  
File(s): `exports/mk0.9.1/`, `renders/mk0.9.1/`, `revisions/mk0.9.1/analysis/`  
Description: Complete mk0.9.1 exports, renders, and analysis CSVs are missing.  
Why it matters: Weight targets, printed/non-printed split, print volume, STL quality, and visual assembly cannot be validated.  
Evidence: Before checks, `exports/mk0.9.1` and `renders/mk0.9.1` did not exist. After failed export, only partial `base_module`, `bottom_grill`, and `foot_mounts` artifacts exist. No complete render set exists.  
Suggested fix: After P0 fixes, run export, analysis/package pipeline, and render commands for mk0.9.1.

ID: MK091-P1-003  
Priority: P1  
Area: Project structure / revision documentation path  
File(s): `revisionsmk0.9.1/`  
Description: There is an unexpected top-level directory named `revisionsmk0.9.1` alongside the correct `revisions/mk0.9.1`.  
Why it matters: This looks like a path-join mistake. Even empty, it is confusing and risks future scripts writing revision artifacts outside the canonical `revisions/` tree.  
Evidence: `Test-Path revisionsmk0.9.1` returned `True`; recursive listing showed no useful contents.  
Suggested fix: Remove the stray directory after confirming it is empty/untracked; verify any script that created it.

## 5. Medium / Low Findings

ID: MK091-P2-001  
Priority: P2  
Area: Parameterization / magic numbers  
File(s): `cad/parts/carriages.py`, `cad/parts/rails.py`  
Description: New mk0.9.1 geometry uses inline dimensions in several places, e.g. clamp bridge/lip sizes, shoe mount inset `24.0`, rail X offset clearance `1.0`, front lip dimensions, mini PC pad radius/height, rail clip sizes.  
Why it matters: This violates the project rule that dimensions belong in `config.py` and makes future rail/carriage tuning harder.  
Suggested fix: Move all mk0.9.1-specific clamp, lip, rail-pocket, rail-clip, shoe-spacing and support-pad dimensions into named config constants.

ID: MK091-P2-002  
Priority: P2  
Area: Legacy config/API noise  
File(s): `cad/config.py`, `cad/parts/modules.py`, `cad/trays.py`, `cad/power_bus.py`, `cad/airflow.py`, `cad/parts/service_spine.py`  
Description: Legacy mk0.3-mk0.9 tray/power/spine/module factories remain in the codebase. This is acceptable for backward compatibility, but mk0.9.1 docs say these systems are not implemented.  
Why it matters: Reviewers may confuse available legacy factories with active mk0.9.1 implementation.  
Suggested fix: Keep legacy code if needed, but ensure mk0.9.1 manifests/export categories label it as `legacy` and exclude it from active printable/review evidence.

ID: MK091-P2-003  
Priority: P2  
Area: Weight verification  
File(s): `cad/config.py`, `revisions/mk0.9.1/BOM.md`  
Description: Weight targets exist, but no mk0.9.1 `plastic_estimate.csv` or slicer evidence is available.  
Why it matters: Base/roof/carriage mass reduction was a central mk0.9.1 goal. Without export/analysis/slicer, the target cannot be trusted.  
Suggested fix: After successful export, run plastic estimate analysis and then validate in slicer.

ID: MK091-P2-004  
Priority: P2  
Area: File structure separation  
File(s): `cad/parts/`  
Description: Requested files such as `grills.py`, `filters.py`, and `fasteners.py` do not exist; related logic is embedded in base/roof/rods/modules.  
Why it matters: Not automatically wrong, but separation is weaker than requested and will become harder to maintain as mk1.0 grows.  
Suggested fix: Keep current structure for the fix phase unless it blocks work; consider extracting grills/filters/fasteners after the geometry is stable.

ID: MK091-P2-005  
Priority: P2  
Area: Clamp/retention realism  
File(s): `cad/parts/carriages.py`  
Description: Clamp documentation says heat-set insert boss, but the visible clamp bridge is a simplified hole/lip; no clear heat-set insert boss geometry is visible around each runner clamp.  
Why it matters: If the M3 screw only passes through a printed bridge without a robust insert/boss/load path, retention may crack or loosen.  
Suggested fix: Model the clamp as a replaceable/robust PETG boss with explicit insert volume and service clearance.

ID: MK091-P3-001  
Priority: P3  
Area: Naming consistency  
File(s): `cad/parts/roof_module.py`  
Description: Module docstring says `mk0.9 Roof Module`, while the revision is mk0.9.1.  
Why it matters: Cosmetic, but confusing during review.  
Suggested fix: Update docstring during the implementation pass.

ID: MK091-P3-002  
Priority: P3  
Area: Documentation precision  
File(s): `revisions/mk0.9.1/KNOWN_LIMITATIONS.md`  
Description: Docs state cable management is ad-hoc until rear spine is designed, which matches scope, but could more explicitly say no final rear service spine geometry is active in mk0.9.1 assembly.  
Why it matters: Avoids overclaiming implementation state.  
Suggested fix: Tighten wording after CAD/export state is fixed.

## 6. Engineering Assessment

Modularity: PARTIAL. Four-stack architecture and module interface features exist, with alignment pins, sockets, bolt holes, and rod clearance holes. However, removable module proof is blocked because carriages do not build.

Repairability: PARTIAL. Front pull lip, front lock screw concept, rear cable exit, replaceable feet, and replaceable POM-C shoe intent are present. Real serviceability cannot be validated until rails, pockets, clips, and carriage clearances render/export.

Stiffness: PARTIAL. Base/roof/module shells retain corner posts and M5 rod holes. M5 placeholders are added in assembly. But the revision lacks completed assembly evidence and no torsion/fit review is available.

Airflow: PARTIAL. Base/roof have fan openings and grilles; carriages are intended as open-frame rings. The lower fan should not blow into a fully solid tray if the carriage is fixed, but no render/section proof exists.

Printability: NOT CHECKED. Compile passes, base/roof factories build, but the core carriage factory fails; STL quality and print volume cannot be checked for the full revision.

Weight/plastic use: NOT CHECKED. Targets are documented and configured, but no mk0.9.1 plastic estimate or slicer result exists. This must be checked after export.

Rail/carriage realism: PARTIAL to FAIL. Correct rail and runner dimensions are configured, but the printable carriage fails and the module shell does not appear to include rail pockets/end-retention integration.

Preparedness for mk1.0: PARTIAL. The docs correctly defer real Mini PC geometry and mk1.0 prep, but current mk0.9.1 is not a reliable pre-measurement platform until the build/export blockers are fixed.

## 7. Rail/Carriage Subsystem Review

Profile 15x10x10x2: PASS. `RAIL_TYPE`, outer width, outer height, wall thickness, and inner width match the requirement.

POM-C Ø8: PASS. `RUNNER_MATERIAL`, `RUNNER_DIAMETER`, and placeholder geometry match the requirement.

Shoes: PARTIAL. 2-per-side and 3-per-side counts are configured. POM-C shoe placeholders are placed in assembly. Printable socket/retention geometry fails before validation.

Clamp screw: PARTIAL/FAIL. Intent is M3 clamp screw into PETG, but `make_pom_c_shoe_clamp()` is the failing geometry and does not yet prove a robust heat-set insert boss.

Placeholders: PASS for registry intent. Aluminum rail is non-printable metal reference; POM-C shoe is placeholder/devices.

Export: FAIL. Complete export cannot be generated.

Risks of binding: NEEDS TEST. U-channel clearances exist in config (`RAIL_POCKET_WIDTH`, `RAIL_POCKET_HEIGHT`, `RAIL_POCKET_CLEARANCE`), but no physical rail pocket geometry is integrated into module shells and no rendered clearance evidence exists.

Risks of looseness: NEEDS TEST. Runner socket clearance is 0.3 mm, but real printed PETG + POM-C tolerance stack needs coupon or slicer/print test.

Risks of assembly: HIGH. Rail mounting is under-specified in active geometry, rail end clips are defined but not integrated, and carriage clamp geometry blocks assembly.

## 8. Base/Roof Weight and Geometry Review

Base:

- Builds successfully as a standalone factory.
- Uses frame-body, fan mount, bottom grille, dust filter slot, and foot mounts.
- Fan screw spacing uses `FAN_120_HOLE_SPACING = 105.0`.
- Not a massive monolithic slab in code structure.
- Weight target cannot be verified because full export/analysis is blocked. Slicer check still required.

Roof:

- Builds successfully as a standalone factory.
- Uses frame, top fan mount, top filter slot, top grille, and lightweight shroud rails.
- Fan screw spacing uses `FAN_120_HOLE_SPACING = 105.0`.
- No complete render, so exhaust obstruction cannot be visually confirmed.
- Weight target cannot be verified because full export/analysis is blocked. Slicer check still required.

## 9. Documentation Review

Requested files exist under `revisions/mk0.9.1/`:

- `README.md`
- `CHANGELOG.md`
- `DESIGN_NOTES.md`
- `BOM.md`
- `PRINTING.md`
- `ASSEMBLY.md`
- `KNOWN_LIMITATIONS.md`
- `MK1_PREPARATION.md`

Docs correctly state the corrective intent after mk0.9, placeholder-based Mini PC path, rail/carriage standard, POM-C Ø8 shoes, no PETG sliding surface, no direct threading into POM-C, and mk1.0 dependency on real Mini PC measurements.

Main documentation risk: it currently overstates implementation confidence because the CAD assembly/export/render pipeline fails. After fixes, docs should be updated with actual generated evidence and any remaining limitations.

## 10. Build/Export/Render Check

Command: `python -m compileall cad scripts`  
Result: PASS  
Notes: Python syntax compilation completed.

Command: `conda run -n cadquery python -c "from cad import config as cfg; from cad.assembly import build_assembly; a=build_assembly(); ..."`  
Result: FAIL  
Error: `OCP.StdFail.StdFail_NotDone: BRep_API: command not done`  
File: `cad/parts/carriages.py:293`  
Likely cause: chamfer operation on the unioned clamp/lip solid in `make_pom_c_shoe_clamp()` is overconstrained or selects invalid edges.

Command: `conda run -n cadquery python scripts\export_revision.py --revision mk0.9.1`  
Result: FAIL  
Error: same `StdFail_NotDone` at `cad/parts/carriages.py:293` while exporting `printable/plastic/rpi_ssd_module`.  
Notes: Partial artifacts were generated under `exports/mk0.9.1/printable/plastic/` for `base_module`, `bottom_grill`, and `foot_mounts` only.

Command: `conda run -n cadquery python scripts\render_views.py --out renders\mk0.9.1 --mode views --target all --revision mk0.9.1 --size 1200 --tolerance 2.0`  
Result: FAIL  
Error: same assembly failure through `collect_render_items()` -> `build_assembly()` -> carriage clamp.

Targeted factory checks:

- `base_module.make_base_module()`: PASS, bbox approximately `(190.0, 190.0, 68.0)`
- `roof_module.make_roof_module()`: PASS, bbox approximately `(190.0, 190.0, 69.0)`
- `carriages.make_rpi_ssd_carriage()`: FAIL, same clamp chamfer
- `carriages.make_mini_pc_placeholder_carriage()`: FAIL, same clamp chamfer

## 11. Fix Plan

| Step | Priority | Goal | Files | Expected result |
| ---- | -------- | ---- | ----- | --------------- |
| 1 | P0 | Fix `make_pom_c_shoe_clamp()` so both carriage factories build | `cad/parts/carriages.py`, `cad/config.py` | `make_rpi_ssd_carriage()` and `make_mini_pc_placeholder_carriage()` return valid solids. |
| 2 | P0 | Restore complete assembly build | `cad/parts/carriages.py`, `cad/parts/rpi_ssd_module.py`, `cad/parts/mini_pc_placeholder_module.py`, `cad/assembly/tower_assembly.py` | `build_assembly()` succeeds and lists all four modules plus placeholders. |
| 3 | P1 | Integrate U-channel rail pockets/end retention into active module shell geometry or explicitly document placeholder-only scope | `cad/parts/rails.py`, `cad/parts/rpi_ssd_module.py`, `cad/parts/mini_pc_placeholder_module.py`, `cad/config.py` | Rails have printable mounting interfaces; rail clips/pockets are parametric and visible in exports/renders. |
| 4 | P1 | Validate printed/non-printed export split | `cad/exporters/part_registry.py`, `scripts/export_revision.py` | Complete `exports/mk0.9.1/` generated; aluminum rails and POM-C shoes absent from printable STL. |
| 5 | P1 | Generate render evidence | `scripts/render_views.py`, `renders/mk0.9.1/` | Front/rear/left/right/top/bottom/isometric render set shows rails, shoes, feet, airflow, module order. |
| 6 | P1 | Run analysis/review package pipeline | `scripts/run_revision_pipeline.py`, `scripts/package_review.py`, `revisions/mk0.9.1/analysis/` | STL quality, print volume, plastic estimate, dimensions, and review package exist for mk0.9.1. |
| 7 | P2 | Move mk0.9.1 magic numbers into config | `cad/config.py`, `cad/parts/carriages.py`, `cad/parts/rails.py` | Rail/carriage/retention dimensions are tunable from `config.py`. |
| 8 | P2 | Confirm base/roof and carriage weight targets | `revisions/mk0.9.1/BOM.md`, `revisions/mk0.9.1/PRINTING.md`, slicer notes | Slicer or volume estimate confirms target/hard-limit status. |
| 9 | P2 | Clean structural/documentation clutter | `revisionsmk0.9.1/`, `revisions/mk0.9.1/*.md` | Stray path removed if empty; docs updated with actual evidence and remaining limitations. |
| 10 | P3 | Improve naming/docstrings | `cad/parts/roof_module.py`, related docs | mk0.9.1 naming is consistent. |

Correction phases:

1. Blockers: Steps 1-2.
2. Rail/carriage corrections: Steps 3 and 7.
3. Feet/base/roof corrections: Step 8, plus only geometry changes if export/render reveals issues.
4. Airflow corrections: Step 5 visual review, then adjust only if the airflow path is blocked.
5. Export/render corrections: Steps 4-6.
6. Documentation corrections: Steps 8-10.

## 12. Recommended Next Prompt for Implementation

```text
Ты работаешь над homelab_modular_tower на ветке cad/mk0.9.1.

Нужно исправить только blockers и high-priority проблемы из reviews/mk0.9.1/kimi_implementation_review.md.

Ограничения:
- не переписывай архитектуру целиком;
- CadQuery остаётся source of truth;
- все новые размеры вынеси в cad/config.py;
- не трогай старые стабильные ревизии;
- не реализуй power/router/DC UPS/full rear service spine/final mini PC tray/duct;
- mini PC остаётся placeholder-based.

Цели:
1. Починить make_pom_c_shoe_clamp()/carriage geometry так, чтобы make_rpi_ssd_carriage(), make_mini_pc_placeholder_carriage() и build_assembly() проходили.
2. Интегрировать или явно ограничить rail pocket / rail end retention для алюминиевого П-швеллера 15x10x10x2.
3. Проверить, что POM-C Ø8 shoes и aluminum rails остаются non-printed placeholders и не попадают в printable STL.
4. Запустить:
   - python -m compileall cad scripts
   - conda run -n cadquery python scripts/export_revision.py --revision mk0.9.1
   - conda run -n cadquery python scripts/run_revision_pipeline.py --revision mk0.9.1
   - conda run -n cadquery python scripts/render_views.py --out renders/mk0.9.1 --mode views --target all --revision mk0.9.1 --size 1200 --tolerance 2.0
5. Обновить mk0.9.1 documentation только фактами, подтверждёнными export/render/analysis.
```

## 13. Final Verdict

Verdict: REWORK REQUIRED

Причина: требования `mk0.9.1` в значительной степени поняты и частично представлены в коде/документации, но ключевая новая подсистема rail/carriage не собирается. Пока `build_assembly()`, export и render падают, ревизия не может считаться инженерно проверенной и не готова даже как reliable corrective iteration.
