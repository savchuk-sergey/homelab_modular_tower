# Kimi Agent Swarm Prompt Guide

## 1. Назначение документа

Этот guide задает проектный стандарт подготовки промптов для внешнего engineering review в `Kimi Agent Swarm` / `Kimi Agents Swarm`.

Цель документа - сделать swarm полезным инструментом для CAD-ревизий Homelab Modular Tower, а не бесконтрольным чтением всего репозитория. Хороший swarm-запуск должен:

- читать только нужный инженерный срез;
- распределять работу между непересекающимися ролями;
- фиксировать evidence status;
- создавать конкретные review-файлы;
- не изменять CAD без явного разрешения;
- останавливаться после одного финального synthesis pass;
- выдавать actionable findings для следующей CAD-ревизии.

Этот документ не является рекламой возможностей Kimi. Он фиксирует практические правила bounded-review процесса для проекта. Публичные источники подтверждают, что Kimi Code является агентным coding tool с доступом к файлам, shell, web и последовательным выбором действий; официальная документация Kimi для coding-интеграций отдельно предупреждает о росте token usage, retries и риске infinite loops, поэтому для Homelab Modular Tower swarm нужно ограничивать явно. Kimi web UI публично показывает наличие режима `Agent Swarm`, но детальная first-party спецификация поведения swarm может меняться. Все лимиты ниже являются проектными guardrails, а не утверждением о внутренних лимитах Kimi.

Полезные источники для обновления этого guide:

- Kimi Code CLI README: https://github.com/MoonshotAI/kimi-code
- Kimi API coding integrations and usage notes: https://platform.kimi.ai/docs/guide/agent-support
- Kimi web UI feature surface: https://www.kimi.com/en
- Anthropic context engineering article, как общий источник по context pollution и long-horizon agent work: https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents
- Existing project review format: `reviews/mk0.7/engineering_review.md` и `reviews/mk0.7.1/engineering_review.md`

## 2. Когда использовать Kimi Agent Swarm

Использовать swarm имеет смысл, когда параллельные инженерные проверки реально уменьшают риск пропустить проблему:

- ревью большой CAD-ревизии перед печатью;
- сравнение двух ревизий, например `mk0.7` -> `mk0.7.1`;
- анализ пригодности к печати на основе STEP/STL, CSV и manifests;
- проверка модульности и извлечения модулей;
- проверка вертикального airflow, intake/exhaust, Mini PC duct и fan service;
- анализ Rear Service Spine, cable management и Power Bus;
- подготовка review-документа для следующей CAD-ревизии;
- поиск противоречий между `cad/`, `exports/`, `renders/`, `revisions/` и review package;
- независимая проверка blockers после patch revision;
- red-team review перед решением `GO FOR PARTIAL TEST PRINT`.

Swarm особенно полезен, если вход уже ограничен review package:

```text
revisions/{REVISION_ID}/review_package/
revisions/{REVISION_ID}/analysis/
exports/{REVISION_ID}/
reviews/{PREVIOUS_REVISION_ID}/engineering_review.md
```

## 3. Когда НЕ использовать Kimi Agent Swarm

Не использовать swarm для задач, где параллелизм только увеличит шум:

- маленькая правка в одном файле;
- генерация одной CadQuery-детали;
- исправление синтаксиса CadQuery;
- быстрый вопрос по `config.py`;
- локальный баг в export script;
- простое обновление revision note;
- механическое переименование;
- задача, где нужен один исполнитель, а не несколько reviewer-ролей;
- задача, где нужно быстро проверить одну гипотезу;
- задача, где нет готового bounded input scope.

Для таких случаев лучше использовать обычный Codex/LLM-agent workflow: прочитать релевантные файлы, внести маленький patch, запустить проверку, обновить документацию.

## 4. Главные риски Agent Swarm в этом проекте

### Context overload

Swarm может попытаться прочитать весь репозиторий: CAD-код, exports, renders, review packages, старые ревизии, generated artifacts и agent outputs. Это ухудшает качество результата и может привести к падению или потере фокуса.

Правило: не давать запрос "проверь весь проект". Давать список входных путей и порядок чтения.

### Excessive sub-agent spawning

Большое число агентов не означает лучшее ревью. Если 20 агентов читают одни и те же файлы, они расходуют бюджет и дублируют findings.

Правило: обычное ревью - 6 агентов, глубокое ревью - 8-10 агентов, только если роли не пересекаются.

### Duplicated analysis

CAD Integrity Reviewer, Printability Reviewer и Manufacturability Reviewer могут повторять одни и те же замечания о деталях.

Правило: роли должны иметь разные input files, questions и output fields.

### Final review loop

Swarm может после готового отчета начать "еще один final review", затем "final final review" и снова агрегировать уже готовые выводы.

Правило: один final aggregation pass. После создания required output files задача завершена.

### Shallow generic recommendations

Общий совет вроде "improve airflow" бесполезен без связи с concrete file, part, render, module или project constraint.

Правило: generic advice без project-specific evidence удаляется.

### Loss of engineering constraints

Swarm может предложить красивое решение, которое нарушает module standard, Rear Service Spine, low-voltage-only power system или принцип "пластик не единственный силовой элемент".

Правило: каждый агент должен проверять findings against `AGENTS.md`.

### Hallucinated CAD facts

Нельзя утверждать, что выполнены CFD, FEA, slicing или physical testing, если таких артефактов нет.

Правило: evidence status обязателен: `CONFIRMED`, `LIKELY`, `UNCERTAIN`, `NEEDS TEST`.

### Попытки изменить архитектуру без понимания истории ревизий

Swarm может предложить переписать `mk0.1` или копировать `cad/` в папку ревизии.

Правило: история ревизий не переписывается. Новые изменения идут в следующую ревизию.

