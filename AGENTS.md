# AGENTS.md

## Назначение

Этот файл задает рабочие правила для LLM-агентов, которые изменяют проект `homelab_modular_tower`.

`homelab_modular_tower` - долгосрочный инженерный CAD-проект модульной настольной мини-стойки для HomeLab. Проект должен развиваться как инженерная платформа, а не как разовый декоративный корпус для 3D-печати.

Historical baseline: `mk0.1`.

Active engineering focus is defined by the latest active revision under `revisions/`.
As of this cleanup, active focus is `mk0.12` (`MVP-2M stack-through-rod`), unless a newer revision explicitly supersedes it.

## Общий стиль работы

Агент должен мыслить как инженер-конструктор. Внешний вид вторичен. Инженерная логика важнее дизайна.

Приоритеты проекта:

- модульность;
- ремонтопригодность;
- жесткость конструкции;
- хорошее охлаждение;
- удобство сборки;
- удобство обслуживания;
- параметрическое проектирование;
- масштабируемость на будущие ревизии.

Любое решение должно оцениваться с позиции реальной сборки, печати, обслуживания и дальнейшего развития конструкции.

## Архитектура корпуса

Конструкция является `Mini Blade Tower`.

Ориентировочные габариты:

- ширина: около 190 мм;
- глубина: около 190 мм;
- высота: около 300-330 мм.

Материалы:

- PETG - основной материал;
- PLA - только для прототипов;
- TPU - ножки, демпферы, фиксаторы.

Каркас не должен держаться только на пластике.

Основную жесткость должны обеспечивать:

- четыре металлические шпильки M5;
- металлические направляющие;
- верхняя силовая рама;
- нижняя силовая рама;
- усиленные угловые блоки.

Пластиковые детали должны работать как соединительные, позиционирующие и сервисные элементы. Они не должны быть единственными силовыми элементами конструкции.

## Модульный состав

Цель проекта - объединить несколько устройств в единую модульную систему:

1. UPS / Power Distribution
2. External SSD Bay
3. SSD / Expansion
4. Raspberry Pi
5. MikroTik hAP ax2
6. Mini PC

Full independent module removal is a long-term design goal, but not a hard requirement for every MVP revision.
Revision-scoped architecture wins.
In `mk0.12`, stack-through-rod architecture requires loosening the stack to remove middle modules. This is an accepted MVP limitation, not a failure, as long as it is documented in the active revision specification.

## Стандарт модулей

Все модули должны использовать единый модульный стандарт:

- одинаковые направляющие;
- одинаковые точки крепления;
- одинаковые ручки;
- одинаковые фиксаторы;
- одинаковые посадочные размеры;
- возможность извлечения модуля без разборки всей башни, если это не переопределено revision-scoped MVP-архитектурой.

Любое новое решение должно проверяться на совместимость с существующим модульным стандартом.

## Rear Service Spine

Сзади корпуса должна быть отдельная сервисная шахта `Rear Service Spine`.

Назначение `Rear Service Spine`:

- силовая DC-шина;
- Ethernet;
- USB;
- провода вентиляторов;
- кабель-менеджмент;
- крепление кабелей.

Все кабели должны проходить через эту шахту. Нельзя прокладывать кабели хаотично между модулями. Исключения допустимы только при явном инженерном обосновании.

## Power System

Архитектура питания:

```text
External AC/DC Power Supply
-> DC UPS
-> Power Bus
-> 19 V / 12 V / 5 V / GND
```

Внутри корпуса не должно быть открытой сети 220 В.

Все устройства должны питаться от внутренней DC-шины. Конструкция должна предусматривать возможность установки DC UPS в будущих ревизиях.

Power Bus должен проектироваться как сервисный узел с понятными зонами крепления, предохранителями, DC-DC преобразователями и быстросъемными разъемами модулей.

## Охлаждение

Базовая схема охлаждения - вертикальный поток воздуха:

- нижний вентилятор 120 мм - intake;
- верхний вентилятор 120 мм - exhaust.

Mini PC имеет отдельный воздуховод.

Приоритет охлаждения:

1. Mini PC
2. Остальные модули

Любые изменения геометрии должны учитывать:

