# mk0.9.2 Assembly Notes

## Module stack

The generated assembly contains 38 children and keeps the four-module stack:

1. base module
2. RPi/SSD module
3. Mini PC placeholder module
4. roof module

## Rail installation intent

The RPi/SSD and Mini PC placeholder module shells now include printable rail
pocket carriers and rail end stops. The aluminum rails remain non-printed
reference parts.

Expected assembly sequence:

1. Print the active module shells and carriages.
2. Install heat-set inserts in clamp and rail stop locations after confirming
   slicer orientation.
3. Fit aluminum U-channel rails into the printed rail pocket carriers.
4. Insert POM-C shoes into the carriage sockets.
5. Use M3 clamp screws into PETG insert bosses to retain the shoes.
6. Verify each carriage slides without binding before installing devices.

## Service notes

- Carriages remain front-serviceable.
- POM-C shoes are intended to be replaceable.
- The Mini PC module remains placeholder-based until real measurements exist.