### Слишком широкий scope

"Full engineering review of everything" почти всегда хуже bounded review.

Правило: задавать `FOCUS_AREAS` и `OUT_OF_SCOPE`.

### Отсутствие критериев остановки

Если не сказать, когда работа завершена, swarm может продолжать проверять и улучшать отчет.

Правило: stop conditions должны быть частью prompt.

## 5. Базовая стратегия промпта

Промпт для swarm должен быть построен сверху вниз:

1. Дать короткий project brief.
2. Зафиксировать revision id и previous revision id.
3. Ограничить scope и input paths.
4. Явно перечислить out of scope.
5. Назначить роли саб-агентов без дублирования.
6. Задать work budget.
7. Задать review criteria и evidence rules.
8. Потребовать конкретные output files.
9. Задать hard stop criteria.
10. Запретить бесконечное повторное ревью.

Нельзя начинать prompt с просьбы "be comprehensive". Для этого проекта лучше формула:

```text
Be strict, bounded, evidence-based, and stop after producing the required files.
```

## 6. Рекомендуемая структура swarm-промпта

Использовать такую структуру:

```text
Mission
Project context
Input files
Scope
Out of scope
Agent roles
Work budget
Review criteria
Evidence rules
Required output files
Stop conditions
Anti-loop rules
Final answer format
```

Каждый блок должен быть коротким и проверяемым. Если prompt становится длинным, лучше убрать второстепенный контекст, а не расширять scope.

## 7. Роли саб-агентов

Роли ниже являются рекомендуемым набором. Не нужно запускать все роли каждый раз.

### CAD Architecture Reviewer

Проверяет:

- соответствие `cad/` правилам проекта;
- параметричность через `config.py`;
- разделение parts, assembly и exporters;
- отсутствие magic numbers;
- соответствие registry/export structure.

Читает:

- `AGENTS.md`;
- `cad/config.py`;
- `cad/assembly/tower_assembly.py`;
- `cad/parts/*.py`;
- `cad/exporters/*.py`;
- `revisions/{REVISION_ID}/REVIEW_INPUTS.md`, если есть.

Не делает:

- не предлагает airflow conclusions без geometry evidence;
- не переписывает CAD;
- не оценивает print supports глубоко.

Output:

```markdown
| Finding ID | File/part | Evidence status | Severity | CAD rule affected | Recommendation |
|---|---|---|---|---|---|
```

### Mechanical Integrity Reviewer

Проверяет:

- load path через M5 rods, rails, top/bottom frames, corner blocks;
- torsion resistance;
- side panel shear path;
- rail fastening;
- tray vertical support;
- tipping risk.

Читает:

- `cad/parts/frame.py`;
- `cad/parts/corner_blocks.py`;
- `cad/parts/rails.py`;
- `cad/parts/rods.py`;
- assembly STEP или review package assembly notes;
- `reviews/{PREVIOUS_REVISION_ID}/engineering_review.md`.

Не делает:

- не выдает FEA как факт;
- не требует металлический каркас там, где проект уже задает M5/rails;
- не меняет module order без обоснования.

Output:

```markdown
| Finding ID | Load path / part | Evidence status | Severity | Failure mode | Next action |
|---|---|---|---|---|---|
```

### Printability Reviewer

Проверяет:

- build volume;
- orientation;
- support risk;
- large flat PETG warp risk;
- minimum printable features;
- split requirements;
- printable/non-printable/placeholders separation.

Читает:

- `revisions/{REVISION_ID}/analysis/printability_check.csv`;
- `revisions/{REVISION_ID}/analysis/part_dimensions.csv`;
- `revisions/{REVISION_ID}/analysis/stl_quality.csv`;
- `exports/{REVISION_ID}/MANIFEST.md`;
- `revisions/{REVISION_ID}/PRINTABLE_PARTS.md`;
- `revisions/{REVISION_ID}/NON_PRINTABLE_PARTS.md`.

Не делает:

- не утверждает slicer result без slicer artifacts;
- не рекомендует декоративные отверстия;
- не смешивает printability with mechanical approval.

Output:

```markdown
| Finding ID | Part | Evidence status | Severity | Print risk | Orientation/support note | Recommendation |
|---|---|---|---|---|---|---|
```

### Airflow Reviewer

Проверяет:

- bottom 120 mm intake;
- top 120 mm exhaust;
- Mini PC priority airflow;
- Mini PC duct realism;
- tray vent blockage;
- filter service;
- fan cable path;
- basement openness and intake obstruction.

Читает:

- `cad/parts/cooling.py`;
- `cad/parts/review.py`;
- `cad/parts/modules.py`;
- airflow review STEP/STL if present;
- renders if present;
- `revisions/{REVISION_ID}/REVIEW_GEOMETRY.md`.

Не делает:

- не заявляет CFD;
- не делает thermal performance claims without test;
- не оценивает electrical safety кроме fan wire routing.

Output:

```markdown
| Finding ID | Airflow zone | Evidence status | Severity | Restriction / risk | Required evidence or fix |
|---|---|---|---|---|---|
```

### Serviceability Reviewer

Проверяет:

- извлечение каждого модуля без разборки башни;
- tray handles and latches;
- access to fans/filter;
- access to screws/nuts;
- side panel removability;
- assembly/disassembly sequence.

Читает:

- assembly notes;
- `cad/parts/carriages.py`;
- `cad/parts/modules.py`;
- `cad/parts/side_panels.py`;
- review package drawings;
- previous review serviceability findings.

Не делает:

- не предлагает заменить весь form factor;
- не игнорирует Rear Service Spine;
- не делает cosmetic suggestions.

Output:

```markdown
| Finding ID | Module / service operation | Evidence status | Severity | Blocked step | Recommendation |
|---|---|---|---|---|---|
```

