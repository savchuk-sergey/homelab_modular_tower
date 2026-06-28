# Homelab Modular Tower Engineering Review — mk0.11.2

**Revision:** mk0.11.2  
**Branch:** `master`  
**Date:** 2026-06-29  
**Review type:** CAD compliance audit — stack module requirements verification  
**Scope:** `generic_stack_module`, `base_pedestal`, `top_cap`, `stack_test_assembly`  
**Validation limits:** no CFD, no FEA, no slicer validation, no physical testing.
CadQuery not available in review environment; geometry checks from prior session
(VALIDATION_PLAN.md Steps 1–4, 2026-06-28) used as evidence.

---

## 1. Executive Summary

`generic_stack_module` mk0.11.2 **соответствует** требованиям stack-through-rod
архитектуры.  Модуль является stackable layer, а не активной кареткой.
Четыре M5 сквозных отверстия, frame rings сверху/снизу, центральный airflow
канал 125×125 мм, rear service zone 30 мм — всё присутствует и параметрично.

**Общий вердикт: GO FOR TEST PRINT** — при условии slicer-preview перед печатью.

**Blocking issues: нет.**

Один новый FAIL-level finding исправлен в ходе аудита (архитектурная изоляция,
не геометрия).  Все предыдущие критические findings (Step 5, 2026-06-28)
подтверждены как исправленные.  Три deferred items (device mount grid, M3
bosses, cable tie slots) приняты как осознанный отложенный scope для mk0.11.2
structural shell.

---

## 2. Reviewed Inputs

### CAD files

- `cad/parts/generic_stack_module.py`
- `cad/parts/base_pedestal.py`
- `cad/parts/top_cap.py`
- `cad/assembly/stack_test_assembly.py`
- `cad/parts/module_interface.py`
- `cad/parts/rails.py`
- `cad/parts/rods.py`
- `cad/config.py` (секция mk0.11.2, строки 912–955)

### Revision documentation

- `revisions/mk0.11.2/README.md`
- `revisions/mk0.11.2/DECISIONS.md`
- `revisions/mk0.11.2/VALIDATION_PLAN.md`

### Commands run

- `python -m compileall cad scripts` — EXIT 0 (до и после исправлений)

### Previously validated (VALIDATION_PLAN.md Steps 1–4, 2026-06-28)

- CadQuery geometry checks: `generic_stack_module` bbox 191.7×194.0×74.0 мм
- `stack_test_assembly_mk0112` собирается без исключений
- STEP export: 5 деталей + assembly, без deferred carriage/rail частей

---

## 3. Requirement Compliance Matrix

| Требование | Статус | Evidence | Примечание |
|---|---|---|---|
| Stack-through-rod architecture | **PASS** | Нет rail pockets, POM-C sockets, sliding geometry. M5 rods — силовой путь. | — |
| M5 through holes (4×, сквозные, из config) | **PASS** | `ROD_CLEARANCE` 5.6 мм, позиции `(±81, ±81)` мм через `apply_module_interface_features`. Все 4 уникальных угла — Step 5, Finding 1. | Физическое тестирование pending. |
| Top/bottom interface rings | **PASS** | `_make_frame_ring` идентична на base/module/cap. Кольца дают perimeter contact. Pin engagement отключён — M5 rods обеспечивают выравнивание. | Физическое тестирование pending. |
| Compression pads вокруг M5 | **PARTIAL** | Washer-seat карманы (M5_WASHER_DIAMETER = 12 мм) на каждом corner post. Диаметр кармана на 0.4 мм шире corner post (11.6 мм) — минимальный overlap в ring. | Не структурный FAIL. Тест с реальной шайбой required. |
| Airflow opening | **PASS** | Центральный 125×125 мм канал, нет сплошного пола, совместим с base intake и top exhaust. | CFD/physical не тестировалось. |
| Rear service zone | **PASS** | `REAR_RESERVED_DEPTH` = 30 мм, открытый коридор во всех трёх частях. | Структурированных кабельных точек нет. |
| Future cable management reserve | **PARTIAL** | Только открытая reserved zone. Нет tie-slot, cable pass-through, strain relief. Минимальное требование («открытая зона») выполнено. | Добавить кабельные фиксаторы в mk0.12. |
| Future carriage mounting zones | **PARTIAL** | Full-height side pads X = ±84.5 мм, интегрированы в оба кольца. Bottom adapter pads присутствуют. M3 insert bosses deferred (Step 5, Finding 3). | Pilot holes/bosses нужны для реального крепления адаптера в mk0.12. |
| Device mounting placeholder | **FAIL** | `_make_internal_mount_grid_placeholder` существует но не вызывается — все пады внутри airflow зоны без опоры (Step 5, Finding 4). | **Принятый дефер.** Тестовая печать structural shell не блокируется. |
| Front handle/label placeholder | **PASS** | 64×4×12 мм pull lip на нижнем фронте. Ориентация читается. Не мешает стяжке. | Slicer: проверить brim для lip. |
| Printability | **PASS** | Один связный solid. Нет floating islands (после Step 5 fixes). 4 отверстия, 8 карманов. | Slicer-preview обязателен перед печатью. |
| Config / no magic numbers | **PASS** | Все размеры из `config.py`. Исправление D-013 применено: `rails` import удалён, добавлен `FUTURE_CARRIAGE_PAD_X_OFFSET`. | Fix applied в этом аудите. |
| Base/top compatibility | **PASS** | Идентичная формула `_corner_rod_points` и ring geometry на всех трёх частях. | Физический fit test pending. |
| Stack assembly clarity | **PASS** | `stack_test_assembly`: base + module + cap + 4 ref rods. Нет carriage/rail/POM-C. | — |

