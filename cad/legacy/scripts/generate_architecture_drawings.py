"""Generate mk0.10 drawing-layer v2 planning SVGs.

LEGACY / CANCELLED — mk0.10 drawing-first workflow
===================================================
This script belongs to the mk0.10 drawing-first workflow iteration.
That workflow has been cancelled.

Do NOT run this script to generate new planning drawings for mk0.11.
Do NOT continue iterating SVG drawings for architectural planning.

Reason (Decision D-001 in revisions/mk0.11/DECISIONS.md):
  The mk0.10 SVG iteration did not unlock any design decision that could not
  be read directly from cad/config.py. Physical prototyping produces faster
  and more reliable validation.

Current active workflow: subsystem-first / testable CAD-first (mk0.11).
See: revisions/mk0.11/README.md

This file is preserved for historical reference only.
===================================================

These sheets are engineering communication artifacts between requirements and
CadQuery. They do not create or modify 3D geometry, STEP, or STL outputs.
"""

from __future__ import annotations

import argparse
import html
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cad import config as cfg  # noqa: E402


PROJECT = "Homelab Modular Tower"
REVISION_DEFAULT = "mk0.10"
SOURCE_BASIS = getattr(cfg, "CURRENT_REVISION", "cad/config.py")
UNITS = "mm"

SHEET_W = 1600
SHEET_H = 1000
MARGIN = 36
TITLE_H = 90
BOTTOM_H = 92
GAP = 22

BLACK = "#111111"
TEXT = "#20242a"
GRAY = "#5f6670"
LIGHT_GRAY = "#f6f7f8"
PANEL_BG = "#ffffff"
PETG = "#e6e8eb"
PETG_DARK = "#cfd5dc"
METAL = "#8fa5b8"
METAL_DARK = "#526b80"
POM = "#f2b84b"
POM_DARK = "#9b6400"
AIR = "#1f78c8"
AIR_FILL = "#dff1ff"
SERVICE = "#d9c7ee"
SERVICE_STROKE = "#7b5aa6"
WARN = "#9d1c20"
PIN = "#7a828a"
SOCKET = "#ffffff"
BOLT = "#ffffff"


def cfg_value(name: str, default: float | str | None = None) -> float | str | None:
    if hasattr(cfg, name):
        return getattr(cfg, name)
    if default is None:
        DrawingWarnings.items.append(f"Missing cad.config.{name}")
        return 0.0
    DrawingWarnings.items.append(f"Missing cad.config.{name}; using drawing default {default}")
    return default


def as_float(name: str, default: float | None = None) -> float:
    return float(cfg_value(name, default))


def fmt_mm(value: float) -> str:
    if abs(value - round(value)) < 0.01:
        return f"{round(value):.0f} mm"
    return f"{value:.1f} mm"


def wrap_lines(text: str, max_chars: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = ""
    for word in words:
        test = word if not current else f"{current} {word}"
        if len(test) <= max_chars:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


@dataclass
class Panel:
    x: float
    y: float
    w: float
    h: float
    title: str


class DrawingWarnings:
    items: list[str] = []


class SvgDrawing:
    def __init__(self, number: str, title: str, revision: str, purpose: str) -> None:
        self.width = SHEET_W
        self.height = SHEET_H
        self.number = number
        self.title = title
        self.revision = revision
        self.purpose = purpose
        self.items: list[str] = []
        self.defs: list[str] = [
            '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" '
            'markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
            '<path d="M 0 0 L 10 5 L 0 10 z" fill="context-stroke" /></marker>',
            '<marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" '
            'markerWidth="5" markerHeight="5">'
            '<circle cx="5" cy="5" r="4" fill="context-stroke" /></marker>',
        ]

    def _attrs(self, **attrs: object) -> str:
        parts = []
        for key, value in attrs.items():
            if value is None:
                continue
            parts.append(f'{key.replace("_", "-")}="{html.escape(str(value))}"')
        return " ".join(parts)

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str = "none",
        stroke: str = BLACK,
        stroke_width: float = 1.2,
        dash: str | None = None,
        rx: float = 0.0,
        opacity: float | None = None,
    ) -> None:
        self.items.append(
            f"<rect {self._attrs(x=x, y=y, width=w, height=h, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, rx=rx, opacity=opacity)} />"
        )

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        stroke: str = BLACK,
        stroke_width: float = 1.2,
        dash: str | None = None,
        marker_start: bool = False,
        marker_end: bool = False,
        marker_dot: bool = False,
    ) -> None:
        self.items.append(
            f"<line {self._attrs(x1=x1, y1=y1, x2=x2, y2=y2, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, marker_start='url(#arrow)' if marker_start else None, marker_end='url(#dot)' if marker_dot else ('url(#arrow)' if marker_end else None))} />"
        )

    def polyline(
        self,
        points: Iterable[tuple[float, float]],
        fill: str = "none",
        stroke: str = BLACK,
        stroke_width: float = 1.2,
        dash: str | None = None,
        marker_end: bool = False,
    ) -> None:
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.items.append(
            f"<polyline {self._attrs(points=pts, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash, marker_end='url(#arrow)' if marker_end else None)} />"
        )

    def polygon(
        self,
        points: Iterable[tuple[float, float]],
        fill: str = "none",
        stroke: str = BLACK,
        stroke_width: float = 1.2,
        dash: str | None = None,
    ) -> None:
        pts = " ".join(f"{x:.1f},{y:.1f}" for x, y in points)
        self.items.append(
            f"<polygon {self._attrs(points=pts, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash)} />"
        )

    def circle(
        self,
        cx: float,
        cy: float,
        r: float,
        fill: str = "none",
        stroke: str = BLACK,
        stroke_width: float = 1.2,
        dash: str | None = None,
    ) -> None:
        self.items.append(
            f"<circle {self._attrs(cx=cx, cy=cy, r=r, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash)} />"
        )

    def ellipse(
        self,
        cx: float,
        cy: float,
        rx: float,
        ry: float,
        fill: str = "none",
        stroke: str = BLACK,
        stroke_width: float = 1.2,
        dash: str | None = None,
    ) -> None:
        self.items.append(
            f"<ellipse {self._attrs(cx=cx, cy=cy, rx=rx, ry=ry, fill=fill, stroke=stroke, stroke_width=stroke_width, stroke_dasharray=dash)} />"
        )

    def arc_path(
        self,
        x1: float,
        y1: float,
        rx: float,
        ry: float,
        x2: float,
        y2: float,
        stroke: str = BLACK,
        stroke_width: float = 1.2,
        dash: str | None = None,
        marker_end: bool = False,
    ) -> None:
        marker = ' marker-end="url(#arrow)"' if marker_end else ""
        dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
        self.items.append(
            f'<path d="M {x1:.1f} {y1:.1f} A {rx:.1f} {ry:.1f} 0 0 1 {x2:.1f} {y2:.1f}" fill="none" stroke="{stroke}" stroke-width="{stroke_width}"{dash_attr}{marker} />'
        )

    def text(
        self,
        x: float,
        y: float,
        value: str,
        size: float = 13,
        fill: str = TEXT,
        anchor: str = "start",
        weight: str = "normal",
        rotate: float | None = None,
    ) -> None:
        transform = f"rotate({rotate} {x} {y})" if rotate is not None else None
        self.items.append(
            f"<text {self._attrs(x=x, y=y, fill=fill, font_size=size, font_family='Arial, Helvetica, sans-serif', text_anchor=anchor, font_weight=weight, transform=transform)}>{html.escape(value)}</text>"
        )

    def multiline(
        self,
        x: float,
        y: float,
        lines: Sequence[str],
        size: float = 12,
        fill: str = TEXT,
        line_h: float | None = None,
        weight: str = "normal",
    ) -> None:
        step = line_h or size + 5
        for i, line in enumerate(lines):
            self.text(x, y + i * step, line, size=size, fill=fill, weight=weight)

    def save(self, path: Path) -> None:
        draw_title_block(self, self.number, self.title, self.revision, self.purpose)
        if DrawingWarnings.items:
            draw_validation_block(self, MARGIN, SHEET_H - BOTTOM_H + 16, 470, BOTTOM_H - 30, ["Config warnings:", *DrawingWarnings.items[:4]])
        svg = [
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.width}" height="{self.height}" viewBox="0 0 {self.width} {self.height}">',
            "<defs>",
            *self.defs,
            "</defs>",
            f'<rect x="0" y="0" width="{self.width}" height="{self.height}" fill="white" />',
            *self.items,
            "</svg>",
            "",
        ]
        path.write_text("\n".join(svg), encoding="utf-8")


