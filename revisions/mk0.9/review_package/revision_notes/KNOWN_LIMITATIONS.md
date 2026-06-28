# mk0.9 Known Limitations

- Mini PC dimensions are unknown.
- Mini PC tray is not final.
- Airflow duct is not final.
- Rear I/O cutout is not final.
- No power distribution module.
- No DC bus.
- No DC UPS module.
- No router module.
- No full rear service spine.
- No final cable management.
- Airflow is checked geometrically, not by CFD.
- Plastic weight is an estimate from mesh volume and must be verified in slicer.
- PETG estimate is below the hard limit but above the preferred target.
- Matplotlib-based render generation is currently blocked by a local `numpy.linalg.inv` fatal exception in the CAD environment; STEP/STL export and analysis are successful.

