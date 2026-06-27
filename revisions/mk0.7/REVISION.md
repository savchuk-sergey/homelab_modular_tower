# Homelab Modular Tower mk0.7

## Цель ревизии

mk0.7 подготавливает конструкцию к первой более реалистичной тестовой печати и сборке. Фокус ревизии: нижний intake, обслуживаемый нижний вентилятор, инженерные placeholders для вентилятора 120 x 120 x 25 mm и Raspberry Pi 3B, а также разделение export-артефактов по типам сущностей.

## Состояние конструкции

- Basement остается секционным и опирается на широкую базу mk0.6, но центральная зона теперь трактуется как `central_bottom_fan_frame` с крупным открытым intake и отдельным `bottom_fan_cartridge`.
- Нижний вентилятор вынесен в обслуживаемый cartridge под центральной рамой, в зоне зазора от стола.
- Ножки подняты до `32 mm`, чтобы нижний intake имел рабочий воздушный зазор.
- Добавлены `bottom_filter_frame` и `bottom_filter_retainer` как базовая механика для будущего пылевого фильтра.
- Добавлен `fan_120x120x25_placeholder` с габаритом 120 x 120 x 25 mm, монтажными отверстиями 105 x 105 mm и keepout volume.
- Добавлен `raspberry_pi_3b_placeholder` с outline платы, монтажными отверстиями и keepout-зонами разъемов.
- Export-структура ревизии разделена на printable, non-printable metal references, placeholders, review bodies и assemblies.

## Airflow Intent

Базовый поток остается вертикальным:

```text
bottom 120 mm intake
-> open central frame
-> vertical module stack flow
-> priority Mini PC duct/review path
-> top 120 mm exhaust
```

Rear Service Spine и Power Bus остаются в задней сервисной зоне и не должны перекрывать центральный вертикальный поток. UPS/power tray сохраняет вентиляцию и не должен превращать нижнюю часть башни в закрытый короб.

## Измененные CAD-области

- `cad/config.py`
- `cad/parts/cooling.py`
- `cad/parts/placeholders.py`
- `cad/parts/review.py`
- `cad/assembly/tower_assembly.py`
- `cad/exporters/part_registry.py`
- `cad/exporters/export_parts.py`
- `cad/exporters/export_assembly.py`
- `cad/export.py`

## Проверка

Проверено:

```powershell
python -m compileall cad
python -m cad.export --revision mk0.7
```

Export создает локальную структуру `exports/mk0.7/`. Папка `exports/` остается generated artifact и не является source of truth.