### Cable Management Reviewer

Проверяет:

- Rear Service Spine capacity;
- cable exits from each module;
- Ethernet/USB/power separation;
- fan cable routing;
- quick disconnect logic;
- strain relief;
- no chaotic cables between modules.

Читает:

- `cad/parts/service_spine.py`;
- `cad/parts/modules.py`;
- `docs/POWER.md`;
- `docs/ARCHITECTURE.md`;
- power bus and spine exports/manifests.

Не делает:

- не проектирует open 220 V inside tower;
- не утверждает electrical compliance без evidence;
- не смешивает cable management с aesthetic cable hiding.

Output:

```markdown
| Finding ID | Cable / connector zone | Evidence status | Severity | Service impact | Recommendation |
|---|---|---|---|---|---|
```

### Revision Consistency Reviewer

Проверяет:

- соответствие docs, review package, exports и CAD;
- не переписана ли старая ревизия;
- все ли generated artifacts относятся к правильному `REVISION_ID`;
- есть ли contradictions between `CHANGELOG`, `DECISIONS`, `KNOWN_ISSUES`, manifests and review outputs.

Читает:

- `revisions/{REVISION_ID}/*.md`;
- `revisions/{REVISION_ID}/review_package/`;
- `exports/{REVISION_ID}/MANIFEST.md`;
- previous review.

Не делает:

- не оценивает geometry deeply;
- не предлагает CAD changes without linking to docs mismatch;
- не исправляет историю ревизий.

Output:

```markdown
| Finding ID | Document/artifact | Evidence status | Severity | Inconsistency | Required update |
|---|---|---|---|---|---|
```

### Cost / Complexity Reviewer

Проверяет:

- material mass;
- print time risk;
- part count;
- hardware complexity;
- assembly operations;
- support-heavy details;
- whether plastic is used where metal should carry load.

Читает:

- `plastic_estimate.csv`;
- `part_dimensions.csv`;
- `docs/BOM.md`;
- printable/non-printable manifests;
- review package exports manifest.

Не делает:

- не оптимизирует ценой rigidity/serviceability;
- не предлагает random thinning;
- не считает price точным без BOM quantities.

Output:

```markdown
| Finding ID | Cost / complexity driver | Evidence status | Severity | Impact | Recommendation |
|---|---|---|---|---|---|
```

### Final Aggregator

Проверяет:

- объединяет findings;
- удаляет дубли;
- назначает severity;
- фиксирует conflicts and unknowns;
- создает required output files.

Читает:

- только outputs саб-агентов;
- top-level project constraints;
- предыдущий review format.

Не делает:

- не перечитывает весь репозиторий;
- не запускает второй final review;
- не добавляет новые unsupported findings;
- не переписывает CAD.

Output:

```text
Required output files are created. Final answer is a short list of file paths and final verdict.
```

## 8. Ограничение объема работы

Правила для любого swarm-промпта:

- не читать весь репозиторий без необходимости;
- сначала читать `AGENTS.md`, `README.md`, revision notes, `cad/config.py`, assembly entrypoint;
- затем читать только релевантные детали;
- если есть review package, начинать с него;
- не запускать больше `MAX_SUB_AGENTS` без явной пользы;
- не делать больше одного final aggregation pass;
- не повторять уже сделанные выводы;
- каждый агент возвращает короткий результат в заданной структуре;
- input paths являются allowlist, а не подсказкой;
- старые ревизии читать только для comparison или regression check;
- generated exports считать evidence, но не source of truth;
- CadQuery source in `cad/` остается главным источником модели;
- при конфликте между STEP/STL и CadQuery фиксировать conflict, не гадать.

Рекомендуемый порядок чтения:

1. `AGENTS.md`
2. `README.md`
3. `revisions/{REVISION_ID}/REVISION.md`
4. `revisions/{REVISION_ID}/CHANGELOG.md`
5. `revisions/{REVISION_ID}/DECISIONS.md`
6. `revisions/{REVISION_ID}/KNOWN_ISSUES.md` или `KNOWN_LIMITATIONS.md`
7. `revisions/{REVISION_ID}/review_package/ASSEMBLY_OVERVIEW.md`
8. `revisions/{REVISION_ID}/review_package/REVIEW_REQUIREMENTS_CHECKLIST.md`
9. `cad/config.py`
10. `cad/assembly/tower_assembly.py`
11. Only relevant `cad/parts/*.py`
12. Relevant analysis CSV
13. Relevant manifests, renders and exports

## 9. Anti-loop rules

Добавлять эти правила в каждый serious swarm prompt:

```text
Do not perform more than one final aggregation pass.
After producing the required output files, stop.
Do not start a second final review loop.
If information is missing, record it in Unknowns instead of launching another analysis cycle.
Do not re-read the whole repository after sub-agent outputs are collected.
Do not modify CAD files unless explicitly allowed.
Every finding must reference a concrete file, part, render, module, or project constraint.
Generic advice without project-specific evidence must be discarded.
If two agents disagree, record the conflict and make a bounded recommendation; do not continue negotiation loops.
Do not improve the final document indefinitely.
Do not rewrite the whole review after every minor note.
The task is complete when the required output files exist and the final answer lists them.
```

Если swarm не имеет возможности реально создавать файлы, он должен вывести file contents in separate fenced blocks with exact target paths. Но предпочтительный режим - file output.

## 10. Формат результата

Swarm должен выдавать не просто chat answer, а файлы:

```text
revisions/{REVISION_ID}/review/kimi_swarm_review.md
revisions/{REVISION_ID}/review/kimi_swarm_findings.csv
revisions/{REVISION_ID}/review/kimi_swarm_action_plan.md
revisions/{REVISION_ID}/review/kimi_swarm_unknowns.md
```