def new_drawing(number: str, title: str, revision: str, purpose: str) -> SvgDrawing:
    DrawingWarnings.items = []
    return SvgDrawing(number, title, revision, purpose)


def draw_title_block(d: SvgDrawing, number: str, title: str, revision: str, purpose: str) -> None:
    d.rect(MARGIN, 20, SHEET_W - 2 * MARGIN, 62, fill="#f9fafb", stroke=BLACK, stroke_width=1.3)
    d.text(MARGIN + 16, 47, number, size=18, weight="bold")
    d.text(MARGIN + 16, 70, title, size=18, weight="bold")
    d.line(575, 20, 575, 82, stroke=BLACK)
    d.text(590, 43, f"Revision: {revision}", size=13, weight="bold")
    d.text(590, 64, f"Purpose: {purpose}", size=12, fill=GRAY)
    d.line(1040, 20, 1040, 82, stroke=BLACK)
    d.text(1055, 43, "PLANNING DRAWING - NOT FOR MANUFACTURING", size=13, fill=WARN, weight="bold")
    d.text(1055, 64, f"Units: {UNITS}; source dimensions: cad/config.py ({SOURCE_BASIS})", size=11, fill=GRAY)


def draw_warning(d: SvgDrawing, x: float, y: float, text: str) -> None:
    lines = wrap_lines(text, 46)
    d.rect(x, y, 330, 28 + len(lines) * 15, fill="#fff5f5", stroke=WARN, stroke_width=1.1)
    d.text(x + 10, y + 20, "WARNING", size=11, fill=WARN, weight="bold")
    d.multiline(x + 10, y + 39, lines, size=11, fill=WARN, line_h=15)


def draw_scale_note(d: SvgDrawing, x: float, y: float, text: str = "Schematic scale; dimensions shown where specified.") -> None:
    d.text(x, y, text, size=10.5, fill=GRAY)


def draw_panel(d: SvgDrawing, panel: Panel) -> None:
    d.rect(panel.x, panel.y, panel.w, panel.h, fill=PANEL_BG, stroke=BLACK, stroke_width=1.25)
    d.rect(panel.x, panel.y, panel.w, 30, fill=LIGHT_GRAY, stroke=BLACK, stroke_width=1.0)
    d.text(panel.x + 12, panel.y + 21, panel.title, size=13, weight="bold")


def draw_dimension(
    d: SvgDrawing,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: str,
    offset: float = 22,
    color: str = GRAY,
) -> None:
    horizontal = abs(x2 - x1) >= abs(y2 - y1)
    if horizontal:
        yy = y1 + offset
        d.line(x1, y1, x1, yy, stroke=color, stroke_width=0.9)
        d.line(x2, y2, x2, yy, stroke=color, stroke_width=0.9)
        d.line(x1, yy, x2, yy, stroke=color, stroke_width=1.0, marker_start=True, marker_end=True)
        d.text((x1 + x2) / 2, yy - 6 if offset > 0 else yy + 16, label, size=10.5, fill=color, anchor="middle")
    else:
        xx = x1 + offset
        d.line(x1, y1, xx, y1, stroke=color, stroke_width=0.9)
        d.line(x2, y2, xx, y2, stroke=color, stroke_width=0.9)
        d.line(xx, y1, xx, y2, stroke=color, stroke_width=1.0, marker_start=True, marker_end=True)
        d.text(xx + 6 if offset > 0 else xx - 6, (y1 + y2) / 2, label, size=10.5, fill=color, anchor="start" if offset > 0 else "end")


def draw_arrow(
    d: SvgDrawing,
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    label: str | None = None,
    color: str = BLACK,
    width: float = 2.3,
    label_pos: str = "end",
) -> None:
    d.line(x1, y1, x2, y2, stroke=color, stroke_width=width, marker_end=True)
    if label:
        if label_pos == "middle":
            d.text((x1 + x2) / 2, (y1 + y2) / 2 - 8, label, size=11, fill=color, anchor="middle", weight="bold")
        else:
            d.text(x2 + 8, y2 - 7, label, size=11, fill=color, weight="bold")


def draw_callout(d: SvgDrawing, x: float, y: float, tx: float, ty: float, label: str, color: str = BLACK) -> None:
    d.line(x, y, tx, ty, stroke=color, stroke_width=1.0, marker_dot=True)
    d.multiline(tx + 7, ty - 3, wrap_lines(label, 30), size=10.5, fill=color, line_h=14)


def draw_legend(d: SvgDrawing, x: float, y: float, items: Sequence[tuple[str, str]]) -> None:
    d.text(x, y, "Legend", size=12, weight="bold")
    cy = y + 22
    for kind, label in items:
        if kind == "m5":
            draw_m5_rod_symbol(d, x + 10, cy - 5, 7)
        elif kind == "bolt":
            draw_bolt_symbol(d, x + 10, cy - 5, 5)
        elif kind == "pin":
            draw_pin_symbol(d, x + 10, cy - 5, 5)
        elif kind == "socket":
            draw_socket_symbol(d, x + 10, cy - 5, 6)
        elif kind == "air":
            d.rect(x + 3, cy - 13, 18, 13, fill=AIR_FILL, stroke=AIR, dash="4 3")
        elif kind == "service":
            d.rect(x + 3, cy - 13, 18, 13, fill=SERVICE, stroke=SERVICE_STROKE, dash="4 3")
        elif kind == "pom":
            d.rect(x + 3, cy - 13, 18, 13, fill=POM, stroke=POM_DARK)
        elif kind == "metal":
            d.rect(x + 3, cy - 13, 18, 13, fill=METAL, stroke=METAL_DARK)
        d.text(x + 32, cy, label, size=10.5)
        cy += 20


def draw_section_line(d: SvgDrawing, x1: float, y1: float, x2: float, y2: float, label: str, color: str = WARN) -> None:
    d.line(x1, y1, x2, y2, stroke=color, stroke_width=2.0, dash="8 5")
    d.text((x1 + x2) / 2, (y1 + y2) / 2 - 6, label, size=11, fill=color, weight="bold", anchor="middle")


def draw_orientation_axes(d: SvgDrawing, x: float, y: float, scale: float = 1.0) -> None:
    draw_arrow(d, x, y, x + 70 * scale, y, "+X shoe insertion", BLACK, 2.0)
    draw_arrow(d, x, y, x + 115 * scale, y - 38 * scale, "+Y rail length / slide", METAL_DARK, 2.0)
    draw_arrow(d, x, y, x, y - 62 * scale, "+Z", GRAY, 2.0)


