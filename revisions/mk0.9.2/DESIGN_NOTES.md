# mk0.9.2 Design Notes

## Rail/carriage intent

The active module standard remains an aluminum U-channel rail with replaceable
POM-C round shoes. PETG is used for positioning, sockets, bosses, rail pocket
carriers, and service features. It is not intended to be the wear surface.

## Clamp correction

The mk0.9.1 clamp failed because a chamfer was applied to a small unioned
bridge/lip solid. `mk0.9.2` replaces that with a simpler printable bridge,
overlap lip, and explicit heat-set insert boss. The M3 screw path is still in
PETG; it does not thread into the POM-C shoe.

## Rail pocket correction

The mk0.9.1 assembly showed separate aluminum rail placeholders, but the active
module shells did not expose a printable rail receiving feature. `mk0.9.2`
adds side rail pocket carriers and rail end stops to both active payload
module shells.

## Airflow

The open-frame carriages and central airflow placeholder remain present. Render
evidence was generated, but no CFD, fan curve calculation, thermal test, or
smoke test was performed.

## Weight

Mesh volume estimates are lower than slicer material usage and do not include
infill, walls, supports, purge, or print settings. The rail pocket carriers add
mass versus the mk0.9.1 intent, so mk0.9.2 should be reviewed for weight before
any full print.