Назначение файлов:

- `kimi_swarm_review.md` - итоговый инженерный отчет с verdict, scope, evidence status, blockers, domain findings, risk register, Go/No-Go.
- `kimi_swarm_findings.csv` - машинно-читаемая таблица findings для сортировки, фильтрации и передачи Codex.
- `kimi_swarm_action_plan.md` - compact next-revision plan: что исправлять, в каком порядке, какие файлы вероятно менять, какие acceptance criteria.
- `kimi_swarm_unknowns.md` - отдельный список отсутствующих данных, assumptions and required tests. Unknowns не должны запускать новый analysis loop.

Минимальные CSV columns:

```csv
id,severity,evidence_status,domain,file_or_artifact,part_or_module,finding,impact,recommendation,next_revision_candidate
```

## 11. Severity model

Использовать уровни:

- `BLOCKER` - нельзя печатать, использовать или считать ревизию build-ready.
- `HIGH` - серьезный инженерный риск, который нужно исправить до full print или hardware ordering.
- `MEDIUM` - желательно исправить до следующей ревизии, но можно планировать как patch.
- `LOW` - улучшение, polish или локальное снижение риска.
- `INFO` - наблюдение, evidence note, useful context.

Связь с Go/No-Go:

- любой unresolved `BLOCKER` обычно ведет к `NO-GO UNTIL BLOCKERS ARE FIXED`;
- несколько `HIGH` по structural, power или serviceability могут тоже вести к `NO-GO`;
- `GO FOR PARTIAL TEST PRINT` допустим, если blockers нет или test print прямо предназначен для проверки isolated blocker-free subset;
- `GO FOR FULL PRINT` допустим только при отсутствии blockers and major unresolved risks.

Evidence status:

- `CONFIRMED` - напрямую подтвержден кодом, CSV, экспортом, измерением или документацией.
- `LIKELY` - сильно следует из доступной геометрии, кода или инженерной практики, но не измерен напрямую.
- `UNCERTAIN` - возможно, но данных недостаточно.
- `NEEDS TEST` - требуется physical print, slicer validation, airflow test, FEA, CFD, electrical validation или дополнительный script.

## 12. Engineering review checklist

Swarm должен проверить:

- модульность;
- ремонтопригодность;
- жесткость;
- устойчивость к скручиванию;
- риск опрокидывания;
- cooling priority: Mini PC first;
- вертикальный airflow path;
- bottom 120 mm intake;
- top 120 mm exhaust;
- compatibility with 120 x 120 x 25 mm fan placeholder;
- Mini PC duct and bypass leakage;
- basement openness and intake blockage;
- Rear Service Spine;
- cable management;
- fan cable routing;
- силовая DC-шина;
- no open 220 V inside printed tower;
- fuse, switch, connector and strain relief placeholders;
- пригодность к печати;
- part orientation;
- supports;
- Bambu Lab P2S build volume or active printer limit if changed;
- large flat PETG warp risk;
- расход пластика;
- print time risk;
- стандартизация направляющих;
- module handle/latch consistency;
- module extraction without disassembling tower;
- separation of printable, non-printable, placeholders and review geometry;
- revision documentation consistency;
- возможность развития ревизий.

## 13. Готовый master prompt template

Скопировать и заполнить:

```text
Mission
You are running a bounded Kimi Agent Swarm engineering review for the Homelab Modular Tower CAD project.

Revision under review: {REVISION_ID}
Previous revision: {PREVIOUS_REVISION_ID}
Project root: {PROJECT_ROOT}

This is an engineering review, not a visual/design compliment.
Your job is to produce bounded, evidence-based review files for Codex handoff.

Project context
Homelab Modular Tower is a parametric CadQuery mini blade tower for homelab hardware.
CAD source of truth: CadQuery code in cad/.
Derived artifacts: exports/, renders/, review package files.
Stable revision history must not be rewritten.
Current module order from bottom to top:
1. UPS / Power Distribution
2. External SSD Bay
3. SSD / Expansion
4. Raspberry Pi
5. MikroTik hAP ax2
6. Mini PC

Hard project constraints
- PETG is the main printed material; PLA is for prototypes; TPU is for feet/dampers/retainers.
- Plastic must not be the only structural system.
- Main stiffness must come from M5 rods, metal rails, top/bottom structural frames, and reinforced corner blocks.
- Every module must be removable without disassembling the whole tower.
- All cables must route through Rear Service Spine unless a specific engineering exception is documented.
- Internal power is DC only. Do not introduce exposed 220 V AC inside the case.
- Bottom 120 mm fan is intake. Top 120 mm fan is exhaust.
- Mini PC cooling has priority over the rest of the system.
- All dimensions must come from config.py.
- Do not use magic numbers.
- Do not mix part generation, assembly generation and export logic.
- Do not rewrite old revision history.

Input files
Read only these paths unless a listed file explicitly points to a directly relevant child artifact:
{INPUT_PATHS}

Focus areas
{FOCUS_AREAS}

Scope
- Review the engineering state of {REVISION_ID}.
- Use {PREVIOUS_REVISION_ID} only for regression comparison.
- Produce actionable findings for the next CAD revision.
- Use existing project review style where useful.

Out of scope
- Do not redesign the whole tower.
- Do not modify CAD files unless explicitly allowed.
- Do not create a new revision.
- Do not edit old revision notes.
- Do not claim CFD, FEA, slicer validation, electrical validation or physical testing unless provided as input artifacts.
- Do not read the whole repository.
- Do not optimize aesthetics.
- Do not recommend decorative holes without engineering purpose.
{DO_NOT_TOUCH}

Agent roles
Use at most {MAX_SUB_AGENTS} sub-agents.
Use only roles that are relevant to the focus areas.
Allowed roles:
- CAD Architecture Reviewer
- Mechanical Integrity Reviewer
- Printability Reviewer
- Airflow Reviewer
- Serviceability Reviewer
- Cable Management Reviewer
- Revision Consistency Reviewer
- Cost / Complexity Reviewer
- Final Aggregator

Work budget
- MAX_SUB_AGENTS: {MAX_SUB_AGENTS}
- MAX_REVIEW_PASSES: {MAX_REVIEW_PASSES}
- MAX_FINAL_AGGREGATION_PASSES: 1
- TIME_BUDGET_HINT: {TIME_BUDGET_HINT}
- Each reviewer returns a concise structured result.
- Final Aggregator performs exactly one synthesis pass.

Evidence rules
Every finding must use one evidence status:
- CONFIRMED: directly supported by CAD source, CSV, export, measurement or documentation.
- LIKELY: strong engineering inference, not directly measured.
- UNCERTAIN: plausible but insufficient data.
- NEEDS TEST: requires slicer, physical print, airflow test, FEA, CFD, electrical validation or additional script.

Every finding must reference at least one concrete file, part, render, module, export, CSV row, or project constraint.
Generic advice without project-specific evidence must be discarded.
If information is missing, record it in Unknowns instead of launching another analysis cycle.

Review criteria
- modularity
- serviceability
- structural stiffness and torsion resistance
- tipping risk
- printability
- airflow path
- bottom intake and top exhaust
- Mini PC airflow priority
- Rear Service Spine and cable management
- DC power bus safety
- printable / non-printable / placeholder separation
- revision consistency
- cost and complexity
- future revision scalability

Known issues
{KNOWN_ISSUES}

Required output files
Create files under:
{OUTPUT_PATH}

Required files:
1. kimi_swarm_review.md
2. kimi_swarm_findings.csv
3. kimi_swarm_action_plan.md
4. kimi_swarm_unknowns.md

Required verdict
The final verdict must be exactly one of:
- GO FOR FULL PRINT
- GO FOR PARTIAL TEST PRINT
- NO-GO UNTIL BLOCKERS ARE FIXED

Stop conditions
Do not perform more than one final aggregation pass.
After producing the required output files, stop.
Do not start a second final review loop.
Do not re-read the whole repository after sub-agent outputs are collected.
If two agents disagree, record the conflict and bounded recommendation; do not continue negotiation loops.
Do not improve the final document indefinitely.
Do not rewrite the whole review after every minor note.

Final answer format
Return only:
- created/updated file paths;
- final verdict;
- count of findings by severity;
- list of unresolved unknowns count;
- confirmation that CAD files were not modified unless explicit mutation permission was provided.
```

## 14. Prompt variants

### Короткое ревью одной ревизии

```text
Run a bounded review of {REVISION_ID}.
Use max 5 sub-agents: CAD Architecture, Printability, Airflow, Serviceability, Final Aggregator.
Read only: AGENTS.md, README.md, revisions/{REVISION_ID}/, revisions/{REVISION_ID}/review_package/, reviews/{PREVIOUS_REVISION_ID}/engineering_review.md.
Do not modify CAD.
Create only revisions/{REVISION_ID}/review/kimi_swarm_review.md and kimi_swarm_findings.csv.
One final aggregation pass only. Stop after files are created.
```

### Глубокое инженерное ревью

```text
Run a deep but bounded engineering review of {REVISION_ID}.
Use max 10 sub-agents.
Include structural, printability, airflow, serviceability, cable management, cost/complexity and revision consistency.
Use analysis CSV as evidence where available.
No CFD/FEA/slicer/physical-test claims unless artifacts are provided.
Create review, findings CSV, action plan and unknowns.
One final aggregation pass only.
```

### Сравнение двух ревизий

```text
Compare {PREVIOUS_REVISION_ID} and {REVISION_ID}.
Focus only on regressions, fixed blockers, new blockers and changed risk level.
Read previous engineering review and current revision package.
Do not re-review unchanged areas unless needed to confirm a regression.
Output: kimi_swarm_revision_comparison.md, kimi_swarm_findings.csv, kimi_swarm_action_plan.md.
Stop after one aggregation pass.
```

### Ревью пригодности к печати

```text
Review printability of {REVISION_ID}.
Use max 5 agents: Printability, Cost/Complexity, CAD Architecture, Revision Consistency, Final Aggregator.
Focus on build volume, supports, part splitting, material classification, STL quality, warp risk, orientation and printable/non-printable separation.
Do not make mechanical approval claims beyond printability evidence.
No slicer claims unless slicer artifacts are provided.
```

### Ревью охлаждения

```text
Review airflow and cooling of {REVISION_ID}.
Use max 6 agents: Airflow, Serviceability, Cable Management, Mechanical Integrity, Revision Consistency, Final Aggregator.
Focus on bottom intake, top exhaust, 120 mm fan placeholders, Mini PC duct, blocked tray vents, Rear Service Spine interference, fan cable routing and filter service.
Do not claim CFD or thermal performance without test artifacts.
Output unknowns separately.
```

### Ревью перед подготовкой новой версии для Codex

```text
Create a Kimi to Codex handoff for the next revision after {REVISION_ID}.
Do not modify CAD.
Convert findings into implementation tasks with likely files to modify, forbidden changes, acceptance criteria and verification commands.
Output only kimi_swarm_action_plan.md and kimi_swarm_unknowns.md.
Stop after files are created.
```

### Ревью только по render/exports без изменения CAD

```text
Review only provided renders and exports for {REVISION_ID}.
Do not inspect or modify CAD source unless a concrete contradiction requires checking config.py or assembly.
Mark all geometry conclusions as LIKELY or UNCERTAIN unless directly measurable from provided artifacts.
Do not infer hidden CAD intent from images.
Output review and unknowns only.
```