def draw_validation_block(d: SvgDrawing, x: float, y: float, w: float, h: float, lines: Sequence[str]) -> None:
    d.rect(x, y, w, h, fill="#fbfbfb", stroke="#a9adb4", stroke_width=1.0)
    d.text(x + 12, y + 22, "Validation gates", size=12, weight="bold")
    d.multiline(x + 12, y + 42, list(lines)[:5], size=10.5, fill=TEXT, line_h=15)


def draw_material_key(d: SvgDrawing, x: float, y: float) -> None:
    draw_legend(
        d,
        x,
        y,
        [
            ("metal", "aluminium / metal"),
            ("pom", "POM-C shoe"),
            ("air", "airflow path/window"),
            ("service", "rear service zone"),
        ],
    )


def draw_m5_rod_symbol(d: SvgDrawing, cx: float, cy: float, r: float = 7) -> None:
    d.circle(cx, cy, r, fill=METAL, stroke=METAL_DARK, stroke_width=2.0)
    d.circle(cx, cy, max(2, r * 0.35), fill="#ffffff", stroke=METAL_DARK, stroke_width=1.0)


def draw_bolt_symbol(d: SvgDrawing, cx: float, cy: float, r: float = 5) -> None:
    d.circle(cx, cy, r, fill=BOLT, stroke=BLACK, stroke_width=1.4)


def draw_pin_symbol(d: SvgDrawing, cx: float, cy: float, r: float = 5) -> None:
    d.circle(cx, cy, r, fill=PIN, stroke=BLACK, stroke_width=1.0)


def draw_socket_symbol(d: SvgDrawing, cx: float, cy: float, r: float = 6) -> None:
    d.circle(cx, cy, r, fill=SOCKET, stroke=BLACK, stroke_width=1.2, dash="4 3")


def draw_u_channel(d: SvgDrawing, x: float, y: float, scale: float, open_side: str = "top") -> None:
    rail_w = as_float("RAIL_OUTER_WIDTH")
    rail_h = as_float("RAIL_OUTER_HEIGHT")
    wall = as_float("RAIL_WALL_THICKNESS")
    if open_side != "top":
        raise ValueError("Only top-open U-channel drawing is supported")
    d.rect(x, y, wall * scale, rail_h * scale, fill=METAL, stroke=BLACK, stroke_width=1.4)
    d.rect(x, y + (rail_h - wall) * scale, rail_w * scale, wall * scale, fill=METAL, stroke=BLACK, stroke_width=1.4)
    d.rect(x + (rail_w - wall) * scale, y, wall * scale, rail_h * scale, fill=METAL, stroke=BLACK, stroke_width=1.4)
    d.line(x + wall * scale, y, x + (rail_w - wall) * scale, y, stroke=WARN, stroke_width=1.2, dash="4 3")


def draw_pom_shoe(d: SvgDrawing, x: float, y: float, length: float, diameter: float, scale: float) -> None:
    w = length * scale
    h = diameter * scale
    d.rect(x, y, w, h, fill=POM, stroke=BLACK, stroke_width=1.3)
    d.ellipse(x, y + h / 2, h / 2, h / 2, fill=POM, stroke=BLACK, stroke_width=1.3)
    d.ellipse(x + w, y + h / 2, h / 2, h / 2, fill=POM, stroke=BLACK, stroke_width=1.3)
    d.line(x, y, x + w, y, stroke=POM_DARK, stroke_width=1.0)
    d.line(x, y + h, x + w, y + h, stroke=POM_DARK, stroke_width=1.0)


def draw_clamp_screw_detail(d: SvgDrawing, x: float, y: float, w: float, h: float) -> None:
    boss_d = as_float("CARRIAGE_RUNNER_BOSS_DIAMETER")
    socket_d = as_float("RUNNER_SOCKET_DIAMETER")
    runner_d = as_float("RUNNER_DIAMETER")
    screw_d = as_float("RUNNER_RETENTION_SCREW_DIAMETER")
    insert_d = as_float("HEAT_SET_INSERT_M3_DIAMETER")
    insert_depth = as_float("HEAT_SET_INSERT_M3_DEPTH")
    cx = x + 155
    cy = y + h * 0.62
    d.circle(cx, cy, boss_d * 4.6, fill=PETG, stroke=BLACK, stroke_width=1.4)
    d.circle(cx, cy, socket_d * 3.9, fill="#fff8e8", stroke=POM_DARK, stroke_width=1.2)
    d.line(cx - 88, cy, cx + 48, cy, stroke=POM, stroke_width=runner_d * 6.5)
    d.rect(cx - insert_d * 4.5, cy - 78, insert_d * 9, insert_depth * 7, fill=METAL, stroke=BLACK)
    d.line(cx, cy - 110, cx, cy - 30, stroke=BLACK, stroke_width=2.4, marker_end=True)
    d.circle(cx, cy - 122, screw_d * 5.5, fill="#ffffff", stroke=BLACK)
    d.circle(cx, cy - 30, 5, fill=WARN, stroke=WARN)
    draw_callout(d, cx, cy - 30, x + 300, y + 83, "clamp/stop contact point", WARN)
    d.text(x + 300, y + 120, "M3 clamp screw into PETG boss / insert", size=11)
    d.text(x + 300, y + 143, "thread in PETG only, not in POM-C", size=11, fill=WARN)
    d.text(x + 300, y + 166, "POM-C shoe remains replaceable", size=11)


def stack_heights() -> list[tuple[str, float, str]]:
    return [
        ("Base structural cap", as_float("BASE_MODULE_HEIGHT"), PETG),
        ("RPi / SSD module", as_float("RPI_SSD_MODULE_HEIGHT"), "#eef3f7"),
        ("Mini PC placeholder", as_float("MINI_PC_MODULE_HEIGHT"), "#eaf0e2"),
        ("Roof structural cap", as_float("ROOF_MODULE_HEIGHT"), PETG),
    ]


def draw_top_footprint(
    d: SvgDrawing,
    x: float,
    y: float,
    w: float,
    h: float,
    labels: bool = True,
    section_lines: bool = False,
) -> None:
    tower_w = as_float("TOWER_WIDTH")
    depth = as_float("TOWER_DEPTH")
    rear = as_float("REAR_RESERVED_DEPTH")
    rod_offset = as_float("ROD_CENTER_OFFSET")
    airflow_w = as_float("AIRFLOW_CHANNEL_WIDTH")
    airflow_d = as_float("AIRFLOW_CHANNEL_DEPTH")
    s = min((w - 45) / tower_w, (h - 60) / depth)
    fx = x + (w - tower_w * s) / 2
    fy = y + 40
    fw = tower_w * s
    fh = depth * s
    d.rect(fx, fy, fw, fh, fill="#ffffff", stroke=BLACK, stroke_width=1.6)
    d.rect(fx, fy + (depth - rear) * s, fw, rear * s, fill=SERVICE, stroke=SERVICE_STROKE, dash="5 4")
    d.rect(
        fx + (tower_w - airflow_w) * s / 2,
        fy + (depth - rear - airflow_d) * s / 2,
        airflow_w * s,
        airflow_d * s,
        fill=AIR_FILL,
        stroke=AIR,
        dash="5 4",
    )
    for x_mm in (rod_offset, tower_w - rod_offset):
        for y_mm in (rod_offset, depth - rod_offset):
            draw_m5_rod_symbol(d, fx + x_mm * s, fy + y_mm * s, 6)
    if labels:
        d.text(fx, fy - 10, "FRONT", size=10.5, weight="bold")
        d.text(fx + fw, fy + fh + 18, "REAR", size=10.5, weight="bold", anchor="end")
        d.text(fx + fw / 2, fy + fh / 2, "airflow window", size=10.5, fill=AIR, anchor="middle")
        d.text(fx + fw / 2, fy + fh - rear * s / 2 + 4, "rear service zone", size=10.5, fill=SERVICE_STROKE, anchor="middle")
    if section_lines:
        draw_section_line(d, fx + fw * 0.22, fy + fh * 0.44, fx + fw * 0.78, fy + fh * 0.44, "A-A")
        draw_section_line(d, fx + rod_offset * s, fy + 5, fx + rod_offset * s, fy + 62, "B-B", METAL_DARK)
        draw_section_line(d, fx + fw * 0.70, fy + 8, fx + fw * 0.70, fy + 70, "C-C", GRAY)


