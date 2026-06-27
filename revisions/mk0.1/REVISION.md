# Homelab Modular Tower CAD Revision mk0.1

Date: 2026-06-27

## Purpose

mk0.1 freezes the current Homelab Modular Tower as the first engineering CAD revision. This revision is a historical checkpoint for the project and should not be changed retroactively.

The goal of mk0.1 is to preserve the first working parametric CadQuery model with visible structural intent, modular trays, service spine, DC power placeholder, airflow placeholder, generated exports, and generated projection renders.

## Current Architecture

Homelab Modular Tower mk0.1 is a compact PETG mini-blade tower prototype for home homelab infrastructure. The design uses a printed modular frame with metal structural placeholders and removable trays.

Architecture elements:

- PETG printed structural and panel parts
- 4x M5 threaded rods at the tower corners
- metal guide rails for tray support
- rear service spine
- power bus placeholder
- Mini PC airflow duct
- modular trays
- removable side panels
- 120 mm intake fan panel
- 120 mm exhaust fan panel

## Module Stack

Bottom to top:

- UPS / Power Distribution tray, 2U
- External SSD Bay, 1U
- SSD / Expansion tray, 1U
- Raspberry Pi tray, 1U
- MikroTik hAP ax2 tray, 1.5U placeholder
- Mini PC tray, 2U

## Main Construction Components

- top frame ring
- bottom frame ring
- corner blocks
- M5 threaded rod placeholders
- metal guide rail placeholders, 10 x 3 mm
- removable trays
- left and right side panels
- rear service spine
- power bus panel
- bottom fan panel
- top fan panel
- Mini PC airflow duct

## Project Status

Status: frozen as first engineering CAD revision.

The model builds and exports through `python -m cad.export`. All major elements are present as first-pass parametric placeholders. mk0.1 is not a print-ready or electrically validated design.