## 15. Промпт для safe bounded review

```text
Mission
Run a safe bounded engineering review of Homelab Modular Tower revision {REVISION_ID}.

Hard limits
- Use maximum 5-8 sub-agents.
- Perform only one final aggregation pass.
- Read only the directories listed in INPUT_PATHS.
- Do not modify CAD files.
- Do not modify config.py, assembly files, part files, exports or renders.
- Do not create a new revision.
- Result must be written only to review files under {OUTPUT_PATH}.
- Unknowns must be recorded separately.
- After creating the required output files, stop.

INPUT_PATHS
{INPUT_PATHS}

FOCUS_AREAS
{FOCUS_AREAS}

Required files
- {OUTPUT_PATH}/kimi_swarm_review.md
- {OUTPUT_PATH}/kimi_swarm_findings.csv
- {OUTPUT_PATH}/kimi_swarm_action_plan.md
- {OUTPUT_PATH}/kimi_swarm_unknowns.md

Evidence and anti-loop rules
- Every finding must reference a concrete file, part, render, module or project constraint.
- Generic advice without project-specific evidence must be discarded.
- Do not perform more than one final aggregation pass.
- Do not start a second final review loop.
- If information is missing, record it in Unknowns instead of launching another analysis cycle.
- Do not re-read the whole repository after sub-agent outputs are collected.
- After producing the required output files, stop.
```

## 16. Промпт для Kimi -> Codex handoff

```text
Mission
Create a bounded handoff document from Kimi Swarm review to Codex implementation.

Important
Kimi Swarm is the external engineering reviewer.
Codex is the implementation agent.
Do not write CAD code.
Do not modify CAD files.
Do not create a new revision.

Input
- Review findings: {INPUT_PATHS}
- Revision under review: {REVISION_ID}
- Previous revision: {PREVIOUS_REVISION_ID}

Output file
Create:
{OUTPUT_PATH}/kimi_to_codex_handoff.md

Required sections
1. Summary verdict
2. Findings selected for next revision
3. Engineering decisions to preserve
4. Project constraints that must not be violated
5. Implementation tasks for Codex
6. Files likely to modify
7. Forbidden changes
8. Acceptance criteria
9. Test/render/export commands
10. Expected output files
11. Unknowns that Codex must not guess

Task format
For each task include:
- ID
- Severity addressed
- Why it matters
- Likely files
- CAD constraints
- Documentation updates
- Verification command
- Acceptance criteria

Stop
After producing kimi_to_codex_handoff.md, stop.
Do not start another review loop.
```

## 17. Чеклист перед запуском Kimi Swarm

Проверить:

- указана ревизия;
- указан previous revision, если нужен diff/regression review;
- указан scope;
- указаны input paths;
- указан output path;
- задан лимит саб-агентов;
- задан максимум review passes;
- задан максимум final aggregation passes;
- запрещен бесконечный final review;
- указаны known issues;
- указано, можно ли менять файлы;
- если mutation не нужна, явно написано `Do not modify CAD files`;
- указаны required output files;
- задан severity model;
- задан evidence status;
- запрещены fake CFD/FEA/slicer/physical-test claims;
- перечислены focus areas;
- указаны out-of-scope areas;
- есть stop condition: `After producing the required output files, stop`.

## 18. Чеклист после запуска Kimi Swarm

Проверить:

- создан `kimi_swarm_review.md`;
- создан `kimi_swarm_findings.csv`;
- создан `kimi_swarm_action_plan.md`;
- создан `kimi_swarm_unknowns.md` при наличии unknowns;
- нет общих советов без привязки к CAD;
- у каждого finding есть severity;
- у каждого finding есть evidence status;
- у каждого finding есть file/part/module/render/constraint;
- нет заявлений о CFD/FEA/slicer/physical tests без артефактов;
- есть concrete next actions;
- есть final verdict;
- вывод можно передать Codex;
- история ревизий не нарушена;
- старые revision notes не переписаны;
- CAD-файлы не изменялись, если запуск был review-only.

## 19. Рекомендуемый workflow

Pipeline:

1. Codex готовит ревизию.
2. Codex генерирует exports/renders/review package.
3. Codex запускает или подготавливает bounded Kimi Swarm prompt.
4. Kimi Swarm делает bounded review.
5. Результат сохраняется в `revisions/{REVISION_ID}/review/`.
6. Kimi Swarm создает handoff document для Codex.
7. Codex читает findings/action_plan/unknowns.
8. Codex создает следующую ревизию или patch branch.
9. Codex вносит изменения в `cad/` и revision docs.
10. Codex обновляет exports/renders/review package при необходимости.
11. Изменения фиксируются в git.
12. Старые ревизии не переписываются.

## 20. Practical rules for this project

Проектные правила:

- не просить swarm "проверь весь проект";
- всегда задавать ревизию;
- всегда задавать список файлов/папок;
- всегда требовать output files;
- всегда задавать stop condition;
- не смешивать CAD-генерацию и ревью в одном swarm-запуске;
- для airflow не требовать полноценный CFD, если нет сетки/симулятора;
- для прочности не выдавать FEA как факт, если расчета не было;
- для printability требовать конкретику по orientation, supports, build volume and part dimensions;
- не менять `mk0.1` или старые revision notes задним числом;
- не переносить changes в `master` вне PR-process;
- не считать STEP/STL source of truth;
- не рекомендовать plastic-only load path;
- не ломать Rear Service Spine как обязательную cable-routing зону;
- не предлагать хаотичную прокладку кабелей между модулями;
- не нарушать единый module standard;
- не добавлять декоративные элементы в ущерб serviceability, cooling или stiffness.