def drawing_01(out: Path, revision: str) -> None:
    d = new_drawing("HMT-mk0.10-DWG-01", "Tower architecture overview", revision, "stack architecture and footprint")
    tower_w = as_float("TOWER_WIDTH")
    tower_h = as_float("TOWER_HEIGHT")
    foot_h = as_float("FOOT_HEIGHT")
    rod_offset = as_float("ROD_CENTER_OFFSET")
    rod_extra = as_float("ROD_EXTRA_THREAD_ALLOWANCE")
    rod_cap_h = as_float("ROD_CAP_HEIGHT")
    physical_h = tower_h + foot_h + rod_extra + rod_cap_h

    main = Panel(44, 112, 650, 710, "A - Main front stack view")
    top = Panel(730, 112, 380, 300, "B - Top footprint inset")
    side = Panel(1140, 112, 410, 300, "C - Physical envelope side inset")
    table = Panel(730, 440, 380, 260, "D - Compact stack table")
    for p in (main, top, side, table):
        draw_panel(d, p)

    s = min((main.w - 210) / tower_w, (main.h - 135) / (tower_h + foot_h))
    left = main.x + 120
    bottom = main.y + main.h - 70
    tower_bottom = bottom - foot_h * s
    tower_top = tower_bottom - tower_h * s
    d.rect(left, tower_top, tower_w * s, tower_h * s, fill="none", stroke=BLACK, stroke_width=2.0)
    d.rect(left, tower_bottom, tower_w * s, foot_h * s, fill="#eeeeee", stroke=GRAY, dash="5 4")

    cursor = tower_bottom
    for label, height, fill in stack_heights():
        y = cursor - height * s
        d.rect(left, y, tower_w * s, height * s, fill=fill, stroke=BLACK, stroke_width=1.2)
        d.text(left + tower_w * s / 2, y + height * s / 2 + 5, label, size=13, anchor="middle", weight="bold" if "structural" in label else "normal")
        cursor = y

    for x_mm in (rod_offset, tower_w - rod_offset):
        x = left + x_mm * s
        d.line(x, tower_top - 13, x, tower_bottom + 18, stroke=METAL_DARK, stroke_width=4.0)
        draw_m5_rod_symbol(d, x, tower_top + 17, 8)
        draw_m5_rod_symbol(d, x, tower_bottom - 17, 8)
    draw_callout(d, left + rod_offset * s, tower_top + 65, main.x + 395, main.y + 94, "front view shows two rod lines; rear rods overlap in this view", METAL_DARK)
    draw_arrow(d, left + tower_w * s / 2, tower_bottom - 65, left + tower_w * s / 2, tower_top + 62, "vertical airflow", AIR, 4.0, "middle")
    d.rect(left + tower_w * s * 0.18, tower_bottom - 30, tower_w * s * 0.64, 20, fill=AIR_FILL, stroke=AIR, dash="5 4")
    d.rect(left + tower_w * s * 0.18, tower_top + 10, tower_w * s * 0.64, 20, fill=AIR_FILL, stroke=AIR, dash="5 4")
    draw_dimension(d, left - 30, tower_top, left - 30, tower_bottom, f"visible stack {fmt_mm(tower_h)}", offset=48)
    draw_dimension(d, left, tower_bottom + 38, left + tower_w * s, tower_bottom + 38, fmt_mm(tower_w), offset=0)
    d.text(left + tower_w * s + 18, tower_bottom + foot_h * s / 2, f"feet {fmt_mm(foot_h)}", size=11, fill=GRAY)
    draw_scale_note(d, main.x + 14, main.y + main.h - 16)

    draw_top_footprint(d, top.x + 10, top.y + 18, top.w - 20, top.h - 32)
    d.text(top.x + 18, top.y + top.h - 16, "Top inset shows all 4 rod positions.", size=11, fill=METAL_DARK, weight="bold")

    sx = side.x + 92
    sy = side.y + 82
    stack_h_px = 155
    d.rect(sx, sy, 70, stack_h_px, fill=PETG, stroke=BLACK)
    d.rect(sx, sy + stack_h_px, 70, foot_h / physical_h * 230, fill="#eeeeee", stroke=GRAY, dash="4 3")
    d.line(sx + 35, sy - 38, sx + 35, sy + stack_h_px + 34, stroke=METAL_DARK, stroke_width=3)
    d.rect(sx + 18, sy - 32, 34, 18, fill=METAL, stroke=BLACK)
    d.text(sx + 95, sy + 68, "visible stack", size=11)
    d.text(sx + 95, sy - 20, "caps / nuts / washers", size=11, fill=METAL_DARK)
    d.text(sx + 95, sy + stack_h_px + 27, "feet clearance", size=11, fill=GRAY)
    draw_dimension(d, sx - 28, sy, sx - 28, sy + stack_h_px, fmt_mm(tower_h), offset=-22)
    draw_dimension(d, sx + 190, sy - 38, sx + 190, sy + stack_h_px + 34, f"approx. {fmt_mm(physical_h)}", offset=18)
    d.text(side.x + 18, side.y + side.h - 18, "physical envelope > visible stack height.", size=12, fill=WARN, weight="bold")

    rows = stack_heights()
    y = table.y + 62
    for i, (label, height, fill) in enumerate(rows, start=1):
        d.rect(table.x + 28, y - 18, 24, 18, fill=fill, stroke=BLACK)
        d.text(table.x + 64, y - 4, f"{i}. {label}", size=12, weight="bold" if "structural" in label else "normal")
        d.text(table.x + 255, y - 4, fmt_mm(height), size=12, anchor="end")
        y += 44
    d.text(table.x + 28, table.y + table.h - 34, "Base and roof are structural caps.", size=11, fill=GRAY)
    d.text(table.x + 28, table.y + table.h - 16, "Extraction direction is defined on side sheet.", size=11, fill=GRAY)

    draw_validation_block(
        d,
        44,
        850,
        1506,
        118,
        [
            "Reader must understand vertical module order, 4-rod footprint, and airflow direction.",
            "Visible stack height intentionally excludes feet, rod caps, nuts/washers, and thread allowance.",
            "Rear service zone is identified in top inset, not hidden behind text.",
        ],
    )
    d.save(out / "01_architecture_layout_front.svg")