- сопротивление воздушному потоку;
- зоны перегрева;
- доступность обслуживания вентиляторов;
- замену фильтра;
- отсутствие блокировки извлечения модулей.

## CAD-правила

CadQuery является единственным источником модели.

Источник истины проекта:

1. CadQuery-код в `cad/`;
2. git-история;
3. инженерная документация ревизий в `revisions/`.

STEP/STL-файлы и рендеры являются производными артефактами. Их нельзя считать источником истины.

Обязательные правила:

- все размеры должны храниться в `config.py`;
- не использовать магические числа;
- каждая деталь должна иметь собственную функцию;
- сборка должна создаваться отдельно;
- каждая деталь должна экспортироваться отдельно в STEP/STL;
- изменения в геометрии должны быть параметрическими;
- нельзя хардкодить размеры внутри функций деталей;
- нельзя смешивать логику разных деталей в одной функции;
- нельзя смешивать детали, сборку и экспорт в одном файле.

Если нужно добавить новый размер, он должен быть добавлен в `config.py` с понятным именем.

## Revision workflow hard gate

Before any CAD work, the active revision specification must be complete, revision-scoped, and internally consistent.

Required order:

1. Create or update the revision-scoped specification.
2. Validate required document structure.
3. Validate consistency across all active revision documents.
4. Resolve conflicts, mark assumptions, and mark unverifiable requirements as `NOT VERIFIED`.
5. Only after valid specification: allow CAD planning.
6. Only after CAD planning: allow CadQuery implementation.
7. Only after CAD validation gates: allow coupon parts.
8. Only after coupon and physical tests: allow full print.

If the active specification is missing, incomplete, contradictory, or structurally invalid, CAD work is BLOCKED.

No CAD development is allowed until the active revision specification is structurally complete and internally consistent.

## Active revision source-of-truth precedence

For active engineering work, source-of-truth precedence is:

1. Revision-scoped documents under `revisions/<revision>/`.
2. Root `AGENTS.md` workflow rules.
3. Legacy/reference snapshots.
4. Generated artifacts such as STEP, STL, PNG, screenshots, slicer previews, and renders.

If documents conflict:

- revision-scoped documents win over legacy/reference snapshots;
- the stricter interpretation wins;
- unresolved ambiguity must be marked `NOT VERIFIED`;
- CAD work remains BLOCKED until the ambiguity is resolved.

## Required revision document structure

For `mk0.12` and later revision-scoped specifications, the required active document set is:

- `README.md`
- `ENGINEERING_SPEC.md`
- `PARTS_SPEC.md`
- `INTERFACES.md`
- `VALIDATION_GATES.md`
- `PHYSICAL_TEST_PLAN.md`
- `AGENT_RULES.md`
- `KNOWN_ISSUES.md`

If any required document is missing, the specification is structurally invalid and CAD work is BLOCKED.

Pre-`mk0.12` revisions may use their historical document structures. Historical structure must not override the required `mk0.12+` active document set.

## Allowed status values

Use explicit status lines in active revision README files:

```text
SPECIFICATION: DRAFT / UNDER REVIEW / PASS FOR CAD INPUT / PASS FOR CAD SKELETON V3 INPUT / BLOCKED
CAD IMPLEMENTATION: NOT STARTED / IN PROGRESS / VALIDATION FAILED / VALIDATION PASSED
COUPON PARTS: BLOCKED / ALLOWED / DONE
FULL PRINT: BLOCKED / ALLOWED / DONE
NEXT STEP: <explicit next engineering step>
```

Rules:

- `COUPON PARTS` must remain `BLOCKED` until CAD validation gates pass.
- `FULL PRINT` must remain `BLOCKED` until coupon and physical tests pass.
- CAD status must not be advanced by documentation-only tasks.

## CAD source of truth

CadQuery source files are the CAD source of truth.

Rules:

- all dimensions must live in `cad/config.py`;
- no magic numbers inside part builders;
- printable builders must return printable plastic geometry only;
- reference builders must return placeholders/reference geometry only;
- assembly must be separate from part definitions;
- STEP/STL/PNG/renders are derived artifacts;
- derived artifacts must never override CadQuery source or revision-scoped specification.