## 21. Recommended defaults for Homelab Modular Tower

Использовать по умолчанию:

```text
MAX_SUB_AGENTS: 6 for normal review
MAX_SUB_AGENTS_DEEP_REVIEW: 8-10
MAX_REVIEW_PASSES: 1
MAX_FINAL_AGGREGATION_PASSES: 1
DEFAULT_OUTPUT_PATH: revisions/{REVISION_ID}/review/
DEFAULT_MODE: bounded review
DEFAULT_MUTATION_POLICY: no CAD modifications during review
DEFAULT_UNKNOWN_POLICY: record unknowns, do not loop
DEFAULT_VERDICT_SET: GO FOR FULL PRINT / GO FOR PARTIAL TEST PRINT / NO-GO UNTIL BLOCKERS ARE FIXED
DEFAULT_EVIDENCE_SET: CONFIRMED / LIKELY / UNCERTAIN / NEEDS TEST
```

Default roles for normal review:

1. CAD Architecture Reviewer
2. Mechanical Integrity Reviewer
3. Printability Reviewer
4. Airflow Reviewer
5. Serviceability / Cable Management Reviewer
6. Final Aggregator

Default roles for deep review:

1. CAD Architecture Reviewer
2. Mechanical Integrity Reviewer
3. Printability Reviewer
4. Airflow Reviewer
5. Serviceability Reviewer
6. Cable Management Reviewer
7. Revision Consistency Reviewer
8. Cost / Complexity Reviewer
9. Red Team / Critic Reviewer, if needed
10. Final Aggregator

## 22. Bad prompt examples

Bad:

```text
Проверь весь проект и скажи что не так.
```

Почему плохо: нет revision id, scope, input paths, output files, stop condition.

Bad:

```text
Сделай полное инженерное ревью и улучши всё.
```

Почему плохо: смешивает review и implementation, провоцирует unbounded redesign.

Bad:

```text
Запусти всех агентов и найди все проблемы.
```

Почему плохо: excessive sub-agent spawning, duplicated analysis, no budget.

Bad:

```text
Проведи финальное ревью до идеального результата.
```

Почему плохо: прямое приглашение к final review loop.

Bad:

```text
Сделай CFD и FEA по картинкам.
```

Почему плохо: требует неподтвержденные симуляции без solver, mesh, loads and boundary conditions.

## 23. Good prompt examples

Good:

```text
Review revision mk0.7.1 only.
Read AGENTS.md, revisions/mk0.7.1/review_package/, reviews/mk0.7/engineering_review.md and cad/config.py.
Use max 6 sub-agents.
Focus on airflow, Rear Service Spine, module extraction and printability.
Do not modify CAD.
Create review files under revisions/mk0.7.1/review/.
One final aggregation pass only.
After producing required files, stop.
```

Good:

```text
Compare mk0.7 to mk0.7.1.
Do not perform a full fresh review.
Identify fixed blockers, new regressions and unchanged blockers.
Use previous review and current review package as evidence.
Output findings CSV and action plan.
Record unknowns separately.
```

Good:

```text
Run printability-only review for mk0.7.1.
Use printability_check.csv, part_dimensions.csv, stl_quality.csv, MANIFEST.md, PRINTABLE_PARTS.md and NON_PRINTABLE_PARTS.md.
Do not claim slicer validation.
Every finding must name a part and evidence source.
Stop after one aggregation pass.
```

Good:

```text
Create a Codex handoff from Kimi findings.
Do not write CAD code.
Convert only BLOCKER and HIGH findings into implementation tasks.
Include likely files, forbidden changes, acceptance criteria and verification commands.
Create kimi_to_codex_handoff.md and stop.
```

## 24. Minimal example for mk0.7.1 airflow bounded review

Use this prompt when reviewing the airflow/serviceability slice of `mk0.7.1`.