def drawing_02(out: Path, revision: str) -> None:
    d = new_drawing("HMT-mk0.10-DWG-02", "Depth zoning, airflow and rear service spine", revision, "side zoning and service separation")
    depth = as_float("TOWER_DEPTH")
    rear = as_float("REAR_RESERVED_DEPTH")
    usable = depth - rear
    tower_h = as_float("TOWER_HEIGHT")
    airflow_d = as_float("AIRFLOW_CHANNEL_DEPTH")

    main = Panel(44, 112, 820, 560, "A - Main side zoning view")
    top = Panel(900, 112, 650, 220, "B - Top depth zoning inset")
    bend = Panel(900, 356, 312, 316, "C - Cable bend detail")
    sep = Panel(1238, 356, 312, 316, "D - Airflow vs service separation")
    for p in (main, top, bend, sep):
        draw_panel(d, p)

    s = min((main.w - 170) / depth, (main.h - 120) / tower_h)
    x = main.x + 84
    y = main.y + 72
    w = depth * s
    h = tower_h * s
    rear_w = rear * s
    usable_w = usable * s
    d.text(x, y - 15, "FRONT", size=12, weight="bold")
    d.text(x + w, y - 15, "REAR", size=12, weight="bold", anchor="end")
    d.rect(x, y, w, h, fill="#ffffff", stroke=BLACK, stroke_width=2)
    d.rect(x, y, usable_w, h, fill="#f8fbfd", stroke=BLACK, stroke_width=1.0)
    d.rect(x + usable_w, y, rear_w, h, fill=SERVICE, stroke=SERVICE_STROKE, stroke_width=1.4, dash="6 4")
    d.text(x + usable_w / 2, y + 28, "usable device zone", size=13, anchor="middle", weight="bold")
    d.text(x + usable_w + rear_w / 2, y + 28, "rear service zone", size=12, fill=SERVICE_STROKE, anchor="middle", weight="bold")
    airflow_x = x + (usable_w - airflow_d * s) / 2
    d.rect(airflow_x, y + 45, airflow_d * s, h - 90, fill=AIR_FILL, stroke=AIR, dash="7 5")
    draw_arrow(d, airflow_x + airflow_d * s / 2, y + h - 42, airflow_x + airflow_d * s / 2, y + 50, "vertical airflow", AIR, 4, "middle")
    draw_arrow(d, x + usable_w * 0.73, y + h * 0.55, x - 55, y + h * 0.55, "module extraction to FRONT", WARN, 3.2, "middle")
    draw_dimension(d, x, y + h + 35, x + w, y + h + 35, f"TOWER_DEPTH {fmt_mm(depth)}", offset=0)
    draw_dimension(d, x + usable_w, y + h + 62, x + w, y + h + 62, f"rear reserved {fmt_mm(rear)}", offset=0)
    draw_callout(d, x + usable_w + rear_w / 2, y + h * 0.68, main.x + 520, main.y + 420, "reserved for DC bus, Ethernet, USB and fan wiring", SERVICE_STROKE)

    tx = top.x + 42
    ty = top.y + 88
    tw = top.w - 90
    th = 72
    d.rect(tx, ty, tw, th, fill="#ffffff", stroke=BLACK, stroke_width=1.5)
    d.rect(tx, ty, tw * usable / depth, th, fill="#f8fbfd", stroke=BLACK)
    d.rect(tx + tw * usable / depth, ty, tw * rear / depth, th, fill=SERVICE, stroke=SERVICE_STROKE, dash="5 4")
    d.text(tx + tw * usable / depth / 2, ty + 42, f"usable module depth = {fmt_mm(usable)}", size=12, anchor="middle")
    d.text(tx + tw * (usable + rear / 2) / depth, ty + 42, f"rear {fmt_mm(rear)}", size=12, fill=SERVICE_STROKE, anchor="middle")
    d.text(tx, ty - 14, "FRONT", size=10.5, weight="bold")
    d.text(tx + tw, ty - 14, "REAR", size=10.5, weight="bold", anchor="end")
    draw_dimension(d, tx, ty + th + 28, tx + tw, ty + th + 28, f"{fmt_mm(depth)}", offset=0)

    bx = bend.x + 54
    by = bend.y + 96
    d.rect(bx, by, 86, 50, fill=PETG, stroke=BLACK)
    d.rect(bx + 86, by + 15, 38, 20, fill=METAL, stroke=BLACK)
    boundary_x = bx + 165
    d.line(boundary_x, bend.y + 52, boundary_x, bend.y + bend.h - 36, stroke=SERVICE_STROKE, stroke_width=2, dash="7 5")
    d.arc_path(bx + 124, by + 25, 78, 78, boundary_x + 68, by + 116, stroke=WARN, stroke_width=3, marker_end=True)
    d.text(boundary_x + 8, bend.y + 75, "rear zone boundary", size=11, fill=SERVICE_STROKE)
    draw_warning(d, bend.x + 18, bend.y + 205, "30 mm rear reserved zone connector bend radius NOT VALIDATED.")

    sx = sep.x + 40
    sy = sep.y + 92
    d.rect(sx, sy, 110, 175, fill=AIR_FILL, stroke=AIR, dash="6 4")
    d.rect(sx + 132, sy, 92, 175, fill=SERVICE, stroke=SERVICE_STROKE, dash="6 4")
    draw_arrow(d, sx + 55, sy + 142, sx + 55, sy + 35, "air", AIR, 3, "middle")
    d.polyline([(sx + 174, sy + 145), (sx + 198, sy + 118), (sx + 162, sy + 92), (sx + 190, sy + 55)], stroke=SERVICE_STROKE, stroke_width=3)
    d.text(sx + 55, sy + 196, "device / airflow", size=11, fill=AIR, anchor="middle")
    d.text(sx + 178, sy + 196, "cables / service", size=11, fill=SERVICE_STROKE, anchor="middle")
    d.multiline(sep.x + 26, sep.y + sep.h - 55, ["No random device geometry may", "consume rear service zone."], size=11, fill=WARN, line_h=15, weight="bold")

    draw_validation_block(
        d,
        44,
        850,
        1506,
        118,
        [
            "Extraction arrow must be horizontal toward FRONT.",
            "Rear service zone is a reserved mechanical/service volume, not unused space.",
            "Cable bend radius remains a geometric risk until tested with real connectors.",
        ],
    )
    d.save(out / "02_architecture_layout_side.svg")


