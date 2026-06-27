# mk0.7 Known Issues

- Нет CFD и нет физической проверки расхода воздуха.
- `BOTTOM_INTAKE_MIN_OPEN_AREA_RATIO` является инженерным review-порогом, а не расчетом по кривой вентилятора.
- `bottom_fan_cartridge` требует print-fit проверки с реальным вентилятором 120 x 120 x 25 mm.
- Filter frame/retainer пока не привязаны к конкретному материалу фильтра и толщине сетки.
- Реальный routing провода вентилятора в Rear Service Spine пока не детализирован.
- Raspberry Pi 3B placeholder использует инженерные reference-объемы и должен быть сверян с конкретной платой/радиатором.
- Mini PC duct остается review/placeholder-level геометрией и требует проверки по реальным отверстиям Mini PC.
- Generated exports находятся в `exports/`, который игнорируется Git; source of truth остается в `cad/` и документации ревизии.