```text
Mission
Run a safe bounded Kimi Agent Swarm review for Homelab Modular Tower revision mk0.7.1.

Project root
C:\Users\ghery\Documents\homelab_modular_tower

Revision under review
mk0.7.1

Previous revision
mk0.7

Mode
bounded review

Focus areas
- airflow path
- bottom 120 x 120 intake fan placeholder
- top 120 x 120 exhaust fan placeholder
- separation of printable and non-printable parts
- Raspberry Pi 3B placeholder clearance and airflow impact
- Rear Service Spine cable path and airflow interference
- module extraction without full tower disassembly
- basement openness: verify that basement is not a blind closed box and does not block bottom intake

Input paths
- AGENTS.md
- README.md
- docs/ARCHITECTURE.md
- docs/POWER.md
- docs/PRINTING.md
- revisions/mk0.7.1/REVISION.md
- revisions/mk0.7.1/DECISIONS.md
- revisions/mk0.7.1/CHANGELOG.md
- revisions/mk0.7.1/KNOWN_LIMITATIONS.md
- revisions/mk0.7.1/REVIEW_GEOMETRY.md
- revisions/mk0.7.1/PRINTABLE_PARTS.md
- revisions/mk0.7.1/NON_PRINTABLE_PARTS.md
- revisions/mk0.7.1/PLACEHOLDERS.md
- revisions/mk0.7.1/review_package/ASSEMBLY_OVERVIEW.md
- revisions/mk0.7.1/review_package/REVIEW_REQUIREMENTS_CHECKLIST.md
- revisions/mk0.7.1/review_package/analysis/part_dimensions.csv
- revisions/mk0.7.1/review_package/analysis/printability_check.csv
- revisions/mk0.7.1/review_package/analysis/stl_quality.csv
- revisions/mk0.7.1/review_package/exports/MANIFEST.md
- reviews/mk0.7/engineering_review.md
- cad/config.py
- cad/assembly/tower_assembly.py
- cad/parts/cooling.py
- cad/parts/review.py
- cad/parts/modules.py
- cad/parts/service_spine.py
- cad/parts/carriages.py

Out of scope
- Do not modify CAD files.
- Do not modify config.py.
- Do not create mk0.7.2 or any new revision.
- Do not edit existing revision notes.
- Do not perform full project review.
- Do not claim CFD, FEA, slicer validation or physical testing.
- Do not re-read the whole repository.

Agent roles
Use max 6 sub-agents:
1. Airflow Reviewer
2. Serviceability Reviewer
3. Cable Management Reviewer
4. Printability Boundary Reviewer
5. Revision Consistency Reviewer
6. Final Aggregator

Required checks
- Confirm whether bottom intake has a real open path through basement into module stack.
- Confirm whether bottom fan placeholder is 120 x 120 class and whether intake is blocked by basement geometry.
- Confirm whether top fan placeholder/exhaust path exists and whether top clearance is constrained.
- Check whether printed and non-printed parts are separated in manifests.
- Check Raspberry Pi 3B placeholder as a real airflow obstacle, not as a heat model.
- Check Rear Service Spine for cable path, fan wire path and airflow interference.
- Check whether modules can be extracted without removing rear cable ties/covers.
- Record missing evidence as unknowns.

Required output path
revisions/mk0.7.1/review/

Required output files
- kimi_swarm_review.md
- kimi_swarm_findings.csv
- kimi_swarm_action_plan.md
- kimi_swarm_unknowns.md

Evidence rules
Use CONFIRMED, LIKELY, UNCERTAIN or NEEDS TEST.
Every finding must reference a concrete file, part, module, export, CSV row or project constraint.
Generic advice without project-specific evidence must be discarded.

Anti-loop rules
Do not perform more than one final aggregation pass.
After producing the required output files, stop.
Do not start a second final review loop.
If information is missing, record it in Unknowns instead of launching another analysis cycle.
Do not re-read the whole repository after sub-agent outputs are collected.
Do not modify CAD files unless explicitly allowed.

Final answer
Return only output file paths, final verdict, severity counts and confirmation that CAD files were not modified.
```

## 25. Existing review compatibility

Если задача просит полный engineering review, использовать существующую структуру проекта как основу. Базовый ориентир:

- `reviews/mk0.7/engineering_review.md`
- `reviews/mk0.7.1/engineering_review.md`

Типовая структура:

1. Executive Summary
2. Reviewed Inputs
3. Evidence Status Legend
4. Requirements Checklist
5. Consolidated Blockers
6. Domain Findings
7. Risk Register
8. Recommended Changes for Next Revision
9. Physical Tests Required
10. Go / No-Go Decision
11. Appendix: Measurements and Evidence

Не нужно создавать новый стиль отчета, если старый подходит. Улучшать формат можно только ради evidence clarity, CSV compatibility или clearer handoff to Codex.

## 26. Analytical CSV as evidence

Если доступны CSV, prompt должен требовать использовать их:

- `part_dimensions.csv`;
- `plastic_estimate.csv` или `part_volume.csv`;
- `printability_check.csv`;
- `stl_quality.csv`;
- `duplicate_geometry_check.csv`;
- export classification / manifest tables.

Обязательная формулировка:

```text
Use provided CSV data where available.
If CSV data is unavailable, mark all mass, volume, dimension and printability claims as LIKELY, UNCERTAIN or NEEDS TEST.
Do not invent measurements.
Reference CSV rows or filenames in Appendix: Measurements and Evidence.
```

## 27. Plastic efficiency rules

Если focus включает plastic efficiency, запретить decorative perforation:

```text
Do not recommend random decorative perforation.
Every cutout, slot, rib, pocket, window, shell reduction, or segmentation must have a clear engineering reason:
- lower mass;
- lower print time;
- lower material use;
- better airflow;
- better fastener access;
- fewer supports;
- preserved stiffness with less material.
```

Проверять:

- самые тяжелые детали по CSV;
- детали с избыточной толщиной;
- массивные блоки, которые можно заменить ребрами;
- панели, где возможны функциональные окна;
- каретки/лотки, где возможны shell reductions;
- зоны, где металл уже несет нагрузку;
- duplicate exported geometry;
- support-heavy детали;
- cutouts that improve airflow;
- cutouts that create bypass leakage.

## 28. Go / No-Go decision

Итоговое решение должно быть строго одним из:

- `GO FOR FULL PRINT`
- `GO FOR PARTIAL TEST PRINT`
- `NO-GO UNTIL BLOCKERS ARE FIXED`

Правила:

- `GO FOR FULL PRINT` - только если нет blockers and major unresolved printability/assembly risks.
- `GO FOR PARTIAL TEST PRINT` - если ревизия перспективна, но требует целевых проверок.
- `NO-GO UNTIL BLOCKERS ARE FIXED` - если есть critical CAD, printability, structural, airflow, power or serviceability blockers.

## 29. Codex integration note

Kimi Swarm используется как внешний инженерный ревьюер.

Codex используется как исполнитель изменений.

Для review-only задач Kimi не должен напрямую менять CAD, `config.py`, assembly, parts, exports или renders.

Codex должен читать результаты Kimi из:

```text
revisions/{REVISION_ID}/review/
```

Следующая ревизия создается только после анализа:

- `kimi_swarm_review.md`;
- `kimi_swarm_findings.csv`;
- `kimi_swarm_action_plan.md`;
- `kimi_swarm_unknowns.md`;
- optional `kimi_to_codex_handoff.md`.

Codex не должен слепо выполнять все рекомендации Kimi. Он должен проверить findings against `AGENTS.md`, текущий CAD-код, revision docs, constraints and actual verification commands.
