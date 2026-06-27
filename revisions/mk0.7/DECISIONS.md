# mk0.7 Engineering Decisions

## Bottom Intake

Решение: сохранить секционную базу mk0.6, но явно оформить нижнюю центральную зону как airflow frame и добавить отдельный `bottom_fan_cartridge`.

Причина: это сохраняет устойчивость и печатаемость предыдущей ревизии, но делает intake проверяемым и обслуживаемым.

Компромисс: появляется больше деталей и крепежа, зато вентилятор можно обслуживать отдельно.

## Bottom Fan Cartridge

Решение: cartridge расположен под central frame в нижнем воздушном зазоре и использует стандартный 120 mm fan pattern 105 x 105 mm.

Причина: вентилятор не должен требовать разборки башни или снятия модулей.

Компромисс: физически нужно проверить, достаточно ли места для конкретной толщины вентилятора, фильтра и провода.

## Filter Provision

Решение: добавить `bottom_filter_frame` и `bottom_filter_retainer` как опциональную механику, не делая фильтр обязательным элементом airflow path.

Причина: пылевой фильтр полезен для настольного homelab, но его сопротивление потоку нужно проверять отдельно.

## Placeholders

Решение: `fan_120x120x25_placeholder` и `raspberry_pi_3b_placeholder` живут как non-printable reference geometry и экспортируются отдельно.

Причина: реальные устройства не должны смешиваться с печатными деталями, иначе export-пакет становится опасным для подготовки к печати.

## Export Taxonomy

Решение: для revision export используется структура:

```text
exports/mk0.7/
  printable/plastic/
  non_printable/metal_reference/
  placeholders/devices/
  placeholders/fans/
  review/
  assemblies/
```

Причина: печатные детали, metal references, placeholders и review bodies имеют разные назначения и не должны попадать в один поток подготовки к печати.