def drawing_03(out: Path, revision: str) -> None:
    d = new_drawing("HMT-mk0.10-DWG-03", "Common module interface plan", revision, "top and bottom module mating convention")
    tower_w = as_float("TOWER_WIDTH")
    depth = as_float("TOWER_DEPTH")
    rear = as_float("REAR_RESERVED_DEPTH")
    rod_offset = as_float("ROD_CENTER_OFFSET")
    bolt_offset = as_float("INTERFACE_BOLT_CENTER_OFFSET")
    bolt_y = as_float("INTERFACE_LOCAL_BOLT_OFFSET_Y")
    airflow_w = as_float("AIRFLOW_CHANNEL_WIDTH")
    airflow_d = as_float("AIRFLOW_CHANNEL_DEPTH")

    main = Panel(44, 112, 760, 630, "A - Main top interface plan")
    bottom = Panel(835, 112, 335, 285, "B - Bottom-side mating inset")
    corner = Panel(1200, 112, 350, 410, "C - Corner zoom detail")
    legend = Panel(835, 420, 335, 322, "D - Legend and coordinates")
    for p in (main, bottom, corner, legend):
        draw_panel(d, p)

    s = min((main.w - 155) / tower_w, (main.h - 130) / depth)
    fx = main.x + 88
    fy = main.y + 72
    fw = tower_w * s
    fh = depth * s
    d.rect(fx, fy, fw, fh, fill="#ffffff", stroke=BLACK, stroke_width=2)
    d.rect(fx, fy + (depth - rear) * s, fw, rear * s, fill=SERVICE, stroke=SERVICE_STROKE, dash="5 4")
    d.rect(fx + (tower_w - airflow_w) * s / 2, fy + (depth - rear - airflow_d) * s / 2, airflow_w * s, airflow_d * s, fill=AIR_FILL, stroke=AIR, dash="5 4")
    for x_mm in (rod_offset, tower_w - rod_offset):
        for y_mm in (rod_offset, depth - rod_offset):
            draw_m5_rod_symbol(d, fx + x_mm * s, fy + y_mm * s, 8)
    for x_mm in (bolt_offset, tower_w - bolt_offset):
        for y_mm in (bolt_y, depth - rear - bolt_y):
            draw_bolt_symbol(d, fx + x_mm * s, fy + y_mm * s, 5)
    pin_positions = [
        (rod_offset + 24, rod_offset + 30),
        (tower_w - rod_offset - 24, rod_offset + 30),
        (rod_offset + 24, depth - rear - 30),
        (tower_w - rod_offset - 24, depth - rear - 30),
    ]
    for px, py in pin_positions:
        draw_pin_symbol(d, fx + px * s, fy + py * s, 5)
    d.text(fx + fw / 2, fy - 16, "+X right", size=11, anchor="middle")
    d.text(fx + fw + 16, fy + fh / 2, "+Y rear", size=11, rotate=90, anchor="middle")
    d.text(fx, fy - 16, "FRONT", size=11, weight="bold")
    d.text(fx + fw, fy + fh + 20, "REAR", size=11, weight="bold", anchor="end")
    draw_callout(d, fx + rod_offset * s, fy + rod_offset * s, main.x + 500, main.y + 88, "M5 rods clamp full tower stack", METAL_DARK)
    draw_callout(d, fx + bolt_offset * s, fy + bolt_y * s, main.x + 500, main.y + 132, "local bolts fasten module interface only")
    draw_callout(d, fx + (rod_offset + 24) * s, fy + (rod_offset + 30) * s, main.x + 500, main.y + 176, "pins/sockets locate only, not compression", PIN)

    bs = min((bottom.w - 75) / tower_w, (bottom.h - 90) / depth)
    bx = bottom.x + 38
    by = bottom.y + 67
    bw = tower_w * bs
    bh = depth * bs
    d.rect(bx, by, bw, bh, fill="#ffffff", stroke=BLACK, stroke_width=1.5)
    d.rect(bx, by + (depth - rear) * bs, bw, rear * bs, fill=SERVICE, stroke=SERVICE_STROKE, dash="5 4")
    for px, py in pin_positions:
        draw_socket_symbol(d, bx + px * bs, by + py * bs, 6)
    d.text(bottom.x + 22, bottom.y + bottom.h - 43, "Top side uses pins; bottom side provides sockets.", size=11)
    d.text(bottom.x + 22, bottom.y + bottom.h - 22, "Sockets are dashed/open to avoid confusion.", size=11, fill=GRAY)

    cx = corner.x + 82
    cy = corner.y + 160
    d.rect(cx - 40, cy - 40, 190, 180, fill=PETG, stroke=BLACK, stroke_width=1.5)
    draw_m5_rod_symbol(d, cx, cy, 18)
    draw_bolt_symbol(d, cx + 90, cy + 28, 11)
    draw_pin_symbol(d, cx + 42, cy + 96, 10)
    draw_socket_symbol(d, cx + 100, cy + 96, 12)
    d.line(cx - 40, cy + 58, cx + 150, cy + 58, stroke=BLACK, dash="5 4")
    draw_callout(d, cx, cy, corner.x + 208, corner.y + 112, "rods clamp", METAL_DARK)
    draw_callout(d, cx + 90, cy + 28, corner.x + 208, corner.y + 178, "bolts fasten locally")
    draw_callout(d, cx + 42, cy + 96, corner.x + 208, corner.y + 246, "pins locate only", PIN)
    draw_callout(d, cx + 100, cy + 96, corner.x + 208, corner.y + 312, "bottom sockets receive pins")

    draw_legend(
        d,
        legend.x + 24,
        legend.y + 62,
        [
            ("m5", "M5 rod / compression path"),
            ("bolt", "local interface bolt"),
            ("pin", "top alignment pin"),
            ("socket", "bottom alignment socket"),
            ("air", "airflow window"),
            ("service", "rear service zone"),
        ],
    )
    d.multiline(
        legend.x + 24,
        legend.y + 220,
        [
            "Origin: module center",
            "+X right",
            "+Y rear",
            f"ROD_CENTER_OFFSET = {fmt_mm(rod_offset)}",
            f"INTERFACE_BOLT_CENTER_OFFSET = {fmt_mm(bolt_offset)}",
            f"INTERFACE_LOCAL_BOLT_OFFSET_Y = {fmt_mm(bolt_y)}",
        ],
        size=11,
        line_h=16,
    )

    draw_validation_block(
        d,
        44,
        850,
        1506,
        118,
        [
            "Rods, local bolts, pins, and sockets use distinct symbols.",
            "Top/bottom mating convention is explicit: top pins, bottom sockets.",
            "Corner detail separates compression, local fastening, and locating functions.",
        ],
    )
    d.save(out / "03_module_interface_top.svg")


