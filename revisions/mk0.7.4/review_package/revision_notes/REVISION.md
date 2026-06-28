# mk0.7.4 Revision

## Purpose

mk0.7.4 is a draft print-readiness revision based on the mk0.7.3 Kimi Agents Swarm review.

The target is to move from `GO FOR COUPON TEST PRINT ONLY` toward `GO FOR ROUGH MOCKUP PRINT` by fixing confirmed impossible geometry, closing high-risk assembly gaps, reducing rough mockup waste, and documenting the build path.

## Scope

- Fix confirmed geometry blockers from mk0.7.3 review.
- Improve side panel, rail, and split-joint interfaces enough for coupon validation.
- Add coupon, BOM, assembly, and print planning documents for a human mockup build.
- Export small coupon geometry before committing to large mockup prints.
- Keep device envelopes, power electronics, thermal validation, and final connector details as non-final placeholders.

## Non-Goals

- Final Mini PC duct against measured device ports.
- Final UPS, Raspberry Pi, MikroTik, SSD, battery, or connector dimensions.
- Final power bus electrical sizing or safety sign-off.
- CFD, FEA, slicer, or physical-test claims without external evidence.
- Production-ready BOM or final side-panel shear-transfer architecture.

## Initial State

mk0.7.4 starts from mk0.7.3 CAD with only the revision identifier and documentation scaffold changed before geometry work.