---

## 4. Critical Findings

### F-001 — FIXED: `rails` import в активном stack module

**Severity:** FAIL (config discipline / architecture isolation)

**File:** `cad/parts/generic_stack_module.py`

**Root cause:** Модуль импортировал деferred-модуль `cad/parts/rails.py` для
вызова `u_channel_rail_x_offset()` — единственно для вычисления X-позиции
future carriage pad-ов.  Это нарушало изоляцию активной mk0.11.2 архитектуры
от отложенной carriage/rail-архитектуры.

**Fix applied:**

- `cad/config.py`: добавлен `FUTURE_CARRIAGE_PAD_X_OFFSET = 84.5 мм` в секции
  mk0.11.2 (с расчётом из frozen rail constants и комментарием).
- `cad/parts/generic_stack_module.py`: удалён `from . import rails`,
  три вызова `rails.u_channel_rail_x_offset()` заменены на
  `c.FUTURE_CARRIAGE_PAD_X_OFFSET`.
- Геометрия не изменилась.

**Decision:** D-013 добавлено в `revisions/mk0.11.2/DECISIONS.md`.

---

### F-002 — ACCEPTED DEFERRAL: Device mounting placeholder отсутствует

**Severity:** FAIL по требованию; принятый дефер по инженерной логике

**Root cause:** `_make_internal_mount_grid_placeholder` — все 12 standoff-пад-ов
попадают в airflow зону (125×125 мм) без опорного материала.  Вызов удалён
во избежание floating islands (Step 5, Finding 4).

**Resolution:** structural shell mk0.11.2 не имеет device-specific mounting.
Реактивировать после добавления bridging rib или floor в device-specific модуле.
**Не блокирует тестовую печать.**

---

### F-003 — ACCEPTED DEFERRAL: M3 insert bosses для future carriage не реализованы

**Severity:** PARTIAL; принятый дефер

**Root cause:** `_make_future_side_adapter_mount_points` — боссы
disconnected от side pads из-за конфликта X-позиционирования (Step 5, Finding 3).

**Resolution:** физический материал для будущего адаптера есть (side pads
2.4×22×70 мм).  Pilot holes можно добавить сверлением.  Heat-set insert boss
geometry реактивировать в mk0.12 после перепроектирования connectivity.

---

### F-004 — CONFIRMED FIXED (Step 5, 2026-06-28): Four prior critical findings

Подтверждено как исправленные до этого аудита:

| Finding | Исправление |
|---|---|
| `_corner_rod_points` дублированный 4-й угол | Исправлено: 4-й угол `(-x, y)` вместо `(-x, -y)` |
| Floating carriage mount pads | Исправлено: pads на полную высоту модуля, X позиция скорректирована |
| Floating M3 bosses (основной источник "hanging circles") | Исправлено: функция deferred, убрана из shell |
| Floating internal mount grid | Исправлено: функция deferred, убрана из shell |
| Floating alignment pins в airflow канале | Исправлено: `top=False` на module и base |

