# Homelab Modular Tower mk0.6

## Цель mk0.6

mk0.6 переводит mk0.5 из компоновочного прототипа в более инженерную эксплуатационную платформу. Ревизия сохраняет философию Mini Blade Tower, но усиливает задний силовой контур, делает базу более устойчивой и печатной, фиксирует единый tray-стандарт и добавляет более явное отображение power/cable management и airflow.

## Отличия от mk0.5

- `rear_service_spine` стал structural backbone: добавлены вертикальные backbone ribs, горизонтальные перемычки по уровням модулей и боковые mounting ears рядом с задним силовым контуром.
- Нижняя база разделена на `central_bottom_fan_frame`, `left_foot_extension`, `right_foot_extension`, `front_stability_wing`, `rear_stability_wing` и отдельные TPU feet.
- В `config.py` добавлены параметры устойчивости, module interface, foot extensions, mass assumptions и review margins.
- Tray-модули проходят через единый стандарт `make_standard_tray_base`, `make_tray_handle`, `make_tray_front_lock`, `make_tray_rear_stop`, `make_tray_cable_exit`, `make_module_rails`.
- Power bus получил крышку, strain relief zones, разделение signal/power и защитные бортики.
- Добавлены review-модели для устойчивости, airflow, blocked zones и printability layout.

## Закрытые проблемы mk0.5

- Скручивание: rear spine теперь механически связывает верх/низ и уровни модулей, а sectional side panels остаются shear elements.
- Rear Service Spine: силовая часть остается на месте при снятии крышки, крышка не является главным несущим элементом.
- Устойчивость: база расширена до параметрического footprint `250 x 260 mm`, высота ножек увеличена до `25 mm`, добавлена `stability_review`.
- Печатаемость базы: большая plate разбита на отдельные детали, совместимые с PETG-печатью на обычном столе.
- Tray стандарт: все существующие trays используют один общий factory path и одинаковую геометрию фиксации/ручки/заднего выхода кабеля.
- Power/cable management: power bus находится в rear spine, имеет крышку, strain relief и разделение cable zones.
- Airflow review: добавлены отдельные review views для общего вертикального потока, Mini PC duct, blocked zones и intake/exhaust clearance.

## Измененные детали

- `rear_service_spine`
- `rear_service_spine_cover`
- `power_bus_panel`
- `power_bus_cover`
- `central_bottom_fan_frame`
- `left_foot_extension`
- `right_foot_extension`
- `front_stability_wing`
- `rear_stability_wing`
- `ups_power_tray`
- `external_ssd_bay`
- `ssd_expansion_tray`
- `raspberry_pi_tray`
- `mikrotik_tray`
- `mini_pc_tray`

## Оценка печатаемости

Основной риск mk0.5 был в большой цельной base stability plate. В mk0.6 assembly использует секционную базу: центральная часть сохраняет 120 mm intake, боковые extensions отвечают за ширину опоры, переднее и заднее крыло отвечают за глубину footprint. Детали остаются плоскими, с ребрами снизу, и должны печататься PETG без цельной детали около `250 x 260 mm`.

## Оценка сборки

Сборка стала более модульной: база собирается винтами, rear spine крепится к силовому контуру, крышки rear spine и power bus снимаются отдельно. Tray-модули сохраняют фронтальное извлечение и получают задний cable exit, rear stop и front lock.

## Оценка жесткости

Жесткость повышается за счет замыкания заднего контура: M5 rods, top/bottom frames, corner blocks, structural rear spine и shear side panels работают как связанная рама. Точная FEA пока не выполнялась, поэтому вывод является инженерной оценкой по геометрии и load path, а не расчетным подтверждением.

## Оценка устойчивости

Footprint задан параметрами `base_width`, `base_depth`, `foot_extension_x`, `foot_extension_y`. Review-модель показывает условный центр масс и сценарий частично выдвинутого Mini PC tray. Оценка не заменяет физический tilt-test с установленными устройствами, особенно при тяжелом UPS.

## Known Limitations

- Нет FEA и нет экспериментального torsion/tilt-test.
- Массы модулей являются оценочными.
- Коннекторы power bus остаются placeholder footprints до выбора точных компонентов.
- Mini PC placeholder требует точных измерений конкретного устройства и его вентиляционных отверстий.
- Cable clamps показывают routing intent, но не являются финальной моделью под конкретные провода и разъемы.

## Next Steps для mk0.7

- Измерить реальные устройства и обновить placeholders.
- Выбрать конкретные DC connectors, fuse blocks и terminal blocks.
- Провести физический print-fit тест секционной базы и tray lock.
- Сделать tilt-test с UPS и частично выдвинутым Mini PC tray.
- Перейти от airflow review geometry к проверке фактических intake/exhaust clearances на конкретных устройствах.