## Legacy and cleanup policy

Rules:

- do not keep multiple active sources of truth for the same revision;
- legacy documents must be explicitly marked as legacy/reference/historical;
- historical review reports must not be treated as active requirements unless explicitly promoted;
- old CAD skeleton notes must be marked historical unless they match the active revision status;
- temporary scratch files should be deleted or moved to an archive;
- if deleting a file may remove engineering history, do not delete it; mark it and report it.

## Структура ревизий

Каждая CAD-ревизия является отдельной инженерной версией.

Версионирование CAD-кода выполняется через Git. Папка `cad/` содержит текущую рабочую CAD-модель проекта, а не архив ревизий.

Папка `revisions/` содержит документальные снимки инженерных ревизий. `revisions/mkX.Y/` - это инженерная документация состояния ревизии, а не копия всего CAD-кода.

Назначение основных папок:

- `cad/` - актуальная рабочая CadQuery-модель;
- `exports/` - актуальные экспортированные STEP/STL-файлы;
- `renders/` - актуальные рендеры;
- `revisions/` - документация инженерных ревизий;
- Git - фактическая история изменений CAD-кода и геометрии.

Правильная структура проекта:

```text
homelab_modular_tower/
  AGENTS.md
  cad/
    config.py
    parts/
    assembly.py
    exporters/
    ...
  exports/
  renders/
  revisions/
    mk0.1/                         # historical/pre-mk0.12 structure
      REVISION.md
      CALCULATIONS.md
      DECISIONS.md
      KNOWN_ISSUES.md
      CHANGELOG.md
    mk0.12/                        # active mk0.12+ structure
      README.md
      ENGINEERING_SPEC.md
      PARTS_SPEC.md
      INTERFACES.md
      VALIDATION_GATES.md
      PHYSICAL_TEST_PLAN.md
      AGENT_RULES.md
      KNOWN_ISSUES.md
```

Для каждой значимой CAD-ревизии должна создаваться отдельная git-ветка или git-тег.

Ветка `master` хранит актуальную стабильную ревизию проекта. Рабочие ветки ревизий вида `cad/mkX.Y` должны попадать в `master` только через Pull Request после инженерной проверки. Нельзя вручную переносить изменения ревизии в `master` в обход PR-процесса.

Документация каждой ревизии должна храниться в `revisions/mkX.Y/`.

Historical/pre-`mk0.12` revisions commonly used:

- `REVISION.md` - общее описание состояния ревизии;
- `CALCULATIONS.md` - расчеты, допущения, проверки размеров, жесткости, охлаждения и компоновки;
- `DECISIONS.md` - принятые инженерные решения и причины;
- `KNOWN_ISSUES.md` - известные проблемы и ограничения ревизии;
- `CHANGELOG.md` - список изменений относительно предыдущей ревизии.

For `mk0.12` and later, the active required structure is defined in `Required revision document structure` above.

История ревизий не должна изменяться задним числом.

Нельзя переписывать `mk0.1`, если требуется развитие. Новые изменения должны выполняться в новой ревизии, например `mk0.2`.

Перед началом новой ревизии агент должен:

- не копировать всю папку `cad/`;
- создать новую git-ветку, например `cad/mk0.2` или `feature/mk0.2`;
- создать новую папку документации `revisions/mk0.2/`;
- описать цель ревизии;
- зафиксировать исходные ограничения;
- после изменений обновить документацию ревизии.

Рекомендуемый процесс работы над ревизией:

```text
1. Создать git-ветку для ревизии.
2. Создать папку revisions/mkX.Y/.
3. Создать обязательный document set для этой ревизии.
4. Проверить структуру спецификации.
5. Проверить внутреннюю согласованность спецификации.
6. Только после валидной спецификации перейти к CAD planning.
7. Только после CAD planning вносить изменения в `cad/`.
8. Проверить параметричность `cad/config.py`.
9. Обновить `exports/` и `renders/` только при необходимости и только после CAD validation gates.
10. Зафиксировать инженерные решения в `revisions/mkX.Y/`.
11. Сделать git commit.
12. Открыть Pull Request из ветки ревизии в `master`.
13. После review и стабилизации смержить ревизию в `master`.
14. После merge поставить git tag `mkX.Y` на стабильное состояние.
```