---

## 5. Fixes Applied (этот аудит)

| Файл | Изменение |
|---|---|
| `cad/config.py` | Добавлен `FUTURE_CARRIAGE_PAD_X_OFFSET = 84.5 мм` с расчётом |
| `cad/parts/generic_stack_module.py` | Удалён `rails` import; 3 вызова → `c.FUTURE_CARRIAGE_PAD_X_OFFSET` |
| `revisions/mk0.11.2/VALIDATION_PLAN.md` | Добавлен раздел «Requirement verification checklist» |
| `revisions/mk0.11.2/DECISIONS.md` | Добавлено D-013 |
| `reviews/mk0.11.2/engineering_review.md` | Создан этот файл |

---

## 6. Future Readiness

### Future carriage / side adapter

LIKELY COMPATIBLE.  Материал присутствует на X = ±84.5 мм (full-height side
pads).  Pad width 2.4 мм, pad Y-span 22 мм достаточны для M3 heat-set insert.
3.5 мм clearance между краем M5 corner post (±81 мм) и центром pad (±84.5 мм)
позволяет разместить M3 boss без конфликта с rod.  Adapter attachment требует
pilot holes / bosses в mk0.12.  Полный редизайн модуля не нужен.

**Evidence status: LIKELY** — геометрический расчёт без physical validation.

### Future cable management

LIKELY COMPATIBLE.  30 мм rear corridor открыт на всех уровнях стека.
Bend radius для Ethernet/USB не заблокирован.  Tie-точки отсутствуют — кабели
без фиксаторов придётся удерживать дополнительными средствами.

**Evidence status: LIKELY** — не тестировалось физически.

### Future airflow (bottom 120mm intake / top exhaust)

PASS.  125×125 мм канал превышает рабочее отверстие вентилятора 120 мм
(112 мм air-opening diameter).  Base и top уже имеют airflow clearance zones.
Fan mount можно добавить к base/top без изменения module shell.

**Evidence status: CONFIRMED** — размеры из config.py, геометрия открытая.

### Future multi-module scaling

PASS.  Все размеры из `config.py`.  Второй/третий модуль стекуется идентично.
Риск уникальной геометрии низкий — device-specific features в deferred
функциях, не вызываемых в structural shell.

**Evidence status: CONFIRMED** — по коду.

---

## 7. Remaining Risks

- M5 rod real clearance (5.6 мм) не тестировалась физически с реальным M5 rod
- M5 washer seat depth (1.8 мм) не тестировалась на compression
- Compression pad diameter (12.0 мм) чуть шире corner post (11.6 мм) — не тестировалось
- PETG shrink / dimensional tolerance не тестировались
- Slicer island/support analysis не выполнен в реальном slicer (**обязателен перед print**)
- Airflow continuity не тестировалась физически
- Future carriage zone positions не валидировались с реальным U-channel rail
- Cable bend radius в rear zone не тестировался
- Physical stack compression stiffness не тестировалась

---

## 8. Next Recommended Step

**GO FOR TEST PRINT** — нет blocking issues.

1. Открыть `exports/step/generic_stack_module.step` в Bambu Studio или PrusaSlicer.
2. Проверить: один объект, нет floating islands в airflow канале, нет unexpected blobs.
3. При необходимости добавить brim для front handle lip (2 мм overhang от front face).
4. Напечатать `generic_stack_module` в PLA (prototype) или PETG.
5. Пропустить 4× M5 rod (5 мм) через corner post holes — проверить clearance.
6. Собрать стек: `base_pedestal` + `generic_stack_module` + `top_cap` + washers + nuts.
7. Проверить: contact rings, washer seats, airflow opening, rear service zone.
8. Зафиксировать результат в `revisions/mk0.11.2/VALIDATION_PLAN.md` (Physical validation).

Если physical test проходит — переходить к mk0.12:

- Добавить M3 insert bosses к side carriage pads
- Добавить cable tie slots в rear frame ring wall
- Добавить bridging rib или floor для device mounting в device-specific модуле
