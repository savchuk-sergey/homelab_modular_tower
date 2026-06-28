# mk0.9.3 Printing Notes

Use `exports/mk0.9.3/PRINT_MANIFEST.md` as the print selection guide after running:

```text
python -m cad.export --revision mk0.9.3
```

Print module-level prototype parts first: `base_module`, `rpi_ssd_module`, `mini_pc_placeholder_module`, `roof_module`, and TPU `foot`.

Do not print aluminum rail, POM-C shoes, M5 rods, fans, filters, or device placeholders as functional printed parts. These are reference or purchased parts.

Mass targets remain unverified by slicer:

- base module target: 180-240 g PETG, desired height 45-55 mm;
- roof module target: 150-220 g PETG, desired height 40-55 mm.

Current mesh-only estimates from `analysis/plastic_estimate.csv`:

- `base_module`: about 249.7 g PETG, exported height about 58 mm including attached lower features;
- `roof_module`: about 245.9 g PETG, exported height about 49 mm.

These values are still above the desired mass ranges and must be treated as review findings for the next lightening pass.

CadQuery export does not replace slicer validation. Slicer checks are required for mass, supports, orientation, perimeters, insert bosses, and bridge quality.