def drawing_04(out: Path, revision: str) -> None:
    d = new_drawing("HMT-mk0.10-DWG-04", "Module vertical mating contract", revision, "vertical interface sections for coupon planning")
    interface_h = as_float("MODULE_INTERFACE_HEIGHT")
    pin_d = as_float("INTERFACE_PIN_DIAMETER")
    pin_clear = as_float("INTERFACE_PIN_CLEARANCE")
    pin_h = as_float("INTERFACE_PIN_HEIGHT")
    socket_depth = as_float("INTERFACE_SOCKET_DEPTH")
    rod_clear = as_float("ROD_CLEARANCE")
    washer_d = as_float("M5_WASHER_DIAMETER")
    nut_flat = as_float("M5_NUT_FLAT_DIAMETER")

    ref = Panel(44, 112, 440, 300, "A - Top reference map")
    ring = Panel(515, 112, 500, 300, "B - A-A ring stack section")
    m5 = Panel(44, 442, 470, 300, "C - B-B M5 compression section")
    align = Panel(545, 442, 470, 300, "D - C-C alignment section")
    notes = Panel(1045, 442, 505, 300, "Function separation")
    for p in (ref, ring, m5, align, notes):
        draw_panel(d, p)

    draw_top_footprint(d, ref.x + 16, ref.y + 24, ref.w - 32, ref.h - 48, section_lines=True)

    sx = ring.x + 62
    split = ring.y + 160
    body_w = 360
    ring_px = interface_h * 16
    d.rect(sx, ring.y + 66, body_w, 55, fill=PETG_DARK, stroke=GRAY)
    d.text(sx + 14, ring.y + 98, "upper module body", size=11)
    d.rect(sx, split - ring_px, body_w, ring_px, fill=PETG, stroke=BLACK)
    d.text(sx + 14, split - 12, "upper bottom interface ring", size=11)
    d.line(sx - 10, split, sx + body_w + 10, split, stroke=WARN, stroke_width=1.8, dash="8 5")
    d.text(sx + body_w - 5, split - 8, "module split line", size=11, fill=WARN, anchor="end")
    d.rect(sx, split, body_w, ring_px, fill=PETG, stroke=BLACK)
    d.text(sx + 14, split + ring_px + 16, "lower top interface ring", size=11)
    d.rect(sx, split + ring_px, body_w, 55, fill=PETG_DARK, stroke=GRAY)
    d.text(sx + 14, split + ring_px + 45, "lower module body", size=11)
    d.rect(sx + 132, ring.y + 82, 95, 155, fill=AIR_FILL, stroke=AIR, dash="6 4")
    d.text(sx + 180, ring.y + 164, "airflow remains open", size=11, fill=AIR, anchor="middle")
    draw_dimension(d, sx + body_w + 28, split - ring_px, sx + body_w + 28, split, f"{fmt_mm(interface_h)} per ring", offset=20)
    d.text(ring.x + 24, ring.y + ring.h - 22, "No M5 rods or pins in A-A: ring function only.", size=11, fill=GRAY)

    mx = m5.x + 128
    my = m5.y + 96
    d.rect(mx - 60, my - 18, 140, 158, fill=PETG, stroke=BLACK)
    d.text(mx - 48, my + 18, "local PETG", size=11)
    d.text(mx - 48, my + 36, "compression pad", size=11)
    d.rect(mx - rod_clear * 5.5, my - 45, rod_clear * 11, 220, fill="#ffffff", stroke=METAL_DARK, dash="4 3")
    d.line(mx, my - 58, mx, my + 185, stroke=METAL_DARK, stroke_width=4)
    d.rect(mx - washer_d * 3.2, my - 30, washer_d * 6.4, 16, fill=METAL, stroke=BLACK)
    d.rect(mx - nut_flat * 3.5, my + 150, nut_flat * 7.0, 26, fill=METAL, stroke=BLACK)
    draw_arrow(d, mx, my - 67, mx, my - 10, "compression", METAL_DARK, 2.6)
    draw_arrow(d, mx, my + 195, mx, my + 126, None, METAL_DARK, 2.6)
    d.multiline(m5.x + 278, m5.y + 88, ["M5 rod clamps", "module stack."], size=11, fill=METAL_DARK, line_h=16, weight="bold")
    d.multiline(m5.x + 278, m5.y + 145, ["PETG spreads load", "locally only."], size=11, line_h=16)
    d.multiline(m5.x + 278, m5.y + 214, ["Not a massive", "plastic column."], size=11, fill=WARN, line_h=16, weight="bold")

    ax = align.x + 112
    ay = align.y + 190
    d.rect(ax - 62, ay - 22, 160, 40, fill=PETG, stroke=BLACK)
    d.rect(ax - pin_clear * 7, ay - socket_depth * 18, pin_clear * 14, socket_depth * 18, fill="#ffffff", stroke=BLACK, dash="4 3")
    d.rect(ax - pin_d * 6, ay - socket_depth * 18 - pin_h * 18 - 28, pin_d * 12, pin_h * 18, fill=PIN, stroke=BLACK)
    d.polygon([(ax - pin_d * 6, ay - socket_depth * 18 - pin_h * 18 - 28), (ax, ay - socket_depth * 18 - pin_h * 18 - 46), (ax + pin_d * 6, ay - socket_depth * 18 - pin_h * 18 - 28)], fill=PIN, stroke=BLACK)
    d.line(ax - 55, ay - socket_depth * 18 - 5, ax + 55, ay - socket_depth * 18 - 5, stroke=WARN, dash="4 3")
    d.text(ax + 78, ay - 76, "visual clearance gap", size=11, fill=WARN)
    draw_dimension(d, ax + 115, ay - socket_depth * 18 - pin_h * 18 - 28, ax + 115, ay - socket_depth * 18 - 28, f"pin {fmt_mm(pin_h)}", offset=18)
    d.multiline(align.x + 285, align.y + 105, ["positioning only", "not compression"], size=12, fill=WARN, line_h=18, weight="bold")
    d.multiline(align.x + 285, align.y + 180, ["lead-in/chamfer", "shown schematically"], size=11, line_h=16)

    d.multiline(
        notes.x + 28,
        notes.y + 70,
        [
            "A-A: interface rings and airflow opening.",
            "B-B: M5 compression path and washer/nut pad.",
            "C-C: pin/socket alignment with clearance.",
            "These functions must not be merged in one feature.",
            f"MODULE_INTERFACE_HEIGHT = {fmt_mm(interface_h)} per ring",
            f"INTERFACE_PIN_DIAMETER = {fmt_mm(pin_d)}",
            f"INTERFACE_PIN_CLEARANCE = {fmt_mm(pin_clear)}",
            f"INTERFACE_SOCKET_DEPTH = {fmt_mm(socket_depth)}",
        ],
        size=11,
        line_h=20,
    )

    draw_validation_block(
        d,
        44,
        850,
        1506,
        118,
        [
            "module_interface_coupon required before relying on stacked ring contract.",
            "pin/socket clearance coupon required before full module stack print.",
            "A-A, B-B, and C-C are explicitly tied to the top reference map.",
        ],
    )
    d.save(out / "04_module_interface_section.svg")


