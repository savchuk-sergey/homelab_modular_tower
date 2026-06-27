# mk0.7 Calculations and Assumptions

## Foot Clearance

- Целевая высота ножек для нижнего intake: 30-35 mm.
- Принятое значение: `FOOT_HEIGHT = 32.0 mm`.
- `BOTTOM_FEET_HEIGHT`, `BOTTOM_AIR_GAP` и `BOTTOM_INTAKE_CLEARANCE` завязаны на это значение.

Инженерная логика: 32 mm сохраняет запас над нижней границей 25 mm и не делает стойку чрезмерно высокой. Физическая проверка потока и устойчивости все еще обязательна.

## Fan Geometry

- Fan envelope: `FAN_120_SIZE = 120.0 mm`.
- Fan thickness: `FAN_120_THICKNESS = 25.0 mm`.
- Mounting pattern: `FAN_120_HOLE_SPACING = 105.0 mm`.
- Screw clearance: `FAN_120_HOLE_DIAMETER = 4.4 mm`.
- Air opening reference: `FAN_120_AIR_OPENING_DIAMETER = 112.0 mm`.

Эти параметры используются и в printable cartridge/filter geometry, и в non-printable fan placeholder.

## Intake Open Area

`BOTTOM_INTAKE_MIN_OPEN_AREA_RATIO = 0.58` зафиксирован как review-порог, а не как CFD-расчет. `bottom_intake_open_area_review` показывает полный reference opening и внутренний minimum marker, чтобы визуально проверять, не превращается ли basement в глухую плиту.

## Raspberry Pi 3B Placeholder

Приняты инженерные reference-размеры:

- board: `85.0 x 56.0 x 1.6 mm`;
- mounting holes: `2.75 mm`;
- component keepout: `15.0 mm`;
- отдельные keepout-зоны для USB/Ethernet, HDMI/power и GPIO.

Эта модель не является фотореалистичной. Ее задача - проверить посадку, mounting pattern и сервисные зоны.

## Limitations

- Airflow review bodies не заменяют CFD.
- Тестовый print-fit нужен для cartridge rails, filter retainer и зазора между вентилятором, столом и central frame.
- Реальные размеры конкретного Raspberry Pi 3B и вентилятора могут потребовать коррекции параметров.
