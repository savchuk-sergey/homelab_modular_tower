"""Generate mk0.12 CAD skeleton review PNG views with Pillow."""

from __future__ import annotations

from pathlib import Path
import sys

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from cad import config as cfg  # noqa: E402


OUT = Path("renders") / cfg.CURRENT_REVISION
SIZE = 900
MARGIN = 80


def font(size: int = 18):
    try:
        return ImageFont.truetype("arial.ttf", size)
    except OSError:
        return ImageFont.load_default()


def canvas(title: str):
    image = Image.new("RGB", (SIZE, SIZE), "white")
    draw = ImageDraw.Draw(image)
    draw.text((24, 18), title, fill=(20, 20, 20), font=font(24))
    return image, draw


def xy(point: tuple[float, float]) -> tuple[int, int]:
    x, y = point
    scale = (SIZE - 2 * MARGIN) / 220.0
    return int(SIZE / 2 + x * scale), int(SIZE / 2 - y * scale)


def xz(point: tuple[float, float]) -> tuple[int, int]:
    x, z = point
    sx = (SIZE - 2 * MARGIN) / 220.0
    sz = (SIZE - 2 * MARGIN) / 280.0
    return int(SIZE / 2 + x * sx), int(SIZE - MARGIN - z * sz)


def rect_xy(draw, center_x: float, center_y: float, width: float, depth: float, outline, fill=None, line: int = 3) -> None:
    x0, y0 = xy((center_x - width / 2, center_y + depth / 2))
    x1, y1 = xy((center_x + width / 2, center_y - depth / 2))
    draw.rectangle((x0, y0, x1, y1), outline=outline, fill=fill, width=line)


def rect_xz(draw, center_x: float, z_min: float, width: float, height: float, outline, fill=None, line: int = 3) -> None:
    x0, y0 = xz((center_x - width / 2, z_min + height))
    x1, y1 = xz((center_x + width / 2, z_min))
    draw.rectangle((x0, y0, x1, y1), outline=outline, fill=fill, width=line)


def circle_xy(draw, center_x: float, center_y: float, diameter: float, outline, fill=None, line: int = 3) -> None:
    x0, y0 = xy((center_x - diameter / 2, center_y + diameter / 2))
    x1, y1 = xy((center_x + diameter / 2, center_y - diameter / 2))
    draw.ellipse((x0, y0, x1, y1), outline=outline, fill=fill, width=line)


def add_grid(draw) -> None:
    for v in range(-100, 101, 20):
        draw.line((xy((-100, v)), xy((100, v))), fill=(230, 230, 230), width=1)
        draw.line((xy((v, -100)), xy((v, 100))), fill=(230, 230, 230), width=1)


def add_footprint(draw) -> None:
    rect_xy(draw, 0, 0, 190, 190, (30, 30, 30), line=4)
    rect_xy(draw, 0, 80, 120, 30, (43, 108, 176), fill=(225, 238, 250), line=3)
    for x, y in cfg.m5_rod_centers():
        circle_xy(draw, x, y, cfg.M5_ROD_CLEARANCE_DIAMETER, (80, 80, 80), line=3)
        circle_xy(draw, x, y, cfg.CORNER_COMPRESSION_PAD_SIZE_X, (140, 140, 140), line=2)


def add_fan(draw) -> None:
    rect_xy(draw, 0, 0, cfg.SKELETON_FAN_RING_OUTER_SIZE, cfg.SKELETON_FAN_RING_OUTER_SIZE, (80, 80, 80), line=3)
    circle_xy(draw, 0, 0, cfg.FAN_AIRFLOW_CUTOUT_DIAMETER_MAX, (15, 118, 110), fill=(228, 248, 245), line=4)
    for x, y in cfg.fan_screw_centers():
        circle_xy(draw, x, y, cfg.FAN_SCREW_BOSS_DIAMETER_MAX, (124, 45, 18), line=3)
    rect_xy(draw, 0, 0, 186, cfg.RIB_THICKNESS, (70, 70, 70), fill=(180, 180, 180), line=1)
    rect_xy(draw, 0, 0, cfg.RIB_THICKNESS, 186, (70, 70, 70), fill=(180, 180, 180), line=1)