def drawing_05(out: Path, revision: str) -> None:
    d = new_drawing("HMT-mk0.10-DWG-05", "Rail, carriage and POM-C shoe contract", revision, "rail-shoe test-jig input")
    rail_w = as_float("RAIL_OUTER_WIDTH")
    rail_h = as_float("RAIL_OUTER_HEIGHT")
    wall = as_float("RAIL_WALL_THICKNESS")
    inner = as_float("RAIL_INNER_WIDTH")
    runner_d = as_float("RUNNER_DIAMETER")
    shoe_len = as_float("RUNNER_SHOE_LENGTH")
    insert_depth = as_float("RUNNER_INSERT_DEPTH_INTO_CARRIAGE")
    protrusion = as_float("RUNNER_PROTRUSION_FROM_CARRIAGE")
    pocket_w = as_float("RAIL_POCKET_WIDTH")
    pocket_h = as_float("RAIL_POCKET_HEIGHT")
    total_clearance = inner - runner_d

    orient = Panel(44, 112, 390, 205, "A - Orientation inset")
    uchan = Panel(462, 112, 505, 315, "B - Real U-channel section")
    engage = Panel(995, 112, 555, 315, "C - Shoe engagement cross-section")
    side = Panel(44, 452, 500, 290, "D - Shoe side view")
    clamp = Panel(572, 452, 500, 290, "E - Clamp screw retention")
    clear = Panel(1100, 452, 450, 290, "F - Clearance and structural warning")
    for p in (orient, uchan, engage, side, clamp, clear):
        draw_panel(d, p)

    draw_orientation_axes(d, orient.x + 80, orient.y + 138, 1.0)
    d.rect(orient.x + 235, orient.y + 105, 92, 22, fill=METAL, stroke=BLACK)
    d.rect(orient.x + 272, orient.y + 76, 28, 80, fill=POM, stroke=BLACK)
    d.text(orient.x + 218, orient.y + 178, "section plane X-Z", size=11)
    d.text(orient.x + 36, orient.y + orient.h - 18, "Carriage slides along Y.", size=12, fill=METAL_DARK, weight="bold")

    ux = uchan.x + 122
    uy = uchan.y + 100
    scale_u = 18.0
    d.rect(ux - 42, uy - 42, rail_w * scale_u + 84, rail_h * scale_u + 82, fill=PETG, stroke=BLACK, stroke_width=1.5)
    d.text(ux - 34, uy - 52, "PETG rail pocket", size=11)
    draw_u_channel(d, ux, uy, scale_u)
    d.text(ux + rail_w * scale_u / 2, uy - 12, "open side", size=11, fill=WARN, anchor="middle")
    d.rect(ux - 28, uy - 12, 20, 42, fill=PETG, stroke=BLACK)
    d.rect(ux + rail_w * scale_u + 8, uy - 12, 20, 42, fill=PETG, stroke=BLACK)
    d.text(uchan.x + 330, uchan.y + 88, "aluminium U-channel", size=12, fill=METAL_DARK, weight="bold")
    d.text(uchan.x + 330, uchan.y + 114, f"outer {fmt_mm(rail_w)} x {fmt_mm(rail_h)} x {fmt_mm(rail_h)}", size=11)
    d.text(uchan.x + 330, uchan.y + 138, f"wall thickness {fmt_mm(wall)}", size=11)
    d.text(uchan.x + 330, uchan.y + 162, f"inner width approx. {fmt_mm(inner)}", size=11)
    d.text(uchan.x + 330, uchan.y + 206, "rail must be mechanically retained,", size=11, fill=WARN, weight="bold")
    d.text(uchan.x + 330, uchan.y + 226, "not glue-only", size=11, fill=WARN, weight="bold")
    draw_dimension(d, ux, uy + rail_h * scale_u + 36, ux + rail_w * scale_u, uy + rail_h * scale_u + 36, fmt_mm(rail_w), offset=0)
    draw_dimension(d, ux + rail_w * scale_u + 24, uy, ux + rail_w * scale_u + 24, uy + rail_h * scale_u, fmt_mm(rail_h), offset=0)

    ex = engage.x + 76
    ey = engage.y + 110
    scale_e = 17.0
    draw_u_channel(d, ex, ey, scale_e)
    d.rect(ex + rail_w * scale_e + 82, ey - 14, 160, 70, fill=PETG, stroke=BLACK, stroke_width=1.4)
    shoe_cx = ex + rail_w * scale_e + 74
    shoe_cy = ey + rail_h * scale_e * 0.46
    d.line(shoe_cx - protrusion * scale_e, shoe_cy, shoe_cx + insert_depth * scale_e, shoe_cy, stroke=POM, stroke_width=runner_d * scale_e)
    d.circle(shoe_cx - protrusion * scale_e, shoe_cy, runner_d * scale_e / 2, fill=POM, stroke=BLACK, stroke_width=1.4)
    d.circle(shoe_cx + insert_depth * scale_e, shoe_cy, runner_d * scale_e / 2, fill=POM, stroke=BLACK, stroke_width=1.4)
    d.rect(shoe_cx, shoe_cy - runner_d * scale_e * 0.62, insert_depth * scale_e + 65, runner_d * scale_e * 1.24, fill="none", stroke=POM_DARK, dash="5 4")
    d.text(engage.x + 310, engage.y + 92, f"POM-C short cylinder Ø{runner_d:.1f} x {fmt_mm(shoe_len)}", size=12, fill=POM_DARK, weight="bold")
    d.text(engage.x + 310, engage.y + 122, "not a wheel, ball, or bearing roller", size=11, fill=WARN, weight="bold")
    d.text(engage.x + 310, engage.y + 152, "shoe protrudes into rail channel", size=11)
    d.text(engage.x + 310, engage.y + 176, "socket holds replaceable shoe", size=11)
    draw_callout(d, shoe_cx - protrusion * scale_e, shoe_cy, engage.x + 305, engage.y + 220, "wear contact inside U-channel", POM_DARK)
    draw_arrow(d, engage.x + 314, engage.y + 262, engage.x + 500, engage.y + 262, "sliding along Y", METAL_DARK, 2.4, "middle")

    sx = side.x + 92
    sy = side.y + 132
    draw_pom_shoe(d, sx, sy, shoe_len, runner_d, 18)
    d.rect(sx, sy - 34, protrusion * 18, runner_d * 18 + 68, fill="none", stroke=AIR, dash="6 4")
    d.rect(sx + (shoe_len - insert_depth) * 18, sy - 22, insert_depth * 18, runner_d * 18 + 44, fill="none", stroke=POM_DARK, dash="6 4")
    draw_dimension(d, sx, sy + runner_d * 18 + 46, sx + shoe_len * 18, sy + runner_d * 18 + 46, f"length {fmt_mm(shoe_len)}", offset=0)
    draw_dimension(d, sx + shoe_len * 18 + 42, sy, sx + shoe_len * 18 + 42, sy + runner_d * 18, f"diameter {fmt_mm(runner_d)}", offset=0)
    d.text(side.x + 330, side.y + 108, "short cylinder", size=12, fill=POM_DARK, weight="bold")
    d.text(side.x + 330, side.y + 136, "not a bearing / not a roller", size=11, fill=WARN, weight="bold")
    d.text(side.x + 330, side.y + 172, f"protrusion: {fmt_mm(protrusion)}", size=11)
    d.text(side.x + 330, side.y + 196, f"insertion depth: {fmt_mm(insert_depth)}", size=11)

    draw_clamp_screw_detail(d, clamp.x + 10, clamp.y + 38, clamp.w - 20, clamp.h - 54)

    d.multiline(
        clear.x + 24,
        clear.y + 66,
        [
            f"Rail inner width approx. {inner:.1f} mm",
            f"Runner diameter = {runner_d:.1f} mm",
            f"Envelope difference: {inner:.1f} - {runner_d:.1f} = {total_clearance:.1f} mm total",
            "This is NOT final working clearance.",
            "Actual sliding contact must be validated.",
            "rail_shoe_test_jig variants: 0.2 / 0.4 / 0.6 mm",
            "Shoe acts as a short cantilever.",
            "Contact force bends PETG boss/ribs.",
            f"RAIL_POCKET = {fmt_mm(pocket_w)} x {fmt_mm(pocket_h)}",
        ],
        size=11,
        line_h=21,
    )

    draw_validation_block(
        d,
        44,
        850,
        1506,
        118,
        [
            "U-channel must be instantly recognizable as top-open aluminium rail.",
            "POM-C shoe is drawn as a short cylinder, not as a wheel, ball, or roller.",
            "Clamp screw retention and boss stiffness require rail_shoe_test_jig validation.",
        ],
    )
    d.save(out / "05_rail_carriage_section.svg")


def write_readme(out: Path, revision: str) -> None:
    readme = f"""# {revision} Architecture Drawings

These SVG files are drawing-layer v2 planning and interface sheets for the
Homelab Modular Tower.

They are not production manufacturing drawings. CadQuery remains the source of
truth for 3D geometry, and generated STEP/STL artifacts remain derived outputs.

If a drawing and the CadQuery model disagree, stop and resolve the discrepancy
before continuing CAD implementation.
"""
    (out / "README.md").write_text(readme, encoding="utf-8")


def generate(revision: str, out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    drawing_01(out, revision)
    drawing_02(out, revision)
    drawing_03(out, revision)
    drawing_04(out, revision)
    drawing_05(out, revision)
    write_readme(out, revision)
    print(f"Generated drawing-layer v2 SVGs in {out}")
    for file in sorted(out.glob("*.svg")):
        print(f" - {file}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate mk0.10 drawing-layer v2 architecture/interface SVGs.")
    parser.add_argument("--revision", default=REVISION_DEFAULT, help="Planning revision label.")
    parser.add_argument("--out", default="drawings/mk0.10", help="Output directory.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    generate(args.revision, Path(args.out))


if __name__ == "__main__":
    main()
