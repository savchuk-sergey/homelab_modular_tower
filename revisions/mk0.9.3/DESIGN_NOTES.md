# mk0.9.3 Design Notes

PETG is not used as the final sliding surface because long-term PETG-on-metal sliding would wear, bind, and depend too much on print quality. The carriage sides instead hold replaceable POM-C round shoes.

The selected rail is an aluminum U-channel `15 x 10 x 10 x 2 mm`. It is stronger and more repeatable than a printed rail, keeps the load path off fragile printed ledges, and leaves an 11 mm internal channel for the POM-C shoe concept.

POM-C `8 mm` round rod cut into `12 mm` shoes is used as the wear element. Short perpendicular shoes reduce binding from imperfect long printed surfaces and make replacement practical.

The shoe retention concept is mechanical: M3 clamp screw, PETG boss, and heat-set insert geometry. Glue-only retention is not accepted, and the screw must not rely on a thread cut directly into POM-C.

Base and roof are treated as frames, not massive blocks. Their jobs are fan support, filter/guard support, M5 rod corner load transfer, and module interface alignment. Extra plastic is avoided unless it supports stiffness, serviceability, or airflow.