def save(image: Image.Image, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    image.save(OUT / name)


def part_top(name: str, title: str) -> None:
    image, draw = canvas(title)
    add_grid(draw)
    add_footprint(draw)
    if "base" in name or "top_cap" in name:
        add_fan(draw)
    elif "rpi_ssd" in name:
        rect_xy(draw, cfg.RPI3B_CENTER_X, cfg.RPI3B_CENTER_Y, cfg.RPI3B_CLEARANCE_WIDTH, cfg.RPI3B_CLEARANCE_DEPTH, (47, 133, 90), line=4)
        rect_xy(draw, cfg.EXTERNAL_SSD_PREFERRED_CENTER_X, cfg.EXTERNAL_SSD_PREFERRED_CENTER_Y, cfg.EXTERNAL_SSD_WIDTH, cfg.EXTERNAL_SSD_DEPTH, (43, 108, 176), line=4)
        rect_xy(draw, 52.5, 15, cfg.SKELETON_RPI_CABLE_WINDOW_WIDTH, 100, (43, 108, 176), fill=(225, 238, 250), line=2)
        rect_xy(draw, 0, 80, cfg.SKELETON_REAR_SERVICE_WINDOW_WIDTH, cfg.SKELETON_REAR_SERVICE_WINDOW_HEIGHT, (43, 108, 176), fill=(225, 238, 250), line=2)
    elif "minipc" in name:
        rect_xy(draw, cfg.MINIPC_CENTER_X, cfg.MINIPC_CENTER_Y, cfg.MINIPC_WIDTH, cfg.MINIPC_DEPTH, (155, 44, 44), line=4)
        rect_xy(draw, -76, cfg.MINIPC_CENTER_Y, cfg.SKELETON_MINIPC_BYPASS_SLOT_WIDTH, cfg.SKELETON_MINIPC_BYPASS_SLOT_LENGTH, (15, 118, 110), fill=(228, 248, 245), line=2)
        rect_xy(draw, 76, cfg.MINIPC_CENTER_Y, cfg.SKELETON_MINIPC_BYPASS_SLOT_WIDTH, cfg.SKELETON_MINIPC_BYPASS_SLOT_LENGTH, (15, 118, 110), fill=(228, 248, 245), line=2)
        rect_xy(draw, 0, 94, cfg.SKELETON_MINIPC_REAR_EXIT_WIDTH, 2, (43, 108, 176), fill=(225, 238, 250), line=2)
    save(image, name)


def side_view(name: str, title: str) -> None:
    image, draw = canvas(title)
    for label, z, height, color in (
        ("base", 0, cfg.BASE_PEDESTAL_HEIGHT, (74, 85, 104)),
        ("rpi/ssd", cfg.RPI_SSD_MODULE_Z_MIN, cfg.RPI_SSD_MODULE_HEIGHT, (47, 133, 90)),
        ("minipc", cfg.MINIPC_MODULE_Z_MIN, cfg.MINIPC_MODULE_HEIGHT, (155, 44, 44)),
        ("top", cfg.TOP_CAP_Z_MIN, cfg.TOP_CAP_HEIGHT, (74, 85, 104)),
    ):
        rect_xz(draw, 0, z, 190, height, color, line=4)
        draw.text(xz((-88, z + height / 2)), label, fill=color, font=font(16))
    for x in (-80, 80):
        draw.line((xz((x, -8)), xz((x, 252))), fill=(80, 80, 80), width=3)
    rect_xz(draw, 0, 65, 120, 155, (43, 108, 176), fill=(235, 244, 252), line=2)
    save(image, name)


def iso_view(name: str, title: str) -> None:
    image, draw = canvas(title)
    z = 40
    for label, height, color in (
        ("base", 32, (74, 85, 104)),
        ("rpi/ssd", 75, (47, 133, 90)),
        ("minipc", 105, (155, 44, 44)),
        ("top", 26, (74, 85, 104)),
    ):
        x0 = 210 + z // 5
        y0 = SIZE - 120 - z
        draw.polygon([(x0, y0), (x0 + 380, y0 - 60), (x0 + 520, y0), (x0 + 140, y0 + 60)], outline=color, fill=(245, 245, 245))
        draw.line((x0, y0, x0, y0 - height * 2), fill=color, width=3)
        draw.line((x0 + 520, y0, x0 + 520, y0 - height * 2), fill=color, width=3)
        draw.text((x0 + 10, y0 - height), label, fill=color, font=font(16))
        z += height
    save(image, name)


def main() -> None:
    part_top("base_pedestal_top.png", "base pedestal top")
    iso_view("base_pedestal_iso.png", "base pedestal iso")
    part_top("rpi_ssd_stack_module_top.png", "rpi ssd module top")
    iso_view("rpi_ssd_stack_module_iso.png", "rpi ssd module iso")
    part_top("minipc_stack_module_top.png", "minipc module top")
    iso_view("minipc_stack_module_iso.png", "minipc module iso")
    part_top("top_cap_top.png", "top cap top")
    iso_view("top_cap_iso.png", "top cap iso")
    for name in ("assembly_front.png", "assembly_rear.png", "assembly_left.png", "assembly_right.png"):
        side_view(name, name.removesuffix(".png"))
    part_top("assembly_top.png", "assembly top")
    iso_view("assembly_iso.png", "assembly iso")
    part_top("rpi_ssd_stack_module_xy_edges.png", "rpi ssd xy edges")
    part_top("minipc_stack_module_xy_edges.png", "minipc xy edges")
    side_view("rear_service_windows_check.png", "rear service windows check")
    part_top("airflow_open_area_check.png", "airflow open area check")
    print(f"Generated {len(list(OUT.glob('*.png')))} mk0.12 review PNG files in {OUT}")


if __name__ == "__main__":
    main()