Пример документации ревизий:

```text
revisions/
  mk0.1/
    REVISION.md
    CALCULATIONS.md
    DECISIONS.md
    KNOWN_ISSUES.md
    CHANGELOG.md
  mk0.12/
    README.md
    ENGINEERING_SPEC.md
    PARTS_SPEC.md
    INTERFACES.md
    VALIDATION_GATES.md
    PHYSICAL_TEST_PLAN.md
    AGENT_RULES.md
    KNOWN_ISSUES.md
```

Текущая веточная схема:

```text
master
cad/mk0.1
cad/mk0.2
cad/mk0.3
cad/mk1.0
cad/mk1.1
```

## Правила внесения изменений

Перед изменением конструкции агент должен оценить влияние решения по критериям:

- повышает ли ремонтопригодность;
- повышает ли модульность;
- повышает ли жесткость;
- упрощает ли печать;
- упрощает ли сборку;
- упрощает ли обслуживание;
- позволяет ли масштабировать проект;
- не ломает ли существующий стандарт модулей.

Для каждого существенного изменения агент должен описывать:

- преимущества;
- недостатки;
- влияние на прочность;
- влияние на стоимость;
- влияние на печать;
- влияние на сборку;
- влияние на обслуживание;
- влияние на будущие ревизии.

## Запреты

Запрещено:

- использовать магические числа в CAD-коде;
- менять стабильные ревизии задним числом;
- создавать папки `cad/mk0.1`, `cad/mk0.2` и подобные без отдельного инженерного решения;
- копировать весь CAD-код ради каждой ревизии;
- считать STEP/STL источником истины;
- редактировать документацию старой стабильной ревизии так, будто она была другой;
- смешивать текущую CAD-модель и архив ревизий;
- хранить расчеты только в комментариях к коду без фиксации в `revisions/mkX.Y/`;
- делать корпус, жесткость которого держится только на пластике;
- усложнять извлечение модулей;
- прокладывать кабели вне `Rear Service Spine` без инженерного обоснования;
- нарушать единый стандарт направляющих и креплений;
- смешивать детали, сборку и экспорт в одном файле;
- добавлять декоративные элементы в ущерб обслуживанию, охлаждению или прочности;
- делать изменения без оценки влияния на печать и сборку.

## Формат ответа LLM-агента

При предложении изменений агент должен отвечать структурировано:

```text
## Предложение

## Инженерная логика

## Преимущества

## Недостатки

## Влияние на прочность

## Влияние на печать

## Влияние на сборку

## Влияние на обслуживание

## Влияние на стоимость

## Влияние на будущие ревизии

## Рекомендация
```

Если агент пишет код, он должен:

- сохранять параметрический стиль;
- использовать `config.py`;
- не удалять существующие функции без причины;
- не ломать экспорт STEP/STL;
- по возможности сохранять обратную совместимость;
- явно указывать, какие файлы изменены.

## Промпты для Kimi Agents Swarm

Если агенту нужно подготовить промпт для внешнего multi-agent engineering review в `Kimi Agents Swarm`, он должен использовать инструкцию:

- `docs/KIMI_AGENTS_SWARM_PROMPT_GUIDE.md`

Перед генерацией такого промпта агент должен учитывать существующую структуру ревью проекта, текущие review packages, аналитические CSV и предыдущие `reviews/mkX.Y/agent_outputs/`.

Промпт для `Kimi Agents Swarm` должен требовать строгого инженерного ревью, evidence status (`CONFIRMED`, `LIKELY`, `UNCERTAIN`, `NEEDS TEST`), запрета на выдуманные CFD/FEA/slicing/physical tests и итогового решения `GO FOR FULL PRINT`, `GO FOR PARTIAL TEST PRINT` или `NO-GO UNTIL BLOCKERS ARE FIXED`.

## Главный рабочий контекст

`AGENTS.md` является главным рабочим контекстом для LLM-агентов в проекте `homelab_modular_tower`.

Все будущие LLM-сессии должны учитывать этот файл перед изменением CAD-кода, структуры проекта или документации.
